<template>
  <ModalWindow v-if="msg_id !== null"
               :title="msg_id == 0 ? 'Message' : 'Comment'"
               :handle-close="handleClose">

    <form class="m-3">

      <div class="mb-3">
        <label for="usernameForm" class="form-label">Username: </label>
        <input :value="isAuth ? auth.username : username"
               @input="event => username = event.target.value"
               type="text"
               class="form-control"
               :class="{'is-invalid': username_error}"
               :disabled="isAuth"
               id="usernameForm"
               placeholder="Username">
        <div class="invalid-feedback">{{ username_error }}</div>
      </div>

      <div class="mb-3">
        <label for="emailForm" class="form-label">Email: </label>
        <input :value="isAuth ? auth.email : email"
               @input="event => email = event.target.value"
               type="email"
               class="form-control"
               :class="{'is-invalid': email_error}"
               :disabled="isAuth"
               id="emailForm"
               placeholder="name@example.com">
        <div class="invalid-feedback">{{ email_error }}</div>
      </div>

      <div class="mb-3">
        <label for="urlForm" class="form-label">Home page: </label>
        <input v-model="home_url" type="url" class="form-control" :class="{'is-invalid': home_url_error}" id="urlForm" placeholder="https://example.com/home/">
        <div class="invalid-feedback">{{ home_url_error }}</div>
      </div>

      <InputImageField v-show="false"
                       :image_field_id="image_field_id"
                       :set-image-data="setImageData" />
      <InputFileField v-show="false"
                      :file_field_id="file_field_id"
                      :set-file-data="setFileData" />
      <InputMessageField :message_field_id="message_field_id"
                         :file_field_id="file_field_id"
                         :image_field_id="image_field_id"
                         :set_message_text="setMessageText"
                         :image_name="image_name"
                         :set_image_data="setImageData"
                         :file_name="file_name"
                         :set_file_data="setFileData"
                         :error="message_error"
      />

      <div class="row justify-content-center mt-3">
        <div class="col-auto">
          <button type="button" class="btn btn-primary btn-lg" @click="sendData">Send</button>
        </div>
      </div>
    </form>

  </ModalWindow>
</template>

<script>
import ModalWindow from "../ModalWindow.vue";
import {inject} from "vue";
import {SEND_MESSAGE} from "../../api/MessageAPI";
import InputFileField from "./MessageFormElements/InputFileField.vue";
import InputImageField from "./MessageFormElements/InputImageField.vue";
import InputMessageField from "./MessageFormElements/InputMessageField.vue";

export default {
  name: "SendMessageForm",
  components: {InputImageField, InputFileField, ModalWindow, InputMessageField},
  computed: {
    isAuth() {
      if (this.auth.username && this.auth.email && this.auth.token) {
        this.username = this.auth.username;
        this.email = this.auth.email;
        return true;
      }
      return false;
    },
  },
  methods: {
    handleClose() {
      this.msg_id = null;
      this.username = "";
      this.username_error = "";
      this.email = "";
      this.email_error = "";
      this.home_url = "";
      this.home_url_error = "";
      this.message = "";
      this.message_error = "";
      this.image_name = "";
      this.image_data = "";
      this.file_name = "";
      this.file_data = "";
    },
    setImageData(image_data, image_name) {
      this.image_data = image_data;
      this.image_name = image_name;
    },
    setFileData(file_data, file_name) {
      this.file_data = file_data;
      this.file_name = file_name;
    },
    setMessageText(msg) {
      this.message = msg;
    },
    checkAll() {
      let check_methods = [this.checkUsername, this.checkEmail, this.checkURL, this.checkMessage];
      let is_valid = true
      for (let i=0; i<check_methods.length; i++) {
        if (!check_methods[i]()) is_valid = false;
      }
      return is_valid;
    },
    checkUsername() {
      if (this.isAuth) return true;
      if (!this.username) {
        this.username_error = "This field is required.";
        return false;
      }
      if (!/^[a-zA-Z0-9_\-]{4,15}$/g.test(this.username)) {
        this.username_error = "Username must be 5-15 characters long. Only symbols are allowed: A-Z, a-z, 0-9, _, -.";
        return false;
      }
      this.username_error = "";
      return true;
    },
    checkEmail() {
      if (this.isAuth) return true;
      if (!this.email) {
        this.email_error = "This field is required.";
        return false;
      }
      if (!/\w+@\w+\.+\w{2}/g.test(this.email)) {
        this.email_error = "Wrong email."
        return false;
      }
      this.email_error = "";
      return true;
    },
    checkURL() {
      if (this.home_url) {
        if (!/http[s]?:\/\/[a-z0-9_\-.]+\.[a-z0-9_\-\/]+/g.test(this.home_url)) {
          this.home_url_error = "Wrong url.";
          return false;
        }
      }
      this.home_url_error = "";
      return true;
    },
    checkMessage() {
      if (!this.message) {
        this.message_error = "Message is empty.";
        return false;
      }
      if (!this.checkForbiddenTags()) {
        this.message_error = "Allowed tags only: <" + this.allowed_tags.join(">, <") + ">.";
        return false;
      }
      if (!this.checkCloseTags()) {
        this.message_error = "There are unclosed tags.";
        return false;
      }
      this.message_error = "";
      return true;
    },
    checkForbiddenTags() {
      let text = this.message.replace("<br>", " ");
      let forbidden = text.match(/<(?!\/?code|\/?b|\/?a|\/?i)\s?.*?>/g);
      if (forbidden) return false;
      return true;
    },
    checkCloseTags() {
      let text = this.message.replace("<br>", " ");
      let re = /<(?<tag>.+)\s?[^>^<]*>[^>^<]*<\/\k<tag>>/g;
      while (text.match(re)) text = text.replace(re, "");
      if (/<.*?>/g.test(text)) return false;
      return true;
    },
    sendData() {
      if (this.checkAll()) {
        let data = {
          parent: this.msg_id ? this.msg_id : null,
          username: this.username,
          email: this.email,
          homepage: this.home_url,
          message: this.message,
          file_name: this.file_name,
          file_data: this.file_data,
          image_name: this.image_name,
          image_data: this.image_data
        }
        SEND_MESSAGE(data)
            .then( r => {
              if (r.data.requires_confirmation) {
                this.confirm = true;
              } else {
                this.info = r.data.result;
              }
              this.handleClose();
            } )
            .catch( e => {
              this.info = e.response.data.result;
              this.handleClose();
            } )
      }
    }
  },
  data() {return {
    username: "",
    username_error: "",
    email: "",
    email_error: "",
    home_url: "",
    home_url_error: "",
    message: "",
    message_error: "",
    image_name: "",
    image_data: "",
    file_name: "",
    file_data: "",
    is_auth: false,
    message_field_id: "messageForm",
    file_field_id: "formFile",
    image_field_id: "formImage",
    allowed_tags: ["a", "b", "i", "code"],
  }},
  setup() {
    let msg_id = inject("send_msg", null);
    let info = inject("info", null);
    let confirm = inject("confirm", null);
    let auth = inject("auth",);

    return {msg_id, info, confirm, auth};
  },
}
</script>

<style scoped>

</style>
