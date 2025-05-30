<template>
  <Popover placement="right-start" class="flex w-full">
    <template #target="{ togglePopover }">
      <button
        :class="[
          active ? 'bg-surface-gray-3' : 'text-ink-gray-6',
          'group w-full flex h-7 items-center justify-between rounded px-2 text-base hover:bg-surface-gray-2',
        ]"
        @click.prevent="togglePopover()"
      >
        <div class="flex gap-2">
          <AppsIcon class="size-4" />
          <span class="whitespace-nowrap">
            {{ __('Apps') }}
          </span>
        </div>
        <FeatherIcon name="chevron-right" class="size-4 text-ink-gray-5" />
      </button>
    </template>
    <template #body>
      <div class="grid grid-cols-3 justify-between mx-3 p-2 min-w-40 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none">
        <div v-for="app in apps.data" :key="app.name">
          <a
            :href="app.route"
            class="flex flex-col gap-1.5 rounded justify-center items-center py-2 px-1 hover:bg-surface-gray-2"
          >
            <img class="size-8" :src="app.logo" />
            <div class="text-sm text-ink-gray-7" @click="app.onClick">
              {{ app.title }}
            </div>
          </a>
        </div>
      </div>
    </template>
  </Popover>
</template>
<script setup>
import AppsIcon from '@/components/Icons/AppsIcon.vue'
import { Popover, createResource } from 'frappe-ui'
import { onUnmounted } from 'vue'
import { stopRecording } from '@/telemetry'

const props = defineProps({
  active: Boolean,
})

const apps = createResource({
  url: 'frappe.apps.get_apps',
  cache: 'apps',
  auto: true,
  transform: (data) => {
    let _apps = [
      {
        name: 'frappe',
        logo: '/assets/frappe/images/framework.png',
        title: __('Desk'),
        route: '/app',
      },
    ]
    data.map((app) => {
      if (app.name === 'next_crm') return
      _apps.push({
        name: app.name,
        logo: app.logo,
        title: __(app.title),
        route: app.route,
      })
    })

    return _apps
  },
})

onUnmounted(() => {
  stopRecording()
})
</script>
