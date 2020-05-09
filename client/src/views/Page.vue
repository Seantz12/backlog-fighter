<template>
  <div class="container">
    <div class="filtered-items">
      <a href="#"
        v-for="(item, key) in this.sortParameters.types" :key="key" @click="removeFilter(item)">
        {{item}}
      </a>
    </div>
    <div class="filters">
      <div class="dropdown">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          id="dropdownMenuButton"
          @click="enableFilterDropdown()"
          aria-haspopup="true"
          aria-expanded="false">
        Select Type
        </button>
        <div
          class="dropdown-container"
          v-show="showTypeFilter"
          aria-labelledby="dropdownMenuButton">
          <div
            class="dropdown-item-container"
            v-for="(item, key) in notTypeFilters"
            :key="key">
            <a
              class="dropdown-item"
              @click="addFilter(item)">
              {{item}}
            </a>
          </div>
        </div>
      </div>
      <div class="search-filter">
        <input v-model="this.sortParameters.searchFilter"/>
      </div>
    </div>
<!--
    <button type="button" class="btn btn-primary" @click='showTypeModal=true'>
      Add backlog type
    </button> -->
    <button type="button" class="btn btn-primary" @click='showItemModal=true'>
      Add backlog item
    </button>

    <!-- <VueTable :rows="this.backlogTypes" :head="this.backlogTypeHeaders"/> -->

    <VueTable
      :rows="this.backlogItems"
      :head="this.backlogItemHeaders"
      @clicked="sortHeader"/>

    <!-- <Modal v-if="showTypeModal">
      <template v-slot:header>
        <h1>Add a new Backlog Type</h1>
      </template>
      <template v-slot:content>
        <input v-model='backlogTypeInput' placeholder='type name'/>
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-primary" @click='addBacklogType()'>
          Confirm
        </button>
        <button @click="showTypeModal=false">
         Cancel
        </button>
      </template>
    </Modal> -->

    <Modal v-if="showItemModal">
      <template v-slot:header>
        <h1>Add a new Backlog Item</h1>
      </template>
      <template v-slot:content>
        <input v-model='backlogItemName' placeholder='item name'/>
        <input v-model='backlogItemType' placeholder='type name'/>
      </template>
      <template v-slot:footer>
        <button type="button" class="btn btn-primary" @click='addBacklogItem()'>
          Confirm
        </button>
        <button @click="showItemModal=false">
         Cancel
        </button>
      </template>
    </Modal>

  </div>
</template>

<script>
import axios from 'axios';
import FormData from 'form-data';
import VueTable from '../components/Table.vue';
import Modal from '../components/Modal.vue';

export default {
  name: 'page',
  components: {
    VueTable,
    Modal,
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
      backlogItemName: '', // PLACEHOLDERS GOD PLEASE REPLACE THESE ^ v
      backlogItemType: '',
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
      showTypeInput: false,
      showTypeFilter: false,
      showType: '',
      showTypeModal: false,
      showItemModal: false,
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
      this.showTypeModal = false;
    },
    getBacklogType() {
      const path = 'http://localhost:5000/backlog/type';
      axios.get(path).then((response) => {
        const { types } = response.data;
        this.backlogTypes.length = 0;
        for (let i = 0; i < types.length; i += 1) {
          this.backlogTypes.push([types[i]]);
        }
      });
    },
    addBacklogItem() {
      const form = new FormData();
      form.append('name', this.backlogItemName);
      form.append('type_id', this.backlogItemType);
      const pathItem = 'http://localhost:5000/backlog/item';
      axios.post(pathItem, form).then(() => {
        this.getBacklogItems();
        this.getBacklogType();
      }).catch((error) => {
        // eslint-disable-next-line
        console.log(error);
      });
      this.showItemModal = false;
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

<style scoped>
.filters {
  display: flex;
}
.dropdown-item {
  background-color: white;
  border: 1px solid;
}

.dropdown-item:hover {
  background-color: blue;
  color: white;
  border: 1px solid;
}
.dropdown-container {
  position: absolute;
}
.dropdown-item-container {
  margin-top: 15px auto;

}
</style>
