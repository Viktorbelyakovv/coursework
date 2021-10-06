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
        <q-input :label="$t('labels.last_name') +' *'" stack-label v-model="form.last_name" :error="$v.form.last_name.$error"/>
        <q-select :label="$t('labels.club') +' *'" stack-label v-model="form.club" :options="options" :error="$v.form.club.$error"/>
        <q-input :label="$t('labels.pucks_tooltip') +' *'" stack-label v-model="form.pucks" type="number" :error="$v.form.pucks.$error"/>
        <q-input :label="$t('labels.setups_tooltip') +' *'" stack-label v-model="form.setups" type="number" :error="$v.form.setups.$error"/>
        <q-input :label="$t('labels.penalty') +' *'" stack-label v-model="form.penalty" mask="fulltime" :rules="['fulltime']" :error="$v.form.penalty.$error">                
          <template v-slot:append>
            <q-icon name="access_time" class="cursor-pointer">
              <q-popup-proxy transition-show="scale" transition-hide="scale">
                <q-time v-model="form.penalty" with-seconds format24h>
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Close" color="primary" flat />
                  </div>
                </q-time>
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>
        <q-select 
        :label="$t('labels.partners')" 
        stack-label 
        v-model="form.partners"    
        use-input             
        multiple 
        clearable
        :options="optionsForwards"
        input-debounce="0"
        @filter="filterPartners"/>
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
import { required, maxLength, minValue} from 'vuelidate/lib/validators'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../../mixins/ErrorDisplayMixin.js'

