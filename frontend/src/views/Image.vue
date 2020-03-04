<template>
  <div class="text-center" style="margin-top:60px">
    <img class="mt-3" :src="dataUrl" width="80%">
  </div>
</template>
<script>
export default {
  props: ['dataUrl']
}
</script>