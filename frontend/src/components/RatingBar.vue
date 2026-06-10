<template>
  <v-chart
    class="chart"
    :option="option"
    autoresize
  />
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  rating: Object
})

const option = computed(() => ({

  title: {
    text: "评分分布",
    left: "center"
  },

  tooltip: {
    trigger: "axis"
  },

  xAxis: {
    type: "category",
    data: ["1星", "2星", "3星", "4星", "5星"]
  },

  yAxis: {
    type: "value"
  },

  series: [
    {
      name: "评论数",

      type: "bar",

      data: [
        props.rating?.["1"] || 0,
        props.rating?.["2"] || 0,
        props.rating?.["3"] || 0,
        props.rating?.["4"] || 0,
        props.rating?.["5"] || 0
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