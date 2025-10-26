<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'xl',
      position: 'top',
    }"
  >
    <template #body>
      <div class="flex items-center">
        <TextInput
          :type="'text'"
          :variant="'outline'"
          v-model="searchQuery"
          :ref_for="true"
          class="ml-4.5 pr-4.5 py-3 w-full [&>input]:pl-9 [&>input]:border-none [&>input]:focus-visible:ring-0 [&>input]:outline-0 [&>input]:hover:shadow-none [&>input]:focus:border-none"
          size="sm"
          placeholder="CRM Search"
          @keydown="handleKeyDown"
        >
          <template #prefix>
            <FeatherIcon class="h-4" name="search" />
          </template>
        </TextInput>
      </div>
      <hr />
      <div v-if="searchResults.length" class="p-4 max-h-96 overflow-y-auto">
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
      <hr />
      <div v-if="searchResults.length" class="flex items-center justify-between px-4.5 h-12">
        <div>
          <p v-if="!loadMoreSearch && searchResults.length" class="text-xs text-gray-600">
            <b>{{ searchResults?.length }} results</b> found
          </p>
        </div>
        <div v-if="searchResults.length" class="p-4 flex justify-center">
          <Button v-if="loadMoreSearch" variant="subtle" class="" @click="loadMoreResults"> Load More </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref } from 'vue'
import { call, TextInput, toast } from 'frappe-ui'
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
const searchDoctypes = ['Lead', 'Opportunity', 'Customer', 'Contact', 'Address', 'Prospect', 'ToDo']
const frontendDoctypes = ['Lead', 'Opportunity', 'Customer', 'Contact', 'Address', 'Prospect']
const loadMoreSearch = ref(false)
let searchOffset = 0

function handleResultClick(result) {
  if (frontendDoctypes.includes(result.doctype)) {
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
    searchResults.value = []
    searchQuery.value = ''
    router.push({ name: result.doctype, params: params })
  } else {
    show.value = false
    const doctypeSlug = result.doctype.toLowerCase().replace(/\s+/g, '-')
    window.open(`/app/${doctypeSlug}/${result.name}`, '_blank')
  }
}

function loadMoreResults() {
  searchOffset += 50
  handleSearch(true)
}

function handleSearch(loadMore = false) {
  if (!loadMore) searchOffset = 0
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  loading.value = true
  call('frappe_search.api.search.get_global_search_results', {
    text: searchQuery.value,
    allowed_doctypes: searchDoctypes,
    limit: 50,
    start: searchOffset,
  })
    .then((res) => {
      if (!res || res.length === 0) {
        searchResults.value = []
        return
      }
      let searchResultsList = res[0] || []
      loadMoreSearch.value = res[1] || false
      let allData = (searchResultsList || [])
        .map((option) => ({
          label: option.doctype ? `${option.doctype} : ${option.name}` : option.name,
          value: option.marked_string,
          doctype: option.doctype,
          name: option.name,
        }))
        .filter((option, idx, self) => idx === self.findIndex((t) => t.value === option.value))
      if (loadMore) allData = [...searchResults.value, ...allData]
      searchResults.value = allData
    })
    .catch(() => {
      toast.error(__('Error fetching search results'))
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
