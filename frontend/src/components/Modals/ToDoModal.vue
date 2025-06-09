<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'xl',
      actions: [
        {
          label: editMode ? __('Update') : __('Create'),
          variant: 'solid',
          onClick: () => updateToDo(),
        },
      ],
    }"
  >
    <template #body-title>
      <div class="flex items-center gap-3">
        <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
          {{ editMode ? __('Edit ToDo') : __('Create ToDo') }}
        </h3>
        <Button
          v-if="todo?.reference_name"
          size="sm"
          :label="todo.reference_type == 'Opportunity' ? __('Open Opportunity') : __('Open Lead')"
          @click="redirect()"
        >
          <template #suffix>
            <ArrowUpRightIcon class="h-4 w-4" />
          </template>
        </Button>
      </div>
    </template>
    <template #body-content>
      <div class="flex flex-col gap-4">
        <div>
          <FormControl
            ref="custom_title"
            :label="__('Title')"
            v-model="_todo.custom_title"
            :placeholder="__('Call with John Doe')"
          />
        </div>
        <div>
          <div class="mb-1.5 text-xs text-ink-gray-5">
            {{ __('Description') }}
          </div>
          <TextEditor
            variant="outline"
            ref="description"
            editor-class="!prose-sm overflow-auto min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 hover:shadow-sm focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors"
            :bubbleMenu="true"
            :content="_todo.description"
            @change="(val) => (_todo.description = val)"
            :placeholder="__('Took a call with John Doe and discussed the new project.')"
          />
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <Dropdown :options="todoStatusOptions(updateToDoStatus)">
            <Button :label="_todo.status" class="w-full justify-between">
              <template #prefix>
                <ToDoStatusIcon :status="_todo.status" />
              </template>
            </Button>
          </Dropdown>
          <Link
            class="form-control"
            :value="getUser(_todo.allocated_to).full_name"
            doctype="User"
            @change="(option) => (_todo.allocated_to = option)"
            :placeholder="__('John Doe')"
            :hideMe="true"
            :filters="[['User', 'user_type', '=', 'System User']]"
          >
            <template #prefix>
              <UserAvatar class="mr-2 !h-4 !w-4" :user="_todo.allocated_to" />
            </template>
            <template #item-prefix="{ option }">
              <UserAvatar class="mr-2" :user="option.value" size="sm" />
            </template>
            <template #item-label="{ option }">
              <Tooltip :text="option.value">
                <div class="cursor-pointer">
                  {{ getUser(option.value).full_name }}
                </div>
              </Tooltip>
            </template>
          </Link>
          <DatePicker
            v-if="!(fromTime && toTime)"
            class="datepicker w-36"
            v-model="_todo.date"
            :placeholder="__('01/04/2024')"
            input-class="border-none"
          />
          <DateTimePicker
            v-if="fromTime"
            class="datepicker w-36"
            v-model="_todo.custom_from_time"
            :placeholder="__('From Time')"
            input-class="border-none"
          />
          <DateTimePicker
            v-if="toTime"
            class="datepicker w-36"
            v-model="_todo.custom_to_time"
            :placeholder="__('To Time')"
            input-class="border-none"
          />
          <Dropdown :options="todoPriorityOptions(updateToDoPriority)">
            <Button :label="_todo.priority" class="w-full justify-between">
              <template #prefix>
                <ToDoPriorityIcon :priority="_todo.priority" />
              </template>
            </Button>
          </Dropdown>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <FormControl
            class="form-control"
            type="checkbox"
            v-model="_event.sync_with_google_calendar"
            @change="(e) => (_event.sync_with_google_calendar = e.target.checked)"
          />
          <label
            class="text-sm text-ink-gray-5"
            @click="_event.sync_with_google_calendar = !_event.sync_with_google_calendar"
          >
            {{ __('Sync with Google Calendar') }}
          </label>
          <Link
            v-if="_event.sync_with_google_calendar"
            class="form-control"
            :value="_event.google_calendar"
            doctype="Google Calendar"
            @change="(option) => (_event.google_calendar = option)"
            :placeholder="__('Google Calendar')"
            :hideMe="true"
            :filters="{ enable: 1 }"
          >
          </Link>
        </div>
        <div class="flex flex-wrap items-center gap-2 w-full" v-if="_event.sync_with_google_calendar">
          <!-- Multi input to enter email addresses for event participants. -->
          <MultiValueInput
            v-model="event_participants"
            class="flex-grow"
            :placeholder="__('Add participants')"
            :errorMessage="(value) => __('Invalid email address: {0}', [value])"
            :validate="validate"
            :error="(value) => !validate(value)"
            :hideMe="true"
            :triggerKeys="['Enter', ',', 'Tab', ' ']"
          ></MultiValueInput>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import ToDoStatusIcon from '@/components/Icons/ToDoStatusIcon.vue'
