<template>
  <main class="container">
    <MessageFilter :set_messages_list="setMessageList" />
    <div v-if="!messages.length" class="m-5 text-center fs-4">There are no messages.<br>Write the first one.</div>
    <MessagesList v-if="messages.length"
                  :messages_list="messages"
                  :set_messages_list="setMessageList"
                  :previous="previous" :next="next"
                  :key="component_key"
    />
    <SendMessageForm />
    <ConfirmModal />
    <InfoModal />
    <div class="row justify-content-center m-4">
      <div class="col-auto text-center">
        <button class="btn btn-warning btn-lg" type="button" @click="() => confirm = true">Confirm</button>
      </div>
      <div class="col-auto text-center">
        <button class="btn btn-primary btn-lg" type="button" @click="() => send_msg_id = 0">New message</button>
      </div>
    </div>
  </main>
</template>

<script>
import {provide, ref, reactive, watch} from "vue";
import { api, GET_MESSAGES } from "./api/MessageAPI";
import { BASE_WS } from "./config";
import MessagesList from "./components/Messages/MessagesList.vue";
import ModalWindow from "./components/ModalWindow.vue";
import SendMessageForm from "./components/Messages/SendMessageForm.vue";
import InfoModal from "./components/Messages/InfoModal.vue";
import ConfirmModal from "./components/Messages/ConfirmModal.vue";
import MessageFilter from "./components/Messages/MessageFilter.vue";

export default {
  name: "App",
  components: {InfoModal, SendMessageForm, ModalWindow, MessagesList, ConfirmModal, MessageFilter},
  methods: {
    getMessages() {
      GET_MESSAGES()
          .then( r => {
            this.messages = r.data.results;
            this.previous = r.data.previous;
            this.next = r.data.next;
          } )
          .catch( e => console.log(e) )
    },
    setMessageList(messages, previous=null, next=null) {
      this.messages = messages;
      this.previous = previous;
      this.next = next;
      this.component_key += 1;
    },
    addNewMessage(data) {
      if (!data.parent) {
        this.messages.push(data);
      } else {
        let el = document.getElementById("msg_" + data.parent);
        if (el) {
          let count = el.getElementsByClassName("comments_num")[0];
          count.innerText = Number(count.innerText) + 1;
          this.recAddNewMessage(this.messages, data);
        }
      }
    },
    recAddNewMessage(messages, data) {
      for (let i=0; i<messages.length; i++) {
        if (messages[i].id === data.parent) {
          messages[i].comments_num += 1;
          if (messages[i].comments) messages[i].comments.push(data);
          return true;
        } else if (msg.comments) {
          let res = this.recAddNewMessage(msg.comments);
          if (res) return true;
        }
      }
      messages.map( (msg) => {
        if (msg.id === data.parent) {
          msg.comments_num += 1;
          if (msg.comments) msg.comments.push(data);
          return 0;
        } else if (msg.comments) {
          this.recAddNewMessage(msg.comments);
        }
      } );
    },
    initWebSockets() {
      try {
        this.socket = new WebSocket(BASE_WS);
        this.socket.onmessage = (e) => {
          let data = JSON.parse(e.data);
          this.addNewMessage(data);
        }
        this.socket.onclose = (e) => {
          console.log("Socket was closed.");
        }
      } catch (err) {
        console.log("Socket error.");
      }
    },
    closeWebSocket() {
      try {
        this.socket.close();
      } catch (err) {
        return 0;
      }
    },
    initAuth() {
      let auth = JSON.parse(sessionStorage.getItem("auth"));
      if (auth) {
        if (auth.token && auth.username && auth.email) {
          this.auth.username = auth.username;
          this.auth.email = auth.email;
          this.auth.token = auth.token;
          api.defaults.headers.common["Authorization"] = "Bearer " + auth.token;
        }
      }
    },
  },
  data() {return {
    messages: [],
    previous: null,
    next: null,
    new_message: null,
    socket: null,
  }},
  setup() {
    let send_msg_id = ref(null);
    provide("send_msg", send_msg_id);

    let info = ref(null);
    provide("info", info);

    let confirm = ref(false);
    provide('confirm', confirm);

    let auth = reactive({
      username: "",
      email: "",
      token: ""
    });
    provide("auth", auth);

    watch(auth, (value) => {
      api.defaults.headers.common["Authorization"] = "Bearer " + value.token;
      sessionStorage.setItem("auth", JSON.stringify(auth));
    });

    let new_msg = ref(null);
    provide("new_msg", new_msg);

    let component_key = ref(0);
    provide("component_key", component_key);

    return {send_msg_id, info, confirm, auth, new_msg, component_key};
  },
  mounted() {
    this.initAuth();
    this.getMessages();
    this.initWebSockets();
  },
  unmounted() {
    this.closeWebSocket();
  }
}
</script>

<style scoped></style>
