<script setup>
import { ref } from 'vue'
import { GET } from "../request.js"
import { formatDatetime } from "../utils.js"

const alarmDatetime = ref(null);
const timeLeft = ref(null);

async function getNextAlarm(){
  var response = await GET("/api/alarms/next_alarm");

  alarmDatetime.value = response.datetime;
  timeLeft.value = response.time_left;
}


function makeTimestampReadable(timestamp){
  var seconds_one_minute = 60;
  var seconds_one_hour = seconds_one_minute * 60;
  var seconds_one_day = seconds_one_hour * 24;
  var seconds_left = timestamp;
  var days = Math.floor(seconds_left / seconds_one_day);
  seconds_left = seconds_left % seconds_one_day;

  var hours = Math.floor(seconds_left / seconds_one_hour);
  seconds_left = seconds_left % seconds_one_hour;

  var minutes = Math.floor(seconds_left / seconds_one_minute);

  return `${days} days, ${hours} hours, ${minutes} minutes`
}


const loading = ref(true);

async function populate(){
  if (!loading.value){
    return;
  }
  await getNextAlarm();
  try {
    loading.value = false;
  }
  catch {
    console.log("Failed to fetch next alarm");
  }
  
}

populate();

</script>

<template>
  <div v-if="!loading">
    <div v-if="alarmDatetime==null || timeLeft == null">
      <h1>
        No alarms set
      </h1>
    </div>

    <div v-else>
      <h1> Open Wake-up Light</h1>
      <h2>Next alarm in:</h2>
      {{  makeTimestampReadable(timeLeft) }}
      <h2>At:</h2>
      {{ formatDatetime(alarmDatetime) }}
    </div>
      
  </div>
</template>
