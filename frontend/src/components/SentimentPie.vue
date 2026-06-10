<template>
  <v-chart
    class="chart"
    :option="option"
    autoresize
  />
</template>

<script setup>
import { computed } from "vue"

import VChart from "vue-echarts"

const props = defineProps({
  sentiment: Object
})

const option = computed(() => ({
  title: {
    text: "情感分布",
    left: "center"
  },

  tooltip: {
    trigger: "item"
  },

  legend: {
    bottom: 0
  },

  series: [
    {
      type: "pie",

      radius: "60%",

      data: [
        {
          value: props.sentiment?.positive_count || 0,
          name: "正面"
        },
        {
          value: props.sentiment?.neutral_count || 0,
          name: "中性"
        },
        {
          value: props.sentiment?.negative_count || 0,
          name: "负面"
        }
      ]
    }
  ]
}))
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>