<template>
  <Dialog
    v-model="show"
    :options="{
      title: __('Set Opportunity From'),
      size: 'md',
      actions: [
        {
          label: __('Save'),
          variant: 'solid',
          onClick: setOpportunityFrom,
        },
      ],
    }"
  >
    <template #body-content>
      <div>
        <Select
          class="form-control"
          label="Opportunity From"
          :options="[
            {
              label: 'Lead',
              value: 'Lead',
            },
            {
              label: 'Customer',
              value: 'Customer',
            },
            {
              label: 'Prospect',
              value: 'Prospect',
            },
          ]"
          v-model="_opportunity_fields.opportunity_from"
        />
      </div>
      <div class="mt-6">
        <Link
          class="form-control"
          label="Party Name"
          :value="_opportunity_fields.party_name"
          :doctype="_opportunity_fields.opportunity_from"
          @change="(option) => (_opportunity_fields.party_name = option)"
          :placeholder="__('Party Name')"
          :hideMe="false"
        >
        </Link>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, nextTick, watch, reactive } from 'vue'
import { createToast } from '@/utils'
import { call, Select } from 'frappe-ui'
import Link from '@/components/Controls/Link.vue'

const props = defineProps({
  opportunity_from: {
    type: String,
    default: '',
  },
  party_name: {
    type: String,
    default: '',
  },
  docname: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['after'])

const _opportunity_fields = reactive({
  opportunity_from: '',
  party_name: '',
})

const show = defineModel()

async function setOpportunityFrom() {
  try {
    await call('frappe.client.set_value', {
      doctype: 'Opportunity',
      name: props.docname,
      fieldname: {
        opportunity_from: _opportunity_fields.opportunity_from,
        party_name: _opportunity_fields.party_name,
      },
    })
    show.value = false
    createToast({
      title: __(`Opportunity Updated`),
      icon: 'check',
      iconClasses: 'text-ink-green-4',
    })
    emit('after')
  } catch (error) {
    createToast({
      title: __('Error'),
      text: error,
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  }
}

watch(
  () => show.value,
  (value) => {
    if (!value) return
    nextTick(() => {
      _opportunity_fields.opportunity_from = props.opportunity_from
      _opportunity_fields.party_name = props.party_name
    })
  },
)
</script>
