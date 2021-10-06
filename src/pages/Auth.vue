<template>
  <q-page padding class="docs-input row justify-center divimage">
      <!--Собственный компонент для вывода ошибки -->
      <ErrorDisplay 
        :showErrorDisplay="ErrorDisplay"
        :message="message"
        @closeErrorDisplay="ErrorDisplay = false; refresh()"
      />
      <div class="auth shadow-10">
      <div class = "q-ma-md" align = "center">
        <p class="caption" align = "center">{{$t('auth.title')}}</p>
        <q-input 
          :placeholder="$t('enter.username')" 
          v-model="form.username" 
          :error="$v.form.username.$error" 
          style="text-align:left;" 
        /> 
				<q-input 
          :placeholder="$t('enter.password')" 
          type="password" 
          v-model="form.password" 
          :error="$v.form.password.$error" 
          @keyup.enter="submit" 
          style="text-align:left;" 
        />
        <div align = "left">{{ $t('enter.required') }} </div><br>
				<q-btn color="primary" class = "q-mt-md" @click="submit" :label="$t('buttons.submit')"/>
				<div class="q-mt-md">{{ $t('auth.no_account') }}<a href="#" @click="$router.push('/reg')">{{ $t('auth.reg') }}</a></div>   
      </div>
    </div>
  </q-page>
</template>


<script>
// Подключение билиотеки axios для работы с API 
import axios from 'axios' 
// Подключение методов валидации 
import { required, minLength, maxLength } from 'vuelidate/lib/validators' 
// Импорт компонента ввода данных 
import { QInput } from 'quasar' 
// Импорт Actions из хранилища данных vuex 
import { mapActions } from 'vuex' 
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../mixins/ErrorDisplayMixin.js'

export default {
  data() {
		return {
			// Данные формы авторизации 
      form: { 
        username: '', 
        password: '' 
      }
		}
	},
  // Экспорт всех используемых в шаблоне компонентов
  components: {QInput},
  // Миксин показа ошибки
  mixins: [ErrorDisplayMixin],
  //Валидаторы
  validations: { 
    form: { 
      username: { required, maxLength: maxLength(30) }, 
      password: { required, minLength: minLength(6), maxLength: maxLength(30) }, 
    } 
  },
  methods: {
  // Методы для работы с хранилищем данных vuex 
    ...mapActions({ 
      setToken: 'setToken',
      setAuth: 'setAuth', 
      setUsername: 'setUsername' 
    }),
    submit () { 
      this.$v.form.$touch() 
      // Валидация поля username 
      if (this.$v.form.username.$error) { 
        if (!this.$v.form.username.required) this.DisplayError('errors.empty_username')
        if (!this.$v.form.username.maxLength) this.DisplayError('errors.max_length30')
        return 
      } 
      // Валидация поля password 
      if (!this.$v.form.password.required) {
        if (!this.$v.form.password.required) this.DisplayError('errors.empty_password')
        if (!this.$v.form.password.minLength) this.DisplayError('errors.short_password')
        if (!this.$v.form.password.maxLength) this.DisplayError('errors.max_length30')
        return 
      } 
      // Формирование запроса к API 
      var request = { 
          username: this.form.username, 
          password: this.form.password 
      } 
      const requestStr = JSON.stringify(request) 
      // Запрос через метод POST, который в случае успеха вернет токен авторизации 
      axios.post('http://localhost:8000/api/token/', requestStr, { 
          headers: { 
              'Content-Type': "application/json"
          } 
      }).then((response) => { 
          this.$q.notify({ message: this.$t('reg.notify.entered'), type: 'positive', icon: 'thumb_up' }) 
          // Вызов методов actions для записи в хранилище токена, имени пользователя и признака авторизации 
          this.setToken(response.data.token) 
          this.setAuth() 
          this.setUsername(this.form.username) 
          // Переадресация на страницу list 
          this.$router.push('/profile'); 
          this.$router.go('/profile'); 
      }).catch((error) => { 
          // eslint-disable-next-line 
          console.log(error.response.status)
          this.DisplayError('auth.notify.password')
      }) 
    },
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

.auth{
    background-color: white;
    opacity: 80%;
    border: 1px solid gray;
    width: 500px; 
    height: 390px;
    border-radius: 5px;
    position: absolute;
    top: 15%;
    font-size: 18px;    
}
</style>