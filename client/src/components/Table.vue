<template>
  <div>
    <table class="table">
      <thead>
        <tr class="first-row">
          <th
            scope="col"
            v-for="(item, key) in this.head"
            :key="key"
            @click="clicked(item)">
            {{item}}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, key) in this.rows" :key="key">
          <th scope="row">{{key + 1}}</th>
          <td v-for="(item, key) in row" :key="key">
            {{item}}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'vueTable',
  methods: {
    clicked(item) {
      this.$emit('clicked', item);
    },
  },
  props: ['head', 'rows'],
};
</script>
