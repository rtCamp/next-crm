// ✅ ActivityListView.vue
<template>
  <ListView
    :class="$attrs.class"
    :columns="columns"
    :rows="rows"
    :options="{
      getRowRoute: (row) => ({
        name: 'Event',
        params: { eventId: row.name },
      }),
      selectable: options.selectable,
      showTooltip: options.showTooltip,
      resizeColumn: options.resizeColumn,
    }"
    row-key="name"
  >
    <ListHeader class="mx-3 sm:mx-5" @columnWidthUpdated="emit('columnWidthUpdated')">
      <ListHeaderItem
        v-for="column in columns"
        :key="column.key"
        :item="column"
        @columnWidthUpdated="emit('columnWidthUpdated', column)"
      />
    </ListHeader>

    <ListRows class="mx-3 sm:mx-5">
      <ListRow v-for="row in rows" :key="row.name" :row="row" v-slot="{ idx, column, item }">
        <ListRowItem :item="item">
          <template #default="{ label }">
            <div
              v-if="['starts_on', 'ends_on', 'modified'].includes(column.key)"
              class="truncate text-base"
              @click="(event) => emit('applyFilter', { event, idx, column, item, firstColumn: columns[0] })"
            >
              <Tooltip :text="item.label">
                <div>{{ item.timeAgo || label }}</div>
              </Tooltip>
            </div>
            <div v-else class="truncate text-base">
              {{ label }}
            </div>
          </template>
        </ListRowItem>
      </ListRow>
    </ListRows>

    <ListSelectBanner>
      <template #actions="{ selections, unselectAll }">
        <Dropdown :options="listBulkActionsRef.bulkActions(selections, unselectAll)">
          <Button icon="more-horizontal" variant="ghost" />
        </Dropdown>
      </template>
    </ListSelectBanner>
  </ListView>

  <ListFooter
    v-if="pageLengthCount"
    class="border-t px-3 py-2 sm:px-5"
    v-model="pageLengthCount"
    :options="{
      rowCount: options.rowCount,
      totalCount: options.totalCount,
    }"
    @loadMore="emit('loadMore')"
  />
</template>

<script setup>
import {
  ListView,
  ListHeader,
  ListHeaderItem,
  ListRows,
  ListRow,
  ListSelectBanner,
  ListRowItem,
  ListFooter,
  Tooltip,
  Dropdown,
  Button,
} from 'frappe-ui'
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  rows: Array,
  columns: Array,
  options: {
    type: Object,
    default: () => ({ selectable: true, showTooltip: true, resizeColumn: false, totalCount: 0, rowCount: 0 }),
  },
})

const emit = defineEmits(['loadMore', 'updatePageCount', 'columnWidthUpdated', 'applyFilter'])

const route = useRoute()
const pageLengthCount = defineModel()
const list = defineModel('list')

const listBulkActionsRef = ref(null)

defineExpose({
  customListActions: computed(() => listBulkActionsRef.value?.customListActions),
})
</script>
