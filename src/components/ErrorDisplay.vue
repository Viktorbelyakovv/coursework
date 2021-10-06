<template>
    <q-dialog v-model="showErrorDisplay" persistent> 
        <q-card> 
            <q-card-section class="bg-primary text-white">
                {{ $t('labels.error') }}
            </q-card-section>
            <q-card-section class="q-pt-none">
              <q-item>
                <q-item-section>
                  <q-icon name="error" class="text-red" style="font-size: 4rem;" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{this.message}}</q-item-label>
                </q-item-section>
              </q-item>                
            </q-card-section>
            <q-card-actions align="right">
                <q-btn :label="$t('buttons.close')"  @click="closeErrorDisplay" class = "q-mr-sm"/>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
export default {
  // Свойства, которые передаются из родительского компонента при его вызове
  props: {
    // Флаг видимости компонента
    showErrorDisplay: null,
    // Сообщение
    message: null,
  },
  methods:{
    // Функция закрытия диалогового окна
    closeErrorDisplay:function()
    {
      // Формирует событие closeErrorDisplay, которое отслеживает родительский компонент, вызвавший это окно
      this.$emit('closeErrorDisplay');
    },
  },
}
</script>