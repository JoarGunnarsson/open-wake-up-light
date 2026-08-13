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

function emitWeekdaysList(newWeekdays){
    emit('edit-weekdays', newWeekdays);
}

emitWeekdaysList(weekdays);

watch(weekdays.value, (newWeekdays) => {
    emitWeekdaysList(newWeekdays)
})
</script>

<template>
    <div class="weekdays-container">
        <div class="weekday" v-for="(weekday) in weekdays" :key="weekday">
            <div v-if="editMode==true">
                <input v-model="weekday.value" type="checkbox" class="hidden" :id="weekday.day + '_checkbox'">
                <label :for="weekday.day + '_checkbox'">{{ weekday.day[0] }}</label>
            </div>
            <span v-else-if="weekday.value" class="weekday-selected">{{ weekday.day[0] }}</span>
            <span v-else class="weekday-unselected">{{ weekday.day[0] }}</span>
        </div>
    </div>
</template>