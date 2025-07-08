<template>
  <LayoutHeader v-if="customer.doc">
    <header
      class="relative flex h-10.5 items-center justify-between gap-2 py-2.5 pl-2"
    >
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </header>
  </LayoutHeader>
  <div v-if="customer.doc" class="flex flex-col h-full">
    <FileUploader
      @success="changeCustomerImage"
      :validateFile="validateFile"
    >
      <template #default="{ openFileSelector, error }">
        <div class="flex flex-col items-start justify-start gap-4 p-4">
          <div class="flex gap-4 items-center">
            <div class="group relative h-14.5 w-14.5">
              <Avatar
                size="3xl"
                class="h-14.5 w-14.5"
                :label="customer.doc.customer_name"
                :image="customer.doc.image"
              />
              <component
                :is="customer.doc.image ? Dropdown : 'div'"
                v-bind="
                  customer.doc.image
                    ? {
                        options: [
                          {
                            icon: 'upload',
                            label: customer.doc.image
                              ? __('Change image')
                              : __('Upload image'),
                            onClick: openFileSelector,
                          },
                          {
                            icon: 'trash-2',
                            label: __('Remove image'),
                            onClick: () => changeCustomerImage(''),
                          },
                        ],
                      }
                    : { onClick: openFileSelector }
                "
                class="!absolute bottom-0 left-0 right-0"
              >
                <div
                  class="absolute bottom-0 left-0 right-0 flex h-14 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-5 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                  style="
                    -webkit-clip-path: inset(22px 0 0 0);
                    clip-path: inset(22px 0 0 0);
                  "
                >
                  <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
                </div>
              </component>
            </div>
            <div class="flex flex-col gap-2 truncate">
              <div class="truncate text-lg font-medium text-ink-gray-9">
                {{ customer.doc.customer_name }}
              </div>
              <div class="flex items-center gap-1.5 relative">
                <Button @click="openWebsite">
                  <FeatherIcon name="link" class="h-4 w-4" />
                </Button>
              
                <Button
                  :label="__('Delete')"
                  theme="red"
                  size="sm"
                  @click="showDeleteModal = true"
                >
                  <template #prefix>
                    <FeatherIcon name="trash-2" class="h-4 w-4" />
                  </template>
                </Button>
              
                <div class="relative">
                  <Button
                    label="Add Activity"
                    theme="blue"
                    size="sm"
                    @click="toggleDropdown"
                    ref="activityBtn"
                  >
                    <template #prefix>
                      <FeatherIcon name="plus" class="h-4 w-4" />
                    </template>
                  </Button>
                </div>
                
                <!-- This goes OUTSIDE the relative container -->
                <div
                  v-if="showDropdown"
                  class="fixed z-[9999] w-40 bg-white border border-gray-200 rounded shadow"
                  :style="{ top: dropdownPosition.top + 'px', left: dropdownPosition.left + 'px' }"
                >
                  <ul>
                    <li
                      v-for="option in activityOptions"
                      :key="option"
                      @click="selectActivity(option)"
                      class="cursor-pointer px-4 py-2 hover:bg-gray-100 text-sm"
                    >
                      {{ option }}
                    </li>
                  </ul>
                </div>
                
              </div>
              
              
              <ErrorMessage :message="__(error)" />
            </div>
          </div>
        </div>
        
      </template>
      
    </FileUploader>
  
    
    <Tabs as="div" v-model="tabIndex" :tabs="tabs" class="overflow-auto">
      <TabList class="!px-4" v-slot="{ tab, selected }">
        <button
          v-if="tab.name !== 'Details'"
          class="group flex items-center gap-2 border-b border-transparent py-2.5 text-base text-ink-gray-5 duration-300 ease-in-out hover:border-outline-gray-3 hover:text-ink-gray-9"
          :class="{ 'text-ink-gray-9': selected }"
        >
          <component v-if="tab.icon" :is="tab.icon" class="h-5" />
          {{ __(tab.label) }}
          <Badge
            class="group-hover:bg-surface-gray-7"
            :class="[selected ? 'bg-surface-gray-7' : 'bg-gray-600']"
            variant="solid"
            theme="gray"
            size="sm"
          >
            {{ tab.count }}
          </Badge>
        </button>
      </TabList>
      <TabPanel v-slot="{ tab }">
        <div v-if="tab.name == 'Details'">
          <div
            v-if="fieldsLayout.data"
            class="flex flex-1 flex-col justify-between overflow-hidden"
          >
            <div class="flex flex-col overflow-y-auto">
              <div
                v-for="(section, i) in fieldsLayout.data"
                :key="section.label"
                class="flex flex-col px-2 py-3 sm:p-3"
                :class="{ 'border-b': i !== fieldsLayout.data.length - 1 }"
              >
                <Section :is-opened="section.opened" :label="section.label">
                  <SectionFields
                    :fields="section.fields"
                    :isLastSection="i == fieldsLayout.data.length - 1"
                    v-model="customer.doc"
                    @update="updateField"
                  />
                </Section>
              </div>
            </div>
          </div>
        </div>
        <OpportunitiesListView
          class="mt-4"
          v-if="tab.label === 'Opportunities' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: false }"
        />
        <ContactsListView
          class="mt-4"
          v-if="tab.label === 'Contacts' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: false }"
        />
        <AddressesListView
          class="mt-4"
          v-if="tab.label === 'Addresses' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: false }"
        />
        <div
          v-if="!rows.length && tab.name !== 'Details'"
          class="grid flex-1 place-items-center text-xl font-medium text-ink-gray-4"
        >
          <div class="flex flex-col items-center justify-center space-y-3">
            <component :is="tab.icon" class="!h-10 !w-10" />
            <div>{{ __('No {0} Found', [__(tab.label)]) }}</div>
          </div>
        </div>
      </TabPanel>



    </Tabs>



  </div>
 
  <AddressModal v-model="showAddressModal" v-model:address="_address" />
  <DeleteModal
    v-model="showDeleteModal"
    doctype="Customer"
    :docname="props.customerId"
    redirect-to="Customers"
  />


  <template>
    <Dialog
      v-model="showActivityModal"
      :options="{
        title: `Create Event`,
        size: 'md',
        actions: [
          {
            label: 'Create',
            variant: 'solid',
            onClick: createActivity,
          },
        ],
      }"
    >
      <template #body-title>
        <h3 class="text-xl font-semibold text-ink-gray-9">
          Create Event
        </h3>
      </template>
  
      <template #body-content>
        <div class="flex flex-col gap-4">
          <Input
            label="Date"
            type="date"
            v-model="activityForm.date"
            required
          />
  
         
  
          <Input
            label="Subject"
            v-model="activityForm.subject"
            required
          />
  
          <Textarea
            label="Description"
            v-model="activityForm.description"
          />
        </div>
      </template>
    </Dialog>
  </template>
