<template>
  <ul>
    <li v-for="(message, index) in messages_list">
      <Message :msg_data="message" :on-click-comments="() => onClickComments(index)" />
      <MessagesList v-if="message['comments'] !== undefined"
                    :messages_list="message.comments"
                    :set_messages_list="(msgs, previous_, next_) => update_comments(index, msgs, previous_, next_)"
                    :previous="message.previous" :next="message.next"
      />
    </li>
  </ul>
  <div class="row justify-content-center">
    <div class="btn-group col-auto">

      <button type="button" class="btn btn-outline-secondary" :class="{disabled: !isPrevious}" @click="previous_page">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/>
        </svg>
      </button>

      <button type="button" class="btn btn-outline-secondary" :class="{disabled: !isNext}" @click="next_page">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
        </svg>
      </button>

    </div>
  </div>
</template>

<script>
import Message from "./Message.vue";
import { GET_MESSAGES } from "../../api/MessageAPI";
import { BASE_URL } from "../../config";
import {inject} from "vue";

export default {
  name: "MessagesList",
  components: {Message},
  props: ["messages_list", "set_messages_list", "previous", "next"],
  computed: {
    isPrevious() {
      if (this.previous) return true;
      return false;
    },
    isNext() {
      if (this.next) return true;
      return false;
    },
  },
  methods: {
    onClickComments(msg_ind) {
      let msg_id = this.messages_list[msg_ind].id;
      if (this.messages_list[msg_ind]["comments"] !== undefined) {
        this.messages_list[msg_ind]["comments"] = undefined;
        this.messages_list[msg_ind].previous = undefined;
        this.messages_list[msg_ind].next = undefined;
      } else {
        GET_MESSAGES(msg_id)
          .then( r => {
            this.messages_list[msg_ind].comments = r.data.results;
            this.messages_list[msg_ind].previous = r.data.previous;
            this.messages_list[msg_ind].next = r.data.next;
          } )
          .catch( e => console.log(e) )
      }
    },
    next_page() {
      if (this.next) {
        let [url, params_str] = this.next.split("?");
        let msg_id = url.split(BASE_URL).pop();
        msg_id = msg_id.replaceAll("/", "");
        let params = this.get_params(params_str);

        GET_MESSAGES(msg_id, params)
            .then( r => {
              this.set_messages_list(r.data.results, r.data.previous, r.data.next);
            } )
            .catch( e => console.log(e) );
      }
    },
    previous_page() {
      if (this.previous) {
        let [url, params_str] = this.previous.split("?");
        let msg_id = url.split(BASE_URL).pop();
        msg_id = msg_id.replaceAll("/", "");
        let params = this.get_params(params_str);

        GET_MESSAGES(msg_id, params)
            .then( r => {
              this.set_messages_list(r.data.results, r.data.previous, r.data.next);
            } )
            .catch( e => console.log(e) );
      }
    },
    update_comments(msg_ind, messages, previous=null, next=null) {
      this.messages_list[msg_ind].comments = messages;
      this.messages_list[msg_ind].previous = previous;
      this.messages_list[msg_ind].next = next;
      this.component_key += 1;
    },
    get_params(params_str) {
      let params = {};
      let page = /page=(\d+)&?/g.exec(params_str);
      if (page) params.page = page[1];
      let username = /username=([^&]+)&?/g.exec(params_str);
      if (username) params.username = username[1];
      let email = /email=([^&]+)&?/g.exec(params_str);
      if (email) params.email = email[1];
      let order = /order=(desc|asc)&?/g.exec(params_str);
      if (order) params.order = order[1];

      return params;
    },
  },
  setup() {
    let component_key = inject("component_key");
    return {component_key};
  },
}
</script>

<style scoped>
ul {
  list-style-type: none;
}
</style>