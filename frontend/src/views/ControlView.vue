<script setup>
import { ref } from 'vue'
import { GET, PUT, POST } from "../request.js"
import DeviceControl from "../components/ControlComponent.vue"

const control = ref(null);

async function controlDevice(){
  let url = "/api/devices/" + control.value.selectedDevice;
  
  var body = {
    action: control.value.selectedAction,
    params: control.value.params,
  };
  var response = await PUT(url, body)

}

</script>

<template>
  <h1> Controls:</h1>

  <DeviceControl ref="control"/>

  <button @click="controlDevice">Control Device</button>
</template>
