import axios from 'axios'

export default {
    methods: {
        checkToken: function() {
          var request = { 
              token: this.getToken, 
          } 
          const requestStr = JSON.stringify(request) 
          // Запрос через метод POST, который в случае успеха вернет токен авторизации 
          axios.post('http://localhost:8000/api-token-verify/', requestStr, { 
              headers: { 
                  'Content-Type': "application/json"
              } 
          }).then((response) => {  
            console.log(response)
          }).catch((error) => { 
              // eslint-disable-next-line 
              console.log(error.response.data)
              switch (error.response.status) {
                default: this.$router.push('/auth'); break
            }
          }) 
        },
        refreshToken: function() {
          var request = { 
              token: this.getToken, 
          } 
          const requestStr = JSON.stringify(request) 
          // Запрос через метод POST, который в случае успеха вернет токен авторизации 
          axios.post('http://localhost:8000/api-token-refresh/', requestStr, { 
              headers: { 
                  'Content-Type': "application/json"
              } 
          }).then((response) => {  
            console.log(response)
            this.setToken(response.data.token) 
          }).catch((error) => { 
            // eslint-disable-next-line 
            console.log(error.response.data)
          }) 
        },
    }
}