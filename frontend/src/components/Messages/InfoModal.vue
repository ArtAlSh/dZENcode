<template>
  <SmallModalWindow v-if="info !== null" title="" :handle-close="handleClose">
    <div class="m-5 text-center">{{ info }}</div>
    <div class="text-center">
      <button class="btn btn-primary" type="button" @click="handleClose">Ok</button>
    </div>
  </SmallModalWindow>
</template>

<script>
import SmallModalWindow from "../SmallModalWindow.vue";
import {inject} from "vue";

export default {
  name: "InfoModal",
  components: {SmallModalWindow},
  methods: {
    handleClose() {
      this.info = null;
    }
  },
  setup() {
    let info = inject("info", null);
    return {info};
  }
}
</script>

<style scoped>

</style>