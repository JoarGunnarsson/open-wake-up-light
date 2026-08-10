<script setup>

const props = defineProps(['weekdays']);

if (props.weekdays == null){
    props.weekdays = {"Monday": false, "Tuesday": false, "Wednesday": false, "Thursday": false, "Friday": false, "Saturday": false, "Sunday": false};
}

</script>

<template>
    <div style="background-color: blue;">
        <div type="weekday" v-for="(value, weekday) in props.weekdays" :key="weekday">
            <input v-model="props.weekdays[weekday]" type="checkbox" class="hidden" :id="weekday + '_checkbox'">
            <label :for="weekday + '_checkbox'">{{ weekday[0] }}</label>
        </div>
    </div>
</template>