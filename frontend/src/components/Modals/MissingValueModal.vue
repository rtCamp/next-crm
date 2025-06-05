<template>
  <Dialog v-model="show" :options="{ size: '3xl' }">
    <template #body>
      <div class="bg-surface-modal px-4 pb-6 pt-5 sm:px-6">
        <div class="mb-5 flex items-center justify-between">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ label }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button variant="ghost" class="w-7" @click="show = false">
              <FeatherIcon name="x" class="h-4 w-4" />
            </Button>
          </div>
        </div>
        <div>
          <Fields
            v-if="props.filteredFields.length"
            class="border-t"
            :sections="[{ fields: props.filteredFields }]"
            :data="fieldValues"
            @change="handleFieldChange"
          />
          <ErrorMessage class="mt-4" v-if="error" :message="error" />
        </div>
      </div>
      <div class="px-4 pb-7 pt-4 sm:px-6">
        <div class="flex flex-row-reverse gap-2">
          <Button variant="solid" :label="__('Update')" :loading="isUpdating" @click="validateAndEmit" />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import Fields from '@/components/Fields.vue'

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  missingFieldValues: {
    type: Object,
    required: true,
  },
  filteredFields: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['update'])

const show = defineModel()
const error = ref(null)
const isUpdating = ref(false)

const fieldValues = reactive({ ...props.missingFieldValues })

watch(
  () => props.missingFieldValues,
  (newValues) => {
    for (const key in newValues) {
      fieldValues[key] = newValues[key]
    }
  },
  { deep: true, immediate: true },
)

function handleFieldChange({ fieldname, value }) {
  fieldValues[fieldname] = value
}

function validateAndEmit() {
  error.value = null
  const missingFields = []

  props.filteredFields.forEach((field) => {
    if (field.reqd && !fieldValues[field.fieldname]) {
      missingFields.push(field.label || field.fieldname)
    }
  })

  if (missingFields.length) {
    error.value = `Please fill in all required fields: ${missingFields.join(', ')}`
    return
  }

  isUpdating.value = true
  emit('update', { ...fieldValues })
  show.value = false
  isUpdating.value = false
}
</script>
