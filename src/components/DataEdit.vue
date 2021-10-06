<template>
    <q-dialog v-model="showDataEdit" persistent @show="onShow()">
        <!--Собственный компонент для вывода ошибки -->
        <ErrorDisplay 
        :showErrorDisplay="ErrorDisplay"
        :message="message"
        @closeErrorDisplay="ErrorDisplay = false; refresh()"
        />
        <q-card>
            <q-card-section>
                <div class="text-h6">{{$t('profile.edit')}}</div>
            </q-card-section>
            <q-card-section class="q-pt-none">
                <q-input 
                    :label="$t('profile.username')" stack-label 
                    v-model="form.username" 
                    :error="$v.form.username.$error" 
                    style="text-align:left;" 
                />
                <q-input 
                    :label="$t('profile.email')" stack-label 
                    v-model="form.email" 
                    :error="$v.form.email.$error" 
                    style="text-align:left;" 
                /> 
                <q-input 
                    :label="$t('profile.surname')" stack-label 
                    v-model="form.surname" 
                    :error="$v.form.surname.$error" 
                    style="text-align:left;" 
                /> 
                <q-input 
                    :label="$t('profile.first_name')" stack-label 
                    v-model="form.first_name" 
                    :error="$v.form.first_name.$error" 
                    style="text-align:left;" 
                /> 
                <q-input 
                    :label="$t('profile.patronymic')" stack-label 
                    v-model="form.patronymic" 
                    :error="$v.form.patronymic.$error" 
                    style="text-align:left;" 
                />
                <q-input
                    :label="$t('profile.password')" stack-label 
                    :placeholder="$t('profile.confirm')" 
                    type="password" 
                    v-model="form.password" 
                    :error="$v.form.password.$error"
                    @keyup.enter="submit" 
                    style="text-align:left;" 
                />                
            </q-card-section>
            <q-card-actions align="right">
                <q-btn :label="$t('buttons.cancel')"  color="primary" @click="closeDataEdit"/>
                <q-btn :label="$t('buttons.submitChange')" color="primary" @click="submit" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
// Подключение билиотеки axios для работы с API
import axios from 'axios'
// Подключение getters из хранилища данных 
import { mapGetters, mapActions } from 'vuex'
// Подключение методов валидации
import { required, email, minLength, maxLength } from 'vuelidate/lib/validators'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../mixins/ErrorDisplayMixin.js'

export default {  
    data () {
        return {
            form: { 
                username: '', 
                email: '',
                surname: '',
                first_name: '',                
                patronymic: '', 
                password: '',  
            },
        }
    },
    // Миксин для вывода сообщения об ошибке
    mixins: [ErrorDisplayMixin],

    validations: { 
        form: { 
            username: { required, maxLength: maxLength(30) }, 
            email: { required, email, maxLength: maxLength(30) }, 
            surname: { maxLength: maxLength(30) }, 
            first_name: { maxLength: maxLength(30) },                 
            patronymic: { maxLength: maxLength(30) }, 
            password: { required, minLength: minLength(6) }, 
        }
    },
    // Свойства, которые передаются из родительского компонента при его вызове
    props: {
        // Флаг видимости компонента
        showDataEdit: null,
    },
    computed: {
    ...mapGetters(['getToken', 'getAuth', 'getUsername'])
    },
    // Метод получения токена из хранилища данных 
    methods:{
        ...mapActions({ 
            setToken: 'setToken',
            setAuth: 'setAuth', 
            setUsername: 'setUsername', 
        }),
        onShow:function() {
            // Сброс ошибок валидации для всех полей формы 
            this.$v.form.$reset()
            this.form.password = '' 
            axios.get('http://localhost:8000/api/user/profile', {
                params: {
                    user : this.$store.getters.getUsername
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
            .catch(() => { 
                this.DisplayError('errors.error')
            })
        },
        submit () {
            this.$v.form.$touch() 
            // Валидация полей формы 
            if (this.$v.form.$error) 
            { 
                if (this.$v.form.username.$error) { 
                    if (!this.$v.form.username.required) this.DisplayError('errors.empty_username')
                    if (!this.$v.form.username.maxLength) this.DisplayError('errors.max_length')
                    return
                } 
                if (this.$v.form.email.$error) { 
                    if (!this.$v.form.email.required) this.DisplayError('errors.empty_email')
                    if (!this.$v.form.email.email) this.DisplayError('errors.uncorrect_email')
                    if (!this.$v.form.email.maxLength) this.DisplayError('errors.max_length') 
                    return
                }             
                if (this.$v.form.surname.$error) { 
                    if (!this.$v.form.surname.maxLength) this.DisplayError('errors.max_length')
                    return
                } 
                if (this.$v.form.first_name.$error) { 
                    if (!this.$v.form.first_name.maxLength) this.DisplayError('errors.max_length')
                    return
                } 
                if (this.$v.form.patronymic.$error) { 
                    if (!this.$v.form.patronymic.maxLength) this.DisplayError('errors.max_length')
                    return
                }
                if (this.$v.form.password.$error) { 
                    if (!this.$v.form.password.required) this.DisplayError('errors.empty_password')
                    if (!this.$v.form.password.minLength) this.DisplayError('errors.short_password')
                    return
                } 
                return 
            }
            var request = { 
                username: this.getUsername,//старый логин
                username2: this.form.username, //в случае изменения новый логин
                email: this.form.email,
                surname: this.form.surname,
                first_name: this.form.first_name,
                patronymic: this.form.patronymic,
                password: this.form.password, 
            } 
            const requestStr = JSON.stringify(request) 
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            // Запрос на изменение данных пользователя
            axios.patch('http://localhost:8000/api/user/editdata', requestStr, { 
                headers: { 
                'Content-Type': 'application/json' 
                } 
            }) 
            .then(() => {            
                if (this.getUsername != this.form.username) { //в случае смены логина
                    var request2 = { 
                        username: this.form.username, 
                        password: this.form.password 
                    } 
                    const requestStr2 = JSON.stringify(request2) 
                    // Запрос через метод POST, который в случае успеха вернет токен авторизации 
                    axios.post('http://localhost:8000/api/token/', requestStr2, { 
                        headers: { 
                            'Content-Type': "application/json"
                        } 
                    }).then((response) => { 
                        // Вызов методов actions для записи в хранилище токена, имени пользователя и признака авторизации 
                        this.setToken(response.data.token) 
                        this.setAuth() 
                        this.setUsername(this.form.username)                         
                    }).catch(() => {                         
                    })
                }
                this.$q.notify({ message: this.$t('profile.success'), type: 'positive', icon: 'thumb_up' }) 
                this.closeDataEdit()        
            }) 
            .catch((error) => { 
             // eslint-disable-next-line 
                console.log(error.response.status)
                switch (error.response.status) { 
                    case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                    case 403: this.DisplayError('errors.uncorrect_password'); break
                    default: this.DisplayError('errors.error'); break 
                }
            })
        },
        // Функция закрытия диалогового окна
        closeDataEdit:function()
        {
        // Формирует событие closeDataEdit, которое отслеживает родительский компонент, вызвавший это окно
        this.$emit('closeDataEdit');
        }
    }
}
</script>