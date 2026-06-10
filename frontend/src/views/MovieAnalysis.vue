<script setup>
import { ref, onMounted, computed } from "vue"
import { useRoute } from "vue-router"
import { getMovieStatistics } from "../api/movie"
import { exportReport } from "../utils/export"

import SentimentPie from "../components/SentimentPie.vue"
import RatingBar from "../components/RatingBar.vue"
import WordCloud from "../components/WordCloud.vue"

const route = useRoute()
const movieName = decodeURIComponent(route.params.name)

const statistics = ref(null)
const downloading = ref(false)

const sentiment = computed(() => statistics.value?.sentiment || {})
const summary = computed(() => statistics.value?.summary || {})
const rating = computed(() => statistics.value?.rating_distribution || {})
const keywords = computed(() => statistics.value?.keywords || [])

// 截图容器 ref
const statsRef = ref(null)
const pieRef = ref(null)
const barRef = ref(null)
const wordCloudRef = ref(null)

onMounted(async () => {
  const res = await getMovieStatistics(movieName)
  statistics.value = res.data
})

async function handleDownload() {
  downloading.value = true
  try {
    await exportReport(movieName, [
      { name: "01_数据概览", el: statsRef.value },
      { name: "02_情感分布", el: pieRef.value },
      { name: "03_评分分布", el: barRef.value },
      { name: "04_关键词云", el: wordCloudRef.value },
    ])
  } catch (e) {
    console.error("导出失败", e)
  } finally {
    downloading.value = false
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
      <h1>{{ movieName }}</h1>
      <button
        class="download-btn"
        :disabled="downloading || !statistics"
        @click="handleDownload"
      >
        <span v-if="downloading" class="spinner" />
        <span v-else>📥</span>
        {{ downloading ? "导出中..." : "导出报告" }}
      </button>
    </div>

    <!-- 数据概览 -->
    <div ref="statsRef" class="stats-container">
      <div class="card">
        <h3>评论数</h3>
        <p>{{ sentiment.total_comments }}</p>
      </div>
      <div class="card">
        <h3>平均评分</h3>
        <p>{{ summary.average_rating }}</p>
      </div>
      <div class="card">
        <h3>情感倾向</h3>
        <p>{{ summary.main_sentiment }}</p>
      </div>
    </div>

    <!-- 情感分析 -->
    <h2>情感分析</h2>
    <div ref="pieRef">
      <SentimentPie :sentiment="sentiment" />
    </div>

    <!-- 评分分析 -->
    <h2>评分分析</h2>
    <div ref="barRef">
      <RatingBar
        v-if="Object.keys(rating).length"
        :rating="rating"
      />
    </div>

    <!-- 关键词云 -->
    <h2>关键词分析</h2>
    <div ref="wordCloudRef">
      <WordCloud
        v-if="keywords.length"
        :keywords="keywords"
      />
    </div>
  </div>
</template>

<style scoped>
.stats-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  background: #fff;
  padding: 12px 0;
}

.card {
  width: 200px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: #fff;
}

.card h3 {
  margin-bottom: 10px;
}

.card p {
  font-size: 28px;
  font-weight: bold;
}

.download-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.download-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.download-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
