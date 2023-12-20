<template>
  <div :id="'msg_' + id" class="mt-3">
    <header class="row justify-content-start align-items-center bg-secondary-subtle rounded-top-3 p-2">

      <div class="col-auto">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
          <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
          <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
        </svg>
      </div>

      <div class="col-auto text-capitalize fw-bold fs-5">
        {{ username }}
      </div>

      <div class="col-auto fw-light">
        {{ date.toLocaleDateString('de-DE') }} at {{ date.toLocaleTimeString('it-IT') }}
      </div>

      <div class="col-auto">

        <a v-if="homepage" :href="homepage" class="btn btn-sm">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-house-door" viewBox="0 0 16 16">
            <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293zM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4z"/>
          </svg>
        </a>

        <button class="btn btn-sm" @click="onClickSend">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-send-plus" viewBox="0 0 16 16">
            <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855a.75.75 0 0 0-.124 1.329l4.995 3.178 1.531 2.406a.5.5 0 0 0 .844-.536L6.637 10.07l7.494-7.494-1.895 4.738a.5.5 0 1 0 .928.372l2.8-7Zm-2.54 1.183L5.93 9.363 1.591 6.602l11.833-4.733Z"/>
            <path d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-3.5-2a.5.5 0 0 0-.5.5v1h-1a.5.5 0 0 0 0 1h1v1a.5.5 0 0 0 1 0v-1h1a.5.5 0 0 0 0-1h-1v-1a.5.5 0 0 0-.5-.5"/>
          </svg>
        </button>

        <button type="button" class="btn btn-sm position-relative" @click="onClickComments">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-chat-left-text" viewBox="0 0 16 16">
            <path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4.414A2 2 0 0 0 3 11.586l-2 2V2a1 1 0 0 1 1-1zM2 0a2 2 0 0 0-2 2v12.793a.5.5 0 0 0 .854.353l2.853-2.853A1 1 0 0 1 4.414 12H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z"/>
            <path d="M3 3.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5M3 6a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 6m0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5"/>
          </svg>
          <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill text-bg-light">
            <span class="comments_num">{{ comments_num }}</span>
            <span class="visually-hidden">unread messages</span>
          </span>
        </button>

      </div>
    </header>

    <main class="p-2 fs-5" v-html="message"></main>

    <footer class="row justify-content-start align-items-center text-secondary p-1">

      <div class="row justify-content-start">

        <div class="col-auto">
          <a v-if="image" :href="image" :data-lightbox="image_name" >
            <img class="preview_img" :src="image" :alt="image_name" />
          </a>
        </div>

        <div class="col-auto">
          <a v-if="file" :href="file">
            <svg xmlns="http://www.w3.org/2000/svg" width="80" height="60" fill="currentColor" class="bi bi-file-earmark-font" viewBox="0 0 16 16">
              <path d="M10.943 6H5.057L5 8h.5c.18-1.096.356-1.192 1.694-1.235l.293-.01v5.09c0 .47-.1.582-.898.655v.5H9.41v-.5c-.803-.073-.903-.184-.903-.654V6.755l.298.01c1.338.043 1.514.14 1.694 1.235h.5l-.057-2z"/>
              <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5z"/>
            </svg>
          </a>
        </div>

      </div>

    </footer>
  </div>
</template>

<script>
import { inject, watch } from "vue";
import { BASE_URL } from "../../config";

export default {
  name: "Message",
  props: ["msg_data", "onClickComments"],
  data() {return {
    id: this.msg_data.id,
    username: this.msg_data.username,
    date: new Date(this.msg_data.date),
    comments_num: this.msg_data.comments_num,
    homepage: this.msg_data.homepage,
    message: this.msg_data.message,
    file: this.msg_data.file,
    image: this.msg_data.image,
  }},
  setup() {
    let msg_id = inject("send_msg");
    let new_msg = inject("new_msg", null);

    watch(new_msg, (data) => {

    });
    return {msg_id, new_msg};
  },
  computed: {
    image_link() {
      return BASE_URL + this.image;
    },
    image_name() {
      let separated = this.image.split("/");
      return separated[separated.length - 1];
    },
  },
  methods: {
    onClickSend() {
      this.msg_id = this.id;
    },
  },
}
</script>

<style scoped>
.preview_img {
  max-height:60px;
  max-width:80px;
  height:auto;
  width:auto;
}
</style>