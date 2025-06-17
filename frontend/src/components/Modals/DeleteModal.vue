<template>
  <Dialog
    v-model="show"
    :options="{
      title: __('Delete ') + props.doctype,
      message: __('Are you sure you want to delete this ') + props.doctype + '?',
      size: 'md',
      actions: [
        {
          label: __('Delete'),
          variant: 'solid',
          theme: 'red',
          onClick: deleteDoc,
        },
      ],
    }"
  >
  </Dialog>
</template>

<script setup>
import { createToast } from '@/utils'
import { call } from 'frappe-ui'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  doctype: {
    type: String,
    default: 'Opportunity',
  },
  docname: {
    type: String,
    default: '',
  },
  redirectTo: {
    type: String,
    default: 'Leads',
  },
})

const show = defineModel()

async function deleteDoc() {
  try {
    await call('frappe.client.delete', {
      doctype: props.doctype,
      name: props.docname,
    })
    show.value = false
    createToast({
      title: __(`${props.doctype} Deleted`),
      icon: 'check',
      iconClasses: 'text-ink-green-4',
    })
    router.push({ name: props.redirectTo || 'Leads' })
  } catch (error) {
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
</script>
