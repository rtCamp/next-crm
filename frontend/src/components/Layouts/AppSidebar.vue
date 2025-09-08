<template>
  <div
    class="relative flex h-full flex-col justify-between transition-all duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-[220px]'"
  >
    <div>
      <UserDropdown class="p-2" :isCollapsed="isSidebarCollapsed" />
    </div>
    <div class="flex-1 overflow-y-auto">
      <div class="flex flex-col">
        <SidebarLink
          id="notifications-btn"
          :label="__('Notifications')"
          :icon="NotificationsIcon"
          :isCollapsed="isSidebarCollapsed"
          @click="() => toggleNotificationPanel()"
          class="relative mx-2 my-0.5"
        >
          <template #right>
            <Badge
              v-if="!isSidebarCollapsed && unreadNotificationsCount"
              :label="unreadNotificationsCount"
              variant="subtle"
            />
            <div
              v-else-if="unreadNotificationsCount"
              class="absolute -left-1.5 top-1 z-20 h-[5px] w-[5px] translate-x-6 translate-y-1 rounded-full bg-surface-gray-6 ring-1 ring-white"
            />
          </template>
        </SidebarLink>
      </div>
      <div class="mb-3 flex flex-col">
        <button
          class="flex h-7 cursor-pointer items-center rounded text-ink-gray-7 duration-300 ease-in-out focus:outline-none focus:transition-none focus-visible:rounded focus-visible:ring-2 focus-visible:ring-gray-400 hover:bg-surface-gray-2 relative mx-2 my-0.5"
          id="search-btn"
          :class="isSidebarCollapsed ? '' : 'hover:bg-surface-gray-2'"
          @click="showSearchModal = true"
        >
          <div class="flex w-full items-center justify-between duration-300 ease-in-out px-2 py-1">
            <div class="flex items-center truncate w-full">
              <span class="grid flex-shrink-0 place-items-center">
                <FeatherIcon :name="'search'" class="size-4 text-ink-gray-7" />
              </span>
              <span
                class="flex-1 w-full flex justify-between flex-shrink-0 truncate text-sm duration-300 ease-in-out ml-2 w-auto opacity-100"
                data-state="closed"
                data-grace-area-trigger=""
                :class="isSidebarCollapsed && 'hidden'"
              >
                <span>Search</span>
                <span class="flex gap-1 items-center">
                  <kbd class="text-[0.65rem] items-center text-ink-gray-5">
                    {{ isMac() ? '⌘' : 'Ctrl' }}
                  </kbd>
                  <kbd class="text-xs items-center text-ink-gray-5">K</kbd>
                </span>
              </span>
            </div>
          </div>
        </button>
      </div>
      <div v-for="view in allViews" :key="view.label">
        <div v-if="!view.hideLabel && isSidebarCollapsed && view.views?.length" class="mx-2 my-2 h-1 border-b" />
        <Section :label="view.name" :hideLabel="view.hideLabel" :isOpened="view.opened">
          <template #header="{ opened, hide, toggle }">
            <div
              v-if="!hide"
              class="flex cursor-pointer gap-1.5 px-1 text-base font-medium text-ink-gray-5 transition-all duration-300 ease-in-out"
              :class="isSidebarCollapsed ? 'ml-0 h-0 overflow-hidden opacity-0' : 'ml-2 mt-4 h-7 w-auto opacity-100'"
              @click="toggle()"
            >
              <FeatherIcon
                name="chevron-right"
                class="h-4 text-ink-gray-9 transition-all duration-300 ease-in-out"
                :class="{ 'rotate-90': opened }"
              />
              <span>{{ __(view.name) }}</span>
            </div>
          </template>
          <nav class="flex flex-col">
            <SidebarLink
              v-for="link in view.views"
              :icon="link.icon"
              :label="__(link.label)"
              :to="link.to"
              :isCollapsed="isSidebarCollapsed"
              class="mx-2 my-0.5"
            />
          </nav>
        </Section>
      </div>
    </div>
    <div class="m-2 flex flex-col gap-1">
      <SidebarLink
        :label="isSidebarCollapsed ? __('Expand') : __('Collapse')"
        :isCollapsed="isSidebarCollapsed"
        @click="isSidebarCollapsed = !isSidebarCollapsed"
        class=""
      >
        <template #icon>
          <span class="grid h-4.5 w-4.5 flex-shrink-0 place-items-center">
            <CollapseSidebar
              class="h-4.5 w-4.5 text-ink-gray-7 duration-300 ease-in-out"
              :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }"
            />
          </span>
        </template>
      </SidebarLink>
    </div>
    <Notifications />
  </div>
  <SearchPopover v-model="showSearchModal" />
