<template>
  <div class="fixed-top">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link to="/" class="navbar-brand">TEST</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <router-link v-if="auth" to="/tareas" tag="li"
              class="nav-item"><a class="nav-link">Tareas</a></router-link>
          </ul>
          <ul v-if="!auth" class="navbar-nav ml-auto">
            <router-link to="/login" tag="li"
              class="nav-item">
              <a class="nav-link">Inicia sesión</a></router-link>
            <router-link to="/sign-up" tag="li"
              class="nav-item"><a class="nav-link">Regístrate</a></router-link>
          </ul>
          <ul v-if="auth" class="navbar-nav ml-auto">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown"
                role="button" data-toggle="dropdown" aria-haspopup="false"
                aria-expanded="false" @click="showDropDown = !showDropDown">
                {{ name }}
              </a>
              <ul v-if="showDropDown" class="dropdown-menu"
                :class="{show: showDropDown}" style="width: 194px">
                <div>
                  <li class="dropdown-item" @click="logout"
                    style="cursor: pointer">Cerrar sesión</li>
                </div>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>
<script>
export default {
  data () {
    return {
      showDropDown: null,
    }
  },
  computed: {
    auth () {
      return this.$store.getters.isAuthenticated
    },
    name () {
      return this.$store.getters.name
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('logout', this.$route.path)
      this.showDropDown = null
    }
  }
}
</script>
<style>
.input {
  width: 98% !important;
  margin: 1%;
}
</style>
