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
  await PUT(url, body);

}

</script>

<template>
  <h1> Controls:</h1>

    <DeviceControl
    :device="data.device"
    :action="data.action"
    :params="data.params"
    @select-device="(device) => data.device = device" 
    @select-action="(action) => data.action = action"  
    @edit-params="(params) => data.params = params"/>

  <button @click="controlDevice">Control Device</button>
</template>