import ToDoPriorityIcon from '@/components/Icons/ToDoPriorityIcon.vue'
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import Link from '@/components/Controls/Link.vue'
import MultiValueInput from '../Controls/MultiValueInput.vue'
import { todoStatusOptions, todoPriorityOptions } from '@/utils'
import { usersStore } from '@/stores/users'
import { capture } from '@/telemetry'
import { TextEditor, Dropdown, Tooltip, call, DatePicker, DateTimePicker } from 'frappe-ui'
import { ref, watch, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMeta } from '@/stores/meta'
import { createToast } from '@/utils'

const props = defineProps({
  todo: {
    type: Object,
    default: {},
  },
  doctype: {
    type: String,
    default: 'Lead',
  },
  doc: {
    type: String,
    default: '',
  },
})

const show = defineModel()
const todos = defineModel('reloadToDos')

const emit = defineEmits(['updateToDo', 'after'])

const router = useRouter()
const { getUser } = usersStore()

const custom_title = ref(null)
const editMode = ref(false)
const fromTime = ref(false)
const toTime = ref(false)

const _todo = ref({
  custom_title: '',
  description: '',
  allocated_to: '',
  assigned_by: '',
  date: '',
  status: 'Open',
  priority: 'Medium',
  reference_type: props.doctype,
  reference_name: null,
  custom_linked_event: '',
})

const _event = ref({
  sync_with_google_calendar: getUser().google_calendar ? 1 : 0,
  google_calendar: getUser().google_calendar,
})

const event_participants = ref([])

function updateToDoStatus(status) {
  _todo.value.status = status
}

function updateToDoPriority(priority) {
  _todo.value.priority = priority
}

function redirect() {
  if (!props.todo?.reference_name) return
  let name = props.todo.reference_type == 'Opportunity' ? 'Opportunity' : 'Lead'
  let params = { leadId: props.todo.reference_name }
  if (name == 'Opportunity') {
    params = { opportunityId: props.todo.reference_name }
  }
  router.push({ name: name, params: params })
}

