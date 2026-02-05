<template>
  <section>
    <input
      ref="fileInput"
      type="file"
      accept=".csv,text/csv"
      @change="onFileChange"
    />

    <p v-if="isUploading">Uploading…</p>
    <p v-if="errorMsg" style="color: red">Error: {{ errorMsg }}</p>

    <div v-if="summary" style="margin-top: 1rem;">
      <h2>Summary</h2>
      <div>Total rows: {{ summary.total_rows }}</div>
      <div>Valid rows: {{ summary.valid_rows }}</div>
      <div>time: {{ summary.runtime }}</div>
      <div>
        By status:
        <ul>
          <li>success: {{ summary.by_status?.success ?? 0 }}</li>
          <li>fail: {{ summary.by_status?.fail ?? 0 }}</li>
          <li>unknown: {{ summary.by_status?.unknown ?? 0 }}</li>
        </ul>
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

async function uploadFile(file: File) {
  isUploading.value = true
  errorMsg.value = null
  summary.value = null
  try {
    const form = new FormData()
    form.append('file', file, file.name)
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

