<template>
  <div>
    <label :for="image_field_id" class="form-label">Image</label>
    <input v-on:change="handleChangeImage" class="form-control" type="file" :id="image_field_id" accept="image/png, image/jpeg, image/gif">
  </div>
</template>

<script>
import {ALLOWED_IMAGE_FORMATS, MAX_IMAGE_HEIGHT, MAX_IMAGE_WIDTH} from "../../../config";

export default {
  name: "InputImageField",
  props: ["image_field_id", "setImageData"],
  methods: {
    handleChangeImage(event) {
      let file = event.target.files[0];

      if (this.checkFormat(file)) {
        let reader = new FileReader();
        let image = new Image();

        reader.onload = (ev) => {
          image.src = ev.target.result;
        }
        image.onload = (ev) => {
          let base64data = this.getBase64Data(image);
          this.setImageData(base64data, file.name);
        }
        reader.readAsDataURL(file);
      }
    },
    getBase64Data(image) {
      const canvas = document.createElement("canvas");

      // change size
      if (image.height > MAX_IMAGE_HEIGHT || image.width > MAX_IMAGE_WIDTH) {

        if (image.width / image.height > MAX_IMAGE_WIDTH / MAX_IMAGE_HEIGHT) {
          canvas.width = MAX_IMAGE_WIDTH;
          canvas.height = Math.floor(image.height / image.width * MAX_IMAGE_WIDTH);
        } else {
          canvas.width = Math.floor(image.width / image.height * MAX_IMAGE_HEIGHT);
          canvas.height = MAX_IMAGE_HEIGHT;
        }

      }
      const ctx = canvas.getContext("2d");
      ctx.drawImage(image, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL();
    },
    checkFormat(file) {
      const regex = new RegExp(".*\.(" + ALLOWED_IMAGE_FORMATS.join("|") + ")$", "g");
      if (!regex.test(file.name)) return false;
      return true;
    },
  },
}
</script>

<style scoped>

</style>