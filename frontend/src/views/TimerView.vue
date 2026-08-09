<script setup>
import { ref } from 'vue'
import { GET, PUT, POST } from "../request.js"
import DeviceControl from "../components/ControlComponent.vue"

const control = ref(null);
const alarmTime = ref(null);

function addTimezoneToDatetime(date){
  var currentDate = new Date();
  var timezoneOffset = -currentDate.getTimezoneOffset();

  var sign = "+";
  if (timezoneOffset < 0){
    timezoneOffset = -timezoneOffset;
    sign = "-";
  }

  var hours = (timezoneOffset / 60).toString();
  var minutes = (timezoneOffset % 60).toString();
  var offsetString = `${sign}${hours.padStart(2, 0)}:${minutes.padStart(2, 0)}`
  return date + offsetString;
}

async function addAlarm(){
  let url = "/api/alarms/create";
  var body = {
    devices: [control.value.selectedDevice],
    action: control.value.selectedAction,
    date: addTimezoneToDatetime(alarmTime.value),
    params: control.value.params,
  };
  await POST(url, body);

}
</script>

<template>
  <h1>Alarms:</h1>

  <DeviceControl ref="control"/>
  <div>
    <div class="button_description">Alarm date:</div>
    <input v-model="alarmTime" type="datetime-local" step="1"/>
  </div>

  <button @click="addAlarm">Add Alarm</button>
</template>
