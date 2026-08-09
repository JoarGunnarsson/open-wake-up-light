<script setup>
import { ref } from 'vue'

const devices = ref(null);
</script>

<template>
  <h1> Devices:</h1>
  <li v-for="device in devices">
    {{device}}
  </li>
</template>
