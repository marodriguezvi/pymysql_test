<template>
  <div>
    <div>
      <app-header></app-header>
    </div>
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  created () {
    this.$store.dispatch('autoLogin')
  },
  components: {
    'app-header': Header
  }
}
</script>
<style>

.invalid {
  color: #dc3545;
}

.invalid-input {
    border: 1px solid #dc3545;
  }

</style>
