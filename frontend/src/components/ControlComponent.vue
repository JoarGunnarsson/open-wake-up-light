

<script setup>
import { ref, watch } from 'vue'
import { GET } from "../request.js"

const props = defineProps(["device", "action", "params", "minutes_before"]);
const emit = defineEmits(['select-device', 'select-action', 'edit-params', 'edit-minutes_before']);

const devices = ref(null);
const possibleActions = ref(["state", "brightness", "gradual_brightness"]);
const selectedDevice = ref(null);
const selectedAction = ref(null);


if (props.device){
  selectedDevice.value = props.device;
}

if (props.action){
  selectedAction.value = props.action;
}
else{
  selectedAction.value = possibleActions.value[0];

}

const params = ref({});
if (props.params){
  params.value = props.params;
}

const minutes_before = ref(null);
if (props.minutes_before){
  minutes_before.value = props.minutes_before;
}

async function getDevices(){
  let resp = await GET("/api/devices");
  devices.value = resp.devices;
  if (selectedDevice.value == null){
    selectedDevice.value = devices.value[0];
  }
}

const loading = ref(true);

async function populate(){
  if (!loading.value){
    return;
  }
  await getDevices();
  loading.value = false;

}

populate();


function emitDefaults(){
  emit('select-device', selectedDevice);
  emit('select-action', selectedAction);
  emit('edit-params', params);
  emit('edit-minutes_before', minutes_before);
}
emitDefaults()

watch(selectedAction, (newAction) => {
  switch (newAction){
    case 'state':
      params.value = {
        state: "ON"
      };
      break

    case 'brightness':
      params.value = {
        brightness: "254"
      };
      break

    case 'gradual_brightness':
      params.value = {
        start: 0,
        stop: 254
      };
      break
  }
  emit('edit-params', params);

}, {immediate: true});

</script>

<template>
  <div>
    <div class="button_description">Device:</div>
    <select class="deviceSelection" v-model="selectedDevice" @change="$emit('select-device', selectedDevice)">
      <option v-for="device in devices" :key="device">{{device}}</option>
    </select>
  </div>
  <div>
    <div class="button_description">Action:</div>
    <select class="actionSelection" v-model="selectedAction" @change="$emit('select-action', selectedAction)">
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
      <div class="button_description">Minutes before:</div>
      <input type="number" v-model="minutes_before" @change="$emit('edit-minutes_before', minutes_before)">
    </div>
  </div>
</template>