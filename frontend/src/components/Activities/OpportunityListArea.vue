<template>
  <OpportunitiesListView
    v-if="rows.length"
    :rows="rows"
    :columns="columns"
    :options="{ selectable: false, showTooltip: false }"
  />
</template>
<script setup>
import OpportunitiesListView from '@/components/ListViews/OpportunitiesListView.vue'
import { computed } from 'vue'
import { usersStore } from '@/stores/users.js'
import { statusesStore } from '@/stores/statuses'

const { getUser } = usersStore()
const { getDealStatus } = statusesStore()

const props = defineProps({
  opportunities: Array,
  docname: String,
  doctype: String,
})

const rows = computed(() => {
  if (!props.opportunities || props.opportunities == []) return []

  return props.opportunities.map((row) => getOpportunityRowObject(row))
})

const columns = computed(() => opportunityColumns)

function getOpportunityRowObject(opportunity) {
  return {
    name: opportunity.name,
    title: opportunity.title,
    status: {
      label: opportunity.status,
      color: getDealStatus(opportunity.status)?.iconColorClass,
    },
    opportunity_owner: {
      label: opportunity.opportunity_owner && getUser(opportunity.opportunity_owner).full_name,
      ...(opportunity.opportunity_owner && getUser(opportunity.opportunity_owner)),
    },
  }
}

const opportunityColumns = [
  {
    label: __('Title'),
    key: 'title',
    width: '20rem',
  },
  {
    label: __('Status'),
    key: 'status',
    width: '8rem',
  },
  {
    label: __('Opportunity owner'),
    key: 'opportunity_owner',
    width: '10rem',
  },
]
</script>
