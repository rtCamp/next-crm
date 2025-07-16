<template>
 
    <div class="mx-4 my-3 flex items-center justify-between text-lg font-medium sm:mx-10 sm:mb-4 sm:mt-8">
      <div class="flex h-8 items-center text-xl font-semibold text-ink-gray-8">
        {{ __('Quotations') }}
      </div>
      <Button variant="solid" @click="goToNewQuotation">
        <template #prefix>
          <FeatherIcon name="plus" class="h-4 w-4" />
        </template>
        <span>{{ __('Create Quotation') }}</span>
      </Button>
    </div>
  
<div v-if="quotations.length === 0" class="flex flex-1 min-h-[40vh] items-center justify-center">
<div class="flex flex-col items-center justify-center gap-3 text-xl font-medium text-ink-gray-4">
  <FeatherIcon name="file-text" class="h-10 w-10" />
  <span>{{ __('No Quotations') }}</span>
  <Button :label="__('Create Quotation')" @click="goToNewQuotation" />
</div>


  </div>
  <div v-else class="w-[90%] mx-auto space-y-3 mt-2">
    <!-- <div v-if="loading" class="text-center text-ink-gray-5">
      {{ __('Loading quotations...') }}
    </div> -->

    
    <div  class="space-y-4">
      <div
        v-for="quotation in quotations"
        :key="quotation.name"
        class="activity group"
      >
        <!-- Header -->
        <div class="mb-1 flex items-center justify-stretch gap-2 py-1 text-base">
          <div class="inline-flex items-center flex-wrap gap-1 text-ink-gray-5">
            <UserAvatar class="mr-1" :user="quotation.owner" size="md" />
            <span class="font-medium text-ink-gray-8" :title="getUser(quotation.owner).full_name">
              {{ getUser(quotation.owner).full_name }}
            </span>
          </div>
          <div class="flex items-center gap-2 ml-auto whitespace-nowrap">
            <Tooltip :text="dateFormat(quotation.creation, dateTooltipFormat)">
              <div class="truncate text-sm text-ink-gray-7">
                {{ timeAgo(quotation.creation) }}
              </div>
            </Tooltip>

            <Dropdown
              :options="[
                {
                  label: __('Cancel Quotation'),
                  icon: 'x',
                  onClick: () => cancelQuotation(quotation.name),
                },
              ]"
              @click.stop
              class="h-6 w-6"
            >
              <Button icon="more-horizontal" variant="ghosted" class="!h-6 !w-6 hover:bg-surface-gray-2" />
            </Dropdown>
          </div>
        </div>

        <!-- Card -->
        <div
          class="activity group flex max-h-64 cursor-pointer flex-col justify-between gap-2 rounded-md bg-surface-gray-1 px-4 py-3 hover:bg-surface-gray-2"
          @click="goToQuotation(quotation.name)"
        >
          <div class="flex items-center justify-between">
            <div class="truncate text-lg font-medium text-ink-gray-8">
              {{ quotation.name }}
            </div>
            <div
              class="text-xs rounded px-2 py-0.5"
              :class="statusColorClass(quotation.status)"
            >
              {{ quotation.status }}
            </div>
          </div>
          <div class="text-sm text-ink-gray-6">
            {{ __('Amount') }}: ₹{{ quotation.grand_total.toLocaleString() }}
          </div>
        </div>
      </div>
    </div>
  </div>

</template>




<script setup>
import { ref, onMounted, watch } from 'vue'
import { call, Tooltip, Dropdown, Button } from 'frappe-ui'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { usersStore } from '@/stores/users'
import UserAvatar from '@/components/UserAvatar.vue'
import { dateFormat, dateTooltipFormat, timeAgo, createToast } from '@/utils'

dayjs.extend(relativeTime)

const props = defineProps({
  opportunityId: String,
  leadId: String,
  count: Object,
})



const quotations = ref([])
const loading = ref(true)
const { getUser } = usersStore()

function statusColorClass(status) {
  switch (status) {
    case 'Draft':
      return 'bg-red-500 text-white'
      case 'Open':
      return 'bg-red-500 text-white'
    case 'Submitted':
      return 'bg-green-500 text-white'
    case 'Cancelled':
      return 'bg-red-500 text-white'
    default:
      return 'bg-ink-gray-4 text-white'
  }
}

function goToQuotation(name) {
  window.location.href = `/app/quotation/${name}`
}

async function cancelQuotation(name) {
  try {
    await call('frappe.client.cancel', {
      doctype: 'Quotation',
      name,
    })
    createToast({
      title: __('Quotation cancelled'),
      icon: 'check',
      iconClasses: 'text-green-500',
    })
    await fetchQuotations()
  } catch (error) {
    createToast({
      title: __('Failed to cancel quotation'),
      text: error.message,
      icon: 'x',
      iconClasses: 'text-red-500',
    })
  }
}
async function fetchQuotations() {

  const filters = []
  if (props.opportunityId) {
    filters.push(['opportunity', '=', props.opportunityId])
  } 
  if (props.leadId) {
    filters.push(['party_name', '=', props.leadId])
  }

  console.log('Quotation Filters:', filters)

  const res = await call('frappe.client.get_list', {
    doctype: 'Quotation',
    fields: ['name', 'status', 'grand_total', 'creation', 'owner'],
    filters,
    order_by: 'creation desc',
  })
  console.log('All Quotations:', res)

  quotations.value = res || []
  props.count.value = quotations.value.length
  loading.value = false
}


onMounted(fetchQuotations)
watch(
  () => [props.opportunityId, props.leadId],
  fetchQuotations
)



function goToNewQuotation() {
  const isOpportunity = Boolean(props.opportunityId)
  const quotationTo = isOpportunity ? 'Opportunity' : 'Lead'
  const partyName = isOpportunity ? props.opportunityId : props.leadId

  const url = `/app/quotation/new?quotation_to=${quotationTo}&party_name=${partyName}`
  window.location.href = url
}


</script>
