<template>
  <div class="flex h-screen w-screen">
    <div class="h-full border-r bg-surface-menu-bar">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto bg-surface-white">
      <AppHeader />
      <Suspense>
        <slot />
      </Suspense>
    </div>
  </div>
</template>
<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import AppHeader from '@/components/Layouts/AppHeader.vue'
</script>
