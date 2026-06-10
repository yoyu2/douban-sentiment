<template>
  <div class="wordcloud-card">
    <v-chart
      class="chart"
      :option="option"
      autoresize
    />
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

/* 莫兰迪低饱和配色 */
const colors = [
  "#46647A", // 灰蓝
  "#738290", // 蓝灰
  "#A67C7C", // 豆沙粉
  "#B39283", // 奶茶棕
  "#76938F", // 鼠尾草绿
  "#9A8C98", // 灰紫
  "#C4A484", // 浅驼色
  "#6B7A8F"  // 雾霾蓝
]

const option = computed(() => ({
  backgroundColor: "transparent",

  title: {
    text: "评论关键词",
    left: "center",
    top: 15,
    textStyle: {
      color: "#445566",
      fontSize: 22,
      fontWeight: 400,
      fontFamily:
        '"PingFang SC","SF Pro Display","Microsoft YaHei",sans-serif'
    }
  },

  tooltip: {
    backgroundColor: "rgba(255,255,255,0.9)",
    borderColor: "#E5E7EB",
    borderWidth: 1,
    textStyle: {
      color: "#4B5563"
    },
    formatter: params => {
      return `
        <div>
          <strong>${params.name}</strong><br/>
          出现次数：${params.value}
        </div>
      `
    }
  },

  series: [
    {
      type: "wordCloud",

      shape: "circle",

      left: "center",
      top: 60,

      width: "90%",
      height: "80%",

      /* 整体缩小 */
      sizeRange: [16, 45],

      /* 水平排列 */
      rotationRange: [0, 0],

      rotationStep: 0,

      /* 词语间距 */
      gridSize: 8,

      drawOutOfBound: false,

      textStyle: {
        fontFamily:
          '"PingFang SC","SF Pro Display","Microsoft YaHei",sans-serif',

        /* 不加粗 */
        fontWeight: 400,

        color: params => {
          return colors[
            params.dataIndex % colors.length
          ]
        }
      },

      emphasis: {
        focus: "self",

        textStyle: {
          shadowBlur: 8,
          shadowColor: "rgba(0,0,0,0.12)"
        }
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
  margin-top: 24px;
  height: 500px;
  border-radius: 12px;

  /* 磨砂玻璃 — 高透明度 */
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);

  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>