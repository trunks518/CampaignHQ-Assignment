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
        <div class="flex items-center justify-center w-full">
            <label for="file-upload" @dragover.prevent @drop.prevent="onDrop" class="flex flex-col items-center justify-center w-full h-64 bg-neutral-secondary-medium border border-dashed border-default-strong rounded-base cursor-pointer hover:bg-neutral-tertiary-medium">
                <div class="flex flex-col items-center justify-center text-body pt-5 pb-6">
                    <svg class="w-8 h-8 mb-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h3a3 3 0 0 0 0-6h-.025a5.56 5.56 0 0 0 .025-.5A5.5 5.5 0 0 0 7.207 9.021C7.137 9.017 7.071 9 7 9a4 4 0 1 0 0 8h2.167M12 19v-9m0 0-2 2m2-2 2 2"/></svg>
                    <p class="mb-2 text-sm"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                    <p class="text-xs">csv</p>
                </div>
                <input id="file-upload"
                            type="file"
                            name="file-upload"
                            class="sr-only"
                            ref="fileInput"
                            accept=".csv,text/csv"
                            @change="onFileChange"/>
                <p class="pl-2"> {{file_name}}</p>
            </label>
        </div> 
        <div v-if="isUploading" style="border: 1rem;">Uploading please wait…</div>
        <p v-if="errorMsg" style="color: red">Error: {{ errorMsg }}</p>

        <div v-if="uploading" class="mt-4 w-full">
          <div class="h-3 w-full bg-gray-200 rounded">
            <div
              class="h-3 bg-blue-600 rounded transition-all"
              style="width: {{progress}}+'%'"
            />
          </div>

          <div class="text-sm text-center mt-1">
            {{ progress }}% uploaded
          </div>
        </div>

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
import axios, { AxiosProgressEvent } from "axios"

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000/api'

const isUploading = ref(false)
const uploading = ref<boolean>(false)
const progress = ref<number>(0);
const summary = ref<any | null>(null)
const errorMsg = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const file_name = ref<String>("No File Chosen")

async function uploadFile(file: File): Promise<void> {
  isUploading.value = true;
  errorMsg.value = null;
  summary.value = null;

  try {
    const form = new FormData();
    form.append("file", file, file.name);
    file_name.value = file.name;
    uploading.value = true

    const res = await axios.post(
      `${API_URL}/results/upload`,
      form, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e: AxiosProgressEvent) => {
          if (e.total) {
            progress.value = Math.round((e.loaded * 100) / e.total);
            if(progress.value >= 100) {
              
            }
          }
        },
      }
    );
    
    summary.value = res.data;
    uploading.value = false

  } catch (error) {
    const err = error as AxiosError<any>;

    if (err.response) {
      errorMsg.value = `Error ${err.response.status}: ` + (err.response.data?.detail ?? "Upload failed");
    } else if (err.request) {
      errorMsg.value = "No response from server";
    } else {
      errorMsg.value = err.message;
    }
  } finally {
    isUploading.value = false;
  }
}

function onDrop(e: DragEvent) {
  const files = e.dataTransfer?.files;
  if (!files || files.length === 0) return;
  uploadFile(files[0])
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) uploadFile(file)
}

defineExpose({ uploadFile })
</script>

