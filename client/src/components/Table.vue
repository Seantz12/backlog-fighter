<template>
  <div>
    <table class="table">
      <thead>
        <tr class="first-row">
          <th scope="col" v-for="(item, key) in this.head" :key="key">
            {{item}}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, key) in this.rows" :key="key">
          <th scope="row">{{key}}}</th>
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
  props: ['head', 'rows'],
};
</script>
