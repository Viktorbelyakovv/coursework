 <template>
  <q-page padding class="docs-input row justify-center divimage">
    <!-- Диалог для редактирования -->
    <ForwardsTableEdit 
      :showDlg="ForwardsTableEdit"
      :id="editId"
      :mode="mode"
      :options="options"
      :forwards="forwards"
      @closeForwardsTableEdit="ForwardsTableEdit = false; refresh()"
    />
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    />
    <q-table
      class="table"      
      :title="$t('labels.forwards_table')"
      color="primary"
      :data="serverData"
      :columns="getAuth?columns:columns2"
      row-key="id"
      @request="request"
      :loading="loading"
      :loading-label="$t('labels.loading')"
      :selected.sync="selected"
      selection="multiple"
      :pagination.sync="serverPagination"
      :rows-per-page-label="$t('labels.rows_per_page')">       

      <template v-if="getAuth" slot="top-right" slot-scope="{}" class="q-ma-sm">
        <q-btn color="positive" flat round icon="add" :title="$t('buttons.add')" @click="mode='add'; ForwardsTableEdit=true"/> 
        <q-btn color="primary" flat round icon="autorenew" :title="$t('buttons.refresh')" @click="refresh" :loading="loading">
          <span slot="loading">
            <q-spinner-hourglass />
          </span>
        </q-btn>
      </template>

      <!-- Фильтрация -->
      <q-tr slot="top-row" slot-scope="{}" :bgcolor="isFilter?'FDEDEC':''">
        <q-td>
          <template v-if="isFilter">
            <q-btn color="red" size="sm" icon="clear" style="width:20px;" @click="clearFilter()"/>
          </template>
          <template v-else>
            <q-btn color="primary" size="sm" icon="filter_list" style="width:20px;" @click="filterStr = ''; setFilter()"/>
          </template>
        </q-td>

        <q-td align="left">
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.last_name" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.club" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.pucks" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.setups" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.penalty" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>
      </q-tr>

      <!-- Кнопки, которые появляются в верхней части таблицы при выборе строк -->
      <template v-if="getAuth" slot="top-selection" slot-scope="{}">
        <q-btn color="primary" flat :label="$t('buttons.delete')" @click="deleteRows()" class="q-mr-sm" />
        <div class="col" />
      </template>      

      <!--  Основной слот, в котором показываются данные -->
      <template slot="body" slot-scope="props">
        <q-tr :props="props" >
          <q-td v-if="getAuth" align="center">
            <q-checkbox color="primary" v-model="props.selected" />
          </q-td>
          <q-td v-if="!getAuth" align="center">
          </q-td>
          <q-td key="index" :props="props">
            {{ props.row.index}}
          </q-td>
          <q-td key="last_name" :props="props">
            {{ props.row.last_name | capitalizeAll}}
          </q-td>
          <q-td key="club" :props="props">
            {{ props.row.club | capitalizeAll}}
          </q-td>
          <q-td key="pucks" :props="props">
            {{ props.row.pucks }}
          </q-td>
          <q-td key="setups" :props="props">
            {{ props.row.setups }}
          </q-td>
          <q-td key="penalty" :props="props">
            {{ props.row.penalty }}
          </q-td>
          <q-td key="partners" :props="props">
            <q-select :label="$t('labels.list')" dense :options="props.row.partners"/>
          </q-td>
          <q-td key="edit" :props="props">
            <q-btn color="primary" flat round icon="edit" :title="$t('buttons.edit')" @click="mode='edit'; editId=props.row.id; ForwardsTableEdit=true"/>
            <q-btn color="red" flat round icon="delete" :title="$t('buttons.delete')" @click="deleteRow(`http://localhost:8000/api/forwards_table/${props.row.id}`)"/>
          </q-td>
        </q-tr>
      </template>  
    </q-table>
  </q-page>
</template>

<script>
// Библиотека axios используется для работы с запросами к API
import axios from 'axios'
// Подключение getters, actions из хранилища данных vuex
import { mapGetters, mapActions } from 'vuex'
// Подключение собственного компонента для добавления и редактирования
import ForwardsTableEdit from '../../components/tables/ForwardsTableEdit.vue'
// Подключение миксина для удаления строк таблицы
import DeleteRowMixin from '../../mixins/DeleteRowMixin.js'
// Подключение миксина для вывода ошибки
import ErrorDisplayMixin from '../../mixins/ErrorDisplayMixin.js'
// Подключение миксина для проверки действительности токена
import TokenMixin from '../../mixins/TokenMixin.js'

