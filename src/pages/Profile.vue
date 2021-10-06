<template>
  <q-page padding class="docs-input row justify-center divimage">
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    />
    <div v-if="getAuth" class="profile shadow-10">
      <div class="q-ma-md"  align = "center"> 
        <div class="title">{{$t('profile.title')}} </div>
        <div class="subtitle" >{{$t('profile.data')}} </div>
        <q-field :label="$t('profile.username')" dense stack-label>
          <template v-slot:control>
            <div class="data">{{form.username}}</div>
          </template>      
        </q-field>
        <q-field :label="$t('profile.email')" dense stack-label>
          <template v-slot:control>
            <div class="data">{{form.email}}</div>
          </template>         
        </q-field>
        <q-field :label="$t('profile.surname')" dense stack-label>
          <template v-slot:control>
            <div class="data">{{form.surname | capitalize}}</div>
          </template>           
        </q-field>
        <q-field :label="$t('profile.first_name')" dense stack-label>
          <template v-slot:control>            
            <div class="data">{{form.first_name | capitalize}}</div>
          </template>
        </q-field>
        <q-field :label="$t('profile.patronymic')" dense stack-label>
          <template v-slot:control>
            <div class="data">{{form.patronymic | capitalize}}</div>
          </template>
        </q-field>
        <!-- Диалог для редактирования данных пользователя-->
        <DataEdit 
          :showDataEdit="DataEdit"
          @closeDataEdit="DataEdit = false; refresh()"
        />
        <q-btn style="background: darkblue; color: white" :label="$t('profile.edit')" @click="DataEdit = true" />
        <!-- Диалог для редактирования пароля-->
        <PasswordEdit 
          :showPasswordEdit="PasswordEdit"
          @closePasswordEdit="PasswordEdit = false; refresh()"
        />
        <br><br><q-btn style="background: darkblue; color: white" :label="$t('profile.change_password.title')" @click="PasswordEdit = true" />
  
        <div class="subtitle">{{$t('profile.settings')}}</div>
          <q-input v-model="rows" :label="$t('profile.rows')" type="number" style="width: 500px" dense :error="$v.rows.$error"> 
            <template v-slot:append>
              <q-btn style="background: darkblue; color: white" :label="$t('buttons.submit')" @click="editRows" />
            </template>            
          </q-input>  
          <q-input v-model="autoUpdate" :label="$t('profile.auto_update')" type="number" style="width: 500px" dense :error="$v.autoUpdate.$error"> 
            <template v-slot:append>
              <q-btn style="background: darkblue; color: white" :label="$t('buttons.submit')" @click="editAutoUpdate" />
            </template>            
          </q-input>   
        <q-btn-dropdown style="background: darkblue; color: white" :label="$t('profile.lang.title')">
          <q-list>
            <q-item :clickable="this.getLang() !='ru'" :active="this.getLang()=='ru'" v-close-popup @click="setLang('ru')">
              <q-item-section>
                <q-item-label>{{$t('profile.lang.ru')}}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item :clickable="this.getLang() !='en'" :active="this.getLang()=='en'" v-close-popup @click="setLang('en')">
              <q-item-section>
                <q-item-label>{{$t('profile.lang.en')}}</q-item-label>
              </q-item-section>
            </q-item>  
          </q-list>
        </q-btn-dropdown>
      </div>
    </div>
  </q-page>
</template>

<script>
// Подключение билиотеки axios для работы с API 
import axios from 'axios' 
// Импорт Getters, Actions из хранилища данных vuex 
import { mapGetters, mapActions } from 'vuex'
// Подключение методов валидации 
import { required, minValue } from 'vuelidate/lib/validators'
// Подключение компонента для редактирования данных
import DataEdit from '../components/DataEdit.vue'
// Подключение компонента для редактирования пароля
import PasswordEdit from '../components/PasswordEdit.vue'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../mixins/ErrorDisplayMixin.js'
// Подключение миксина для проверки действительности токена
import TokenMixin from '../mixins/TokenMixin.js'

