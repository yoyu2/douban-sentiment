<template>
  <div class="pie-card">
    <h3 class="chart-title">情感分析</h3>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from "vue"
import VChart from "vue-echarts"

const props = defineProps({
  sentiment: Object
})

const option = computed(() => ({
  tooltip: {
    trigger: "item",
    backgroundColor: "#fff",
    borderColor: "#e5e7eb",
    borderWidth: 1,
    textStyle: { color: "#374151" },
    formatter: "{b}: {c} 条 ({d}%)"
  },

  legend: {
    bottom: 0,
    textStyle: { color: "#6b7280", fontSize: 13 }
  },

  series: [
    {
      type: "pie",
      radius: ["55%", "78%"],
      center: ["50%", "48%"],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 4,
        borderColor: "#fff",
        borderWidth: 3
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: "bold"
        },
        scaleSize: 8
      },
      data: [
        {
          value: props.sentiment?.positive_count || 0,
          name: "正面",
          itemStyle: { color: "#34d399" }
        },
        {
          value: props.sentiment?.neutral_count || 0,
          name: "中性",
          itemStyle: { color: "#94a3b8" }
        },
        {
          value: props.sentiment?.negative_count || 0,
          name: "负面",
          itemStyle: { color: "#f87171" }
        }
      ]
    }
  ]
}))
</script>

<style scoped>
.pie-card {
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
