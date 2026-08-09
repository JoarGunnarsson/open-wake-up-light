<script setup>
import { ref } from 'vue'

const devices = ref(null);

</script>

<template>

  <div id="AppNavigation" class="sidenav">
    <router-link to="/">Home</router-link>
    <router-link to="/control">Control</router-link>
    <router-link to="/timers">Timers</router-link>
  </div>
  <div id="main">
    <router-view></router-view>
  </div>
</template>