async function updateToDo() {
  if (!_todo.value.allocated_to) {
    _todo.value.allocated_to = getUser().name
  }
  _todo.value.assigned_by = getUser().name

  if (!_todo.value.description.trim() && !_todo.value.custom_title.trim()) {
    createToast({
      title: __(`Error ${editMode.value ? 'updating' : 'adding'} ToDo`),
      text: __('ToDo must have either a title or a description.'),
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
    return
  }

  try {
    let current_doc_link = new URL(window.location.href)
    current_doc_link.hash = '#todos'
    if (_todo.value.name) {
      if (fromTime && toTime) {
        if (!_todo.value.custom_to_time || !_todo.value.custom_from_time) {
          createToast({
            title: __('Validation error'),
            text: __('From Time and To Time is required'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }
        const fromDateTime = new Date(_todo.value.custom_from_time).getTime()
        const toDateTime = new Date(_todo.value.custom_to_time).getTime()

        if (toDateTime < fromDateTime) {
          createToast({
            title: __('Validation error'),
            text: __('To Time cannot be earlier than From Time'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }

        if (_todo.value.custom_to_time) {
          const datetimeStr = _todo.value.custom_to_time
          const dateStr = new Date(datetimeStr)?.toISOString()?.split('T')[0]
          _todo.value.date = dateStr
        }
      }

      if (!_event.value.sync_with_google_calendar) {
        _event.value.google_calendar = null
      } else if (!_event.value.google_calendar) {
        createToast({
          title: __('Error'),
          text: __('Select Google Calendar to which event should be synced'),
          icon: 'x',
          iconClasses: 'text-ink-red-4',
        })
        return
      }

      try {
        if (_event.value.name) {
          _event.value.event_participants = _event.value.event_participants.filter(
            (participant) => participant.reference_doctype !== 'User' || participant.reference_docname !== 'Guest',
          )
          _event.value.event_participants = [
            ..._event.value.event_participants,
            ...event_participants.value.map((email) => ({
              reference_doctype: 'User',
              reference_docname: 'Guest',
              email: email,
            })),
          ]

          await call('frappe.client.set_value', {
            doctype: 'Event',
            name: _event.value.name,
            fieldname: {
              ..._event.value,
              subject: 'ToDo: ' + (_todo.value.custom_title || __('No Title')),
              description: (_todo.value.description || '') + `\n\n${__('Created from {0}', [current_doc_link.href])}`,
              starts_on: _todo.value.custom_from_time,
              ends_on: _todo.value.custom_to_time,
            },
          })
        }
      } catch (error) {
        createToast({
          title: __('Error updating event'),
          text: __(error.message),
          icon: 'x',
          iconClasses: 'text-ink-red-4',
        })
        return
      }

      let d = await call('frappe.client.set_value', {
        doctype: 'ToDo',
        name: _todo.value.name,
        fieldname: _todo.value,
      })
      if (d.name) {
        todos.value.reload()
      }
      createToast({
        title: __('Todo updated successfully'),
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
    } else {
      if (fromTime && toTime) {
        if (!_todo.value.custom_to_time || !_todo.value.custom_from_time) {
          createToast({
            title: __('Validation error'),
            text: __('From Time and To Time is required'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }
        const fromDateTime = new Date(_todo.value.custom_from_time).getTime()
        const toDateTime = new Date(_todo.value.custom_to_time).getTime()

        if (toDateTime < fromDateTime) {
          createToast({
            title: __('Validation error'),
            text: __('To Time cannot be earlier than From Time'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }

        if (_todo.value.custom_to_time) {
          const datetimeStr = _todo.value.custom_to_time
          const dateStr = new Date(datetimeStr)?.toISOString()?.split('T')[0]
          _todo.value.date = dateStr
        }
      }
      _todo.value.custom_linked_event = ''

      if (!_event.value.sync_with_google_calendar) {
        _event.value.google_calendar = null
      } else if (!_event.value.google_calendar) {
        createToast({
          title: __('Error'),
          text: __('Select Google Calendar to which event should be synced'),
          icon: 'x',
          iconClasses: 'text-ink-red-4',
        })
        return
      }

      if (_event.value.sync_with_google_calendar) {
        if (!_todo.value.custom_from_time || !_todo.value.custom_to_time) {
          createToast({
            title: __('Validation error'),
            text: __('From Time and To Time is required to sync with Google Calendar'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }

        let doc = {
          doctype: 'Event',
          event_participants: [
            ...event_participants.value.map((email) => ({
              reference_doctype: 'User',
              reference_docname: 'Guest',
              email: email,
            })),
          ],
          custom_create_free_event: 1,
          subject: 'ToDo: ' + (_todo.value.custom_title || __('No Title')),
          description: (_todo.value.description || '') + `\n\n${__('Created from {0}', [current_doc_link.href])}`,
          starts_on: _todo.value.custom_from_time,
          ends_on: _todo.value.custom_to_time,
          status: 'Open',
          event_type: 'Private',
          event_category: 'Event',
          ..._event.value,
        }
        let d = await call('frappe.client.insert', {
          doc: doc,
        })
        if (d.name) {
          _todo.value.custom_linked_event = d.name
          capture('event_created')
        } else {
          createToast({
            title: __('Error creating event'),
            text: __('Please try again later.'),
            icon: 'x',
            iconClasses: 'text-ink-red-4',
          })
          return
        }
      }
      let d = await call('frappe.client.insert', {
        doc: {
          doctype: 'ToDo',
          reference_type: props.doctype,
          reference_name: props.doc || null,
          ..._todo.value,
        },
      })
      if (d.name) {
        capture('todo_created')
        todos.value.reload()
        emit('after')
      }
      createToast({
        title: __('Todo created successfully'),
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
    }
    show.value = false
  } catch (error) {
    createToast({
      title: __(`Error ${editMode.value ? 'updating' : 'adding'} ToDo`),
      text: __(error.message),
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  }
}

async function render() {
  editMode.value = false
  nextTick(async () => {
    custom_title.value?.el?.focus?.()
    _todo.value = { ...props.todo }

    if (_todo.value._event) {
      _event.value = _todo.value._event

      if (_event.value.name) {
        // get event_participants from event, if any
        event_participants.value = (_event.value.event_participants || [])
          .filter(
            (participant) => participant.reference_doctype === 'User' && participant.reference_docname === 'Guest',
          )
          .map((participant) => participant.email)
      } else {
        event_participants.value = [getUser().email]
      }
    } else {
      _event.value = {
        sync_with_google_calendar: getUser().google_calendar ? 1 : 0,
        google_calendar: getUser().google_calendar,
      }
      event_participants.value = [getUser().email]
    }

    const { getFields } = await getMeta('ToDo')
    const todoFields = getFields()
    fromTime.value = todoFields?.some((item) => item.fieldname === 'custom_from_time')
    toTime.value = todoFields?.some((item) => item.fieldname === 'custom_to_time')

    if (_todo.value.description) {
      editMode.value = true
    }
  })
}

onMounted(() => show.value && render())

watch(show, (value) => {
  if (!value) return
  render()
})
</script>

<style scoped>
:deep(.datepicker svg) {
  width: 0.875rem;
  height: 0.875rem;
}
</style>
