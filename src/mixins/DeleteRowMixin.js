import axios from 'axios'

export default {
    methods: {
        deleteRow: function(url) {
          this.$q.dialog({
            title: this.$t('labels.delete_row'),
            message: this.$t('questions.delete_row'),
            ok: this.$t('buttons.yes'),
            cancel: this.$t('buttons.no'),
            }).onOk(() => {
              axios.defaults.xsrfCookieName = 'csrftoken';
              axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
              // Вызов метода delete через Axios по url
              axios.delete(url, {
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'JWT ' + this.getToken
                }
              }).then(() => {
                this.$q.notify({message: this.$t('success.delete_row'), type: 'positive', icon: 'thumb_up' })      
                this.refresh()
              })
              .catch((e) => {
                // eslint-disable-next-line
                console.log(e.response.data)
                switch (e.response.status) {
                    case 401: this.message = this.$t('errors.user_no_auth'); this.ErrorDisplay=true; break
                    default: this.message = this.$t('errors.delete_rows') + ': '+ e.response.statusText; this.ErrorDisplay=true; break
                }
              })
            }).OnCancel(() => {
                this.$q.notify({ message: this.$t('warnings.cancel_operation') , type: 'warning', icon: 'report_problem' })      
            })
        },
    }
}