<template>
  <div class="relative w-full">
    <div class="sm:mx-10 mx-4 max-h-[50vh] overflow-y-auto border-t px-1">
      <input
        v-model="title"
        type="text"
        class="flex-1 border-none text-ink-gray-9 text-base bg-surface-white hover:bg-surface-white focus:border-none focus:!shadow-none focus-visible:!ring-0 my-2 px-0 w-full"
        :placeholder="__('Call with John Doe')"
      />
      <TextEditor
        ref="textEditor"
        :editor-class="['prose-sm max-w-none', editable && 'min-h-[7rem]']"
        :content="content"
        @change="editable ? (content = $event) : null"
        :starterkit-options="{ heading: { levels: [2, 3, 4, 5, 6] } }"
        :placeholder="__('Took a call with John Doe and discussed the new project.')"
        :editable="editable"
        :mentions="users"
      >
        <template v-slot:editor="{ editor }">
          <EditorContent :class="['border-t py-3 overflow-y-auto max-h-[40vh]']" :editor="editor" />
        </template>

        <template v-slot:bottom>
          <div class="my-3">
            <AttachmentArea :attachments="filteredAttachments" @reload="updateAttachments()" />
          </div>
          <div v-if="editable" class="flex justify-between items-center py-2 border-t">
            <div class="flex gap-2 items-center">
              <TextEditorBubbleMenu :buttons="textEditorMenuButtons" />
              <IconPicker v-model="emoji" v-slot="{ togglePopover }" @update:modelValue="() => appendEmoji()">
                <Button variant="ghost" @click="togglePopover()">
                  <SmileIcon class="h-4" />
                </Button>
              </IconPicker>
              <Button v-if="props.doctype" variant="ghost" @click="showFilesUploader = true">
                <AttachmentIcon />
              </Button>
            </div>
            <div class="flex gap-2">
              <Button v-bind="discardButtonProps || {}" :label="__('Discard')" />
              <Button variant="solid" v-bind="submitButtonProps || {}" :label="__('Add Note')" />
            </div>
          </div>
        </template>
      </TextEditor>
      <FilesUploader
        v-if="props.doctype"
        v-model="showFilesUploader"
        :doctype="props.doctype"
        :docname="props.docname"
        @after="
          (files) => {
            updateAttachments(files)
          }
        "
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineModel, watch } from 'vue'
import { EditorContent } from '@tiptap/vue-3'
import { TextEditor, TextEditorBubbleMenu } from 'frappe-ui'
import IconPicker from '@/components/IconPicker.vue'
import SmileIcon from '@/components/Icons/SmileIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import { usersStore } from '@/stores/users'
import { capture } from '@/telemetry'
import AttachmentArea from './Activities/AttachmentArea.vue'
import FilesUploader from '@/components/FilesUploader/FilesUploader.vue'

const props = defineProps({
  editable: {
    type: Boolean,
    default: true,
  },
  submitButtonProps: Object,
  discardButtonProps: Object,
  doctype: String,
  docname: String,
  attachments: Array,
  reload: Function,
})

const title = defineModel('title')
const content = defineModel('content')
const fileAttachments = defineModel('fileAttachments')

const textEditor = ref(null)
const emoji = ref('')
const editor = computed(() => textEditor.value?.editor)
const showFilesUploader = ref(false)

const emit = defineEmits(['reload'])

const filteredAttachments = ref([])

const updateAttachments = (files) => {
  if (files?.length > 0) {
    fileAttachments.value = [...files, ...fileAttachments.value]
  }
  emit('reload')
}

watch(
  [() => props.attachments, fileAttachments],
  ([attachments, fileNames]) => {
    if (!attachments || !fileNames?.length) {
      filteredAttachments.value = []
      return
    }
    filteredAttachments.value = attachments?.filter((att) => fileNames?.includes(att.name))
  },
  { immediate: true },
)

function appendEmoji() {
  editor.value?.commands.insertContent(emoji.value)
  editor.value?.commands.focus()
  capture('emoji_inserted_in_note', { emoji: emoji.value })
  emoji.value = ''
}

const { users: usersList } = usersStore()
const users = computed(
  () =>
    usersList.data
      ?.filter((u) => u.enabled)
      .map((u) => ({
        label: u.full_name.trimEnd(),
        value: u.name,
      })) || [],
)

const textEditorMenuButtons = [
  'Paragraph',
  ['Heading 2', 'Heading 3', 'Heading 4'],
  'Bold',
  'Italic',
  'Bullet List',
  'Numbered List',
  'Blockquote',
  'Code',
  'Link',
  'Horizontal Rule',
]

defineExpose({ editor })
</script>