export default {
  data () {
    return {
      form: {
        last_name: '',
        club: '',
        pucks: '',
        setups: '',
        penalty: '',
        partners: [],        
      },
      optionsForwards: this.forwards,
      //id для записи в таблицу partners
      idData: 0,
      filterStr: '',
      partnersBeforeEdit: [],
    }
  },
  // Миксин для вывода сообщения об ошибке
  mixins: [ErrorDisplayMixin],

  validations: {
    form: {
      last_name: { required, maxLength: maxLength(50) },
      club: { required},
      pucks: {required, min: minValue(0)},
      setups: {required,min: minValue(0)},
      penalty: {required},
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
    // список нападающих
    forwards: null,
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
        this.form.last_name = ''
        this.form.club = ''
        this.form.pucks = '0'
        this.form.setups = '0'
        this.form.penalty = '00:00:00'
        this.form.partners = []
      } else {
        // Если режим редактирования, то делаем запрос через API, чтобы загрузить все значения для редактируемой записи
        axios.get(`http://localhost:8000/api/forwards_table/${this.id}`, {
          headers: {
            'Content-Type': 'application/json',
          }
        }).then (({ data }) => {
          this.form.last_name = data.last_name
          this.form.club = data.club
          this.form.pucks = data.pucks
          this.form.setups = data.setups
          this.form.penalty = data.penalty
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error.response.status)
          switch (error.response.status) {
            default: this.DisplayError('errors.error'); break
          }
        })
        //Загрузка списка бывших партнёров по звену
        axios.get(`http://localhost:8000/api/partners?last_name=${this.id}`, {
          headers: {
            'Content-Type': 'application/json',
          }
        }).then(({ data }) => {
          var temp = [];
          var auxil = [];
          Object.entries(data).forEach((entry) => {            
            const [key, value] = entry;
            auxil[key] = value["last_name"]
            temp.push(value["partner"])
          });
          this.form.partners = temp
          this.partnersBeforeEdit = temp                              
        })
        .catch (error =>{
          console.log(error.response.data)
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
        if (this.$v.form.last_name.$error) { 
          if (!this.$v.form.last_name.required) this.DisplayError('errors.empty')
          if (!this.$v.form.last_name.maxLength) this.DisplayError('errors.max_length50')
          return
        }
        if (this.$v.form.club.$error) { 
          if (!this.$v.form.club.required) this.DisplayError('errors.empty')
          return
        }
        if (this.$v.form.pucks.$error) { 
          if (!this.$v.form.pucks.required) this.DisplayError('errors.empty')
          if (!this.$v.form.pucks.min) this.DisplayError('errors.not_negative')
          return
        }
        if (this.$v.form.setups.$error) { 
          if (!this.$v.form.setups.required) this.DisplayError('errors.empty')
          if (!this.$v.form.setups.min) this.DisplayError('errors.not_negative')
          return
        }
        if (this.$v.form.penalty.$error) { 
          if (!this.$v.form.penalty.required) this.DisplayError('errors.empty')
          return
        }
        return
      }
      // Формирование запроса
      var request = {
        last_name: this.form.last_name,
        club: this.form.club,
        pucks: this.form.pucks,
        setups: this.form.setups,
        penalty: this.form.penalty,
      }
      const requestStr = JSON.stringify(request)
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      // Если режим добавления, то используем метод POST для добавления новой записи
      if (this.mode == 'add') {
        axios.post('http://localhost:8000/api/forwards_table',  requestStr, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
          this.filterStr += 'limit=1&last_name=' + this.form.last_name
          this.filterStr += '&club__name=' + this.form.club
          if (this.form.pucks != '') this.filterStr += '&pucks=' + this.form.pucks
          if (this.form.setups != '') this.filterStr += '&setups=' + this.form.setups
          if (this.form.penalty != '') this.filterStr += '&penalty=' + this.form.penalty
          axios.get(`http://localhost:8000/api/forwards_table?${this.filterStr}`, {
            headers: {
              'Content-Type': 'application/json',
            }
          }).then(({ data }) => {
            Object.entries(data).forEach((entry) => {                      
              const [key, value] = entry;
              if (key == 0) this.idData = value["id"]
            });
            this.form.partners.forEach((index) => {
              var requestPartners = {
                last_name: this.idData,
                partner: index,
              }
              const requestPartnersStr = JSON.stringify(requestPartners)
              axios.post('http://localhost:8000/api/partners',  requestPartnersStr, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'JWT ' + this.getToken
                }
              }).then(() => {                  
              }).catch((e) => {
                // eslint-disable-next-line
                console.log(e.response.data)
                switch (e.response.status) {
                  case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                  default: this.DisplayError('errors.add'); break
                }
              })              
            })
            this.$q.notify({ message: this.$t('success.add'), type: 'positive', icon: 'thumb_up' })
            this.closeDlg()
          })
          .catch ((e) =>{
            // eslint-disable-next-line
            console.log(e.response.data)
            switch (e.response.status) {
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.add'); break
            }
          })
        }).catch((e) => {
            // eslint-disable-next-line
            console.log(e.response.data)
            switch (e.response.status) {
              case 400: this.DisplayError('errors.unique'); break
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.add'); break
            }
        })
      } else {
        // Если режим редактирования, то используем метод PUT с указанием текущего id записи
        axios.put(`http://localhost:8000/api/forwards_table/${this.id}`,  requestStr, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getToken
          }
        }).then(() => {
          axios.get(`http://localhost:8000/api/partners?last_name=${this.id}`, {
            headers: {
              'Content-Type': 'application/json',
            }
          }).then(({ data }) => {             
            if (data.length == 0) {
              this.form.partners.forEach((index) => {
                var requestPartners = {
                  last_name: this.id,
                  partner: index,
                }
                const requestPartnersStr = JSON.stringify(requestPartners)
                axios.post('http://localhost:8000/api/partners',  requestPartnersStr, {
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + this.getToken
                  }
                }).then(() => { 
                                            
                }).catch((e) => {
                  // eslint-disable-next-line
                  console.log(e.response.data)
                  switch (e.response.status) {
                    case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                    default: this.DisplayError('errors.edit'); break
                  }
                })                             
              })
              this.$q.notify({ message: this.$t('success.edit'), type: 'positive', icon: 'thumb_up' })
              this.closeDlg() 
            }
            else {
              Object.entries(data).forEach((entry) => {                      
                const [key, value] = entry;
                axios.delete(`http://localhost:8000/api/partners/${value["id"]}`, {
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'JWT ' + this.getToken
                  }
                }).then(() => {
                  if (key == data.length - 1) {
                    this.form.partners.forEach((index) => {
                      var requestPartners = {
                        last_name: this.id,
                        partner: index,
                      }
                      const requestPartnersStr = JSON.stringify(requestPartners)
                      axios.post('http://localhost:8000/api/partners',  requestPartnersStr, {
                        headers: {
                          'Content-Type': 'application/json',
                          'Authorization': 'JWT ' + this.getToken
                        }
                      }).then(() => {                              
                        this.closeDlg()                                         
                      }).catch((e) => {
                        // eslint-disable-next-line
                        console.log(e.response.data)
                        switch (e.response.status) {
                          case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                          default: this.DisplayError('errors.edit'); break
                        }
                      })              
                    })                    
                  }                                   
                }).catch((e) => {
                  // eslint-disable-next-line
                  console.log(e.response.data)
                  switch (e.response.status) {
                    case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                    default: this.DisplayError('errors.edit'); break
                  }
                })                
              });
              this.closeDlg()  
              this.$q.notify({ message: this.$t('success.edit'), type: 'positive', icon: 'thumb_up' })                                           
            }      
          }).catch ((e) =>{
            // eslint-disable-next-line
            console.log(e.response.data)
            switch (e.response.status) {
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.edit'); break
            }
          })          
        }).catch((e) => {
          // eslint-disable-next-line
          console.log(e.response.data)
          switch (e.response.status) {
              case 400: this.DisplayError('errors.unique'); break
              case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
              default: this.DisplayError('errors.edit'); break
          }
        })                             
      }
    },
    // Фильтрация списка нападающих для бывших партнёров по звену
    filterPartners (val, update) {
      if (val === '') {
        update(() => {
          this.optionsForwards = this.forwards
        })
        return
      }
      update(() => {
        const needle = val.toLowerCase()
        this.optionsForwards = this.forwards.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    },
    // Функция закрытия диалогового окна
    closeDlg:function()
    {
      // Формирует событие closeForwardsTableEdit, которое отслеживает родительский компонент, вызвавший это окно
      this.$emit('closeForwardsTableEdit');
    }
  },
}
</script>

<style>
</style>