<template>
    <div class="w-full">
        <div class="relative">
            <!-- Tags container -->
            <div class="min-h-10 w-full bg-gray-100 rounded px-2 py-2 flex flex-wrap items-center focus-within:ring-none gap-1 focus-within:ring-gray-300"
                @click="focusInput">
                <!-- Selected tags -->
                <div v-if="selectedTags.length > 0" class="flex gap-2 flex-wrap">
                    <div v-for="(tag, index) in selectedTags" :key="index"
                        class="bg-white rounded px-2 py-1 text-sm flex items-center gap-1">
                        {{ tag }}
                        <button type="button" @click.stop="removeTag(index)" class="text-gray-500 hover:text-gray-700">
                            <span class="ml-1">×</span>
                        </button>
                    </div>
                </div>

                <!-- Search input -->
                <input ref="inputRef" :value="searchQuery" @input="handleInput" type="text"
                    class="w-full p-1 bg-transparent border-none focus-within:ring-0 outline-none text-sm"
                    @focus="isDropdownOpen = true" @blur="handleBlur" @keydown.backspace="handleBackspace" />
            </div>

            <!-- Dropdown -->
            <div v-if="isDropdownOpen"
                class="absolute left-0 right-0 mt-1 bg-white border rounded border-gray-200 shadow-lg z-10 p-1">
                <div class="py-1">
                    <div v-if="loading" class="flex gap-1 py-2 flex-col justify-center items-center w-full">
                        <LoadingIndicator class="h-4 w-4" />
                        <span class="text-sm">Loading...</span>
                    </div>

                    <div v-else-if="availableOptions.length > 0">
                        <!-- Available options -->
                        <div v-for="(option, index) in availableOptions" :key="index"
                            class="px-3 py-2 rounded hover:bg-gray-100 cursor-pointer text-sm"
                            @mousedown.prevent="selectTag(option)">
                            {{ option }}
                        </div>
                    </div>

                    <div v-else-if="!loading && data.length === 0" class="px-3 py-2 text-sm text-gray-500">
                        No results
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue';
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue';
import { debounce } from '../utils';

const props = defineProps({
    modelValue: {
        type: Array,
        default: () => [],
    },
    data: {
        type: Array,
        default: () => [],
    },
    searchQuery: {
        type: String,
        default: '',
    },
    loading: {
        type: Boolean,
        default: false,
    },
    onChange: {
        type: Function,
        default: null,
    },
});

const emit = defineEmits(['update:modelValue', 'update:searchQuery']);

const selectedTags = ref([...props.modelValue]);
const isDropdownOpen = ref(false);
const inputRef = ref(null);

const availableOptions = computed(() => {
    return props.data.filter((option) => !selectedTags.value.includes(option));
});

const focusInput = () => {
    inputRef.value?.focus();
};

const handleBlur = () => {
    setTimeout(() => {
        isDropdownOpen.value = false;
    }, 150);
};

const handleInput = (e) => {
    debouncedEmitSearchQuery(e.target.value);
};

const removeTag = (index) => {
    const newTags = [...selectedTags.value];
    newTags.splice(index, 1);
    selectedTags.value = newTags;
    emit('update:modelValue', newTags);
    props.onChange?.(newTags);
};

const selectTag = (tag) => {
    if (!selectedTags.value.includes(tag)) {
        const newTags = [...selectedTags.value, tag];
        selectedTags.value = newTags;
        emit('update:modelValue', newTags);
        props.onChange?.(newTags);
    }
    emit('update:searchQuery', '');
    nextTick(() => {
        inputRef.value?.focus();
    });
};

const handleBackspace = () => {
    if (props.searchQuery === '' && selectedTags.value.length > 0) {
        removeTag(selectedTags.value.length - 1);
    }
};

const debouncedEmitSearchQuery = debounce((value) => {
    emit('update:searchQuery', value);
}, 400);

watch(() => props.modelValue, (newVal) => {
    selectedTags.value = [...newVal];
});
</script>