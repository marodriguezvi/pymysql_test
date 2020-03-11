<template>
  <div style="margin-top:60px">
    <div class="row">
      <div class="col-md-4 mt-4 border">
        <div class="form-group mt-4">
          <label for="name">Nombre</label>
          <input
            id="name"
            type="text"
            class="form-control"
            v-model="name"
            @blur="$v.name.$touch()"
            :class="{'is-invalid': $v.name.$error}">
          <small
            v-if="$v.name.$error"
            class="form-text invalid">Campo requerido.</small>
        </div>
        <div class="form-group">
          <label for="description">Descripción</label>
          <textarea
            class="form-control"
            id="description"
            cols="30" 
            rows="3"
            maxlength="250"
            v-model="description"
            @blur="$v.description.$touch()"
            :class="{'is-invalid': $v.description.$error}"></textarea>
          <small class="form-text text-muted float-right">
            {{ description.length }}/250</small>
        </div>
        <div class="form-group">
          <label for="image">Imagen</label>
          <input
            id="image"
            ref="inputfile"
            type="file"
            accept="image/*"
            @change="readFile"
            :class="{'invalid': imageError}"
            class="form-control-file">
        </div>
        <div class="form-group">
          <button
            v-if="currentItem.length == 0"
            class="btn btn-success"
            @click="sendTask">Crear</button>
          <button v-else class="btn btn-success"
            @click="updateTask">Actualizar</button>
          <button
            class="btn btn-secondary float-right"
            @click="clearForm">Cancelar</button>
        </div>
        <hr>
        <div class="form-group">
          <download-csv
            class = "btn btn-success"
            :data = "tasksData"
            name = "tasks.csv">
            Exportar tareas
          </download-csv>
        </div>
      </div>
      <div class="col-md-8 mt-4 table-wrapper-scroll-y my-custom-scrollbar">
        <table class="table table-borderless table-bordered mb-0">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Nombre</th>
              <th scope="col">Descripción</th>
              <th scope="col">Fecha de creación</th>
              <th scope="col">imagen</th>
              <th scope="col" colspan="2">Opciones</th>
            </tr>
          </thead>
          <tbody v-for="(item, index) in tasks" :key="item.id">
            <tr>
              <th scope="row">{{ index+1 }}</th>
              <td>{{ item[2] }}</td>
              <td>{{ item[3] }}</td>
              <td>{{ item[4] }}</td>
              <td><a href="#" @click="showImage(item[5])">{{ item[6] }}</a></td>
              <td>
                <button
                  class="btn btn-primary btn-sm"
                  @click="loadTask(item)">Editar</button>
              </td>
              <td>
                <button
                  data-toggle="modal"
                  data-target="#modal"
                  class="btn btn-danger btn-sm"
                  @click="taskKey = item[0]">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- Alert -->
    <div class="modal fade" id="modal" tabindex="-1" role="dialog"
      aria-labelledby="modalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"
              aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            ¿Eliminar permanentemente?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" 
              data-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-primary"
              data-dismiss="modal" @click="deleteTask">Aceptar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { required } from 'vuelidate/lib/validators'

export default {
  mounted() {
    this.$store.dispatch('getTasks')
  },
  data() {
    return {
      name: '',
      image: null,
      description: '',
      imageError: false,
      currentItem: [],
      taskKey: ''
    }
  },
  validations: {
    name: {
      required
    },
    description: {
      required
    }
  },
  computed: {
    tasks () {
      return this.$store.getters.getTasks
    },
    tasksData () {
      let tasks = this.$store.getters.getTasks
      let data = []
      data.push(['nombre', 'descripcion', 'fecha de creacion', 'imagen'])
      for (let i of tasks) {
        data.push([i[2], i[3], i[4], i[6]])
      }
      return data
    }
  },
  methods: {
    showImage (data) {
      this.$router.push({name: 'image', params: {dataUrl: data}})
    },
    readFile (e) {
      this.image = e.target.files[0]
    },
    loadTask (item) {
      this.currentItem = item
      this.name = item[2]
      this.description = item[3]
    },
    clearForm () {
      this.name = ''
      this.image = null
      this.description = ''
      this.currentItem = []
      this.imageError = false
      this.$v.$reset()
      this.$refs.inputfile.value = ''
    },
    sendTask () {
      if (this.image) {
        if (!this.$v.$invalid) {
          var formData = new FormData()
          formData.append('nombre', this.name)
          formData.append('descripcion', this.description)
          formData.append('imagen', this.image)
          this.$store.dispatch('saveTask', formData)
          this.clearForm()
        }
      }else {
        this.imageError = true
      }
    },
    updateTask () {
        var formData = new FormData()
        formData.append('id', this.currentItem[0])
        formData.append('nombre', this.name)
        formData.append('descripcion', this.description)
        if (this.image) {
          formData.append('imagen', this.image)
          this.$store.dispatch('updateEntireTask', formData)
        } else {
          this.$store.dispatch('updateTaskPartially', formData)
        }
        this.clearForm()
    },
    deleteTask () {
      const formData = {
        id: this.taskKey
      }
      this.$store.dispatch('deleteTask', formData)
    }
  }
}
</script>
<style>
.my-custom-scrollbar {
  position: relative;
  height: 402px;
  overflow: auto;
}
.table-wrapper-scroll-y {
  display: block;
}
</style>