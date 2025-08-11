import { createResource } from 'frappe-ui'
import { computed, ref } from 'vue'

export const whatsappEnabled = ref(false)
export const isWhatsappInstalled = ref(false)
export const hiddenPages = ref([])
createResource({
  url: 'next_crm.api.whatsapp.is_whatsapp_enabled',
  cache: 'Is Whatsapp Enabled',
  auto: true,
  onSuccess: (data) => {
    whatsappEnabled.value = Boolean(data)
  },
})
createResource({
  url: 'next_crm.api.whatsapp.is_whatsapp_installed',
  cache: 'Is Whatsapp Installed',
  auto: true,
  onSuccess: (data) => {
    isWhatsappInstalled.value = Boolean(data)
  },
})

export const hiddenPagesResource = ref(createResource({
  url: 'next_crm.api.erpnext.get_pages_visibility',
  cache: 'crm-hidden-pages',
  auto: true,
  onSuccess: (data) => {
    hiddenPages.value = data
  },
}))

export const callEnabled = ref(false)
createResource({
  url: 'next_crm.integrations.twilio.api.is_enabled',
  cache: 'Is Twilio Enabled',
  auto: true,
  onSuccess: (data) => {
    callEnabled.value = Boolean(data)
  },
})

export const mobileSidebarOpened = ref(false)

export const isMobileView = computed(() => window.innerWidth < 768)
