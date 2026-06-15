import axios from "axios"

export const API_BASE = ""

const api = axios.create({
    baseURL: API_BASE
})

export function getMovies() {
    return api.get("/api/movies")
}
export function searchMovies(query) {
    return api.get("/api/movies/search", { params: { q: query } })
}
export function getMovieStatistics(movieName) {
    return api.get(`/api/movies/${movieName}/statistics`)
}
export function getMovieComments(movieName, params = {}) {
    return api.get(`/api/movies/${movieName}/comments`, { params })
}