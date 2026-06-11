<template>
  <div class="bar-card">
    <h3 class="chart-title">评分分析</h3>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  rating: Object
})

const option = computed(() => ({
  tooltip: {
    trigger: "axis",
    backgroundColor: "#fff",
    borderColor: "#e5e7eb",
    borderWidth: 1,
    textStyle: { color: "#374151" },
    axisPointer: { type: "shadow" }
  },

  grid: {
    left: 40,
    right: 20,
    top: 20,
    bottom: 30
  },

  xAxis: {
    type: "category",
    data: ["1星", "2星", "3星", "4星", "5星"],
    axisLine: { lineStyle: { color: "#e5e7eb" } },
    axisTick: { show: false },
    axisLabel: { color: "#6b7280", fontSize: 13 }
  },

  yAxis: {
    type: "value",
    splitLine: { lineStyle: { color: "#f3f4f6" } },
    axisLabel: { color: "#9ca3af", fontSize: 12 }
  },

  series: [
    {
      type: "bar",
      barWidth: "55%",
      itemStyle: {
        borderRadius: [6, 6, 0, 0],
        color: {
          type: "linear",
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: "#818cf8" },
            { offset: 1, color: "#6366f1" }
          ]
        }
      },
      emphasis: {
        itemStyle: { color: "#4f46e5" }
      },
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
.bar-card {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 4px 0;
}

.chart {
  height: 300px;
}
</style>
