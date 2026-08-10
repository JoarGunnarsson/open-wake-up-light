<script setup>
import { ref } from 'vue'
import { useRouter} from 'vue-router';
import { GET } from "@/request.js"

const router = useRouter();

const alarms = ref({});

async function getAlarms(){
  alarms.value = await GET("/api/alarms");
}

getAlarms();

</script>

<template>
  <h1>Alarms:</h1>
  <button @click="router.push('/alarms/create')">Create Alarm</button>


  <div v-for="(value, key) in alarms" style="margin-top: 10px; background-color: bisque;">
    <div> {{ value.date.time }}</div>
    <div> {{ value.date.weekdays }}</div>
    <div class="button_description">Active</div><input v-model="value.is_active" type="checkbox"/>
    <button @click="router.push('/alarms/edit/' + key)">Edit alarm</button>
  </div>


</template>
