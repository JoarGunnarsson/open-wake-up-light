<script setup>
import { ref, watch } from 'vue'
const props = defineProps(['weekdays', "editMode"]);

const weekdays = ref(null);

if (props.weekdays != null){
    weekdays.value = props.weekdays;
}else{
    weekdays.value = [{day: "Monday", value: false}, {day: "Tuesday", value: false}, {day: "Wednesday", value: false}, {day: "Thursday", value: false}, {day: "Friday", value: false}, {day: "Saturday", value: false}, {day: "Sunday", value: false}, ];
}

const emit = defineEmits(["edit-weekdays"]);

watch(weekdays.value, (newWeekdays) => {
    emit('edit-weekdays', newWeekdays);
})
</script>

<template>
    <div style="background-color: blue;">
        <div type="weekday" v-for="(weekday) in weekdays" :key="weekday">
            <div v-if="editMode==true">
                <input v-model="weekday.value" type="checkbox" class="hidden" :id="weekday.day + '_checkbox'">
                <label :for="weekday.day + '_checkbox'">{{ weekday.day[0] }}</label>
            </div>
            <span v-else-if="weekday.value" style="color: coral;">{{ weekday.day[0] }}</span>
            <span v-else style="color: #592c1b;">{{ weekday.day[0] }}</span>
        </div>
    </div>
</template>