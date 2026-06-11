<script setup>
import { ref, onMounted, computed } from "vue"
import { useRoute } from "vue-router"
import { getMovieStatistics, API_BASE } from "../api/movie"
import { exportReport } from "../utils/export"

import SentimentPie from "../components/SentimentPie.vue"
import RatingBar from "../components/RatingBar.vue"
import WordCloud from "../components/WordCloud.vue"
import CommentList from "../components/CommentList.vue"

const route = useRoute()
const movieName = decodeURIComponent(route.params.name || "")

const statistics = ref(null)
const downloading = ref(false)
const invalidMovie = computed(() => !movieName || movieName === "undefined")

const sentiment = computed(() => statistics.value?.sentiment || {})
const summary = computed(() => statistics.value?.summary || {})
const rating = computed(() => statistics.value?.rating_distribution || {})
const keywords = computed(() => statistics.value?.keywords || [])
const poster = computed(() => statistics.value?.poster || "")
const posterUrl = computed(() => poster.value ? API_BASE + poster.value : "")

// 截图容器 ref
const statsRef = ref(null)
const pieRef = ref(null)
const barRef = ref(null)
const wordCloudRef = ref(null)

onMounted(async () => {
  if (invalidMovie.value) return
  try {
    const res = await getMovieStatistics(movieName)
    statistics.value = res.data
  } catch (e) {
    console.error("加载统计数据失败", e)
  }
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
    <!-- 无效影片名 -->
    <div v-if="invalidMovie" class="error-state">
      <p>无效的影片名称，请从首页重新进入</p>
    </div>

    <div v-else>
    <!-- 影片头部：海报 + 标题 + 概览数据 + 导出 -->
    <div ref="statsRef" class="movie-header">
      <div class="poster-box">
        <img
          v-if="posterUrl"
          :src="posterUrl"
          :alt="movieName"
          class="poster-img"
        />
        <div v-else class="poster-placeholder">
          <span>🎞️</span>
        </div>
      </div>

      <div class="header-info">
        <h1 class="movie-title">{{ movieName }}</h1>
        <div class="header-stats">
          <div class="stat-item">
            <span class="stat-value">{{ sentiment.total_comments ?? "-" }}</span>
            <span class="stat-label">评论数</span>
          </div>
          <div class="stat-divider" />
          <div class="stat-item">
            <span class="stat-value">{{ summary.average_rating ?? "-" }}</span>
            <span class="stat-label">平均评分</span>
          </div>
          <div class="stat-divider" />
          <div class="stat-item">
            <span class="stat-value sentiment-value" :class="summary.main_sentiment">
              {{ summary.main_sentiment ?? "-" }}
            </span>
            <span class="stat-label">情感倾向</span>
          </div>
        </div>
      </div>

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

    <!-- 情感 + 评分并排 -->
    <div class="charts-row">
      <div class="chart-half" ref="pieRef">
        <SentimentPie :sentiment="sentiment" />
      </div>
      <div class="chart-half" ref="barRef">
        <RatingBar
          v-if="Object.keys(rating).length"
          :rating="rating"
        />
      </div>
    </div>

    <!-- 关键词云 -->
    <div ref="wordCloudRef">
      <WordCloud
        v-if="keywords.length"
        :keywords="keywords"
      />
    </div>

    <!-- 评论列表 -->
    <CommentList :movieName="movieName" commentType="hot" />
    </div>
  </div>
</template>

<style scoped>
.error-state {
  text-align: center;
  padding: 80px 20px;
  color: #9ca3af;
  font-size: 16px;
}

/* ========== 影片头部 ========== */
.movie-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  margin-bottom: 28px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 14px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}

.poster-box {
  flex-shrink: 0;
  width: 120px;
  height: 168px;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0e7ff, #fae8ff);
  font-size: 36px;
}

.header-info {
  flex: 1;
  min-width: 0;
}

.movie-title {
  font-size: 26px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.header-stats {
  display: flex;
  align-items: center;
  gap: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 20px;
}

.stat-item:first-child {
  padding-left: 0;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #374151;
}

.stat-value.sentiment-value.positive {
  color: #16a34a;
}

.stat-value.sentiment-value.negative {
  color: #dc2626;
}

.stat-value.sentiment-value.neutral {
  color: #6b7280;
}

.stat-label {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: #e5e7eb;
}

/* ========== 图表并排 ========== */
.charts-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-half {
  flex: 1;
  min-width: 0;
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
