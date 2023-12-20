<template>
  <div><label :for="message_field_id" class="form-label">Message: </label></div>
  <div class="border border-1 border-secondary rounded-2 p-1">

    <div class="btn-group mb-1 me-1" role="group">

      <button id="preview-btn" @click="handleClickPreview" type="button" class="btn btn-sm btn-outline-secondary">

        <svg v-if="!is_preview_on" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
          <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
          <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
        </svg>

        <svg v-if="is_preview_on" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
          <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486z"/>
          <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
          <path d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708"/>
        </svg>

      </button>
    </div>

    <div class="btn-group mb-1 me-1" role="group">

      <button id="upload-file-btn" @click="handleClickUploadFile" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-font" viewBox="0 0 16 16">
          <path d="M10.943 6H5.057L5 8h.5c.18-1.096.356-1.192 1.694-1.235l.293-.01v5.09c0 .47-.1.582-.898.655v.5H9.41v-.5c-.803-.073-.903-.184-.903-.654V6.755l.298.01c1.338.043 1.514.14 1.694 1.235h.5l-.057-2z"/>
          <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5z"/>
        </svg>
      </button>

      <button id="upload-image-btn" @click="handleClickUploadImage" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-image" viewBox="0 0 16 16">
          <path d="M6.502 7a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/>
          <path d="M14 14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5L14 4.5zM4 1a1 1 0 0 0-1 1v10l2.224-2.224a.5.5 0 0 1 .61-.075L8 11l2.157-3.02a.5.5 0 0 1 .76-.063L13 10V4.5h-2A1.5 1.5 0 0 1 9.5 3V1z"/>
        </svg>
      </button>

    </div>

    <div class="btn-group mb-1 me-1" role="group">

      <button id="bold-btn" @click="() => handleClickAddTag('b')" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-type-bold" viewBox="0 0 16 16">
          <path d="M8.21 13c2.106 0 3.412-1.087 3.412-2.823 0-1.306-.984-2.283-2.324-2.386v-.055a2.176 2.176 0 0 0 1.852-2.14c0-1.51-1.162-2.46-3.014-2.46H3.843V13zM5.908 4.674h1.696c.963 0 1.517.451 1.517 1.244 0 .834-.629 1.32-1.73 1.32H5.908V4.673zm0 6.788V8.598h1.73c1.217 0 1.88.492 1.88 1.415 0 .943-.643 1.449-1.832 1.449H5.907z"/>
        </svg>
      </button>

      <button id="italic-btn" @click="() => handleClickAddTag('i')" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-type-italic" viewBox="0 0 16 16">
          <path d="M7.991 11.674 9.53 4.455c.123-.595.246-.71 1.347-.807l.11-.52H7.211l-.11.52c1.06.096 1.128.212 1.005.807L6.57 11.674c-.123.595-.246.71-1.346.806l-.11.52h3.774l.11-.52c-1.06-.095-1.129-.211-1.006-.806z"/>
        </svg>
      </button>

      <button id="code-btn" @click="() => handleClickAddTag('code')" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-code-slash" viewBox="0 0 16 16">
          <path d="M10.478 1.647a.5.5 0 1 0-.956-.294l-4 13a.5.5 0 0 0 .956.294l4-13zM4.854 4.146a.5.5 0 0 1 0 .708L1.707 8l3.147 3.146a.5.5 0 0 1-.708.708l-3.5-3.5a.5.5 0 0 1 0-.708l3.5-3.5a.5.5 0 0 1 .708 0zm6.292 0a.5.5 0 0 0 0 .708L14.293 8l-3.147 3.146a.5.5 0 0 0 .708.708l3.5-3.5a.5.5 0 0 0 0-.708l-3.5-3.5a.5.5 0 0 0-.708 0z"/>
        </svg>
      </button>

      <button id="link-btn" @click="() => handleClickAddTag('a')" type="button" class="btn btn-sm btn-outline-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-link-45deg" viewBox="0 0 16 16">
          <path d="M4.715 6.542 3.343 7.914a3 3 0 1 0 4.243 4.243l1.828-1.829A3 3 0 0 0 8.586 5.5L8 6.086a1.002 1.002 0 0 0-.154.199 2 2 0 0 1 .861 3.337L6.88 11.45a2 2 0 1 1-2.83-2.83l.793-.792a4.018 4.018 0 0 1-.128-1.287z"/>
          <path d="M6.586 4.672A3 3 0 0 0 7.414 9.5l.775-.776a2 2 0 0 1-.896-3.346L9.12 3.55a2 2 0 1 1 2.83 2.83l-.793.792c.112.42.155.855.128 1.287l1.372-1.372a3 3 0 1 0-4.243-4.243z"/>
        </svg>
      </button>

    </div>

    <textarea :id="message_field_id" v-show="!is_preview_on" v-model="message_text" class="form-control" :class="{'is-invalid': error}" rows="3"></textarea>
    <div id="preview-msg" v-show="is_preview_on" class="border border-1 border-secondary rounded-2 p-2" v-html="messageTextHTML"></div>
    <div class="invalid-feedback">{{ error }}</div>

    <div class="m-1">
      <div v-if="file_name">
        <span>{{ file_name }}</span>
        <button class="btn-close" @click="handleClickDelFile" type="button"></button>
      </div>
      <div v-if="image_name">
        <span>{{ image_name }}</span>
        <button class="btn-close" @click="handleClickDelImage" type="button"></button>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "InputMessageField",
  props: [
    "message_field_id", "file_field_id", "image_field_id",
    "set_message_text", "error",
    "image_name", "set_image_data",
    "file_name", "set_file_data"],
  computed: {
    messageTextHTML() {
      let html_text = this.message_text.replace("\n", "<br>");
      this.set_message_text(html_text);
      return html_text;
    },
  },
  methods: {
    handleClickDelFile() {
      this.set_file_data("", "");
    },
    handleClickDelImage() {
      this.set_image_data("", "");
    },
    handleClickUploadFile() {
      let input = document.getElementById(this.file_field_id);
      input.click();
    },
    handleClickUploadImage() {
      let input = document.getElementById(this.image_field_id);
      input.click();
    },
    handleClickPreview() {
      this.is_preview_on = !this.is_preview_on;
    },
    handleClickAddTag(tag) {
      let text = document.getElementById(this.message_field_id);
      let start_select = text.selectionStart;
      let end_select = text.selectionEnd;

      let sliced_msg = [
        this.message_text.substring(0, start_select),
        this.message_text.substring(start_select, end_select),
        this.message_text.substring(end_select)
      ];
      this.message_text = sliced_msg[0] + this.tags[tag][0] + sliced_msg[1] + this.tags[tag][1] + sliced_msg[2];
    },
  },
  data() {return{
    message_text: "",
    is_preview_on: false,
    tags: {
      a: ['<a href="" title="">', '</a>'],
      b: ['<b>', '</b>'],
      i: ['<i>', '</i>'],
      code: ['<code>', '</code>']
    },
  }},
}
</script>

<style scoped>
#preview-msg {
  min-height: 80px;
}
</style>