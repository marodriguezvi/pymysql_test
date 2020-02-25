<template>
  <div class="mx-auto" style="margin-top:60px; width:35%">
    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <router-link to="sign-up" class="nav-item nav-link h5 text-secondary active">Regístrate</router-link>
        <router-link to="login" class="nav-item nav-link h5 text-secondary">Inicia sesión</router-link>
      </div>
    </nav>
    <div class="tab-content" id="nav-tabContent">
      <div class="tab-pane fade show active" id="nav-signup" role="tabpanel" aria-labelledby="nav-signup-tab">
        <div class="mt-4">
          <div class="form-group">
            <app-error v-if="error" :error="error"></app-error>
            <label for="name">Nombre completo</label>
            <input
              id="name"
              type="text"
              class="form-control"
              :class="{'is-invalid': $v.name.$error}"
              @blur="$v.name.$touch()"
              v-model="name"
              >
            <small v-if="$v.name.$error" class="form-text invalid">Campo requerido.</small>
          </div>
          <div class="form-group">
            <label for="email">Correo electrónico</label>
            <input
              id="email"
              type="email"
              class="form-control"
              :class="{'is-invalid': $v.email.$error}"
              aria-describedby="emailHelp"
              @blur="$v.email.$touch()"
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
          <div class="form-group">
            <label for="gender">Género</label>
            <select
              id="gender"
              v-model="gender"
              class="form-control"
              :class="{'is-invalid': $v.gender.$error}"
              @blur="$v.gender.$touch()"
              
            >
              <option value="">---</option>
              <option value="masculino">Masculino</option>
              <option value="femenino">Femenino</option>
            </select>
            <small v-if="$v.gender.$error" class="form-text invalid">
              Campo requerido.</small>
          </div>
          <div class="form-group">
            <label for="fecha-nacimiento">Fecha de nacimiento</label>
            <input
              type="date"
              class="form-control"
              v-model="dateBirth"
              :class="{'is-invalid': $v.dateBirth.$error}"
              @blur="$v.dateBirth.$touch()"
            >
            <small v-if="$v.dateBirth.$error" class="form-text invalid">
              Campo requerido.</small>
          </div>
            <button class="btn btn-success float-right" @click="submit">Registrarse</button>
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
      name: '',
      email: '',
      password: '',
      gender: '',
      dateBirth: ''
    }
  },
  validations: {
    name: {
      required
    },
    email: {
      required,
      email
    },
    password: {
      required,
      minLength: minLength(6)
    },
    gender: {
      required
    },
    dateBirth: {
      required
    }
  },
  computed: {
    error () {
      return this.$store.getters.authError
    }
  },
  methods: {
    submit () {
      if (!this.$v.$invalid) {
        const formData = {
          nombre: this.name,
          correo: this.email,
          clave: this.password,
          genero: this.gender,
          fecha_nacimiento: this.dateBirth
        }

        this.$store.dispatch('signup', formData)
      }
    }
  },
  components: {
    'app-error': MessageError
  }

}
</script>
