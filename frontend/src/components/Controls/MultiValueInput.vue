<template>
  <div>
    <div
      class="group flex flex-wrap gap-1 min-h-10 p-1.5 h-auto cursor-text rounded text-base bg-surface-gray-2 hover:bg-surface-gray-3 focus:border-outline-gray-4 focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors w-full"
      @click="setFocus"
    >
      <Button
        ref="emails"
        v-for="value in values"
        :key="value"
        :label="value"
        theme="gray"
        variant="subtle"
        class="rounded bg-surface-gray-3 group-hover:bg-surface-gray-4 focus-visible:ring-outline-gray-4"
        @keydown.delete.capture.stop="removeLastValue"
      >
        <template #suffix>
          <FeatherIcon class="h-3.5" name="x" @click.stop="removeValue(value)" />
        </template>
      </Button>
      <div class="flex-1 min-w-[150px]">
        <Input
          ref="search"
          class="w-full border-none h-7 text-base bg-surface-gray-2 group-hover:bg-surface-gray-3 focus:border-none focus:!shadow-none focus-visible:!ring-0 transition-colors"
          type="text"
          v-model="query"
          :placeholder="placeholder"
          @keydown.capture="handleKeydown"
          @blur="addValue"
        />
      </div>
    </div>
    <ErrorMessage class="mt-2 pl-2" v-if="error" :message="error" />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const props = defineProps({
  validate: {
    type: Function,
    default: null,
  },
  placeholder: {
    type: String,
    default: 'example@email.com',
  },
  errorMessage: {
    type: Function,
    default: (value) => `${value} is an Invalid value`,
  },
  triggerKeys: {
    type: Array,
    default: () => ['Enter', ','], // Default keys to trigger addValue
  },
})

const values = defineModel()

const emails = ref([])
const search = ref(null)
const error = ref(null)
const query = ref('')

const addValue = () => {
  const value = query.value.trim()
  error.value = null

  if (value) {
    const splitValues = value
      .split(',')
      .map((val) => val.trim())
      .filter((val) => val)
    for (const val of splitValues) {
      if (!values.value.includes(val)) {
        if (props.validate && !props.validate(val)) {
          error.value = props.errorMessage(val)
          return
        }
        values.value.push(val)
      }
    }
    if (!error.value) query.value = ''
  }
}

const removeValue = (value) => {
  values.value = values.value.filter((v) => v !== value)
}

const removeLastValue = () => {
  if (query.value) return

  const emailRef = emails.value[emails.value.length - 1]?.$el
  if (document.activeElement === emailRef) {
    values.value.pop()
    nextTick(() => {
      if (values.value.length) {
        const lastEmailRef = emails.value[emails.value.length - 1].$el
        lastEmailRef?.focus()
      } else {
        setFocus()
      }
    })
  } else {
    emailRef?.focus()
  }
}

const handleKeydown = (event) => {
  // first update value of query from input
  query.value = event.target.value
  if (props.triggerKeys.includes(event.key)) {
    event.preventDefault()
    addValue()
  } else if (event.key === 'Backspace' && !query.value) {
    event.preventDefault()
    removeLastValue()
  }
}

function setFocus() {
  search.value?.$el?.focus()
}

defineExpose({ setFocus })
</script>
