// src/router/index.js

import { createRouter, createWebHistory }
from "vue-router"

import MovieList
from "../views/MovieList.vue"

import MovieAnalysis
from "../views/MovieAnalysis.vue"

const routes = [

  {
    path: "/",
    component: MovieList
  },

  {
    path: "/movie/:name",
    component: MovieAnalysis
  }

]

const router = createRouter({

  history: createWebHistory(),

  routes

})

export default router