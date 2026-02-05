<template>
  <section>
    <div class="bg-card border border-card-line shadow-2xs rounded-xl">
      <div class="p-4">
        <h1 class="font-semibold text-foreground">
          Results Upload
        </h1>
        <!-- <div>
          <label class="block mb-2.5 text-sm font-medium text-heading" for="file_input">Upload file</label>
          <input
            class="cursor-pointer bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full shadow-xs placeholder:text-body"
            ref="fileInput"
            type="file"
            accept=".csv,text/csv"
            @change="onFileChange"
          />
        </div> -->
        <div class="mt-4 flex text-sm/6 text-gray-400">
                <label for="file-upload" class="relative cursor-pointer rounded-md bg-transparent font-semibold text-indigo-400 focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-indigo-500 hover:text-indigo-300">
                  <span>Upload a file</span>
                  <input id="file-upload"
                    type="file"
                    name="file-upload"
                    class="sr-only"
                    ref="fileInput"
                    accept=".csv,text/csv"
                    @change="onFileChange"
                  />
                </label>
                <p class="pl-2"> {{file_name}}</p>
              </div>
        <div v-if="isUploading" style="border: 1rem;">Uploading please wait…</div>
        <p v-if="errorMsg" style="color: red">Error: {{ errorMsg }}</p>

        <div v-if="summary" style="margin-top: 1rem;">
          <h2>Summary</h2>
          <ul class="pl-2 list-desc">
            <li>Total rows: {{ summary.total_rows }}</li>
            <li>Valid rows: {{ summary.valid_rows }}</li>
            <li>Completion Time: {{ summary.runtime ?? "unkown" }}</li>
          </ul>
          <div style="margin-top: 1rem;">
            By status:
            <ul class="pl-2 list-desc">
              <li>success: {{ summary.by_status?.success ?? 0 }}</li>
              <li>fail: {{ summary.by_status?.fail ?? 0 }}</li>
              <li>unknown: {{ summary.by_status?.unknown ?? 0 }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api'

const isUploading = ref(false)
const summary = ref<any | null>(null)
const errorMsg = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const file_name = ref<String>("none chosen")

async function uploadFile(file: File) {
  isUploading.value = true
  errorMsg.value = null
  summary.value = null
  try {
    const form = new FormData()
    form.append('file', file, file.name)
    file_name.value = file.name
    const res = await fetch(`${API_URL}/results/upload`, { method: 'POST', body: form })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    const data = await res.json()
    summary.value = data
  } catch (err: any) {
    errorMsg.value = err?.message ?? String(err)
  } finally {
    isUploading.value = false
  }
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) uploadFile(file)
}

defineExpose({ uploadFile })
</script>

