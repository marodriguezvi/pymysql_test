import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router/index'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    name: null,
    token: null,
    tasks: [],
    authError: null,
  },
  mutations: {
    authUser (state, userData) {
      state.token = userData.token
      state.name = userData.name
    },
    authError (state, errorData) {
      state.authError = errorData
    },
    setTasks (state, tasks) {
      state.tasks = tasks
    },
    clearAuthData (state) {
      state.name = null
      state.token = null
      state.authError = null
      state.tasks = []
    },
    clearError (state) {
      state.authError = null
    }
  },
  actions: {
    signup ({ commit }, authData) {
      Vue.http.post('http://localhost:8000/sign-up', authData)
        .then(response => {
          const data = response.body
          console.log(data)
          commit('authUser', {
            token: data.token,
            name: data.name
          })
          localStorage.setItem('token', data.token)
          localStorage.setItem('name', data.name)
          router.push('/')
        }, error => {
          commit('authError', error.body)
          console.log(error.body)
        })
    },
    login ({ commit }, authData) {
      Vue.http.post('http://localhost:8000/login', authData)
        .then(response => {
          const data = response.body
          console.log(data)
          commit('authUser', {
            token: data.token,
            name: data.name
          })
          localStorage.setItem('token', data.token)
          localStorage.setItem('name', data.name)
          router.push('/')
        }, error => {
          console.log(error.body)
          commit('authError', error.body)
        })
    },
    autoLogin ({ commit }) {
      const token = localStorage.getItem('token')
      const name = localStorage.getItem('name')
      if (token) {
        commit('authUser', {
          token: token,
          name: name
        })
      }
    },
    logout ({ commit }, route) {
      commit('clearAuthData')
      localStorage.removeItem('token')
      localStorage.removeItem('name')
      if (route !== '/') {
        router.push('/')
      }
    },
    getTasks ({ commit, state }) {
      Vue.http.get('http://localhost:8000/tasks', {
        headers: {
          'Authorization': 'Bearer ' + state.token
        }
      }).then(response => {
          console.log(response.body.tasks)
          commit('setTasks', response.body.tasks)
        }, error => {
          console.log(error)
        })
    },
    saveTask ({dispatch, state}, userData) {
      Vue.http.post('http://localhost:8000/tasks', userData, {
        headers: {
          'Authorization': 'Bearer ' + state.token
        }
      }).then(response => {
        console.log(response.body)
        dispatch('getTasks')
      }, error => {
        console.log(error)
      })
    },
    updateEntireTask ({dispatch, state}, userData) {
      Vue.http.put('http://localhost:8000/tasks/' + userData.get('id'), 
      userData, {
        headers: {
          'Authorization': 'Bearer ' + state.token
        }
      }).then(response => {
        console.log(response.body)
        dispatch('getTasks')
      }, error => {
        console.log(error)
      })
    },
    updateTaskPartially ({dispatch, state}, userData) {
      Vue.http.patch('http://localhost:8000/tasks/' + userData.get('id'), 
      userData, {
        headers: {
          'Authorization': 'Bearer ' + state.token
        }
      }).then(response => {
        console.log(response.body)
        dispatch('getTasks')
      }, error => {
        console.log(error)
      })
    },
    deleteTask ({dispatch, state}, userData) {
      Vue.http.delete('http://localhost:8000/tasks/' + userData.id, {
        headers: {
          'Authorization': 'Bearer ' + state.token
        }
      }).then(response => {
        console.log(response.body)
        dispatch('getTasks')
      }, error => {
        console.log(error)
      })
    },
    clearError ({ commit }) {
      commit('clearError')
    }
  },
  getters: {
    isAuthenticated (state) {
      return state.token !== null
    },
    authError (state) {
      return state.authError
    },
    name (state) {
      return state.name
    },
    getTasks (state) {
      return state.tasks
    }
  }
})
