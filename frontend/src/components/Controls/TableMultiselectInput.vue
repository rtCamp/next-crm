<template>
  <div>
    <div
      :class="[
        'group flex flex-wrap gap-1 min-h-20 p-1.5 rounded text-base bg-surface-gray-2 hover:bg-surface-gray-3 focus:border-outline-gray-4 focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors w-full',
        { 'pointer-events-none opacity-70': isDisabled },
      ]"
    >
      <Button
        ref="valuesRef"
        v-for="value in parsedValues"
        :key="value"
        :label="value"
        theme="gray"
        variant="subtle"
        class="rounded bg-surface-white hover:!bg-surface-gray-1 focus-visible:ring-outline-gray-4"
        @keydown.delete.capture.stop="removeLastValue"
      >
        <template v-if="!isDisabled" #suffix>
          <FeatherIcon class="h-3.5" name="x" @click.stop="removeValue(value)" />
        </template>
      </Button>
      <div class="w-full">
        <Link
          v-if="linkField"
          class="form-control flex-1 truncate cursor-text"
          :value="query"
          :doctype="linkField.options"
          @change="(v) => addValue(v)"
          :hideMe="true"
        >
          <template #target="{ togglePopover }">
            <button class="w-full h-7 cursor-text" @click.stop="togglePopover" />
          </template>
        </Link>
      </div>
    </div>
    <ErrorMessage class="mt-2 pl-2" v-if="error" :message="error" />
  </div>
</template>

<script setup>
import Link from '@/components/Controls/Link.vue'
import { getMeta } from '@/stores/meta'
import { ref, computed, nextTick, watch } from 'vue'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  errorMessage: {
    type: Function,
    default: (value) => `${value} is an Invalid value`,
  },
  defaultValue: {
    type: Array,
    default: () => [],
  },
  read_only: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['change'])

const { getFields } = getMeta(props.doctype)

const values = defineModel({ default: () => [] })
const isDisabled = computed(() => props.read_only || props.disabled)
watch(
  () => props.defaultValue,
  (newValue) => {
    values.value = newValue
  },
  { immediate: true },
)
const valuesRef = ref([])
const error = ref(null)
const query = ref('')

const linkField = ref('')

const parsedValues = computed(() => {
  error.value = ''
  getLinkField()
  if (!linkField.value) return []
  return values.value?.map((row) => row?.[linkField.value?.fieldname]).filter((v) => v)
})

const getLinkField = () => {
  error.value = ''
  if (!linkField.value) {
    let fields = getFields()
    if (!fields) return
    linkField.value = fields?.find((df) => ['Link', 'User'].includes(df.fieldtype))

    if (!linkField.value) {
      error.value = 'Table MultiSelect requires a Table with atleast one Link field'
    }
  }
  return linkField.value
}

const addValue = (value) => {
  error.value = null

  if (values.value?.some((row) => row[linkField.value.fieldname] === value)) {
    error.value = 'Value already exists'
    return
  }
  if (value) {
    values.value = [...values.value, { [linkField.value.fieldname]: value }]

    emit('change', values.value)
    !error.value && (query.value = '')
  }
}
const removeValue = (value) => {
  if (!linkField.value?.fieldname) return

  const key = linkField.value.fieldname

  values.value = values.value.filter((row) => row[key] !== value)
  emit('change', values.value)
}

const removeLastValue = () => {
  if (query.value || !values.value.length) return

  const lastIndex = values.value.length - 1
  const valueRef = valuesRef.value[lastIndex]?.$el

  if (document.activeElement === valueRef) {
    values.value = values.value.slice(0, lastIndex)
    emit('change', values.value)

    nextTick(() => {
      const newLastRef = valuesRef.value[values.value.length - 1]?.$el
      newLastRef?.focus()
    })
  } else {
    valueRef?.focus()
  }
}
</script>
