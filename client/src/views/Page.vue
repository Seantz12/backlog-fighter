<template>
  <div class="container">
    <button type="button" class="btn btn-primary" @click='enableTypeInput()'>
      Add backlog type
    </button>
    <div class="text-input" v-if="showTypeInput">
      <input v-model='backlog_type_input' placeholder='type name'/>
      <button type="button" class="btn btn-primary" @click='addBacklogType()'>
        Confirm
      </button>
    </div>
    <input v-model='backlog_item_input_1' placeholder='item name'/>
    <input v-model='backlog_item_input_2' placeholder='type name'/>
    <button type="button" class="btn btn-primary">
      Add backlog item
    </button>
    <VueTable :rows="this.backlog_types" :head="this.backlog_type_headers"/>
  </div>
</template>

<script>
import axios from 'axios';
import FormData from 'form-data';
import VueTable from '../components/Table.vue';

export default {
  name: 'page',
  components: {
    VueTable,
  },
  data() {
    return {
      msg: 'Hello World Vue!',
      backlog_type_input: '',
      backlog_item_input_1: '', // PLACEHOLDERS GOD PLEASE REPLACE THESE ^ v
      backlog_item_input_2: '',
      backlog_types: [],
      backlog_items: [],
      backlog_type_headers: ['ID', 'Name'],
      showTypeInput: false,
    };
  },
  methods: {
    enableTypeInput() {
      this.showTypeInput = !this.showTypeInput;
    },
    addBacklogType() {
      const path = 'http://localhost:5000/backlog/type';
      const form = new FormData();
      form.append('type', this.backlog_type_input);
      axios.post(path, form).then(() => {
        this.getBacklogType();
      }).catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
      this.showTypeInput = false;
    },
    getBacklogType() {
      const path = 'http://localhost:5000/backlog/type';
      axios.get(path).then((response) => {
        const { types } = response.data;
        this.backlog_types.length = 0;
        for (let i = 0; i < types.length; i += 1) {
          this.backlog_types.push([types[i]]);
        }
      });
    },
  },
  created() {
    this.getBacklogType();
  },
};
</script>
