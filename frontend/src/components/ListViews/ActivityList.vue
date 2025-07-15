<template>
    <div class="w-[90%] mx-auto space-y-3">
      <div v-if="loading" class="text-center text-ink-gray-5">
        {{ __('Loading activities...') }}
      </div>
  
      <div v-else-if="activities.length === 0" class="text-center text-ink-gray-5">
        {{ __('No activities found for this customer.') }}
      </div>
  
      <div v-else class="space-y-4">
        <div
          v-for="activity in activities"
          :key="activity.name"
          class="activity group"
        >
          
          <div class="mb-1 flex items-center justify-between gap-2 py-1 text-base">
            <div class="inline-flex items-center flex-wrap gap-1 text-ink-gray-5">
              <UserAvatar class="mr-1" :user="activity.owner" size="md" />
              <span class="font-medium text-ink-gray-8" :title="getUser(activity.owner)?.full_name">
                {{ getUser(activity.owner)?.full_name || activity.owner }}
              </span>
            </div>
            <Tooltip :text="dateFormat(activity.modified, dateTooltipFormat)">
              <div class="truncate text-sm text-ink-gray-7">
                {{ timeAgo(activity.modified) }}
              </div>
            </Tooltip>
          </div>
  
       
          <div
            class="group flex cursor-pointer flex-col justify-between gap-2 rounded-md bg-surface-gray-1 px-4 py-3 hover:bg-surface-gray-2"
            @click="openEventModal(activity)"

          >
            <div class="flex items-center justify-between">
              <div class="truncate text-lg font-medium text-ink-gray-8">
                {{ activity.event_category }}
              </div>
             
              <div class="text-xs rounded px-2 py-0.5 bg-red-5 text-black"              
               :class="statusColorClass(activity.status)"
              >
                {{ activity.status}}
              </div>
            </div>
            <div class="text-sm font-medium text-ink-gray-8">
              {{ activity.subject }}
            </div>
            <div class="text-sm text-ink-gray-6">
              {{ dateFormat(activity.starts_on, 'MMM DD, YYYY hh:mm A') }}
            </div>
            <div v-if="activity.description" class="text-sm text-ink-gray-7 line-clamp-2">
              {{ activity.description }}
            </div>
          </div>
        </div>
      </div>
      <EventModal
  v-model="showEventModal"
  :event="selectedEvent"
  :doc="props.customerId"
  doctype="Customer"
  v-model:reloadEvents="reloadEvents"
  @after="fetchActivities"
/>


    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { Tooltip, call } from 'frappe-ui'
  import UserAvatar from '@/components/UserAvatar.vue'
  import { usersStore } from '@/stores/users'
  import { dateFormat, timeAgo, dateTooltipFormat } from '@/utils'


  import EventModal from '@/components/Modals/EventModal.vue'

const showEventModal = ref(false)
const selectedEvent = ref({})

function openEventModal(event) {
  selectedEvent.value = { ...event }
  showEventModal.value = true
}



  const props = defineProps({
    customerId: { type: String, required: true },
    count: { type: Object, required: true },

  })


  function statusColorClass(status) {
  switch (status) {
    case 'Open':
      return 'bg-red-500 text-white'
      case 'Completed':
      return 'bg-red-500 text-white'
    case 'Closed':
      return 'bg-green-500 text-white'
    case 'Cancelled':
      return 'bg-red-500 text-white'
    default:
      return 'bg-ink-gray-4 text-white'
  }
}
  const loading = ref(true)
  const activities = ref([])
  const { getUser } = usersStore()
  async function fetchActivities() {
  loading.value = true

  try {
    const oppRes = await fetch('/api/resource/Opportunity?' + new URLSearchParams({
      fields: JSON.stringify(['name']),
      filters: JSON.stringify([['party_name', '=', props.customerId]]),
      limit_page_length: 1000
    }))
    const oppJson = await oppRes.json()
    const opportunityNames = (oppJson.data || []).map(o => o.name)

    if (!opportunityNames.length) {
      activities.value = []
      loading.value = false
      return
    }

    const eventRes = await fetch('/api/method/next_crm.api.api.get_all_events')
    const allEvents = (await eventRes.json()).message || []

    const filteredEvents = allEvents.filter(event =>
      (event.event_participants || []).some(participant =>
        participant.reference_doctype === 'Opportunity' &&
        opportunityNames.includes(participant.reference_docname)
      )
    )

    activities.value = filteredEvents
    props.count.value = filteredEvents.length

  } catch (err) {
    console.error('Error fetching activities:', err)
    activities.value = []
    emit('update:count', 0)
  } finally {
    loading.value = false
  }
}



const reloadEvents = ref({
  reload: fetchActivities,
})



  onMounted(fetchActivities)
  // watch(() => props.customerId, fetchActivities)
  </script>
  