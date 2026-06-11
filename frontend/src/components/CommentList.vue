<script setup>
import { ref, watch } from "vue"
import { getMovieComments } from "../api/movie"

const props = defineProps({
  movieName: { type: String, required: true },
  commentType: { type: String, default: "latest" }
})

const comments = ref([])
const loading = ref(false)
const total = ref(0)
const activeFilter = ref("all")

const filters = [
  { key: "all", label: "全部" },
  { key: "positive", label: "正面" },
  { key: "neutral", label: "中性" },
  { key: "negative", label: "负面" }
]

const sentimentLabel = {
  positive: "正面",
  neutral: "中性",
  negative: "负面"
}

async function loadComments() {
  loading.value = true
  try {
    const params = { type: props.commentType }
    if (activeFilter.value !== "all") {
      params.sentiment = activeFilter.value
    }
    const res = await getMovieComments(props.movieName, params)
    comments.value = res.data.comments || []
    total.value = res.data.count || 0
  } catch (e) {
    console.error("加载评论失败", e)
    comments.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function switchFilter(key) {
  activeFilter.value = key
}

// 当筛选条件或影片变化时重新加载
watch(
  () => [activeFilter.value, props.movieName, props.commentType],
  loadComments,
  { immediate: true }
)

function renderStars(rating) {
  const n = Number(rating) || 0
  return "★".repeat(n) + "☆".repeat(5 - n)
}
</script>

<template>
  <div class="comment-list-section">
    <!-- 筛选栏 -->
    <div class="filter-bar">
      <span class="filter-label">评论筛选</span>
      <div class="filter-buttons">
        <button
          v-for="f in filters"
          :key="f.key"
          :class="['filter-btn', { active: activeFilter === f.key }]"
          @click="switchFilter(f.key)"
        >
          {{ f.label }}
        </button>
      </div>
      <span class="filter-count">共 {{ total }} 条</span>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <span class="spinner" />
      加载中...
    </div>

    <!-- 空状态 -->
    <div v-else-if="comments.length === 0" class="empty-state">
      <span class="empty-icon">💬</span>
      <p>暂无评论数据</p>
    </div>

    <!-- 评论列表 -->
    <div v-else class="comment-cards">
      <div
        v-for="(comment, index) in comments"
        :key="index"
        class="comment-card"
      >
        <div class="comment-body">
          <p class="comment-content">{{ comment.content }}</p>
          <div class="comment-meta">
            <span
              :class="['sentiment-badge', comment.sentiment || 'neutral']"
            >
              {{ sentimentLabel[comment.sentiment] || "中性" }}
            </span>
            <span class="comment-rating">{{ renderStars(comment.rating) }}</span>
            <span
              v-if="comment.time"
              class="comment-time"
            >{{ comment.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-list-section {
  margin-top: 32px;
}

/* ========== 筛选栏 ========== */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
}

.filter-label {
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

.filter-buttons {
  display: flex;
  gap: 6px;
  flex: 1;
}

.filter-btn {
  padding: 6px 16px;
  font-size: 13px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.55);
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.filter-btn.active {
  background: #6366f1;
  color: #fff;
  border-color: #6366f1;
}

.filter-count {
  color: #9ca3af;
  font-size: 13px;
  white-space: nowrap;
}

/* ========== 加载 / 空状态 ========== */
.loading-state,
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 60px 20px;
  color: #9ca3af;
  font-size: 15px;
}

.empty-icon {
  font-size: 32px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(99, 102, 241, 0.2);
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========== 评论卡片 ========== */
.comment-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-card {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s;
}

.comment-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.comment-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.comment-content {
  font-size: 15px;
  line-height: 1.7;
  color: #1f2937;
  margin: 0;
}

.comment-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.sentiment-badge {
  display: inline-block;
  padding: 2px 10px;
  font-size: 12px;
  border-radius: 12px;
  font-weight: 500;
}

.sentiment-badge.positive {
  background: #dcfce7;
  color: #16a34a;
}

.sentiment-badge.neutral {
  background: #f3f4f6;
  color: #6b7280;
}

.sentiment-badge.negative {
  background: #fef2f2;
  color: #dc2626;
}

.comment-rating {
  font-size: 14px;
  color: #f59e0b;
  letter-spacing: 1px;
}

.comment-time {
  font-size: 12px;
  color: #9ca3af;
}
</style>