</template>

<script setup>
import AddressIcon from '@/components/Icons/AddressIcon.vue'
import Section from '@/components/Section.vue'
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import PinIcon from '@/components/Icons/PinIcon.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import OpportunitiesIcon from '@/components/Icons/OpportunitiesIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import CustomersIcon from '@/components/Icons/CustomersIcon.vue'
import ToDoIcon from '@/components/Icons/ToDoIcon.vue'
import FileTextIcon from '@/components/Icons/FileTextIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import ProspectsIcon from '@/components/Icons/ProspectsIcon.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
// import SearchIcon from '@/components/Icons/SearchIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import Notifications from '@/components/Notifications.vue'
import SearchPopover from '@/components/SearchPopover.vue'
import { viewsStore } from '@/stores/views'
import { unreadNotificationsCount, notificationsStore } from '@/stores/notifications'
import { FeatherIcon } from 'frappe-ui'
import { useStorage } from '@vueuse/core'
import { computed, h, onBeforeUnmount, onMounted, ref } from 'vue'
import { hiddenPages } from '../../composables/settings'

const { getPinnedViews, getPublicViews } = viewsStore()
const { toggle: toggleNotificationPanel } = notificationsStore()

const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)
const showSearchModal = ref(false)

const links = computed(() =>
  [
    {
      label: 'Leads',
      icon: LeadsIcon,
      to: 'Leads',
    },
    {
      label: 'Opportunities',
      icon: OpportunitiesIcon,
      to: 'Opportunities',
    },
    {
      label: 'Prospects',
      icon: ProspectsIcon,
      to: 'Prospects',
    },
    {
      label: 'Contacts',
      icon: ContactsIcon,
      to: 'Contacts',
    },
    {
      label: 'Addresses',
      icon: AddressIcon,
      to: 'Addresses',
    },
    {
      label: 'Customers',
      icon: CustomersIcon,
      to: 'Customers',
    },
    {
      label: 'Reports',
      icon: FileTextIcon,
      to: 'Reports',
    },
    {
      label: 'ToDos',
      icon: ToDoIcon,
      to: 'ToDos',
    },
    {
      label: 'Call Logs',
      icon: PhoneIcon,
      to: 'Call Logs',
    },
    {
      label: 'Email Templates',
      icon: Email2Icon,
      to: 'Email Templates',
    },
  ].filter((link) => !hiddenPages.value.includes(link.label)),
)

const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links.value,
    },
  ]
  if (getPublicViews().length) {
    _views.push({
      name: 'Public views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }

  if (getPinnedViews().length) {
    _views.push({
      name: 'Pinned views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }
  return _views
})

function parseView(views) {
  return views.map((view) => {
    return {
      label: view.label,
      icon: getIcon(view.route_name, view.icon),
      to: {
        name: view.route_name,
        params: { viewType: view.type || 'list' },
        query: { view: view.name },
      },
    }
  })
}

function getIcon(routeName, icon) {
  if (icon) return h('div', { class: 'size-auto' }, icon)

  switch (routeName) {
    case 'Leads':
      return LeadsIcon
    case 'Opportunities':
      return OpportunitiesIcon
    case 'Contacts':
      return ContactsIcon
    case 'Addresses':
      return AddressIcon
    case 'Customers':
      return CustomersIcon
    case 'Notes':
      return NoteIcon
    case 'Call Logs':
      return PhoneIcon
    case 'Reports':
      return FileTextIcon
    default:
      return PinIcon
  }
}

function toggleGlobalSearch(e) {
  if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
    e.preventDefault()
    showSearchModal.value = !showSearchModal.value
  }
}

function isMac() {
  return navigator.platform.toUpperCase().indexOf('MAC') >= 0
}

onMounted(() => {
  window.addEventListener('keydown', toggleGlobalSearch)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', toggleGlobalSearch)
})
</script>
