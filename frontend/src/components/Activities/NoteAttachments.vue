<template>
  <div class="mt-2 border-t" :class="{ 'py-2': props.editMode }" v-if="attachments.length">
    <div v-if="!props.editMode" class="flex items-center gap-2 my-3">
      <AttachmentIcon class="size-3" />
      <p class="text-base">Attachments</p>
      <Badge :variant="'solid'" :ref_for="true" theme="gray" size="sm" :label="attachments.length">
        {{ attachments.length }}
      </Badge>
    </div>
    <div :class="{ 'flex gap-2 overflow-x-auto': !props.editMode }">
      <div :class="{ flex: !props.editMode }" v-for="(attachment, i) in attachments" :key="attachment.name">
        <div
          class="activity flex justify-between gap-2 hover:bg-gray-50 rounded text-base p-2.5 cursor-pointer"
          @click.stop="openFile(attachment)"
          :class="{ 'bg-surface-white hover:bg-surface-white border-2 border-dashed max-w-52': !props.editMode }"
        >
          <div class="flex gap-2 truncate">
            <div
              class="size-11 bg-surface-white rounded overflow-hidden flex-shrink-0 flex justify-center items-center"
              :class="{ border: !isImage(attachment.file_type) }"
            >
              <img
                v-if="isImage(attachment.file_type)"
                class="size-full object-cover"
                :src="attachment.file_url"
                :alt="attachment.file_name"
              />
              <component v-else class="size-4 text-ink-gray-7" :is="fileIcon(attachment.file_type)" />
            </div>
            <div class="flex flex-col justify-center gap-1 truncate">
              <div class="text-base text-ink-gray-8 truncate">
                {{ attachment.file_name }}
              </div>
              <div class="mb-1 text-sm text-ink-gray-5">
                {{ convertSize(attachment.file_size) }}
              </div>
            </div>
          </div>
          <div v-if="props.editMode" class="flex flex-col items-end gap-2 flex-shrink-0">
            <Tooltip :text="dateFormat(attachment.creation, dateTooltipFormat)">
              <div class="text-sm text-ink-gray-5">
                {{ __(timeAgo(attachment.creation)) }}
              </div>
            </Tooltip>
            <div class="flex gap-1">
              <Tooltip :text="attachment.is_private ? __('Make public') : __('Make private')">
                <Button class="!size-5" @click.stop="openTogglePrivate(attachment.name, attachment.is_private)">
                  <FeatherIcon :name="attachment.is_private ? 'lock' : 'unlock'" class="size-3 text-ink-gray-7" />
                </Button>
              </Tooltip>
              <Tooltip :text="__('Delete attachment')">
                <Button class="!size-5" @click.stop="() => openDeleteAttachment(attachment.name)">
                  <FeatherIcon name="trash-2" class="size-3 text-ink-gray-7" />
                </Button>
              </Tooltip>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Dialog
    v-model="showDeleteModal"
    :options="{
      title: __('Delete Attachment'),
      message: __('Are you sure you want to delete this attachment?'),
      size: 'md',
      closeOnOutsideClick: false,
      actions: [
        {
          label: __('Delete'),
          variant: 'solid',
          theme: 'red',
          onClick: deleteAttachment,
        },
      ],
    }"
  />

  <Dialog
    v-model="showToggleModal"
    :options="{
      title: fileToToggle?.is_private ? __('Make Attachment Public') : __('Make Attachment Private'),
      message: fileToToggle?.is_private
        ? __('Are you sure you want to make this attachment public?')
        : __('Are you sure you want to make this attachment private?'),
      size: 'md',
      closeOnOutsideClick: false,
      actions: [
        {
          label: fileToToggle?.is_private ? __('Make Public') : __('Make Private'),
          variant: 'solid',
          onClick: confirmTogglePrivate,
        },
      ],
    }"
  />
</template>
<script setup>
import FileAudioIcon from '@/components/Icons/FileAudioIcon.vue'
import FileTextIcon from '@/components/Icons/FileTextIcon.vue'
import FileVideoIcon from '@/components/Icons/FileVideoIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import { globalStore } from '@/stores/global'
import { call, Tooltip, Badge } from 'frappe-ui'
import { dateFormat, timeAgo, dateTooltipFormat, convertSize, isImage, createToast } from '@/utils'
import { ref } from 'vue'

const props = defineProps({
  attachments: Array,
  editMode: Boolean,
  note_name: String,
})

const showDeleteModal = ref(false)
const fileToDelete = ref(null)
const showToggleModal = ref(false)
const fileToToggle = ref(null)

const emit = defineEmits(['reload'])

function openFile(attachment) {
  window.open(attachment.file_url, '_blank')
}

const openDeleteAttachment = (fileName) => {
  fileToDelete.value = fileName
  showDeleteModal.value = true
  return
}

const deleteAttachment = async () => {
  try {
    await call('next_crm.api.crm_note.delete_note_attachments', {
      note_name: props.note_name,
      file_name: fileToDelete.value,
    })
    emit('reload')
    showDeleteModal.value = false
  } catch (e) {
    const errorMessage =
      error.name === 'LinkExistsError' || error.message.includes('LinkExistsError')
        ? __('Cannot delete this doc because it is linked to other records.')
        : __('Failed to delete the doc. Please try again later.')
    createToast({
      title: __('Error'),
      text: errorMessage,
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  }
}

const openTogglePrivate = (fileName, isPrivate) => {
  fileToToggle.value = { name: fileName, is_private: isPrivate }
  showToggleModal.value = true
}

const confirmTogglePrivate = async () => {
  const { name, is_private } = fileToToggle.value
  try {
    await call('frappe.client.set_value', {
      doctype: 'File',
      name,
      fieldname: {
        is_private: !is_private,
      },
    })
    emit('reload')
  } catch (e) {
    createToast({
      title: __('Error'),
      text: __('Failed to update attachment privacy'),
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  } finally {
    showToggleModal.value = false
  }
}

function fileIcon(type) {
  if (!type) return FileTextIcon
  let audioExtentions = ['wav', 'mp3', 'ogg', 'flac', 'aac']
  let videoExtentions = ['mp4', 'avi', 'mkv', 'flv', 'mov']
  if (audioExtentions.includes(type.toLowerCase())) {
    return FileAudioIcon
  } else if (videoExtentions.includes(type.toLowerCase())) {
    return FileVideoIcon
  }
  return FileTextIcon
}
</script>
