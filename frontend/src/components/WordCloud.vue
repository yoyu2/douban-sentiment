<template>
  <div class="wordcloud-card">
    <h3 class="chart-title">词云图</h3>
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  keywords: {
    type: Array,
    default: () => []
  }
})

const colors = [
  "#2527a5", "#8b5cf6", "#a78bfa",
  "#818cf8", "#60a5fa", "#38bdf8",
  "#34d399", "#b5cf8b", "#facc15",
  "#fb923c", "#f87171", "#f472b6"
]

const option = computed(() => ({
  backgroundColor: "transparent",

  tooltip: {
    backgroundColor: "#fff",
    borderColor: "#e5e7eb",
    borderWidth: 1,
    textStyle: { color: "#4b5563" },
    formatter: params => `
      <div style="padding:4px 8px">
        <strong>${params.name}</strong><br/>
        出现次数：${params.value}
      </div>
    `
  },

  series: [
    {
      type: "wordCloud",
      shape: "circle",
      left: "center",
      top: 2,
      width: "98%",
      height: "96%",
      sizeRange: [20, 72],
      rotationRange: [0, 0],
      rotationStep: 0,
      gridSize: 2,
      drawOutOfBound: false,

      textStyle: {
        fontFamily: '"PingFang SC","SF Pro Display","Microsoft YaHei",sans-serif',
        fontWeight: 400,
        color: params => colors[params.dataIndex % colors.length]
      },

      emphasis: {
        focus: "self",
        textStyle: { shadowBlur: 8, shadowColor: "rgba(0,0,0,0.12)" }
      },

      data: props.keywords.map(item => ({
        name: item.word,
        value: item.count
      }))
    }
  ]
}))
</script>

<style scoped>
.wordcloud-card {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 4px 0;
}

.chart {
  width: 100%;
  height: 460px;
}
</style>
