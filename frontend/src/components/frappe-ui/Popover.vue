<template>
  <PopoverRoot v-model:open="isOpen" @update:open="onUpdateOpen">
    <PopoverAnchor asChild>
      <div ref="anchorRef" :class="['flex', $attrs.class]" @mouseover="onMouseover" @mouseleave="onMouseleave">
        <slot
          name="target"
          v-bind="{
            togglePopover,
            updatePosition,
            open,
            close,
            isOpen,
          }"
        />
      </div>
    </PopoverAnchor>
    <PopoverPortal>
      <PopoverContent
        :side="placementSide"
        :align="placementAlign"
        :style="{
          minWidth: matchTargetWidth ? 'var(--reka-popover-trigger-width)' : undefined,
        }"
        :class="['PopoverContent', { 'has-transition': hasTransition }]"
        @mouseover="pointerOverTargetOrPopup = true"
        @mouseleave="onMouseleave"
        @interact-outside="onInteractOutside"
      >
        <div class="relative" :class="['body-container', popoverClass]">
          <slot name="body" v-bind="{ togglePopover, updatePosition, open, close, isOpen }">
            <div class="rounded-lg border bg-surface-modal shadow-xl">
              <slot
                name="body-main"
                v-bind="{
                  togglePopover,
                  updatePosition,
                  open,
                  close,
                  isOpen,
                }"
              />
            </div>
          </slot>
        </div>
      </PopoverContent>
    </PopoverPortal>
  </PopoverRoot>
</template>

<script>
import { PopoverAnchor, PopoverContent, PopoverPortal, PopoverRoot } from 'reka-ui'

export default {
  name: 'Popover',
  inheritAttrs: false,
  components: {
    PopoverAnchor,
    PopoverContent,
    PopoverPortal,
    PopoverRoot,
  },
  props: {
    show: {
      default: undefined,
    },
    trigger: {
      type: String,
      default: 'click', // click, hover
    },
    hoverDelay: {
      type: Number,
      default: 0,
    },
    leaveDelay: {
      type: Number,
      default: 0.5,
    },
    placement: {
      type: String,
      default: 'bottom-start',
    },
    popoverClass: {
      type: [String, Object, Array],
      default: '',
    },
    transition: {
      type: String,
      default: null, // 'default' or null
    },
    hideOnBlur: {
      type: Boolean,
      default: true,
    },
    matchTargetWidth: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['open', 'close', 'update:show'],
  expose: ['open', 'close'],
  data() {
    return {
      internalOpen: false,
      pointerOverTargetOrPopup: false,
      hoverTimer: null,
      leaveTimer: null,
    }
  },
  computed: {
    isShowPropPassed() {
      return this.show !== undefined
    },
    isOpen: {
      get() {
        return this.isShowPropPassed ? this.show : this.internalOpen
      },
      set(value) {
        if (!this.isShowPropPassed) {
          this.internalOpen = value
        }
        this.$emit('update:show', value)
      },
    },
    placementSide() {
      const [side] = this.placement.split('-')
      return side
    },
    placementAlign() {
      const [, align] = this.placement.split('-')
      if (!align) return 'center'
      return align
    },
    hasTransition() {
      return this.transition === 'default'
    },
  },
  methods: {
    togglePopover(flag) {
      if (flag instanceof Event) {
        flag = undefined
      }
      if (flag == null) {
        flag = !this.isOpen
      }
      flag = Boolean(flag)
      if (flag) {
        this.open()
      } else {
        this.close()
      }
    },
    updatePosition() {
      // Positioning is handled internally by reka-ui
    },
    open() {
      this.isOpen = true
    },
    close() {
      this.isOpen = false
    },
    onUpdateOpen(value) {
      this.$emit('update:show', value)
      if (value) {
        this.$emit('open')
      } else {
        this.$emit('close')
      }
    },
    onMouseover() {
      this.pointerOverTargetOrPopup = true
      if (this.leaveTimer) {
        clearTimeout(this.leaveTimer)
        this.leaveTimer = null
      }
      if (this.trigger === 'hover') {
        if (this.hoverDelay) {
          this.hoverTimer = setTimeout(
            () => {
              if (this.pointerOverTargetOrPopup) {
                this.open()
              }
            },
            Number(this.hoverDelay) * 1000,
          )
        } else {
          this.open()
        }
      }
    },
    onMouseleave() {
      this.pointerOverTargetOrPopup = false
      if (this.hoverTimer) {
        clearTimeout(this.hoverTimer)
        this.hoverTimer = null
      }
      if (this.trigger === 'hover') {
        if (this.leaveTimer) {
          clearTimeout(this.leaveTimer)
        }
        if (this.leaveDelay) {
          this.leaveTimer = setTimeout(
            () => {
              if (!this.pointerOverTargetOrPopup) {
                this.close()
              }
            },
            Number(this.leaveDelay) * 1000,
          )
        } else if (!this.pointerOverTargetOrPopup) {
          this.close()
        }
      }
    },
    onInteractOutside(event) {
      if (!this.hideOnBlur) {
        event.preventDefault()
        return
      }

      const target = event.target
      const anchor = this.$refs.anchorRef
      if (anchor && (anchor.contains(target) || anchor === target)) {
        event.preventDefault()
      }
    },
  },
  beforeUnmount() {
    if (this.hoverTimer) {
      clearTimeout(this.hoverTimer)
    }
    if (this.leaveTimer) {
      clearTimeout(this.leaveTimer)
    }
  },
}
</script>
