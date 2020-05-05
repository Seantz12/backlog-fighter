<template>
  <div class="container">
    <button type="button" class="btn btn-primary" @click='enableTypeInput()'>
      Add backlog type
    </button>
    <div class="text-input" v-if="showTypeInput">
      <input v-model='backlogTypeInput' placeholder='type name'/>
      <button type="button" class="btn btn-primary" @click='addBacklogType()'>
        Confirm
      </button>
    </div>
    <input v-model='backlogItemInput1' placeholder='item name'/>
    <input v-model='backlogItemInput2' placeholder='type name'/>
    <button type="button" class="btn btn-primary">
      Add backlog item
    </button>
    <VueTable :rows="this.backlogTypes" :head="this.backlogTypeHeaders"/>
    <div class="filtered-items">
      <p v-for="(item, key) in this.sortParameters.types" :key="key" @click="removeFilter(item)">
        {{item}}
      </p>
    </div>
    <div class="dropdown">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        id="dropdownMenuButton"
        @click="enableFilterDropdown()"
        aria-haspopup="true"
        aria-expanded="false">
        Dropdown button
      </button>
      <div v-show="showTypeFilter" aria-labelledby="dropdownMenuButton">
        <a
          class="dropdown-item"
          v-for="(item, key) in notTypeFilters"
          :key="key"
          @click="addFilter(item)">
          {{item}}
        </a>
      </div>
    </div>
    <VueTable
      :rows="this.backlogItems"
      :head="this.backlogItemHeaders"
      @clicked="sortHeader"/>
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
  computed: {
    notTypeFilters() {
      const typeFilters = [];
      this.backlogTypes.map((element) => typeFilters.push(element[0]));
      return typeFilters.filter((element) => !(this.sortParameters.types.includes(element)));
    },
  },
  data() {
    return {
      msg: 'Hello World Vue!',
      backlogTypeInput: '',
      backlogItemInput1: '', // PLACEHOLDERS GOD PLEASE REPLACE THESE ^ v
      backlogItemInput2: '',
      backlogTypes: [],
      backlogItems: [],
      backlogTypeHeaders: ['ID', 'Name'],
      backlogItemHeaders: ['ID', 'Type Name', 'Item Name', 'Created Date', 'Goal Date'],
      sortParameters: {
        order: { parameter: 'Name', ascending: false },
        searchFilter: '',
        types: [],
        // consider adding date range sort
      },
      // notTypeFilters: [],
      showTypeInput: false,
      showTypeFilter: false,
      showType: '',
    };
  },
  methods: {
    addFilter(item) {
      this.sortParameters.types.push(item);
      // send filter request to change backlog items here
    },
    removeFilter(item) {
      const index = this.sortParameters.types.indexOf(item);
      this.sortParameters.types.splice(index, 1);
    },
    enableTypeInput() {
      this.showTypeInput = !this.showTypeInput;
    },
    enableFilterDropdown() {
      this.showTypeFilter = !this.showTypeFilter;
    },
    addBacklogType() {
      const path = 'http://localhost:5000/backlog/type';
      const form = new FormData();
      form.append('type', this.backlogTypeInput);
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
        this.backlogTypes.length = 0;
        // this.typeFilters.length = 0;
        for (let i = 0; i < types.length; i += 1) {
          this.backlogTypes.push([types[i]]);
        }
      });
    },
    getBacklogItems() {
      const path = 'http://localhost:5000/backlog/item';
      axios.get(path).then((response) => {
        const { data } = response;
        this.backlogItems.length = 0;
        for (let i = 0; i < data.length; i += 1) {
          const rowItems = [];
          rowItems.push(data[i].backlog_type);
          rowItems.push(data[i].task_name);
          rowItems.push(data[i].created);
          rowItems.push(data[i].goal_date);
          this.backlogItems.push(rowItems);
        }
      });
    },
    sortHeader(name) {
      // eslint-disable-next-line
      console.log(name);
      if (this.sortParameters.order.parameter === name) {
        this.sortParameters.order.ascending = !this.sortParameters.order.ascending;
      }
      this.sortParameters.order.parameter = name;
    },
  },
  created() {
    this.getBacklogType();
    this.getBacklogItems();
  },
};
</script>
