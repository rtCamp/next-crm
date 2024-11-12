# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import json

import frappe
from frappe import _
from frappe.desk.form.assign_to import add as assign

from erpnext.crm.doctype.opportunity.opportunity import Opportunity

from next_crm.ncrm.doctype.crm_service_level_agreement.utils import get_sla
from next_crm.ncrm.doctype.crm_status_change_log.crm_status_change_log import add_status_change_log


class Opportunity(Opportunity):

	def before_validate(self):
		self.set_sla()

	def validate(self):
		self.set_primary_contact()
		self.set_primary_email_mobile_no()
		if not self.is_new() and self.has_value_changed("opportunity_owner") and self.opportunity_owner:
			self.share_with_agent(self.opportunity_owner)
			self.assign_agent(self.opportunity_owner)
		# if self.has_value_changed("status"):
		# 	add_status_change_log(self)
		super().validate()

	def after_insert(self):
		if self.opportunity_owner:
			self.assign_agent(self.opportunity_owner)
		super().after_insert()

	def before_save(self):
		self.apply_sla()

	def set_primary_contact(self, contact=None):
		if not self.contacts:
			return

		if not contact and len(self.contacts) == 1:
			self.contacts[0].is_primary = 1
		elif contact:
			for d in self.contacts:
				if d.contact == contact:
					d.is_primary = 1
				else:
					d.is_primary = 0

	def set_primary_email_mobile_no(self):
		if not self.contacts:
			self.email = ""
			self.mobile_no = ""
			self.phone = ""
			return

		if len([contact for contact in self.contacts if contact.is_primary]) > 1:
			frappe.throw(_("Only one {0} can be set as primary.").format(frappe.bold("Contact")))

		primary_contact_exists = False
		for d in self.contacts:
			if d.is_primary == 1:
				primary_contact_exists = True
				self.email = d.email.strip() if d.email else ""
				self.mobile_no = d.mobile_no.strip() if d.mobile_no else ""
				self.phone = d.phone.strip() if d.phone else ""
				break

		if not primary_contact_exists:
			self.email = ""
			self.mobile_no = ""
			self.phone = ""

	def assign_agent(self, agent):
		if not agent:
			return

		assignees = self.get_assigned_users()
		if assignees:
			for assignee in assignees:
				if agent == assignee:
					# the agent is already set as an assignee
					return

		assign({"assign_to": [agent], "doctype": "Opportunity", "name": self.name})

	def share_with_agent(self, agent):
		if not agent:
			return

		docshares = frappe.get_all(
			"DocShare",
			filters={"share_name": self.name, "share_doctype": self.doctype},
			fields=["name", "user"],
		)

		shared_with = [d.user for d in docshares] + [agent]

		for user in shared_with:
			if user == agent and not frappe.db.exists("DocShare", {"user": agent, "share_name": self.name, "share_doctype": self.doctype}):
				frappe.share.add_docshare(
					self.doctype, self.name, agent, write=1, flags={"ignore_share_permission": True}
				)
			elif user != agent:
				frappe.share.remove(self.doctype, self.name, user)


	def set_sla(self):
		"""
		Find an SLA to apply to the opportunity.
		"""
		if self.sla: return

		sla = get_sla(self)
		if not sla:
			self.first_responded_on = None
			self.first_response_time = None
			return
		self.sla = sla.name

	def apply_sla(self):
		"""
		Apply SLA if set.
		"""
		if not self.sla:
			return
		sla = frappe.get_last_doc("CRM Service Level Agreement", {"name": self.sla})
		if sla:
			sla.apply(self)

	@staticmethod
	def default_list_data():
		columns = [
			{
				'label': 'Customer',
				'type': 'Link',
				'key': 'customer',
				'options': 'Customer',
				'width': '11rem',
			},
			{
				'label': 'Amount',
				'type': 'Currency',
				'key': 'opportunity_amount',
				'width': '9rem',
			},
			{
				'label': 'Status',
				'type': 'Select',
				'key': 'status',
				'width': '10rem',
			},
			{
				'label': 'Email',
				'type': 'Data',
				'key': 'contact_email',
				'width': '12rem',
			},
			{
				'label': 'Mobile No',
				'type': 'Data',
				'key': 'contact_mobile',
				'width': '11rem',
			},
			{
				'label': 'Assigned To',
				'type': 'Text',
				'key': '_assign',
				'width': '10rem',
			},
			{
				'label': 'Last Modified',
				'type': 'Datetime',
				'key': 'modified',
				'width': '8rem',
			},
		]
		rows = [
			"name",
			"customer",
			"opportunity_amount",
			"status",
			"contact_email",
			"currency",
			"contact_mobile",
			"opportunity_owner",
			"sla_status",
			"response_by",
			"first_response_time",
			"first_responded_on",
			"modified",
			"_assign",
		]
		return {'columns': columns, 'rows': rows}

	@staticmethod
	def default_kanban_settings():
		return {
			"column_field": "status",
			"title_field": "customer",
			"kanban_fields": '["opportunity_amount", "contact_email", "contact_mobile", "_assign", "modified"]'
		}

