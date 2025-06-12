<template>
  <div class="activity group">
    <div class="mb-1 flex items-center justify-stretch gap-2 py-1 text-base">
      <div class="inline-flex items-center flex-wrap gap-1 text-ink-gray-5">
        <UserAvatar class="mr-1" :user="note.owner" size="md" />
        <span class="font-medium text-ink-gray-8" :title="getUser(note.owner).full_name">
          {{ getUser(note.owner).full_name }}
        </span>
      </div>
      <div class="flex items-center gap-2 ml-auto whitespace-nowrap">
        <Tooltip :text="dateFormat(note.added_on, dateTooltipFormat)">
          <div class="truncate text-sm text-ink-gray-7">
            {{ __(timeAgo(note.added_on)) }}
          </div>
        </Tooltip>
        <Tooltip v-if="!note.custom_parent_note" :text="__('Reply')">
          <div @click.stop="replyNote">
            <Button variant="ghost" class="text-ink-gray-7 !h-6 !w-6 hover:bg-surface-gray-2">
              <template #icon>
                <ReplyIcon />
              </template>
            </Button>
          </div>
        </Tooltip>
        <Dropdown
          :options="[
            {
              label: __('Delete'),
              icon: 'trash-2',
              onClick: () => deleteNote(note.name),
            },
          ]"
          @click.stop
          class="h-6 w-6"
        >
          <Button icon="more-horizontal" variant="ghosted" class="!h-6 !w-6 hover:bg-surface-gray-2" />
        </Dropdown>
      </div>
    </div>
    <div
      class="activity group flex max-h-64 cursor-pointer flex-col justify-between gap-2 rounded-md bg-surface-gray-1 px-4 py-3 hover:bg-surface-gray-2"
      @click="props.modalRef.showNote(note)"
    >
      <div class="flex items-center justify-between">
        <div class="truncate text-lg font-medium text-ink-gray-8">
          {{ note.custom_title }}
        </div>
      </div>
      <TextEditor
        v-if="note.note"
        :content="note.note"
        :editable="false"
        editor-class="!prose-sm max-w-none !text-sm text-ink-gray-5 focus:outline-none"
        class="flex-1 overflow-x-hidden"
      />
    </div>
    <div v-if="note.noteReplies?.length" class="ml-6 mt-2 space-y-3 border-l border-gray-200 pl-4">
      <NoteArea :modalRef="props.modalRef" v-for="reply in note.noteReplies" :note="reply" v-model="notes" />
    </div>
  </div>
</template>
<script setup>
import UserAvatar from '@/components/UserAvatar.vue'
import { timeAgo, dateFormat, dateTooltipFormat } from '@/utils'
import { Tooltip, Dropdown, TextEditor, call } from 'frappe-ui'
import { usersStore } from '@/stores/users'
import ReplyIcon from '@/components/Icons/ReplyIcon.vue'
import { createToast } from '@/utils'

const props = defineProps({
  note: Object,
  modalRef: Object,
})

const notes = defineModel()

const { getUser } = usersStore()

const emit = defineEmits(['reply-note'])

function replyNote() {
  emit('reply-note', props.note)
}

async function deleteNote(name) {
  try {
    await call('next_crm.api.crm_note.delete_note', {
      note_name: name,
    })
    notes.value?.reload()
    createToast({
      title: __('Note deleted successfully'),
      icon: 'check',
      iconClasses: 'text-ink-green-3',
    })
  } catch (error) {
    createToast({
      title: __('Error deleting note'),
      text: error.message,
      icon: 'x',
      iconClasses: 'text-ink-red-4',
    })
  }
}
</script>
