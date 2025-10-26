<template>
  <FrappeUIProvider>
    <Layout v-if="session().isLoggedIn">
      <router-view :key="routeKey"/>
    </Layout>
    <Dialogs />
  </FrappeUIProvider>
</template>

<script setup>
import { Dialogs } from '@/utils/dialogs'
import { sessionStore as session } from '@/stores/session'
import { FrappeUIProvider, setConfig } from 'frappe-ui'
import { computed, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const routeKey = computed(() => {
  if (route.name === 'Lead') return route.params.leadId
  if (route.name === 'Opportunity') return route.params.opportunityId
  return route.fullPath
})

const MobileLayout = defineAsyncComponent(() =>
  import('./components/Layouts/MobileLayout.vue')
)
const DesktopLayout = defineAsyncComponent(() =>
  import('./components/Layouts/DesktopLayout.vue')
)
const Layout = computed(() => {
  if (window.innerWidth < 640) {
    return MobileLayout
  } else {
    return DesktopLayout
  }
})

setConfig('timezone', window.timezone)
</script>
