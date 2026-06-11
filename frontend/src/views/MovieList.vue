<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getMovies, API_BASE } from "../api/movie"

const movies = ref([])
const router = useRouter()

onMounted(async () => {
  const res = await getMovies()
  // 兼容旧格式（字符串数组）和新格式（对象数组）
  const raw = res.data.movies || []
  movies.value = raw.map(item =>
    typeof item === "string" ? { name: item, poster: null } : item
  )
})

function openMovie(movieName) {
  router.push(`/movie/${encodeURIComponent(movieName)}`)
}

function posterUrl(movie) {
  if (!movie.poster) return ""
  return API_BASE + movie.poster
}
</script>

<template>
  <div class="movie-list-page">
    <!-- 首页标题 -->
    <header class="hero">
      <div class="hero-badge">🎬</div>
      <h1 class="hero-title">豆瓣影评情感分析平台</h1>
    </header>

    <div v-if="movies.length === 0" class="empty-state">
      <span>暂无影片数据，请先运行爬虫抓取影评</span>
    </div>

    <div v-else class="movie-grid">
      <div
        v-for="movie in movies"
        :key="movie.name"
        class="movie-card"
        @click="openMovie(movie.name)"
      >
        <div class="poster-wrapper">
          <img
            v-if="movie.poster"
            :src="posterUrl(movie)"
            :alt="movie.name"
            class="poster-img"
          />
          <div v-else class="poster-placeholder">
            <span class="placeholder-icon">🎞️</span>
          </div>
        </div>
        <div class="movie-name">{{ movie.name }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.movie-list-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 20px;
}

/* ========== 首页标题 ========== */
.hero {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding: 40px 20px 32px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  font-size: 28px;
  background: linear-gradient(135deg, #e0e7ff, #ede9fe);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.12);
  flex-shrink: 0;
}

.hero-title {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #4338ca, #6366f1, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.3;
}

/* ========== 空状态 ========== */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #9ca3af;
  font-size: 16px;
}

/* ========== 影片卡片网格 ========== */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 24px;
}

.movie-card {
  cursor: pointer;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* ========== 海报区 ========== */
.poster-wrapper {
  width: 100%;
  aspect-ratio: 3 / 4;
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
}

.placeholder-icon {
  font-size: 48px;
  opacity: 0.5;
}

/* ========== 影片名称 ========== */
.movie-name {
  padding: 12px 10px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
