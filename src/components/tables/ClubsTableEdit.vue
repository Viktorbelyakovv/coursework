<template>
  <q-dialog v-model="showDlg" persistent @show="onShow()">
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    /> 
    <q-card> 
      <q-card-section class="bg-primary text-white">
        {{ mode=='add'?$t('labels.add'):$t('labels.edit') }}
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-select :label="$t('labels.name')+' *'" stack-label v-model="form.name" dense :options="options" :error="$v.form.name.$error"/>
        <q-input :label="$t('labels.fio') +' *'" stack-label v-model="form.fio" dense :error="$v.form.fio.$error"/>
        <q-input :label="$t('labels.year') +' *'" stack-label v-model="form.year" dense type="number" :error="$v.form.year.$error"/>
        <q-input v-if="mode == 'edit'" :label="$t('labels.currentPhoto')" readonly dense style="width: 500px" stack-label v-model="form.currentPhoto"/>
        <q-checkbox v-if="mode == 'edit'&this.form.currentPhoto != null" v-model="isDelete" :label="$t('labels.deleteCurrentPhoto')" />
        <q-uploader 
          :label="mode == 'add'?$t('labels.photo'):$t('labels.newPhoto')"
          stack-label 
          send-raw
          style="max-width: 400px"
          max-files="1"
          accept=".jpg, .png, image/*"
          @rejected="onRejected"
          @added="addImage"
          dense
        >
          <template v-slot:header="scope">
          <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
            <q-btn v-if="scope.uploadedFiles.length > 0" icon="done_all" @click="scope.removeUploadedFiles" round dense flat >
              <q-tooltip>{{$t('labels.deletePhoto') }}</q-tooltip>
            </q-btn>
            <q-spinner v-if="loading" class="q-uploader__spinner" />
            <div class="col">
              <div class="q-uploader__title">{{ mode == 'add'?$t('labels.photo'):$t('labels.newPhoto') }}</div>
            </div>
            <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" round dense flat>
              <q-uploader-add-trigger />
              <q-tooltip>{{$t('labels.addPhoto') }}</q-tooltip>
            </q-btn>
          </div>
        </template>
      </q-uploader>
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
import { required, maxLength, minValue, maxValue } from 'vuelidate/lib/validators'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../../mixins/ErrorDisplayMixin.js'

export default {
  data () {
    return {
      form: {
        name: '',
        fio: '',
        year: '',
        currentPhoto: null,
        newPhoto: null,
      },
      //Флаг удаления текущего фото
      isDelete: false,
      // Флаг процесса загрузки
      loading: false,
    }
  },
  // Миксин для вывода сообщения об ошибке
  mixins: [ErrorDisplayMixin],
  validations: {
    form: {
      name: { required, maxLength: maxLength(20) },
      fio: { required, maxLength: maxLength(50) },
      year: { required, minValue: minValue(1900), maxValue: maxValue(2021)},
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
      this.isDelete = false
      // Если режим добавления, тогда очищаем все поля
      if (this.mode == 'add') {
        this.form.name = ''
        this.form.fio = ''
        this.form.year = ''
      } else {
        // Если режим редактирования, то делаем запрос через API, чтобы загрузить все значения для редактируемой записи
        axios.get(`http://localhost:8000/api/clubs_table/${this.id}`, {
          headers: {
            'Content-Type': 'application/json',
          }
        }).then (({ data }) => {
          this.form.name = data.name
          this.form.fio = data.fio
          this.form.year = data.year
          this.form.currentPhoto = data.photo
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error.response.status)
          switch (error.response.status) {
            case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
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
        if (this.$v.form.fio.$error) { 
          if (!this.$v.form.fio.required) this.DisplayError('errors.empty')
          if (!this.$v.form.fio.maxLength) this.DisplayError('errors.max_length50')
          return
        }
        if (this.$v.form.year.$error) { 
          if (!this.$v.form.year.required) {
            this.DisplayError('errors.empty')
            return
          }
          else {
            if (!this.$v.form.year.minValue) this.DisplayError('errors.min_value')
            if (!this.$v.form.year.maxValue) this.DisplayError('errors.max_value')
            return
          }            
        }
        return
      }
      let formData = new FormData();
      formData.append('name', this.form.name);
      formData.append('fio', this.form.fio);
      formData.append('year', this.form.year);
      if (this.isDelete) {
        formData.append('photo', '')
      }        
      else {
        formData.append('photo', this.form.newPhoto); 
      }
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      // Ставим флаг процесса загрузки в значение true
      this.loading = true
      // Если режим добавления, то используем метод POST для добавления новой записи
      if (this.mode == 'add') {
        axios.post(`http://localhost:8000/api/clubs_table`,  formData, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
          this.loading = false
          this.$q.notify({ message: this.$t('success.add'), type: 'positive', icon: 'thumb_up' })
          this.closeDlg()
        }).catch((e) => {
          // eslint-disable-next-line
          console.log(e.response.data)
          switch (e.response.status) {
            case 500: this.DisplayError('errors.club_exists'); break
            case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
            default: this.DisplayError('errors.add'); break
          }
          this.loading = false
        })
      } else {
        // Если режим редактирования, то используем метод PUT с указанием текущего id записи
        axios.put(`http://localhost:8000/api/clubs_table/${this.id}`,  formData, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
          this.loading = false
          this.$q.notify({ message: this.$t('success.edit'), type: 'positive', icon: 'thumb_up' })
          this.closeDlg()
        }).catch((e) => {
          // eslint-disable-next-line
          console.log(e.response.data)
          switch (e.response.status) {
            case 500: this.DisplayError('errors.club_exists'); break
            case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
            default: this.DisplayError('errors.edit'); break
          }
          this.loading = false
        })
      }
    },
    // Функция закрытия диалогового окна
    closeDlg:function()
    {
      // Формирует событие closeClubsLibEdit, которое отслеживает родительский компонент, вызвавший это окно
      this.$emit('closeClubsTableEdit');
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      })
    },
    addImage (files) {
      this.form.newPhoto = files[0]
    },
  },
}
</script>

<style>
</style>