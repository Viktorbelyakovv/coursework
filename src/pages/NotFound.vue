<template>
  <q-page padding class="docs-input row justify-center divimage">
      <div class="main shadow-10" align="center">
          <br><br><br><h4>{{$t('notfound')}} </h4>
      </div>
  </q-page>
</template>

<script>
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
    width: 500px; 
    height: 287px;
    border-radius: 5px;
    position: absolute;
    top: 21%;   
}
</style>