<script setup>

</script>

<template>

  <div id="AppNavigation" class="sidenav">
    <router-link to="/">Home</router-link>
    <router-link to="/control">Control</router-link>
    <router-link to="/alarms">Alarms</router-link>
    <a href="/zigbee2mqtt">Zigbee2MQTT</a>
  </div>
  <div id="main">
    <router-view></router-view>
  </div>
</template>
