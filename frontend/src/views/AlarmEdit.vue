<script setup>
import { ref } from 'vue'
import { GET, POST, PUT } from "../request.js"
import DeviceControl from '@/components/ControlComponent.vue'
import WeekdayPicker from '@/components/WeekdayPicker.vue';
import { useRouter} from 'vue-router';

const router = useRouter();
const props = defineProps(["id"]);

const data = ref({
    name: "",
    device: null,
    action: null,
    params: {},
    date: {weekdays: null, time:"07:00"},
    is_active: true,
    minutes_before: null,
});


async function fillAlarmData(){
  if (props.id != null){
    data.value = await GET("/api/alarms/" + props.id);
  }
}

const loading = ref(true);

async function populate(){
  if (!loading.value){
    return;
  }
  try {
    await fillAlarmData();
    loading.value = false;
  }
  catch {
    console.log("Failed to fetch alarm");
  }
  
}

populate();


async function createAlarm(){
  let url = "/api/alarms/create";
  await POST(url, data.value);
  close();
}


async function updateAlarm(){
  let url = "/api/alarms/update/" + props.id;
  await PUT(url, data.value);
  close();
}


function close() {
  router.back();
}

</script>

<template>
  <div v-if="!loading" class="alarm-edit">
    <h1 v-if="props.id != null">Edit an alarm:</h1>
    <h1 v-else>Create an alarm:</h1>

    <div>
      <div class="button_description">Name:</div> <input v-model="data.name" type="text"/>
    </div>
    <DeviceControl
    :device="data.device"
    :action="data.action"
    :params="data.params"
    :minutes_before="data.minutes_before"
    @select-device="(device) => data.device = device" 
    @select-action="(action) => data.action = action"  
    @edit-params="(params) => data.params = params"
    @edit-minutes_before="(minutes_before) => data.minutes_before = minutes_before"
    />

    <div>
      <div class="button_description">Alarm time:</div>
      <input v-model="data.date.time" type="time"/>
    </div>

    <WeekdayPicker 
    :edit-mode="true"
    :weekdays="data.date.weekdays"
    @edit-weekdays="(weekdays) => data.date.weekdays = weekdays" 
    />
    <div>
      <div class="button_description">Active:</div>
      <input v-model="data.is_active" type="checkbox"/>
    </div>

    <button v-if="props.id != null" @click="updateAlarm()">Save</button>
    <button v-else @click="createAlarm()">Save</button>
    <button @click="close()">Cancel</button>
  </div>

</template>
