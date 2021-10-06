<template>  
  <q-dialog v-model="showDlg" persistent @show="onShow()"> 
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    />
    <q-card > 
      <q-card-section class="bg-primary text-white">
        {{ mode=='add'?$t('labels.add'):$t('labels.edit') }}
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input :label="$t('labels.name') +' *'" stack-label v-model="form.name" :error="$v.form.name.$error"/>
        <q-select :label="$t('labels.division')+' *'" stack-label v-model="form.division" :options="options" :error="$v.form.division.$error"/>
        <div align = "left">{{ $t('enter.required') }} </div><br>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn :label="$t('buttons.cancel')"  @click="closeDlg" class = "q-mr-sm"/>
        <q-btn :label="mode == 'add'?$t('buttons.add'):$t('buttons.edit')" @click="submit" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
// Подключение билиотеки axios для работы с API
import axios from 'axios'
// Подключение getters из хранилища данных 
import { mapGetters } from 'vuex'
// Подключение методов валидации
import { required, maxLength } from 'vuelidate/lib/validators'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../../mixins/ErrorDisplayMixin.js'

export default {
  data () {
    return {
      form: {
        name: '',
        division: '',
      },
    }
  },
  // Миксин для вывода сообщения об ошибке
  mixins: [ErrorDisplayMixin],
  
  validations: {
    form: {
      name: { required, maxLength: maxLength(20) },
      division: { required },
    }
  },
  // Свойства, которые передаются из родительского компонента при его вызове
  props: {
    // Флаг видимости компонента
    showDlg: null,
    // Режим работы компонента (add или edit)
    mode: null,
    // Заголовок диалогового окна
    title: null,
    // id записи (используется только в режиме редактирования для хранения текущего id)
    id: null,
    // список дивизионов
    options: null,
  },
  // Метод получения токена из хранилища данных 
  computed: {
    ...mapGetters(['getToken'])
  },
  methods:{
    onShow:function() {
      // Сброс ошибок валидации для всех полей формы 
      this.$v.form.$reset()
      // Если режим добавления, тогда очищаем все поля
      if (this.mode == 'add') {
        this.form.name = ''
        this.form.division = ''
      } else {
        // Если режим редактирования, то делаем запрос через API, чтобы загрузить все значения для редактируемой записи
        axios.get(`http://localhost:8000/api/clubs_lib/${this.id}`, {
          headers: {
            'Content-Type': 'application/json',
          }
        }).then (({ data }) => {
          this.form.name = data.name
          this.form.division = data.division
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error.response.status)
          switch (error.response.status) {
            default: this.DisplayError('errors.error'); break
          }
        })
      }
    },
    // Обработчик кнопки "Добавить/Редактировать"
    submit () {
      this.$v.form.$touch()
      // Валидация всех полей
      if (this.$v.form.$error)
      {
        if (this.$v.form.name.$error) { 
          if (!this.$v.form.name.required) this.DisplayError('errors.empty')
          if (!this.$v.form.name.maxLength) this.DisplayError('errors.max_length20')
          return
        }
        if (this.$v.form.division.$error) { 
          if (!this.$v.form.division.required) this.DisplayError('errors.empty')
          return
        }
        return
      }
      // Формирование запроса
      var request = {
        name: this.form.name,
        division: this.form.division,
      }
      const requestStr = JSON.stringify(request)
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      // Если режим добавления, то используем метод POST для добавления новой записи
      if (this.mode == 'add') {
        axios.post(`http://localhost:8000/api/clubs_lib`,  requestStr, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
            this.$q.notify({ message: this.$t('success.add'), type: 'positive', icon: 'thumb_up' })
            this.closeDlg()
        }).catch((e) => {
            // eslint-disable-next-line
            console.log(e.response.data)
            switch (e.response.status) {
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.add'); break
            }
        })
      } else {
        // Если режим редактирования, то используем метод PUT с указанием текущего id записи
        axios.put(`http://localhost:8000/api/clubs_lib/${this.id}`,  requestStr, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
            this.$q.notify({ message: this.$t('success.edit'), type: 'positive', icon: 'thumb_up' })
            this.closeDlg()
        }).catch((e) => {
            // eslint-disable-next-line
            console.log(e.response.data)
            switch (e.response.status) {
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.edit'); break
            }
        })
      }
    },
    // Функция закрытия диалогового окна
    closeDlg:function()
    {
      // Формирует событие closeClubsLibEdit, которое отслеживает родительский компонент, вызвавший это окно
      this.$emit('closeClubsLibEdit');
    }
  },
}
</script>

<style>
</style>