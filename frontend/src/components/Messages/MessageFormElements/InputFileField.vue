<template>
  <div>
    <label :for="file_field_id" class="form-label">File</label>
    <input v-on:change="handleChangeFile" class="form-control" type="file" :id="file_field_id" accept="text/plain">
  </div>
</template>

<script>
import {ALLOWED_FILE_FORMATS, MAX_FILE_SIZE} from "../../../config";

export default {
  name: "InputFileField",
  props: ["file_field_id", "setFileData"],
  methods: {
    handleChangeFile(event) {
      let file = event.target.files[0];

      if (this.checkFile(file)) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (f) => {
          this.setFileData(f.target.result, file.name);
        };
      }
    },
    checkFile(file) {
      const regex = new RegExp(".*\.(" + ALLOWED_FILE_FORMATS.join("|") + ")$", "g");
      if (!regex.test(file.name)) return false;
      if (file.side > MAX_FILE_SIZE) return false;
      if (file.type !== "text/plain") return false;
      return true;
    },
  },
}
</script>

<style scoped>

</style>