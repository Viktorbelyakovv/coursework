<template> 
	<q-page padding class="docs-input row justify-center divimage">  
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    /> 
		<div class="reg shadow-10">
			<div class = "q-ma-md" align = "center"> 
        <p align = "center">{{$t('reg.title')}}</p>
				<q-input dense
          :placeholder="$t('enter.username')" 
          v-model="form.username" 
          :error="$v.form.username.$error" 
          style="text-align:left;" 
        />
				<q-input dense
          :placeholder="$t('enter.email')" 
          v-model="form.email" 
          :error="$v.form.email.$error" 
          style="text-align:left;" 
        /> 
        <q-input dense
          :placeholder="$t('enter.surname')" 
          v-model="form.surname" 
          :error="$v.form.surname.$error" 
          style="text-align:left;" 
        /> 
        <q-input dense
          :placeholder="$t('enter.first_name')" 
          v-model="form.first_name" 
          :error="$v.form.first_name.$error" 
          style="text-align:left;" 
        /> 
        <q-input dense
          :placeholder="$t('enter.patronymic')" 
          v-model="form.patronymic" 
          :error="$v.form.patronymic.$error" 
          style="text-align:left;" 
        /> 
        <q-input dense
          :placeholder="$t('enter.password')" 
          type="password" 
          v-model="form.password" 
          :error="$v.form.password.$error"
          style="text-align:left;" 
        /> 
        <q-input dense
          :placeholder="$t('enter.password_confirm')" 
          type="password" 
          v-model="form.password_confirm" 
          :error="$v.form.password_confirm.$error" 
          @keyup.enter="submit" 
          style="text-align:left;" 
        /> 
        <div align = "left">{{ $t('enter.required') }} </div><br>
        <q-btn color="primary" class = "q-mt-md" @click="submit" :label="$t('buttons.registration')"/>
			</div>
		</div> 
	</q-page>
</template>

<script>
import { QInput } from 'quasar' 
// Подключение методов валидации 
import { required, email, sameAs, minLength, maxLength } from 'vuelidate/lib/validators' 
// Подключение билиотеки axios для работы с API 
import axios from 'axios' 
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../mixins/ErrorDisplayMixin.js'

export default {
	components: { QInput},
	data() {
		return {
			form: { 
        username: '', 
        email: '',
        surname: '',
        first_name: '',                
        patronymic: '', 
        password: '', 
        password_confirm: '' 
      } 
		}
	},
  // Миксин показа ошибки
  mixins: [ErrorDisplayMixin],
  validations: { 
    form: { 
      username: { required, maxLength: maxLength(30) }, 
      email: { required, email, maxLength: maxLength(30) }, 
      surname: { maxLength: maxLength(30) }, 
      first_name: { maxLength: maxLength(30) },                 
      patronymic: { maxLength: maxLength(30) }, 
      password: { required, minLength: minLength(6) }, 
      password_confirm: { sameAsPassword:sameAs('password') } 
    } 
  }, 
	methods: {
		submit () {
      this.$v.form.$touch() 
      if (this.$v.form.$error) 
      { 
        if (this.$v.form.username.$error) { 
          if (!this.$v.form.username.required) this.DisplayError('errors.empty_username')
          if (!this.$v.form.username.maxLength) this.DisplayError('errors.max_length30')
          return 
        } 
        if (this.$v.form.email.$error) { 
          if (!this.$v.form.email.required) this.DisplayError('errors.empty_email')
          if (!this.$v.form.email.email) this.DisplayError('errors.uncorrect_email')
          if (!this.$v.form.email.maxLength) this.DisplayError('errors.max_length30')
          return 
        }             
        if (this.$v.form.surname.$error) { 
          if (!this.$v.form.surname.maxLength) this.DisplayError('errors.max_length30') 
          return
        } 
        if (this.$v.form.first_name.$error) { 
          if (!this.$v.form.first_name.maxLength) this.DisplayError('errors.max_length30')
          return
        } 
        if (this.$v.form.patronymic.$error) { 
          if (!this.$v.form.patronymic.maxLength) this.DisplayError('errors.max_length30')  
          return
        } 
        if (this.$v.form.password.$error) { 
          if (!this.$v.form.password.required) this.DisplayError('errors.empty_password')
          if (!this.$v.form.password.minLength) this.DisplayError('errors.short_password')
          return
        } 
        if (this.$v.form.password_confirm.$error) { 
          if (!this.$v.form.password_confirm.sameAs) this.DisplayError('errors.password_not_match')
          return
        } 
        return 
      } 
      var request = { 
        username: this.form.username, 
        email: this.form.email,
        surname: this.form.surname,
        first_name: this.form.first_name,
        patronymic: this.form.patronymic,
        password: this.form.password, 
      } 

      const requestStr = JSON.stringify(request) 
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"; 
      axios.post('http://localhost:8000/api/user/reguser', requestStr, { 
        headers: { 
          'Content-Type': 'application/json' 
        } 
      }) 
      .then(() => { 
        this.$q.notify({ message: this.$t('success.registration'), type: 'positive', icon: 'thumb_up' })  
        this.$router.push('/auth')
        this.$router.go('/auth')
      }) 
      .catch((error) => { 
        // eslint-disable-next-line 
        console.log(error.response.status) 
        switch (error.response.status) { 
          case 304: this.DisplayError('errors.user_exists'); break 
          default: this.DisplayError('errors.error'); break 
        } 
      }) 
    }
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

.reg{
  background-color: white;
  opacity: 80%;
  border: 1px solid gray;
  width: 500px; 
  height: 600px;
  border-radius: 1px;
  position: absolute;    
  font-size: 18px;
}
</style>