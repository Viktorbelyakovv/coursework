<template>
  <q-page padding class="docs-input row justify-center divimage">
      <div class="main shadow-10" align="center">
          <h4>{{$t('main.title')}} </h4>
          <div class = "q-ma-md" >
            <div align = "center">{{$t('main.welcome')}}</div>
            <br><br>
            <div align = "left">{{$t('main.text')}}</div>
          </div>
      </div>
  </q-page>
</template>

<script>
// Подключение getters, actions из хранилища данных vuex
import { mapGetters, mapActions } from 'vuex'
// Подключение миксина для проверки действительности токена
import TokenMixin from '../mixins/TokenMixin.js'

export default {
  name: 'Main',
    // Подключаемые миксины
  mixins: [TokenMixin],
  computed: {
  ...mapGetters(['getToken', 'getAuth'])
  },
  methods: {
    // Методы для работы с хранилищем данных vuex 
    ...mapActions({ 
      setToken: 'setToken',
    })
  },
  mounted () {  
    if (this.getAuth) this.checkToken()   
    this.interval = window.setInterval(() => {    
      if (this.getAuth) {
        this.checkToken() 
        this.refreshToken()  
      }    
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

.main{
    background-color: white;
    opacity: 80%;
    border: 1px solid gray;
    width: 600px; 
    height: 400px;
    border-radius: 5px;
    position: absolute;
    top: 15%;  
    font-size: 18px;   
}
</style>