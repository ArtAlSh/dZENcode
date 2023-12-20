<template>
  <div class="modal modal-sm show" style="display: block;" tabindex="-1">
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
export default {
  name: "SmallModalWindow.vue",
  props: ["title", "handleClose"],
}
</script>

<style scoped>

</style>