</template>

<script setup>
import Section from '@/components/Section.vue'
import SectionFields from '@/components/SectionFields.vue'
import Icon from '@/components/Icon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import AddressModal from '@/components/Modals/AddressModal.vue'
import DeleteModal from '@/components/Modals/DeleteModal.vue'
import AddressesListView from '@/components/ListViews/AddressesListView.vue'
import OpportunitiesListView from '@/components/ListViews/OpportunitiesListView.vue'
import ContactsListView from '@/components/ListViews/ContactsListView.vue'
import DetailsIcon from '@/components/Icons/DetailsIcon.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import OpportunitiesIcon from '@/components/Icons/OpportunitiesIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import AddressIcon from '@/components/Icons/AddressIcon.vue'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { getView } from '@/utils/view'
import {
  dateFormat,
  dateTooltipFormat,
  timeAgo,
  formatNumberIntoCurrency,
  createToast,
} from '@/utils'
import {
  Breadcrumbs,
  Avatar,
  FileUploader,
  Dropdown,
  Tabs,
  TabList,
  TabPanel,
  call,
  createListResource,
  createDocumentResource,
  usePageMeta,
  createResource,
  Dialog,
  Input,
  Select,
  Textarea
} from 'frappe-ui'
import { h, computed, ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  customerId: {
    type: String,
    required: true,
  },
})

const { getUser } = usersStore()
const { getDealStatus } = statusesStore()

const route = useRoute()
const showDeleteModal = ref(false)
const showDropdown = ref(false)
const showActivityModal = ref(false)
const selectedActivity = ref('')
const activityOptions = ['Event', 'Call', 'Meeting', 'Sent/Received Email', 'Follow Up', 'Demo', 'Other']
const userList = createListResource({
  doctype: 'User',
  fields: ['name', 'full_name'],
  filters: [['enabled', '=', 1], ['user_type', '=', 'System User']],
  limit: 100,
  auto: true,
})


const customer = createDocumentResource({
  doctype: 'Customer',
  name: props.customerId,
  cache: ['customer', props.customerId],
  fields: ['*'],
  auto: true,
})

async function updateField(fieldname, value) {
  await customer.setValue.submit({
    [fieldname]: value,
  })
  createToast({
    title: __('Customer updated'),
    icon: 'check',
    iconClasses: 'text-ink-green-3',
  })
}

