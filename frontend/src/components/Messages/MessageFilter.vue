<template>
  <div class="row justify-content-start mt-2">

    <div class="col-1 text-end">
      <button class="btn" @click="() => sort_by_asc = !sort_by_asc">

        <svg v-if="sort_by_asc" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-alpha-down" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M10.082 5.629 9.664 7H8.598l1.789-5.332h1.234L13.402 7h-1.12l-.419-1.371h-1.781zm1.57-.785L11 2.687h-.047l-.652 2.157h1.351"/>
          <path d="M12.96 14H9.028v-.691l2.579-3.72v-.054H9.098v-.867h3.785v.691l-2.567 3.72v.054h2.645V14zM4.5 2.5a.5.5 0 0 0-1 0v9.793l-1.146-1.147a.5.5 0 0 0-.708.708l2 1.999.007.007a.497.497 0 0 0 .7-.006l2-2a.5.5 0 0 0-.707-.708L4.5 12.293z"/>
        </svg>

        <svg v-if="!sort_by_asc" xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sort-alpha-up" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M10.082 5.629 9.664 7H8.598l1.789-5.332h1.234L13.402 7h-1.12l-.419-1.371h-1.781zm1.57-.785L11 2.687h-.047l-.652 2.157h1.351"/>
          <path d="M12.96 14H9.028v-.691l2.579-3.72v-.054H9.098v-.867h3.785v.691l-2.567 3.72v.054h2.645V14zm-8.46-.5a.5.5 0 0 1-1 0V3.707L2.354 4.854a.5.5 0 1 1-.708-.708l2-1.999.007-.007a.498.498 0 0 1 .7.006l2 2a.5.5 0 1 1-.707.708L4.5 3.707z"/>
        </svg>

      </button>
    </div>

    <div class="col-3 text-start">
       <input v-model="username" type="text" class="form-control" id="username_filter" placeholder="username">
    </div>

    <div class="col-3 text-start">
      <input v-model="email" type="text" class="form-control" id="email_filter" placeholder="email">
    </div>

    <div class="col-2 offset-3 text-end">
      <button class="btn btn-secondary" @click="filter">
        Filter
      </button>
    </div>

  </div>
</template>

<script>
import { GET_MESSAGES } from "../../api/MessageAPI";

export default {
  name: "MessageFilter",
  props: ["set_messages_list"],
  methods: {
    filter() {
      let params = {};
      if (this.username) params.username = this.username;
      if (this.email) params.email = this.email;
      params.order = (this.sort_by_asc ? "asc" : "desc");

      GET_MESSAGES("", params)
          .then( r => {
            this.set_messages_list(r.data.results, r.data.previous, r.data.next);
          } )
          .catch( e => console.log(e) );
    },
  },
  data() {return {
    sort_by_asc: false,
    username: "",
    email: "",
  }},
}
</script>

<style scoped>

</style>