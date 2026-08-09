

<script setup>
import { ref } from 'vue'
import { GET, PUT, POST } from "../request.js"


const emit = defineEmits(['controls-change']);

const devices = ref(null);
const selectedDevice = ref(null);

const possibleActions = ref(["state", "brightness", "gradual_brightness"]);
const selectedAction = ref(possibleActions.value[0]);
const params = ref({state: "ON"});

async function getDevices(){
  let resp = await GET("/api/devices");
  devices.value = resp.devices;
  if (selectedDevice.value == null){
    selectedDevice.value = devices.value[0];
  }
}

function selectDevice(device){
  selectedDevice.value = device;
}

function selectAction(action){
  selectedAction.value = action;
}

defineExpose({
  selectedDevice,
  selectedAction,
  params
})

getDevices();
</script>

<template>
  <div>
    <div class="button_description">Device:</div>
    <select class="deviceSelection" v-model="selectedDevice" @change="selectDevice(selectedDevice)">
      <option v-for="device in devices" :key="device">{{device}}</option>
    </select>
  </div>

  <div>
    <div class="button_description">Action:</div>
    <select class="actionSelection" v-model="selectedAction" @change="selectAction(selectedAction)">
      <option v-for="action in possibleActions" :key="action">{{action}}</option>
    </select>
  </div>

  <div v-if="selectedAction=='state'">
    <div class="button_description">Power State:</div>
    <select v-model="params.state">
      <option>ON</option>
      <option>OFF</option>
      <option>TOGGLE</option>
    </select>
  </div>

  <div v-else-if="selectedAction=='brightness'">
    <div class="button_description">Brightness:</div><input v-model="params.brightness" type="text"/>
  </div>

  <div v-else-if="selectedAction=='gradual_brightness'">
    <div>
      <div class="button_description">Start brightness:</div> <input v-model="params.start" type="text"/>
    </div>
    <div>
      <div class="button_description">Stop brightness:</div> <input v-model="params.stop" type="text"/>
    </div>
    <div>
      <div class="button_description">Duration:</div> <input v-model="params.duration" type="text"/>
    </div>
  </div>
</template>