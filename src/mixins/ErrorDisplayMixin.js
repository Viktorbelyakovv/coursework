import ErrorDisplay from '../components/ErrorDisplay.vue'

export default {
    data() {
		return {
          // Флаг отображения ошибки
          ErrorDisplay: false,
          //Сообщение об ошибке
          message: '',
		}
	},
  // Экспорт компонента
    components: {ErrorDisplay},
    methods: {
        DisplayError: function(text) {
            this.message = this.$t(text);
            this.ErrorDisplay=true;
        }
    },
}