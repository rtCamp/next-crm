<template>
  <SettingsPage
    doctype="NCRM Settings"
    :title="__('NCRM Settings')"
    :successMessage="__('NCRM Settings updated')"
    class="p-8"
  />
</template>
<script setup>
import SettingsPage from '@/components/Settings/SettingsPage.vue'
</script>
