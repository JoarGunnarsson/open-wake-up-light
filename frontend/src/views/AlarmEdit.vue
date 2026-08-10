<script setup>
import { ref } from 'vue'
import { GET, POST, PUT } from "../request.js"
import DeviceControl from '@/components/ControlComponent.vue'
import WeekdayPicker from '@/components/WeekdayPicker.vue';
import { useRouter} from 'vue-router';

const router = useRouter();
const props = defineProps(["id"]);

const weekdaySelection = ref(null);

const data = ref({
    device: null,
    action: null,
    params: {},
    date: {weekdays: {}, time:"07:00"},
    is_active: true,
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
  await fillAlarmData();
  loading.value = false;

}

populate();

function makeAlarmRequestData(){
  return {
    device: data.value.device,
    action: data.value.action,
    params: data.value.params,
    is_active: data.value.is_active,
    date: {
      weekdays: weekdaySelection.value.weekdays,
      time: data.value.date.time,
    },
  };
}


async function createAlarm(){
  let url = "/api/alarms/create";
  var body = makeAlarmRequestData();
  await POST(url, body);
  close();
}


async function updateAlarm(){
  let url = "/api/alarms/update/" + props.id;
  var body = makeAlarmRequestData();
  await PUT(url, body);
  close();
}


function close() {
  router.back();
}



</script>

<template>
  <div style="background-color: aquamarine;">
    <h1 v-if="props.id != null">Edit an alarm:</h1>
    <h1 v-else>Create an alarm:</h1>

    <DeviceControl v-if="!loading" 
    :device="data.device"
    :action="data.action"
    :params="data.params"
    @select-device="(device) => data.device = device" 
    @select-action="(action) => data.action = action"  
    @edit-params="(params) => data.params = params"/>


    <div> Data action: {{ data.action }}</div>
    <div>
      <div class="button_description">Alarm time:</div>
      <input v-model="data.date.time" type="time"/>
    </div>

    <WeekdayPicker ref="weekdaySelection"/>
    <div>
      <div class="button_description">Active:</div>
      <input v-model="data.is_active" type="checkbox"/>
    </div>

    <button v-if="props.id != null" @click="updateAlarm()">Save</button>
    <button v-else @click="createAlarm()">Save</button>
    <button @click="close()">Cancel</button>

  </div>

</template>
