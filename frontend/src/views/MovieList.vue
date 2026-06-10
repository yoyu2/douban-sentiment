<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { getMovies } from "../api/movie"

const movies = ref([])
const router = useRouter()

onMounted(async () => {
  const res = await getMovies()
  movies.value = res.data.movies
})

function openMovie(movieName) {
  router.push(`/movie/${movieName}`)
}
</script>

<template>

  <div>

    <h1>豆瓣影评情感分析平台</h1>

    <ul>

      <li
        v-for="movie in movies"
        :key="movie"
        @click="openMovie(movie)"
      >
        {{ movie }}
      </li>

    </ul>

  </div>

</template>