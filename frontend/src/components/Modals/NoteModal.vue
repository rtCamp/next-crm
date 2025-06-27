<template>
  <Dialog
    v-model="show"
    :options="{
      size: 'xl',
      actions: [
        {
          label: editMode ? __('Update') : __('Create'),
          variant: 'solid',
          onClick: () => updateNote(),
        },
      ],
    }"
  >
    <template #body-title>
      <div class="flex items-center gap-3">
        <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
          {{ editMode ? __('Edit Note') : __('Create Note') }}
        </h3>
        <Button
          v-if="_note?.parent"
          size="sm"
          :label="_note.parenttype == 'Opportunity' ? __('Open Opportunity') : __('Open Lead')"
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
            ref="title"
            :label="__('Title')"
            v-model="_note.custom_title"
            :placeholder="__('Call with John Doe')"
          />
        </div>
        <div>
          <div class="mb-1.5 text-xs text-ink-gray-5">{{ __('Content') }}</div>
          <TextEditor
            variant="outline"
            ref="content"
            editor-class="!prose-sm overflow-auto min-h-[180px] max-h-80 py-1.5 px-2 rounded-b border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 hover:shadow-sm focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors"
            :fixed-menu="editorMenu"
            :content="_note.note"
            @change="(val) => (_note.note = val)"
            :placeholder="__('Took a call with John Doe and discussed the new project.')"
            :mentions="users"
          />
        </div>
      </div>
      <FilesUploader
        v-if="props.doc"
        v-model="showFilesUploader"
        :doctype="props.doctype"
        :docname="props.doc"
        @after="
          () => {
            // console.log('hello')
          }
        "
      />
    </template>
  </Dialog>
</template>

<script setup>
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import { capture } from '@/telemetry'
import { TextEditor, call } from 'frappe-ui'
import { ref, computed, nextTick, watch, h } from 'vue'
import { useRouter } from 'vue-router'
import { usersStore } from '@/stores/users'
import { createToast } from '@/utils'
import FilesUploader from '@/components/FilesUploader/FilesUploader.vue'

const props = defineProps({
  note: {
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
const notes = defineModel('reloadNotes')

const emit = defineEmits(['after'])

const { users: usersList } = usersStore()

const router = useRouter()

const title = ref(null)
const editMode = ref(false)
let _note = ref({})

async function updateNote() {
  if (props.note.custom_title === _note.value.custom_title && props.note.note === _note.value.note) return
  try {
    if (_note.value.name) {
      let d = await call('next_crm.api.crm_note.update_note', {
        doctype: props.doctype,
        docname: props.doc || '',
        note_name: _note.value.name,
        note: { custom_title: _note.value.custom_title, note: _note.value.note || '' },
      })
      if (d.name) {
        notes.value?.reload()
        emit('after', d)
      }
      createToast({
        title: __('Note updated successfully'),
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
    } else {
      let d = await call('next_crm.api.crm_note.create_note', {
        doctype: props.doctype,
        docname: props.doc || '',
        title: _note.value.custom_title,
        note: _note.value.note || '',
      })
      if (d.name) {
        capture('note_created')
        notes.value?.reload()
        emit('after', d, true)
      }
      createToast({
        title: __('Note created successfully'),
        icon: 'check',
        iconClasses: 'text-ink-green-3',
      })
    }
    show.value = false
  } catch (error) {
    createToast({
      title: __(`Error ${_note.value.name ? 'updating' : 'creating'} note`),
      text: error.message,
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  }
}

function redirect() {
  if (!props.note?.parent) return
  let name = props.note.parenttype == 'Opportunity' ? 'Opportunity' : 'Lead'
  let params = { leadId: props.note.parent }
  if (name == 'Opportunity') {
    params = { opportunityId: props.note.parent }
  }
  router.push({ name: name, params: params })
}

const users = computed(() => {
  return (
    usersList.data
      ?.filter((user) => user.enabled)
      .map((user) => ({
        label: user.full_name.trimEnd(),
        value: user.name,
      })) || []
  )
})

watch(
  () => show.value,
  (value) => {
    if (!value) return
    editMode.value = false
    nextTick(() => {
      title.value?.el?.focus()
      _note.value = { ...props.note }
      if (_note.value.custom_title || _note.value.note) {
        editMode.value = true
      }
    })
  },
)
const AttachmentIcon = h(
  'svg',
  {
    width: '16',
    height: '16',
    viewBox: '0 0 16 16',
    fill: 'none',
    xmlns: 'http://www.w3.org/2000/svg',
    class: 'w-4 h-4',
  },
  [
    h('path', {
      'fill-rule': 'evenodd',
      'clip-rule': 'evenodd',
      d: 'M12.5684 2.50774C11.5403 1.49742 9.95026 1.49742 8.92215 2.50774L3.62404 7.71417C2.12532 9.18695 2.12532 11.669 3.62404 13.1418C5.12762 14.6194 7.66861 14.6194 9.17219 13.1418L12.1609 10.2049C12.3578 10.0113 12.6744 10.0141 12.8679 10.211C13.0615 10.408 13.0587 10.7246 12.8618 10.9181L9.8731 13.8551C7.98045 15.715 4.81578 15.715 2.92313 13.8551C1.02562 11.9904 1.02562 8.86558 2.92313 7.00091L8.22124 1.79449C9.63842 0.401838 11.8521 0.401838 13.2693 1.79449C14.6914 3.19191 14.6914 5.38225 13.2693 6.77968L13.2668 6.78213L13.2668 6.78212L8.37876 11.5189C8.37834 11.5193 8.37793 11.5197 8.37752 11.5201C7.51767 12.3638 6.11144 12.3939 5.29119 11.5097C4.43611 10.6596 4.40778 9.26893 5.30922 8.46081L7.33823 6.46692C7.53518 6.27337 7.85175 6.27613 8.04531 6.47309C8.23886 6.67005 8.23609 6.98662 8.03913 7.18017L6.0014 9.18264L5.99203 9.19185L5.98219 9.20055C5.5391 9.59243 5.5104 10.3231 6.0014 10.8056L6.01078 10.8148L6.01967 10.8245C6.42299 11.2649 7.18224 11.2926 7.67785 10.8056L7.68034 10.8032L7.68035 10.8032L12.5684 6.06643C12.5688 6.06604 12.5692 6.06565 12.5696 6.06526C13.5917 5.05969 13.5913 3.51289 12.5684 2.50774Z',
      fill: 'currentColor',
    }),
  ],
)
const showFilesUploader = ref(false)
const editorMenu = ref([
  ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 'Heading 6'],
  'Paragraph',
  'Separator',
  'Bold',
  'Italic',
  'Separator',
  'Bullet List',
  'Numbered List',
  'Separator',
  'Align Left',
  'Align Center',
  'Align Right',
  'FontColor',
  'Separator',
  'Image',
  'Video',
  'Link',
  'Blockquote',
  'Code',
  'Horizontal Rule',
  [
    'InsertTable',
    'AddColumnBefore',
    'AddColumnAfter',
    'DeleteColumn',
    'AddRowBefore',
    'AddRowAfter',
    'DeleteRow',
    'MergeCells',
    'SplitCell',
    'ToggleHeaderColumn',
    'ToggleHeaderRow',
    'ToggleHeaderCell',
    'DeleteTable',
  ],
  'Separator',
  'Undo',
  'Redo',
  'Separator',
  {
    label: 'Attach File',
    icon: AttachmentIcon,
    isActive: () => false,
    action: () => {
      showFilesUploader.value = true
    },
  },
])
</script>
