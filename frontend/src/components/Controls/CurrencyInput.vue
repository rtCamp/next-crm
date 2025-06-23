<template>
  <TextInput
    type="text"
    :value="displayValue"
    :placeholder="placeholder"
    :debounce="debounce"
    :class="inputClass"
    :disabled="disabled"
    @focus="handleFocus"
    @blur="handleBlur"
    @input="(e) => (rawInputValue = e.target.value)"
  />
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { TextInput } from 'frappe-ui'
import { formatNumberIntoCurrency } from '../../utils'

const props = defineProps({
  modelValue: [String, Number],
  currency: { type: String, default: 'INR' },
  placeholder: { type: String, default: 'Enter amount' },
  debounce: { type: [Number, String], default: 300 },
  inputClass: { type: [String, Object, Array], default: '' },
  disabled: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'change'])

const isFocused = ref(false)
const internalValue = ref(props.modelValue)
const rawInputValue = ref('')

const displayValue = computed(() => {
  if (isFocused.value) {
    return rawInputValue.value || internalValue.value?.toString() || ''
  }
  return formatNumberIntoCurrency(internalValue.value, props.currency)
})

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== internalValue.value) {
      internalValue.value = newVal
    }
  },
)

function handleFocus() {
  isFocused.value = true
  rawInputValue.value = internalValue.value?.toString() || ''
}

function handleBlur() {
  isFocused.value = false

  const cleanedValue = rawInputValue.value.replace(/[^\d.-]/g, '')
  const numericVal = parseFloat(cleanedValue)
  const newValue = !isNaN(numericVal) ? numericVal : null

  if (newValue !== internalValue.value) {
    internalValue.value = newValue
    emit('update:modelValue', newValue)
    emit('change', newValue)
  }

  rawInputValue.value = ''
}
</script>
