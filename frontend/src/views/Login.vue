<template>
  <div class="mx-auto" style="margin-top:60px; width:35%">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <router-link to="sign-up" class="nav-item nav-link h5 text-secondary">Regístrate</router-link>
        <router-link to="login" class="nav-item nav-link h5 text-secondary active">Inicia sesión</router-link>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-signup" role="tabpanel" aria-labelledby="nav-signup-tab">
        <div class="mt-4">
          <div class="form-group">
            <app-error v-if="error" :error="error"></app-error>
            <label for="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              class="form-control"
              :class="{'is-invalid': $v.email.$error}"
              @blur="$v.email.$touch()"
              aria-describedby="emailHelp"
              v-model="email"
            >
            <small v-if="$v.email.$error" class="form-text invalid">Ingrese una dirección de correo válida.</small>
          </div>
          <div class="form-group">
            <label for="password">Contraseña</label>
            <input
              id="password"
              type="password"
              class="form-control"
              :class="{'is-invalid': $v.password.$error}"
              @blur="$v.password.$touch()"
              v-model="password"
            >
            <small v-if="$v.password.$error" class="form-text invalid">La contraseña debe tener al menos 6 caracteres.</small>
          </div>
            <button class="btn btn-success float-right" @click="login">Iniciar sesión</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required, email, minLength } from 'vuelidate/lib/validators'
import MessageError from './../components/Error.vue'

export default {
  created () {
    this.$store.dispatch('clearError')
  },
  data () {
    return {
      email: '',
      password: ''
    }
  },
  validations: {
    email: {
      required,
      email
    },
    password: {
      required,
      minLength: minLength(6)
    }
  },
  computed: {
    error () {
      return this.$store.getters.authError
    }
  },
  methods: {
    login () {
      if (!this.$v.$invalid) {
        const formData = {
          correo: this.email,
          clave: this.password
        }
        this.$store.dispatch('login', formData)
      }
    }
  },
  components: {
    'app-error': MessageError
  }

}
</script>