export default {
  data() {
    return {
      // Флаг процесса загрузки
      loading: true,
      // Массив, в который записываются данные получаемые с сервера
      serverData: [],          
      // Описание колонок таблицы
      columns: [
        { name: 'index', label: this.$t('labels.index'), field: 'index', align: 'center', required:true, sortable: true },
        { name: 'last_name', label: this.$t('labels.last_name'), field: 'last_name', align: 'left', required:true, sortable: true },
        { name: 'club', label: this.$t('labels.club'), field: 'club', align: 'left', required:true, sortable: true },
        { name: 'pucks', label: this.$t('labels.pucks'), field: 'pucks', align: 'center', sortable: true },
        { name: 'setups', label: this.$t('labels.setups'), field: 'setups', align: 'center', sortable: true },
        { name: 'penalty', label: this.$t('labels.penalty'), field: 'penalty', align: 'center', sortable: true },
        { name: 'partners', label: this.$t('labels.partners'), field: 'partners', align: 'left' },
        { name: 'edit', label: this.$t('labels.actions'), field: 'edit', align: 'center' }  
      ],
      columns2: [
        { name: 'index', label: this.$t('labels.index'), field: 'index', align: 'center', required:true, sortable: true },
        { name: 'last_name', label: this.$t('labels.last_name'), field: 'last_name', align: 'left', required:true, sortable: true },
        { name: 'club', label: this.$t('labels.club'), field: 'club', align: 'left', required:true, sortable: true },
        { name: 'pucks', label: this.$t('labels.pucks'), field: 'pucks', align: 'center', sortable: true },
        { name: 'setups', label: this.$t('labels.setups'), field: 'setups', align: 'center', sortable: true },
        { name: 'penalty', label: this.$t('labels.penalty'), field: 'penalty', align: 'center', sortable: true },
        { name: 'partners', label: this.$t('labels.partners'), field: 'partners', align: 'left' },
      ],
      // Параметры пагинатора
      serverPagination: {
        page: 1, rowsNumber: 10, rowsPerPage: this.getRows()
      },
      // Массив для хранения отмеченных в таблице строк
      selected: [],
      // Флаг отображения диалогового окна редактирования/добавления данных
      ForwardsTableEdit: false,
      // Режим работы диалогового окна: add - добавление, edit - редактирование
      mode: 'add',
      // Переменная, в которой хранится текущее значение id, выбранного для редактирования
      editId: 0,
      // список дивизионов
      options: [],
      //список нападающих
      forwards: [],
      // список партнёров
      partnersData: [],
      // Флаг, по которому определяется есьт фильтрация или нет
      isFilter: false,
      // Строка фильтрации, передаваемая на сервер в формате <Имя_параметра>=<Значение>
      filterStr: '',
      // Словарь для хранения параметров фильтрации, вводимых пользователем
      filter: {
        last_name: '',
        club: '',
        pucks: '',
        setups: '',
        penalty: '',
      },
    }    
  },
  // Экспорт всех используемых в шаблоне компонентов
  components: { ForwardsTableEdit},
  // Подключаемые миксины
  mixins: [DeleteRowMixin, ErrorDisplayMixin, TokenMixin],
  // getter для получения токена из хранилища данных
  // После авторизации токен доступа записывается в Storage и все последующие запросы к API используют этот токен
  computed: {
    ...mapGetters(['getToken', 'getAuth'])
  },
  methods: {
    // Методы для работы с хранилищем данных vuex 
    ...mapActions({ 
      setToken: 'setToken',
    }),
    ...mapGetters({ 
    getRows: 'getRows', 
    getAutoUpdate: 'getAutoUpdate',
    }),
    // Очистка полей фильтра
    // forced=true - без запроса
    // forced=false - c выводом диалогового окна подтверждения
    clearFilter: function(forced=false) {
      if (forced)
      {
        this.resetFilterFields()
        this.refresh()          
        return
      } 
      this.$q.dialog({
        title: this.$t('labels.filter'),
        message: this.$t('questions.hide'),
        ok: this.$t('buttons.yes'),
        cancel: this.$t('buttons.no'),
        }).onOk(() => {
          this.resetFilterFields()          
          this.refresh()
        })
    },
    // Сброс всех полей фильтрации
    resetFilterFields: function() {
      this.filterStr = ''
      this.filter.last_name = ''
      this.filter.club = ''
      this.filter.pucks = ''
      this.filter.setups = ''
      this.filter.penalty = ''
      this.isFilter = false
    },    
    // Функция установки фильтра и формирования строки фильтрации
    setFilter: function()  {
      if (this.filter.last_name != '') this.filterStr += '&last_name=' + this.filter.last_name
      if (this.filter.club != '') this.filterStr += '&club__name=' + this.filter.club
      if (this.filter.pucks != '') this.filterStr += '&pucks=' + this.filter.pucks
      if (this.filter.setups != '') this.filterStr += '&setups=' + this.filter.setups
      if (this.filter.penalty != '') this.filterStr += '&penalty=' + this.filter.penalty
      
      this.refresh()
      this.isFilter = this.filterStr?true:false
    },
    // Удаление нескольких строк, если пользователь отметил их в таблице
    deleteRows: function() {
      this.$q.dialog({
        title: this.$t('labels.delete_rows'),
        message: this.$t('questions.delete_rows'),
        ok: this.$t('buttons.yes'),
        cancel: this.$t('buttons.no'),
        }).onOk(() => {
          // Цикл по массиву selected, в котором хранятся все отмеченные галочкой строки
          this.selected.forEach(el => 
          {
            // Вызов метода delete через Axios по el.id
            axios.delete(`http://localhost:8000/api/forwards_table/${el.id}`, {
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + this.getToken
              }
            }).then(() => {
              this.$q.notify({  message: this.$t('success.delete_rows'), type: 'positive', icon: 'thumb_up' })      
              this.selected = []
              this.refresh()
            })
            .catch((e) => {
              this.selected = []
              // eslint-disable-next-line
              console.log(e.response.data)
              switch (e.response.status) {
                case 401: this.$router.push('/auth'); this.$router.go('/auth'); break
                default: this.DisplayError('errors.delete_rows'); break
              }
            })
          })
        }).OnCancel(() => {
            this.$q.notify({ message: this.$t('warnings.cancel_operation'), type: 'warning', icon: 'report_problem' })      
        })
    },
    // Функция обновления данных на странице
    refresh: function() {      
      this.request({
        pagination: this.serverPagination
      })   
      this.partners()   
      this.clubs()            
    },
    clubs: function() {
      axios.get('http://localhost:8000/api/clubs_lib', {
        headers: {
          'Content-Type': 'application/json',
        }
      }).then(({ data }) => {
          Object.entries(data).forEach((entry) => {            
            const [key, value] = entry;
            this.options[key] = value["name"]
          });
      })
      .catch (error =>{
        console.log(error.response.data)
        switch (error.response.status) {
          default: this.DisplayError('errors.error'); break
        }
      })
    },
    partners: function() {
      axios.get('http://localhost:8000/api/partners', {
        headers: {
          'Content-Type': 'application/json',
        }
      }).then(({ data }) => {
        this.partnersData = data          
      })
      .catch (error =>{
        console.log(error.response.data)
        switch (error.response.status) {
          default: this.DisplayError('errors.error'); break
        }
      })
    },
    request ({ pagination }) {
      // Ставим флаг процесса загрузки в значение true
      this.loading = true
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      // Запрос к API с использованием метода GET
      // filterStr содержит строку для фильтрации на стороне сервера
      axios.get(`http://localhost:8000/api/forwards_table?limit=1000${this.filterStr}`, {
        headers: {
          'Content-Type': 'application/json',
        }
      }).then(({ data }) => {
          // Установка параметров пагинатора
          this.serverPagination = pagination
          this.serverPagination.rowsNumber = data.count
          // Запись данных в массив serverData
          this.serverData = data
          this.serverData.forEach((row, index) => {
            row.index = index + 1
          })
          Object.entries(data).forEach((entry) => {            
            const [key, value] = entry;
            this.forwards[key] = value["last_name"]
          });         
          this.serverData.forEach((row) => {
            var temp = [];
            var auxil = [];
            Object.entries(this.partnersData).forEach((entry) => {            
              const [key, value] = entry;
              auxil[key] = value["last_name"]
              if (row.id == value["last_name"])
                temp.push(value["partner"])
            });
            row.partners = temp                        
          })
          // Сброс флага процесса загрузки
          this.loading = false
      })
      .catch (error =>{
        // eslint-disable-next-line
        console.log(error.response.data)
        switch (error.response.status) {
          default: this.DisplayError('errors.error'); break
        }
        this.loading = false
      })
    }
  },
  mounted () {    
    if (this.getAuth) this.checkToken() 
    this.refresh()     
    //автоматическое обновление данных    
    this.interval = window.setInterval(() => {         
      this.refresh()      
    }, this.getAutoUpdate() * 1000)
    if (this.getAuth) {
      this.interval = window.setInterval(() => {    
      this.refreshToken()   
      this.checkToken()           
      }, 10000)
    }    
  }  
}
</script>

<style lang="sass">

.tooltips
  background-color: rgba(90, 120, 150, 0.6);
  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0
</style>