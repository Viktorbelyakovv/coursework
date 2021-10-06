 <template>
  <q-page padding class="docs-input row justify-center divimage">
    <!-- Диалог для редактирования -->
    <ClubsTableEdit 
      :showDlg="ClubsTableEdit"
      :id="editId"
      :mode="mode"
      :options="options"
      @closeClubsTableEdit="ClubsTableEdit = false; refresh()"
    />    
    <ImageOpen 
      :showImageOpen="ImageOpen"
      :url="url"
      @closeImageOpen="ImageOpen = false"
    />
    <!--Собственный компонент для вывода ошибки -->
    <ErrorDisplay 
      :showErrorDisplay="ErrorDisplay"
      :message="message"
      @closeErrorDisplay="ErrorDisplay = false; refresh()"
    />
    <q-table
      class="table"      
      :title="$t('labels.clubs_table')"
      color="primary"
      :data="serverData"
      :columns="getAuth?columns:columns2"
      row-key="id"
      @request="request"
      :loading="loading"
      :loading-label="$t('labels.loading')" 
      selection="multiple"
      :selected.sync="selected"
      :pagination.sync="serverPagination"
      :rows-per-page-label="$t('labels.rows_per_page')">       

      <template v-if="getAuth" slot="top-right" slot-scope="{}" class="q-ma-sm">
        <q-btn color="positive" flat round icon="add" :title="$t('buttons.add')" @click="mode='add'; ClubsTableEdit=true"/> 
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
          <q-input v-model="filter.name" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.fio" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
        </q-td>

        <q-td align="left">
          <q-input v-model="filter.year" hide-underline class="filter" @input="filterStr = ''; setFilter()"/>
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
          <q-td key="name" :props="props">
            {{ props.row.name | capitalizeAll}}
          </q-td>
          <q-td key="fio" :props="props">
            {{ props.row.fio | capitalizeAll}}
          </q-td>
          <q-td key="year" :props="props">
            {{ props.row.year }}
          </q-td>
          <q-td key="photo" :props="props">
            <q-btn :label="$t('buttons.open')" @click="ImageOpen=true; url=props.row.photo"/>
          </q-td>
          <q-td key="edit" :props="props">
            <q-btn color="primary" flat round icon="edit" :title="$t('buttons.edit')" @click="mode='edit'; editId=props.row.id; ClubsTableEdit=true"/>
            <q-btn color="red" flat round icon="delete" :title="$t('buttons.delete')" @click="deleteRow(`http://localhost:8000/api/clubs_table/${props.row.id}`)"/>
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
import ClubsTableEdit from '../../components/tables/ClubsTableEdit.vue'
// Подключение компонента для показа фото
import ImageOpen from '../../components/ImageOpen.vue'
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
        { name: 'index', label: this.$t('labels.index'), field: 'index', align: 'center', required:true, sortable: true},
        { name: 'name', label: this.$t('labels.name'), field: 'name', align: 'left', required:true, sortable: true },
        { name: 'fio', label: this.$t('labels.fio'), field: 'fio', align: 'left', required:true, sortable: true },
        { name: 'year', label: this.$t('labels.year'), field: 'year', align: 'center', required:true, sortable: true },
        { name: 'photo', label: this.$t('labels.photo'), field: 'photo', align: 'left', required:true },
        { name: 'edit', label: this.$t('labels.actions'), field: 'edit', align: 'center' }  
      ],
      columns2: [
        { name: 'index', label: this.$t('labels.index'), field: 'index', align: 'center', required:true, sortable: true},
        { name: 'name', label: this.$t('labels.name'), field: 'name', align: 'left', required:true, sortable: true },
        { name: 'fio', label: this.$t('labels.fio'), field: 'fio', align: 'left', required:true, sortable: true },
        { name: 'year', label: this.$t('labels.year'), field: 'year', align: 'center', required:true, sortable: true },
        { name: 'photo', label: this.$t('labels.photo'), field: 'photo', align: 'left', required:true },
      ],
      // Параметры пагинатора
      serverPagination: {
        page: 1, rowsNumber: 10, rowsPerPage: this.getRows()
      },
      // Массив для хранения отмеченных в таблице строк
      selected: [],
      // Флаг отображения диалогового окна редактирования/добавления данных
      ClubsTableEdit: false,
      // Флаг отображения диалогового окна показа фото
      ImageOpen: false,
      // Ссылка на фото
      url: '',
      // Режим работы диалогового окна: add - добавление, edit - редактирование
      mode: 'add',
      // Переменная, в которой хранится текущее значение id, выбранного для редактирования
      editId: 0,
      // список дивизионов
      options: [{ name: 'name', field: 'name'},],
      // Флаг, по которому определяется есьт фильтрация или нет
      isFilter: false,
      // Строка фильтрации, передаваемая на сервер в формате <Имя_параметра>=<Значение>
      filterStr: '',
      // Словарь для хранения параметров фильтрации, вводимых пользователем
      filter: {
        name: '',
        fio: '',
        year: '',
      },
    }    
  },
  // Экспорт всех используемых в шаблоне компонентов
  components: { ClubsTableEdit, ImageOpen},
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
      this.filter.name = ''
      this.filter.fio = ''
      this.filter.year = ''
      this.isFilter = false
    },    
    // Функция установки фильтра и формирования строки фильтрации
    setFilter: function()  {
      if (this.filter.name != '') this.filterStr += '&name__name=' + this.filter.name
      if (this.filter.fio != '') this.filterStr += '&fio=' + this.filter.fio
      if (this.filter.year != '') this.filterStr += '&year=' + this.filter.year
      
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
            axios.delete(`http://localhost:8000/api/clubs_table/${el.id}`, {
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
            this.options[key] = value['name']
          });
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
      // Запрос к API с использованием метода GET
      // filterStr содержит строку для фильтрации на стороне сервера
      axios.get(`http://localhost:8000/api/clubs_table?limit=1000${this.filterStr}`, {
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
</style>