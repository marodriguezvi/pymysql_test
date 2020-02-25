<template>
  <div class="text-center container" style="margin-top:60px">
    <h2 class="my-4">Tareas</h2>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Nombre</th>
          <th scope="col">Descripción</th>
          <th scope="col">Fecha de creación</th>
          <th scope="col">imagen</th>
        </tr>
      </thead>
      <tbody v-for="(item, index) in tasks" :key="item.id">
        <tr>
          <th scope="row">{{ index+1 }}</th>
          <td>{{ item[2] }}</td>
          <td>{{ item[3] }}</td>
          <td>{{ item[4] }}</td>
          <td>{{ item[6] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('getTasks')
  },
  computed: {
    tasks() {
      return this.$store.getters.getTasks
    }
  }
}
</script>