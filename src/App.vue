<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="glossy">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          :disable="!getAuth"
          icon="menu"
        />
        <q-toolbar-title align="center">
          {{$t('app.product')}}
        </q-toolbar-title>
        <template v-if="getAuth">          
          {{getUsername}}
          <q-btn color = "primary" :label ="$t('buttons.exit')" class = "q-ml-md" @click="onExit" />
        </template>
        <template v-else>
          <q-btn to="/auth">{{$t('buttons.enter')}}</q-btn>
        </template>        
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>{{$t('app.menu.title')}}</q-item-label>    
        <q-item clickable @click="$router.push('/').catch(()=>{}); $router.go('/').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.main')}}</q-item-label>
          </q-item-section>
        </q-item>    
        <q-item v-if="getAuth" clickable @click="$router.push('/profile').catch(()=>{}); $router.go('/profile').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="person" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.profile')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item v-if="!getAuth" clickable @click="$router.push('/auth').catch(()=>{}); $router.go('/auth').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="login" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.auth')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item v-if="!getAuth" clickable @click="$router.push('/reg').catch(()=>{}); $router.go('/reg').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="person_add_alt" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.reg')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/division').catch(()=>{}); $router.go('/division').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="sports_hockey" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.division')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/clubslib').catch(()=>{}); $router.go('/clubslib').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="sports_hockey" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.clubs_lib')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/clubstable').catch(()=>{}); $router.go('/clubstable').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="sports_hockey" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.clubs_table')}}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable @click="$router.push('/forwardstable').catch(()=>{}); $router.go('/forwardstable').catch(()=>{})">
          <q-item-section avatar>
            <q-icon name="sports_hockey" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{$t('app.menu.forwards_table')}}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

// Подключение Actions и Getters из хранилища Vuex
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'LayoutDefault',
  components: {
  },
  data () {
    return {
      langState: true,
      leftDrawerOpen: false,
    }
  },
  computed: {
    ...mapGetters(['getAuth', 'getUsername'])
  },
  methods: {
    // Формирование Actions для сброса state после выхода из приложения
    ...mapActions({
      unsetStorage: 'unsetStorage'
    }),
    onExit() {
      this.$store.dispatch('unsetStorage');
      this.$router.push('/'); 
      this.$router.go('/'); 
    },
  }
}
</script>