export default {  
  data () {
    return {      
      form: { 
        username: '', 
        email: '',
        surname: '',
        first_name: '',                
        patronymic: '', 
      },
      DataEdit: false,
      PasswordEdit: false,
      rows: '',
      autoUpdate: '',
    }
  },
  // Экспорт всех используемых в шаблоне компонентов
  components: { DataEdit, PasswordEdit},
  // Подключаемые миксины
  mixins: [ErrorDisplayMixin, TokenMixin],
  // Описание параметров валидации для полей формы 
  validations: { 
    rows: {required, minValue:minValue(0)},
    autoUpdate: {required, minValue:minValue(1)},
  },
  computed: {
    ...mapGetters(['getToken', 'getAuth', 'getUsername'])
  },
  methods: {
    ...mapGetters({  
    getLang: 'getLang', 
    getRows: 'getRows', 
    getAutoUpdate: 'getAutoUpdate', 
    }),
    ...mapActions({ 
      setToken: 'setToken',
      setAuth: 'setAuth', 
      setUsername: 'setUsername', 
      setLang: 'setLang',
      setRows: 'setRows',
      setAutoUpdate: 'setAutoUpdate', 
    }),
    editRows(){
      this.$v.rows.$touch() 
      // Валидация полей формы 
      if (this.$v.rows.$error) 
      {
        if (!this.$v.rows.required) this.DisplayError('errors.empty') 
        if (!this.$v.rows.minValue) this.DisplayError('errors.not_negative')   
        return 
      }
      this.setRows(this.rows)
      this.rows = this.getRows()
      this.$q.notify({ message: this.$t('success.rows_per_page'), type: 'positive', icon: 'thumb_up' })
    },
    editAutoUpdate(){
      this.$v.autoUpdate.$touch() 
      // Валидация полей формы 
      if (this.$v.autoUpdate.$error) 
      {
        if (!this.$v.autoUpdate.required) this.DisplayError('errors.empty') 
        if (!this.$v.autoUpdate.minValue) this.DisplayError('errors.positive')  
        return 
      }
      this.setAutoUpdate(this.autoUpdate)
      this.autoUpdate = this.getAutoUpdate()
      this.$q.notify({ message: this.$t('success.auto_update'), type: 'positive', icon: 'thumb_up' })
    },
    setLang(locale) {
      this.$store.dispatch('setLang', locale);
      this.$i18n.locale = locale;
    },
    // Функция обновления данных на странице
    refresh: function() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      axios.get('http://localhost:8000/api/user/profile', {
        params: {
          user : this.getUsername
        },
        headers: { 
          'Content-Type': 'application/json',
        }
      })
      .then(({ data }) => {
        this.form.username = data.username 
        this.form.email = data.email 
        this.form.surname = data.surname 
        this.form.first_name = data.first_name 
        this.form.patronymic = data.patronymic 
      }) 
      .catch((e) => {
        // eslint-disable-next-line
        //console.log(e.response.data)
        switch (e.response.status) {
          case 401: this.$router.push('/auth'); this.$router.go('/auth');  break
          //default: this.DisplayError('errors.error'); break
        }
      })
      this.rows = this.getRows()
      this.autoUpdate = this.getAutoUpdate()
    },    
  },
  mounted () {
    this.checkToken() 
    this.refresh()
    this.interval = window.setInterval(() => {    
      this.refreshToken()   
      this.checkToken()      
      this.refresh()      
    }, 10000)
  }
}
</script>

<style scoped>
.divimage{
    background-image: url('../assets/background.jpeg');
    background-repeat: repeat-y; 
    background-repeat: repeat-x; 
    background-size: 100%;
}

.profile{
    background-color: white;
    opacity: 80%;
    border: 1px solid gray;
    width: 550px; 
    border-radius: 5px;
    position: absolute;
    top: 5%;        
}

.title{
  font-size: 30px;
}

.subtitle{
  font-size: 20px;
}

.data{
  font-size: 20px;
}
</style>