const breadcrumbs = computed(() => {
  let items = [{ label: __('Customers'), route: { name: 'Customers' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(
      route.query.view,
      route.query.viewType,
      'Customer',
    )
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'Customers',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: props.customerId,
    route: {
      name: 'Customer',
      params: { customerId: props.customerId },
    },
  })
  return items
})

usePageMeta(() => {
  return {
    title: props.customerId,
  }
})

function validateFile(file) {
  let extn = file.name.split('.').pop().toLowerCase()
  if (!['png', 'jpg', 'jpeg'].includes(extn)) {
    return __('Only PNG and JPG images are allowed')
  }
}

async function changeCustomerImage(file) {
  await call('frappe.client.set_value', {
    doctype: 'Customer',
    name: props.customerId,
    fieldname: 'image',
    value: file?.file_url || '',
  })
  customer.reload()
}

function openWebsite() {
  if (!customer.doc.website)
    createToast({
      title: __('Website not found'),
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  else window.open(customer.doc.website, '_blank')
}

const showAddressModal = ref(false)
const _customer = ref({})
const _address = ref({})

const fieldsLayout = createResource({
  url: 'next_crm.api.doc.get_sidebar_fields',
  cache: ['fieldsLayout', props.customerId],
  params: { doctype: 'Customer', name: props.customerId },
  auto: true,
  transform: (data) => getParsedFields(data),
})

function getParsedFields(data) {
  return data.map((section) => {
    return {
      ...section,
      fields: computed(() =>
        section.fields.map((field) => {
          if (field.name === 'address') {
            return {
              ...field,
              create: (value, close) => {
                _customer.value.address = value
                _address.value = {}
                showAddressModal.value = true
                close()
              },
              edit: async (addr) => {
                _address.value = await call('frappe.client.get', {
                  doctype: 'Address',
                  name: addr,
                })
                showAddressModal.value = true
              },
            }
          } else {
            return field
          }
        }),
      ),
    }
  })
}

const tabIndex = ref(0)
const tabs = [
  {
    name: 'Details',
    label: __('Details'),
    icon: DetailsIcon,
  },
  {
    name: 'Opportunities',
    label: __('Opportunities'),
    icon: h(OpportunitiesIcon, { class: 'h-4 w-4' }),
    count: computed(() => opportunities.data?.length),
  },
  {
    name: 'Contacts',
    label: __('Contacts'),
    icon: h(ContactsIcon, { class: 'h-4 w-4' }),
    count: computed(() => contacts.value.data?.length),
  },
  {
    label: 'Addresses',
    label: __('Addresses'),
    icon: h(AddressIcon, { class: 'h-4 w-4' }),
    count: computed(() => addresses.value.data?.length),
  },
]

const opportunities = createListResource({
  type: 'list',
  doctype: 'Opportunity',
  cache: ['opportunities', props.customerId],
  fields: [
    'name',
    'customer',
    'currency',
    'opportunity_amount',
    'status',
    'contact_email',
    'contact_mobile',
    'opportunity_owner',
    'modified',
  ],
  filters: {
    customer: props.customerId,
  },
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true,
})

async function getContactsList() { 
  const contact_names = await call('next_crm.api.contact.get_linked_contact', {
    link_doctype: 'Customer',
    link_name: props.customerId,
  })

  const list = createListResource({
    type: 'list',
    doctype: 'Contact',
    fields: [
      'name',
      'first_name',
      'image',
      'email_id',
      'company_name',
      'modified',
    ],
    filters: {
      name: ['in', contact_names],
    },
    orderBy: 'modified desc',
    pageLength: 20,
    auto: true,
  })

  return list
}

async function getAddressesList() { 
  const address_names = await call('next_crm.api.address.get_linked_address', {
    link_doctype: 'Customer', 
    link_name: props.customerId,
  })

  const list = createListResource({
    type: 'list',
    doctype: 'Address',
    fields: [
      'name',
      'address_title',
      'address_type',
      'address_line1',
      'phone',
      'modified',
    ],
    filters: {
      name: ['in', address_names],
    },
    orderBy: 'modified desc',
    pageLength: 20,
    auto: true,
  })

  return list
}

const contacts = ref();
async function setContactsList() {
  contacts.value = await getContactsList()
}
setContactsList()

const addresses = ref();
async function setAddressesList() {
  addresses.value = await getAddressesList()
}
setAddressesList()

const rows = computed(() => {
  let list = ref([])
  if (tabIndex.value === 1)
    list.value = opportunities
  else if (tabIndex.value === 2)
    list.value = contacts.value
  else if (tabIndex.value === 3)
    list.value = addresses.value

  if (!list.value.data) return []

  return list.value.data.map((row) => {
    if (tabIndex.value === 1)
      return getOpportunityRowObject(row)
    else if (tabIndex.value === 2)
      return getContactRowObject(row)
    else if (tabIndex.value === 3)
      return getAddressRowObject(row)
  })
})

const columns = computed(() => {
  if (tabIndex.value === 1)
    return opportunityColumns
  else if (tabIndex.value === 2)
    return contactColumns
  else if (tabIndex.value === 3)
    return addressColumns
})

function getOpportunityRowObject(opportunity) {
  return {
    name: opportunity.name,
    customer: {
      label: opportunity.customer,
      logo: props.customer?.image,
    },
    opportunity_amount: formatNumberIntoCurrency(
      opportunity.opportunity_amount,
      opportunity.currency,
    ),
    status: {
      label: opportunity.status,
      color: getDealStatus(opportunity.status)?.iconColorClass,
    },
    email: opportunity.contact_email,
    mobile_no: opportunity.contact_mobile,
    opportunity_owner: {
      label: opportunity.opportunity_owner && getUser(opportunity.opportunity_owner).full_name,
      ...(opportunity.opportunity_owner && getUser(opportunity.opportunity_owner)),
    },
    modified: {
      label: dateFormat(opportunity.modified, dateTooltipFormat),
      timeAgo: __(timeAgo(opportunity.modified)),
    },
  }
}

function getContactRowObject(contact) {
  return {
    name: contact.name,
    full_name: {
      label: contact.full_name,
      image_label: contact.full_name,
      image: contact.image,
    },
    email: contact.email_id,
    mobile_no: contact.mobile_no,
    company_name: {
      label: contact.company_name,
      logo: props.customer?.image,
    },
    modified: {
      label: dateFormat(contact.modified, dateTooltipFormat),
      timeAgo: __(timeAgo(contact.modified)),
    },
  }
}

function getAddressRowObject(address) {
  return {
    name: address.name,
    address_title: address.address_title,
    address_type: address.address_type,
    address_line1: address.address_line1,
    phone: address.phone,
    modified: {
      label: dateFormat(address.modified, dateTooltipFormat),
      timeAgo: __(timeAgo(address.modified)),
    },
  }
}

const opportunityColumns = [
  {
    label: __('Amount'),
    key: 'opportunity_amount',
    width: '9rem',
  },
  {
    label: __('Status'),
    key: 'status',
    width: '10rem',
  },
  {
    label: __('Email'),
    key: 'contact_email',
    width: '12rem',
  },
  {
    label: __('Mobile no'),
    key: 'contact_mobile',
    width: '11rem',
  },
  {
    label: __('Opportunity owner'),
    key: 'opportunity_owner',
    width: '10rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]

const contactColumns = [
  {
    label: __('Name'),
    key: 'name',
    width: '17rem',
  },
  {
    label: __('Email'),
    key: 'email',
    width: '12rem' ,
  },
  {
    label: __('Company'),
    key: 'company_name',
    width: '12rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]

const addressColumns = [
  {
    label: __('Title'),
    key: 'address_title',
    width: '17rem',
  },
  {
    label: __('Type'),
    key: 'address_type',
    width: '12rem' ,
  },
  {
    label: __('Line 1'),
    key: 'address_line1',
    width: '12rem',
  },
  {
    label: __('Phone'),
    key: 'phone',
    width: '12rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]



const activityForm = ref({
  date: '',
  assigned_to: '',
  subject: '',
  description: '',
})

// Close dropdown and show modal
function selectActivity(option) {
  selectedActivity.value = option
  showDropdown.value = false
  showActivityModal.value = true
}

async function createActivity() {
  try {
    const opportunity = await call('frappe.client.insert', {
      doc: {
        doctype: 'Opportunity',
        customer: customer.doc.name,
        opportunity_from: 'Customer',
        party_name:customer.doc.name,
        status: 'Open',
      },
    })
// console.log("opportunity", opportunity.name)
    const event = await call('frappe.client.insert', {
      doc: {
        doctype: 'Event',
        subject: activityForm.value.subject,
        event_category: selectedActivity.value,
        description: activityForm.value.description,

        starts_on: activityForm.value.date,
       event_participants: [
  {
    reference_doctype: 'Opportunity',
    reference_docname: opportunity.name,
  }
]
      },
    })

    createToast({
      title: 'Activity Created',
      icon: 'check',
      variant: 'success',
    })
    showActivityModal.value = false
  } catch (error) {
    createToast({
      title: 'Error',
      icon: 'x',
      variant: 'error',
      message: error.message,
    })
  }
}

const activityBtn = ref(null)
const dropdownPosition = ref({ top: 0, left: 0 })

function toggleDropdown() {
  showDropdown.value = !showDropdown.value
  if (showDropdown.value && activityBtn.value) {
    const rect = activityBtn.value.$el.getBoundingClientRect()
    dropdownPosition.value = {
      top: rect.bottom + window.scrollY,
      left: rect.left + window.scrollX,
    }
  }
}


</script>
