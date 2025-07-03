import { createResource } from "frappe-ui"
import { employeeResource } from "./employee"
import { reactive } from "vue"

export const expenseClaimSummary = createResource({
	url: "shop.api.get_expense_claim_summary",
	params: {
		// employee: employeeResource.data.name,
	},
	auto: true,
	cache: "shop:expense_claim_summary",
})

const transformClaimData = (data) => {
	return data.map((claim) => {
		claim.doctype = "Expense Claim"
		return claim
	})
}

export const myClaims = createResource({
	url: "shop.api.get_expense_claims",
	params: {
		// employee: employeeResource.data.name,
		limit: 5,
	},
	auto: true,
	cache: "shop:my_claims",
	transform(data) {
		return transformClaimData(data)
	},
	onSuccess() {
		expenseClaimSummary.reload()
	},
})

export const teamClaims = createResource({
	url: "shop.api.get_expense_claims",
	params: {
		// employee: employeeResource.data.name,
		// approver_id: employeeResource.data.user_id,
		for_approval: 1,
		limit: 5,
	},
	auto: true,
	cache: "shop:team_claims",
	transform(data) {
		return transformClaimData(data)
	},
})

export let claimTypesByID = reactive({})

export const claimTypesResource = createResource({
	url: "shop.api.get_expense_claim_types",
	auto: true,
	transform(data) {
		return data.map((row) => {
			claimTypesByID[row.name] = row
			return row
		})
	},
})
