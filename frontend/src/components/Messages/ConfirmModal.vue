<template>
  <SmallModalWindow v-if="confirm" title="Confirm" :handle-close="handleClose">
    <div class="mt-5 mb-4 fs-4 text-center">
       Enter the code sent to your email.
    </div>

    <form>

      <div class="row justify-content-center mb-4 align-items-center">
        <div class="col-4 text-end">
          <label for="code_confirm" class="form-label fs-5">Code: </label>
        </div>
        <div class="col-8 text-start">
          <input v-model="code" type="text" class="form-control" id="code_confirm">
        </div>
      </div>

      <div class="text-center">
        <button class="btn btn-primary" type="button" @click="handleClickConfirm">Confirm</button>
      </div>

    </form>
  </SmallModalWindow>
</template>

<script>
import SmallModalWindow from "../SmallModalWindow.vue";
import {CONFIRM_MESSAGE} from "../../api/MessageAPI";
import {inject} from "vue";

export default {
  name: "ConfirmModal",
  components: {SmallModalWindow},
  methods: {
    handleClose() {
      this.confirm = false;
      this.code = "";
    },
    handleClickConfirm() {
      if (this.code) {
        CONFIRM_MESSAGE({key: this.code})
          .then( r => {
            this.handleClose();
            this.auth.username = r.data.auth.username;
            this.auth.email = r.data.auth.email;
            this.auth.token = r.data.auth.access;
            this.info = r.data.result;
          } )
          .catch( e => {
            this.handleClose();
            this.info = e.response.data.result;
          } );
      }
    },
  },
  data() {return {
    code: "",
  }},
  setup() {
    let confirm = inject("confirm");
    let info = inject("info");
    let auth = inject("auth");
    return {confirm, info, auth};
  }
}
</script>

<style scoped>

</style>