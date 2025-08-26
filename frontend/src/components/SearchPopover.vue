<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'xl',
      position: 'top',
    }"
  >
    <template #body>
      <div class="flex items-center relative">
        <div class="pl-4.5 inset-y-0 left-0 flex items-center">
          <FeatherIcon class="h-4" name="search" />
        </div>
        <TextInput
          :type="'search'"
          :variant="'subtle'"
          theme="gray"
          v-model="searchQuery"
          :ref_for="true"
          class="pl-4.5 pr-4.5 w-full border-none bg-transparent py-3 focus:ring-0"
          size="sm"
          placeholder="CRM Search"
          @keydown="handleKeyDown"
        />
      </div>
      <!-- Search Results Section -->
      <div v-if="searchResults.length" class="p-4">
        <ul class="divide-y divide-gray-200">
          <li
            v-for="result in searchResults"
            :key="result.value"
            class="py-2 px-2 hover:bg-gray-50 cursor-pointer"
            @click="handleResultClick(result)"
          >
            <div class="text-base text-gray-800">{{ result.label }}</div>
            <div class="text-sm text-gray-500" v-html="result.value"></div>
          </li>
        </ul>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { createToast } from '@/utils'
import { call, TextInput } from 'frappe-ui'
import { useRouter } from 'vue-router'

const props = defineProps({
  opportunityFrom: {
    type: Object,
    default: {
      opportunityFrom: 'Lead',
      partyName: '',
    },
  },
  docname: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['after'])

const show = defineModel()

const searchQuery = ref('')
const searchResults = ref([])
const loading = ref(false)
const router = useRouter()
const searchDoctypes = ['Lead', 'Opportunity', 'Customer', 'Contact', 'Sales Invoice', 'Prospect', 'CRM Note']
const frontendDoctypes = ['Lead', 'Opportunity', 'Customer', 'Contact']

function handleResultClick(result) {
  if (frontendDoctypes.includes(result.doctype)) {
    // Route in current frontend using vue router
    let params = null
    if (result.doctype === 'Lead') {
      params = { leadId: result.name }
    } else if (result.doctype === 'Opportunity') {
      params = { opportunityId: result.name }
    } else if (result.doctype === 'Customer') {
      params = { customerId: result.name }
    } else if (result.doctype === 'Contact') {
      params = { contactId: result.name }
    }
    show.value = false
    router.push({ name: result.doctype, params: params })
  } else {
    // Open in another view, doctype name should be lowercase and spaces replaced with hyphens
    show.value = false
    const doctypeSlug = result.doctype.toLowerCase().replace(/\s+/g, '-')
    window.open(`/app/${doctypeSlug}/${result.name}`, '_blank')
  }
}

// Add a method to handle the Enter key press
function handleSearch() {
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  loading.value = true
  call('frappe_search.api.search.get_global_search_results', {
    text: searchQuery.value,
    allowed_doctypes: searchDoctypes,
  })
    .then((res) => {
      // Transform and deduplicate results
      console.log('Search results:', res)
      let allData = (res || [])
        .map((option) => ({
          label: option.doctype ? `${option.doctype} : ${option.name}` : option.name,
          value: option.marked_string,
          doctype: option.doctype,
          name: option.name,
        }))
        .filter((option, idx, self) => idx === self.findIndex((t) => t.value === option.value))
      searchResults.value = allData
    })
    .catch(() => {
      createToast({ message: 'Error fetching search results', type: 'error' })
      searchResults.value = []
    })
    .finally(() => {
      loading.value = false
    })
}

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    handleSearch()
  }
}
</script>
