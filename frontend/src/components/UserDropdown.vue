<template>
  <Dropdown :options="dropdownOptions" v-bind="$attrs">
    <template v-slot="{ open }">
      <button
        class="flex h-12 items-center rounded-md py-2 duration-300 ease-in-out"
        :class="isCollapsed ? 'w-auto px-0' : open ? 'w-52 bg-surface-white px-2 shadow-sm' : 'w-52 px-2 hover:bg-surface-gray-3'"
      >
        <CRMLogo class="size-8 flex-shrink-0 rounded" />
        <div
          class="flex flex-1 flex-col text-left duration-300 ease-in-out"
          :class="isCollapsed ? 'ml-0 w-0 overflow-hidden opacity-0' : 'ml-2 w-auto opacity-100'"
        >
          <div class="text-base font-medium leading-none text-ink-gray-9">
            {{ __('Next CRM') }}
          </div>
          <div class="mt-1 text-sm leading-none text-ink-gray-7">
            {{ user.full_name }}
          </div>
        </div>
        <div
          class="duration-300 ease-in-out"
          :class="isCollapsed ? 'ml-0 w-0 overflow-hidden opacity-0' : 'ml-2 w-auto opacity-100'"
        >
          <FeatherIcon name="chevron-down" class="size-4 text-ink-gray-5" aria-hidden="true" />
        </div>
      </button>
    </template>
  </Dropdown>
  <SettingsModal v-if="showSettingsModal" v-model="showSettingsModal" />
</template>

<script setup>
import SettingsModal from '@/components/Settings/SettingsModal.vue'
import CRMLogo from '@/components/Icons/CRMLogo.vue'
import Apps from '@/components/Apps.vue'
import { sessionStore } from '@/stores/session'
import { usersStore } from '@/stores/users'
import { Dropdown } from 'frappe-ui'
import { useStorage } from '@vueuse/core'
import { computed, ref, markRaw, onMounted } from 'vue'

const props = defineProps({
  isCollapsed: {
    type: Boolean,
    default: false,
  },
})

const { logout } = sessionStore()
const { getUser } = usersStore()

const user = computed(() => getUser() || {})

const showSettingsModal = ref(false)
const theme = useStorage('theme', 'light')

let dropdownOptions = ref([
  {
    group: 'Manage',
    hideLabel: true,
    items: [
      {
        component: markRaw(Apps),
      },
      {
        icon: 'life-buoy',
        label: computed(() => __('Support')),
        onClick: () => window.open('https://github.com/rtCamp/next-crm', '_blank'),
      },
      {
        icon: 'book-open',
        label: computed(() => __('Docs')),
        onClick: () => window.open('https://docs.frappe.io/crm', '_blank'),
      },
    ],
  },
  {
    group: 'Others',
    hideLabel: true,
    items: [
      {
        icon: computed(() => (theme.value === 'dark' ? 'sun' : 'moon')),
        label: computed(() => __('Toggle theme')),
        onClick: toggleTheme,
      },
      {
        icon: 'settings',
        label: computed(() => __('Settings')),
        onClick: () => (showSettingsModal.value = true),
      },
      {
        icon: 'log-out',
        label: computed(() => __('Log out')),
        onClick: () => logout.submit(),
      },
    ],
  },
])

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme')
  theme.value = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', theme.value)
}
onMounted(() => {
  if (['light', 'dark'].includes(theme.value)) {
    document.documentElement.setAttribute('data-theme', theme.value)
  }
})
</script>