@frappe.whitelist()
def add_contact(opportunity, contact):
	if not frappe.has_permission("Opportunity", "write", opportunity):
		frappe.throw(_("Not allowed to add contact to Opportunity"), frappe.PermissionError)

	opportunity = frappe.get_cached_doc("Opportunity", opportunity)
	opportunity.append("contacts", {"contact": contact})
	opportunity.save()
	return True

@frappe.whitelist()
def remove_contact(opportunity, contact):
	if not frappe.has_permission("Opportunity", "write", opportunity):
		frappe.throw(_("Not allowed to remove contact from Opportunity"), frappe.PermissionError)

	opportunity = frappe.get_cached_doc("Opportunity", opportunity)
	opportunity.contacts = [d for d in opportunity.contacts if d.contact != contact]
	opportunity.save()
	return True

@frappe.whitelist()
def set_primary_contact(opportunity, contact):
	if not frappe.has_permission("Opportunity", "write", opportunity):
		frappe.throw(_("Not allowed to set primary contact for Opportunity"), frappe.PermissionError)

	opportunity = frappe.get_cached_doc("Opportunity", opportunity)
	opportunity.set_primary_contact(contact)
	opportunity.save()
	return True

def create_customer(doc):
	if not doc.get("customer_name"):
		return

	existing_customer = frappe.db.exists("Customer", {"customer_name": doc.get("customer_name")})
	if existing_customer:
		return existing_customer

	customer = frappe.new_doc("Customer")
	customer.update(
		{
			"customer_name": doc.get("customer_name"),
			"website": doc.get("website"),
			"territory": doc.get("territory"),
			"industry": doc.get("industry"),
			"annual_revenue": doc.get("opportunity_amount"),
		}
	)
	customer.insert(ignore_permissions=True)
	return customer.name

def contact_exists(doc):
	email_exist = frappe.db.exists("Contact Email", {"email_id": doc.get("contact_email")})
	mobile_exist = frappe.db.exists("Contact Phone", {"phone": doc.get("contact_mobile")})

	doctype = "Contact Email" if email_exist else "Contact Phone"
	name = email_exist or mobile_exist

	if name:
		return frappe.db.get_value(doctype, name, "parent")

	return False

def create_contact(doc):
	existing_contact = contact_exists(doc)
	if existing_contact:
		return existing_contact

	contact = frappe.new_doc("Contact")
	contact.update(
		{
			"first_name": doc.get("first_name"),
			"last_name": doc.get("last_name"),
			"salutation": doc.get("salutation"),
			"company_name": doc.get("customer") or doc.get("customer_name"),
		}
	)

	if doc.get("contact_email"):
		contact.append("email_ids", {"email_id": doc.get("contact_email"), "is_primary": 1})

	if doc.get("contact_mobile"):
		contact.append("phone_nos", {"phone": doc.get("contact_mobile"), "is_primary_mobile_no": 1})

	contact.insert(ignore_permissions=True)
	contact.reload()  # load changes by hooks on contact

	return contact.name

@frappe.whitelist()
def create_opportunity(args):
	opportunity = frappe.new_doc("Opportunity")

	contact = args.get("contact")
	if not contact and (args.get("first_name") or args.get("last_name") or args.get("email") or args.get("mobile_no")):
		contact = create_contact(args)

	opportunity.update({
		"customer": args.get("customer") or create_customer(args),
		"contacts": [{"contact": contact, "is_primary": 1}] if contact else [],
		"opportunity_from": "lead",
		"party_name": args.get("lead")
	})

	args.pop("customer", None)
	args.pop("lead", None)

	opportunity.update(args)

	opportunity.insert(ignore_permissions=True)
	return opportunity.name
