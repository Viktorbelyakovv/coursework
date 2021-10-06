<template>
    <q-dialog v-model="showPasswordEdit" persistent @show="onShow()">
        <!--Собственный компонент для вывода ошибки -->
        <ErrorDisplay 
        :showErrorDisplay="ErrorDisplay"
        :message="message"
        @closeErrorDisplay="ErrorDisplay = false; refresh()"
        />
        <q-card>
            <q-card-section>
                <div class="text-h6">{{$t('profile.change_password.title')}}</div>
            </q-card-section>
            <q-card-section class="q-pt-none">
                <q-input
                    :label="$t('profile.change_password.current')" stack-label 
                    type="password" 
                    v-model="form.passwordold" 
                    :error="$v.form.passwordold.$error"
                    style="text-align:left;" 
                />
                <q-input
                    :label="$t('profile.change_password.new')" stack-label 
                    type="password" 
                    v-model="form.password" 
                    :error="$v.form.password.$error"
                    style="text-align:left;" 
                />                 
                <q-input
                    :label="$t('profile.change_password.new_again')" stack-label 
                    type="password" 
                    v-model="form.password_confirm" 
                    :error="$v.form.password_confirm.$error" 
                    @keyup.enter="submit" 
                    style="text-align:left;" 
                /> 
            </q-card-section>
            <q-card-actions align="right">
                <q-btn :label="$t('buttons.cancel')"  color="primary" @click="closePasswordEdit"/>
                <q-btn :label="$t('buttons.submit')" color="primary" @click="submit" />
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
import { required, sameAs, minLength } from 'vuelidate/lib/validators'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../mixins/ErrorDisplayMixin.js'

export default {  
    data () {
        return {
            form: { 
                passwordold: '',
                password: '', 
                password_confirm: ''  
            },
        }
    },
    // Миксин для вывода сообщения об ошибке
    mixins: [ErrorDisplayMixin],
    
    validations: { 
        form: { 
            passwordold: { required, minLength: minLength(6) },
            password: { required, minLength: minLength(6) }, 
            password_confirm: { sameAsPassword:sameAs('password') } 
        }
    },
    // Свойства, которые передаются из родительского компонента при его вызове
    props: {
        // Флаг видимости компонента
        showPasswordEdit: null,
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
            this.form.passwordold = '' 
            this.form.password = '' 
            this.form.password_confirm = '' 
        },
        submit (){
            this.$v.form.$touch() 
            // Валидация полей формы 
            if (this.$v.form.$error) 
            {
                if (this.$v.form.passwordold.$error) { 
                    if (!this.$v.form.passwordold.required) this.DisplayError('errors.empty_password')
                    if (!this.$v.form.passwordold.minLength) this.DisplayError('errors.uncorrect_password')
                    return
                }  
                if (this.$v.form.password.$error) { 
                    if (!this.$v.form.password.required) this.DisplayError('errors.empty_password')
                    if (!this.$v.form.password.minLength) this.DisplayError('errors.uncorrect_password')
                    return
                } 
                if (this.$v.form.password_confirm.$error) { 
                    if (!this.$v.form.password_confirm.sameAs) this.DisplayError('errors.password_not_match')
                    return
                } 
                return 
            }
            var request = { 
                username: this.getUsername, 
                passwordold: this.form.passwordold, 
                password: this.form.password, 
            }
            const requestStr = JSON.stringify(request) 
            axios.defaults.xsrfCookieName = 'csrftoken';
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.patch('http://localhost:8000/api/user/editpassword', requestStr, { 
                headers: { 
                'Content-Type': 'application/json' 
                } 
            }) 
            .then(() => { 
                this.$q.notify({ message: this.$t('profile.change_password.success'), type: 'positive', icon: 'thumb_up' })
                this.closePasswordEdit()
            }) 
            .catch((error) => { 
                console.log(error.response.status) 
                switch (error.response.status) { 
                    case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                    case 403: this.DisplayError('errors.uncorrect_password'); break
                    default: this.DisplayError('errors.error'); break 
                } 
            })
        },
        // Функция закрытия диалогового окна
        closePasswordEdit:function()
        {
        // Формирует событие closeDataEdit, которое отслеживает родительский компонент, вызвавший это окно
        this.$emit('closePasswordEdit');
        }
    }
}
</script>