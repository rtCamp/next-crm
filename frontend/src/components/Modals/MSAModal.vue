<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'lg',
      title: label,
      actions: [
        {
          label: __('Update'),
          variant: 'solid',
          onClick: validateAndEmit,
        },
      ],
    }"
  >
    <template #body-content>
      <div>
        <p class="text-sm">If MSA is not in place yet, please enter tentative Start Date of MSA.</p>
      </div>
      <div class="flex flex-row gap-4">
        <div>
          <div class="mt-4">
            <DatePicker
              v-model="fieldValues.msa_start_date"
              :placeholder="'MSA Start Date'"
              input-class="border-none"
            />
          </div>
          <div class="mt-4">
            <DatePicker v-model="fieldValues.msa_end_date" :placeholder="'MSA End Date'" input-class="border-none" />
          </div>
          <div class="mt-4">
            <FormControl type="text" :placeholder="'MSA Document Link'" v-model="fieldValues.msa_document_link" />
          </div>
        </div>
        <div>
          <div class="mt-4">
            <FormControl
              class="form-control"
              type="checkbox"
              v-model="fieldValues.insurance_requested"
              :label="'Insurance Requested'"
            />
          </div>
          <div v-if="fieldValues.insurance_requested">
            <div class="mt-4">
              <DatePicker
                v-model="fieldValues.insurance_start_date"
                :placeholder="'Insurance Start Date'"
                input-class="border-none"
              />
            </div>
            <div class="mt-4">
              <DatePicker
                v-model="fieldValues.insurance_end_date"
                :placeholder="'Insurance End Date'"
                input-class="border-none"
              />
            </div>
            <div class="mt-4">
              <FormControl
                type="text"
                :placeholder="'Insurance Document Link'"
                v-model="fieldValues.insurance_document_link"
              />
            </div>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { DatePicker, call } from 'frappe-ui'
import { createToast } from '../../utils'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  customer: {
    type: String,
    required: true,
  },
})

const fieldValues = reactive({
  msa_start_date: '',
  msa_end_date: '',
  msa_document_link: '',
  insurance_document_link: '',
  insurance_requested: false,
  insurance_start_date: '',
  insurance_end_date: '',
})

const emit = defineEmits(['msa_set'])

const show = defineModel()
const isUpdating = ref(false)

setDefaultValues()

function setDefaultValues() {
  call('frappe.client.get_value', {
    doctype: 'Customer',
    filters: { name: props.customer },
    fieldname: [
      'custom_msa_start_date',
      'custom_msa_end_date',
      'custom_msa_document_link',
      'custom_insurance_document_link',
      'custom_insurance_requested',
      'custom_insurance_start_date',
      'custom_insurance_end_date',
    ],
  }).then((response) => {
    if (response) {
      fieldValues.msa_start_date = response.custom_msa_start_date || ''
      fieldValues.msa_end_date = response.custom_msa_end_date || ''
      fieldValues.msa_document_link = response.custom_msa_document_link || ''
      fieldValues.insurance_document_link = response.custom_insurance_document_link || ''
      fieldValues.insurance_requested = response.custom_insurance_requested || false
      fieldValues.insurance_start_date = response.custom_insurance_start_date || ''
      fieldValues.insurance_end_date = response.custom_insurance_end_date || ''
    }
  })
}

function validateAndEmit() {
  if (!fieldValues.msa_start_date) {
    createToast({
      title: __('Error'),
      text: __('MSA Start Date is required.'),
      icon: 'x',
      iconClasses: 'text-ink-red-3',
    })
    return
  }
  if (fieldValues.msa_start_date && fieldValues.msa_end_date) {
    if (new Date(fieldValues.msa_start_date) >= new Date(fieldValues.msa_end_date)) {
      createToast({
        title: __('Error'),
        text: __('MSA Start Date must be before MSA End Date.'),
        icon: 'x',
        iconClasses: 'text-ink-red-3',
      })
      return
    }
  } else if (fieldValues.insurance_requested) {
    if (fieldValues.insurance_start_date && fieldValues.insurance_end_date) {
      if (new Date(fieldValues.insurance_start_date) >= new Date(fieldValues.insurance_end_date)) {
        createToast({
          title: __('Error'),
          text: __('Insurance Start Date must be before Insurance End Date.'),
          icon: 'x',
          iconClasses: 'text-ink-red-3',
        })
        return
      }
    }
  } else if (!fieldValues.msa_document_link) {
    createToast({
      title: __('Info'),
      text: `MSA should be signed and updated by ${new Date(fieldValues.msa_start_date).setDate(
        new Date(fieldValues.msa_start_date).getDate() + 30,
      )}`,
      icon: 'info',
      iconClasses: 'text-ink-blue-3',
    })
  }

  isUpdating.value = true

  call('frappe.client.set_value', {
    doctype: 'Customer',
    name: props.customer,
    fieldname: {
      custom_msa_start_date: fieldValues.msa_start_date,
      custom_msa_end_date: fieldValues.msa_end_date,
      custom_msa_document_link: fieldValues.msa_document_link,
      custom_insurance_document_link: fieldValues.insurance_document_link,
      custom_insurance_requested: fieldValues.insurance_requested,
      custom_insurance_start_date: fieldValues.insurance_start_date,
      custom_insurance_end_date: fieldValues.insurance_end_date,
    },
  })
    .then(() => {
      createToast({
        title: __('Success'),
        text: __('MSA details updated successfully.'),
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
      emit('msa_set')
    })
    .catch((err) => {
      createToast({
        title: __('Error'),
        text: err.message || __('Failed to update MSA details.'),
        icon: 'x',
        iconClasses: 'text-ink-red-3',
      })
    })
    .finally(() => {
      isUpdating.value = false
    })
  emit('msa_set')
  isUpdating.value = false
}
</script>
