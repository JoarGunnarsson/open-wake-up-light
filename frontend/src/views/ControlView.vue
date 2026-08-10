<script setup>
import { ref } from 'vue'
import { GET, PUT, POST } from "../request.js"
import DeviceControl from "../components/ControlComponent.vue"

const data = ref({
  device: null,
  action: null,
  params: {},
  });

async function controlDevice(){
  let url = "/api/devices/" + data.value.device;
  
  var body = {
    action: data.value.action,
    params: data.value.params,
  };
  var response = await PUT(url, body)

}

</script>

<template>
  <h1> Controls:</h1>

  <DeviceControl v-model:device="data.device" v-model:action="data.action" v-model:params="data.params"/>

  <button @click="controlDevice">Control Device</button>
</template>
