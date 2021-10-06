<template>
    <q-dialog v-model="showImageOpen" persistent> 
        <q-card> 
            <q-card-section class="bg-primary text-white">
                {{ $t('labels.image') }}
            </q-card-section>
            <q-card-section class="q-pt-none">
                <q-img
                :src="this.url"
                spinner-color="white"
                style="height: 500px; width: 500px"
                />
            </q-card-section>
            <q-card-actions align="right">
                <q-btn :label="$t('buttons.close')"  @click="closeImageOpen" class = "q-mr-sm"/>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
export default {
  // Свойства, которые передаются из родительского компонента при его вызове
  props: {
    // Флаг видимости компонента
    showImageOpen: null,
    // Ссылка на фото
    url: null,
  },
  methods:{
    // Функция закрытия диалогового окна
    closeImageOpen:function()
    {
      // Формирует событие closeImage, которое отслеживает родительский компонент, вызвавший это окно
      this.$emit('closeImageOpen');
    },
  },
}
</script>