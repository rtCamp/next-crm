<template>
  <div class="space-y-1.5 p-[2px] -m-[2px] truncate max-w-40">
    <label class="block" :class="labelClasses" v-if="attrs.label">
      {{ __(attrs.label) }}
    </label>
    <Autocomplete
      ref="autocomplete"
      :options="options.data ?? []"
      v-model="value"
      :size="attrs.size || 'sm'"
      :variant="attrs.variant"
      :placeholder="attrs.placeholder"
      :filterable="false"
      :multiple="props.multiple"
      @update:query="onQueryUpdate"
    >
      <template #target="{ open, togglePopover }">
        <slot name="target" v-bind="{ open, togglePopover }" />
      </template>

      <template #prefix>
        <slot name="prefix" />
      </template>

      <template #item-prefix="{ active, selected, option }">
        <slot name="item-prefix" v-bind="{ active, selected, option }" />
      </template>

      <template #item-label="{ active, selected, option }">
        <slot name="item-label" v-bind="{ active, selected, option }" />
      </template>

      <template #footer="{ value, close }">
        <div v-if="attrs.onCreate">
          <Button
            variant="ghost"
            class="w-full !justify-start"
            :label="__('Create New')"
            @click="attrs.onCreate(value, close)"
          >
            <template #prefix>
              <FeatherIcon name="plus" class="h-4" />
            </template>
          </Button>
        </div>
        <div>
          <Button variant="ghost" class="w-full !justify-start" :label="__('Clear')" @click="() => clearValue(close)">
            <template #prefix>
              <FeatherIcon name="x" class="h-4" />
            </template>
          </Button>
        </div>
      </template>
    </Autocomplete>
  </div>
</template>

<script setup>
import { Autocomplete } from 'frappe-ui'
import { watchDebounced } from '@vueuse/core'
import { createResource } from 'frappe-ui'
import { useAttrs, computed, ref } from 'vue'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  filters: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: [String, Array],
    default: '',
  },
  hideMe: {
    type: Boolean,
    default: false,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const attrs = useAttrs()

const valuePropPassed = computed(() => 'value' in attrs)

const value = computed({
  get: () => {
    if (valuePropPassed.value) {
      if (attrs.value === '') {
        return attrs.value
      } else if (Array.isArray(attrs.value)) {
        return attrs.value
      } else {
        return [attrs.value]
      }
    } else {
      if (Array.isArray(props.modelValue)) {
        return props.modelValue
      } else {
        return [props.modelValue]
      }
    }
  },
  set: (val) => {
    if (props.multiple) {
      if (Array.isArray(val)) {
        const filtered = val.filter((v) => v && v.value !== undefined && v.value !== null && v.value !== '')
        emit(
          valuePropPassed.value ? 'change' : 'update:modelValue',
          filtered.map((v) => v.value),
        )
      } else {
        emit(valuePropPassed.value ? 'change' : 'update:modelValue', [])
      }
    } else {
      emit(valuePropPassed.value ? 'change' : 'update:modelValue', val?.value)
    }
  },
})

const autocomplete = ref(null)
const text = ref('')
const query = ref('')

function onQueryUpdate(val) {
  query.value = val
}

watchDebounced(
  query,
  (val) => {
    val = val || ''
    if (text.value === val) return
    text.value = val
    reload(val)
  },
  { debounce: 300, immediate: false },
)

watchDebounced(
  () => props.doctype,
  () => reload(''),
  { debounce: 300, immediate: true },
)

const options = createResource({
  url: 'frappe.desk.search.search_link',
  cache: [props.doctype, text.value, props.hideMe],
  method: 'POST',
  params: {
    txt: text.value,
    doctype: props.doctype,
    filters: props.filters,
  },
  transform: (data) => {
    let allData = data.map((option) => {
      return {
        label: option.value,
        value: option.value,
      }
    })
    if (!props.hideMe && props.doctype == 'User') {
      allData.unshift({
        label: '@me',
        value: '@me',
      })
    }
    return allData
  },
})

function reload(val) {
  if (options.data?.length && val === options.params?.txt && props.doctype === options.params?.doctype) return

  options.update({
    params: {
      txt: val,
      doctype: props.doctype,
      filters: props.filters,
    },
  })
  options.reload()
}

function clearValue(close) {
  emit(valuePropPassed.value ? 'change' : 'update:modelValue', '')
  close?.()
}

const labelClasses = computed(() => {
  return [
    {
      sm: 'text-xs',
      md: 'text-base',
    }[attrs.size || 'sm'],
    'text-ink-gray-5',
  ]
})
</script>
