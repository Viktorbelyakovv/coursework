import Vue from 'vue'
import App from './App.vue'
import './quasar'

import VueRouter from 'vue-router'
import Main from './pages/Main.vue'
import NotFound from './pages/NotFound.vue'
import Auth from './pages/Auth.vue'
import Reg from './pages/Reg.vue'
import Profile from './pages/Profile.vue'
import Division from './pages/tables/Division.vue'
import ClubsLib from './pages/tables/ClubsLib.vue'
import ClubsTable from './pages/tables/ClubsTable.vue'
import ForwardsTable from './pages/tables/ForwardsTable.vue'

Vue.config.productionTip = false

const router = new VueRouter({
  routes: [
    { path: '/', component: Main },
    { path: '*', component: NotFound },
    { path: '/auth', component: Auth },
    { path: '/reg', component: Reg },
    { path: '/profile', component: Profile },
    { path: '/division', component: Division },
    { path: '/clubslib', component: ClubsLib },
    { path: '/clubstable', component: ClubsTable },
    { path: '/forwardstable', component: ForwardsTable },
  ]
})
Vue.use(VueRouter)

//Локальное хранилище данных
//Используется для хранения состояния приложения
import Vuex from 'vuex'
//state описывает все поля данных, которые необходимо хранить
import state from './store/state'
//getters - функции, которые возвращают данные из state
import * as getters from './store/getters'
//mutations - функции изменения данных в state
import * as mutations from './store/mutations'
//actions - функции для доступа к mutations
import * as actions from './store/actions'
//Специальный плагин, который позволяет сохранять состояние в storage браузера,
// если его не использовать, то после обновления страницы хранилище данных очистится
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)
const store = new Vuex.Store({
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
    plugins: [createPersistedState()],
})

//Поддержка мультиязычности
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)
//Для добавления новых переводов необходимо создать файл с переводами на других языках
//и поменять store.state.lang
import ru from './i18n/ru.js'
import en from './i18n/en.js'

const messages = {
  ru,
  en,
}

const i18n = new VueI18n({
    locale: store.state.lang,
    messages,
})
Vue.config.lang = 'ru';

// Подключение валидатора 
import Vuelidate from 'vuelidate' 
Vue.use(Vuelidate) 

//Делает заглавной первую букву первого слова в строке
Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

//Делает заглавной первую букву каждого слова в строке
Vue.filter('capitalizeAll', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.replace(/(?:^|\s)\S/g, function(a) { return a.toUpperCase(); });
})

new Vue({
    i18n,
    router: router,
    store: store,
    render: h => h(App),
}).$mount('#app')
