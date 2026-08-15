<script setup>
import { ref } from 'vue'
import { useRouter} from 'vue-router';
import { GET, PUT, DELETE } from "@/request.js"
import { formatDatetime } from "../utils.js"
import WeekdayPicker from '@/components/WeekdayPicker.vue';
const router = useRouter();

const alarms = ref({});


async function updateAlarm(alarmData){
  let url = "/api/alarms/update/" + alarmData.id;
  var body = alarmData;
  await PUT(url, body);
  close();
}


async function deleteAlarm(id){
  await DELETE("/api/alarms/delete/" + id);
  await getAlarms();
}

async function getAlarms(){
  alarms.value = await GET("/api/alarms");
}

const loading = ref(true);

async function populate(){
  if (!loading.value){
    return;
  }
  await getAlarms();
  loading.value = false;
}

populate();

</script>

<template>
  <h1>Alarms:</h1>
  <button @click="router.push('/alarms/create')">Create Alarm</button>
  <div v-if="!loading">
    <div v-for="(value, key) in alarms" class="alarm-container">
      <div v-if="value.name != ''"> {{ value.name }}</div>
      <div v-if="value.next_activation != ''"> {{ formatDatetime(value.next_activation)  }}</div>
      <div v-else> {{ value.date.time }}</div>
      <WeekdayPicker 
        :edit-mode="false"
        :weekdays="value.date.weekdays"
      />
      <div class="button_description">Active</div><input v-model="value.is_active" @change="updateAlarm(value)" type="checkbox"/>
      <button @click="router.push('/alarms/edit/' + key)">Edit alarm</button>
      <button @click="deleteAlarm(key)">Delete alarm</button>
    </div>
  </div>


</template>
