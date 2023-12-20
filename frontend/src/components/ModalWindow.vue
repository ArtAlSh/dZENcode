<template>
  <div class="modal modal-xl show" style="display: block;" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="handleClose"></button>
        </div>

        <div class="modal-body">
          <slot></slot>
        </div>

      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" />

</template>

<script>
import {inject} from "vue";
export default {
  name: "ModalWindow",
  props: ["title", "handleClose"],
  setup() {
    let msg_id = inject("send_msg");
    return {msg_id};
  },
}
</script>

<style scoped>

</style>