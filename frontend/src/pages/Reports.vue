<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="Reports" />
    </template>
    <template #right-header>
      <CustomActions v-if="reportsListView?.customListActions" :actions="reportsListView.customListActions" />
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="reports"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="Report"
    :options="{
      allowedViews: ['list'],
    }"
  />
  <ReportsListView
    ref="reportsListView"
    v-if="reports.data && rows.length"
    v-model="reports.data.page_length_count"
    v-model:list="reports"
    :rows="rows"
    :columns="reports.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: reports.data.row_count,
      totalCount: reports.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
    @applyLikeFilter="(data) => viewControls.applyLikeFilter(data)"
    @likeDoc="(data) => viewControls.likeDoc(data)"
  />
  <div v-else-if="reports.data" class="flex h-full items-center justify-center">
    <div class="flex flex-col items-center gap-3 text-xl font-medium text-ink-gray-4">
      <FileTextIcon class="h-10 w-10" />
      <span>{{ __('No {0} Found', [__('Reports')]) }}</span>
    </div>
  </div>
</template>

<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import FileTextIcon from '@/components/Icons/FileTextIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ReportsListView from '@/components/ListViews/ReportsListView.vue'
import ViewControls from '@/components/ViewControls.vue'
import { dateFormat, dateTooltipFormat, timeAgo } from '@/utils'
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const reportsListView = ref(null)

// reports data is loaded in the ViewControls component
const reports = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const viewControls = ref(null)

// Rows
const rows = computed(() => {
  if (!reports.value?.data?.data) return []
  return parseRows(reports.value?.data.data)
})

function parseRows(rows) {
  return rows.map((report) => {
    let _rows = {}
    reports.value.data.rows.forEach((row) => {
      _rows[row] = report[row]

      if (['modified', 'creation'].includes(row)) {
        _rows[row] = {
          label: dateFormat(report[row], dateTooltipFormat),
          timeAgo: __(timeAgo(report[row])),
        }
      }
    })
    return _rows
  })
}
</script>
