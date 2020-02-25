<template>
  <div class="p4 text-center error">
    <span>{{ error.message }}</span>
  </div>
</template>
<script>
export default {
  props: ['error']
}
</script>
<style>

.error {
  margin: 3% 0;
  padding: 3%;
  font-size: 0.9em;
  border: 1px solid #dc3545;
  background-color: #fcebee;
}

</style>
