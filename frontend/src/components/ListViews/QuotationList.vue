<template>
  <div class="w-[90%] mx-auto space-y-3">
    <div v-if="loading" class="text-center text-ink-gray-5">
      {{ __('Loading quotations...') }}
    </div>

    <div v-else-if="quotations.length === 0" class="text-center text-ink-gray-5">
      {{ __('No quotations linked to this opportunity.') }}
    </div>

    <div v-else class="space-y-4">
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
  opportunityId: { type: String, default: null },
  leadId: { type: String, default: null },
  count: { type: Object, required: true },
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
  loading.value = true

  const filters = []
  if (props.opportunityId) {
    filters.push(['opportunity', '=', props.opportunityId])
  } else if (props.leadId) {
    filters.push(['party_name', '=', props.leadId])
  }

  const res = await call('frappe.client.get_list', {
    doctype: 'Quotation',
    fields: ['name', 'status', 'grand_total', 'creation', 'owner'],
    filters,
    order_by: 'creation desc',
  })

  quotations.value = res || []
  props.count.value = quotations.value.length
  loading.value = false
}


onMounted(fetchQuotations)
watch(
  () => [props.opportunityId, props.leadId],
  fetchQuotations
)
</script>
