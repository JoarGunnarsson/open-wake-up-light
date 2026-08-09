<script setup>
import { ref } from 'vue'
import { GET, PUT, POST } from "../request.js"

const devices = ref(null);
const selectedDevice = ref(null);

const possibleActions = ref(["state", "brightness", "gradual_brightness"]);
const selectedAction = ref("state");

const params = ref({});

async function setup(){
  let resp = await GET("/api/devices");
  devices.value = resp.devices;
}

function selectDevice(device){
  selectedDevice.value = device;
}

function selectAction(action){
  selectedAction.value = action;
}

async function controlDevice(){
  var response;
  let url = "/api/devices/" + selectedDevice.value + "/" + selectedAction.value;

  if (selectedAction.value == "gradual_brightness"){
    response = await POST(url, params.value)
  }
  else{
    response = await PUT(url, params.value)
  }

  console.log(response);
}

setup();
</script>

<template>
  <h1> Controls:</h1>
  <div>
    <select class="deviceSelection" v-model="selectedDevice" @change="selectDevice(selectedDevice)">
      <option v-for="device in devices" :key="device">{{device}}</option>
    </select>
  </div>
  <div>
  <select class="actionSelection" v-model="selectedAction" @change="selectAction(selectedAction)">
    <option v-for="action in possibleActions" :key="action">{{action}}</option>
  </select>
  </div>

  <div v-if="selectedAction=='state'">
  <select v-model="params.state">
    <option>ON</option>
    <option>OFF</option>
    <option>TOGGLE</option>
  </select>
</div>

  <div v-else-if="selectedAction=='brightness'">
    <p>Brightness:</p><input v-model="params.brightness" type="text"/>
  </div>

  <div v-else-if="selectedAction=='gradual_brightness'">
    <p>Start brightness:</p> <input v-model="params.start" type="text"/>
    <p>Stop brightness:</p> <input v-model="params.stop" type="text"/>
    <p>Duration:</p> <input v-model="params.duration" type="text"/>
  </div>

  <button @click="controlDevice()">Control Device</button>
</template>
