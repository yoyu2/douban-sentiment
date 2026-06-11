import axios from "axios"

export const API_BASE = "http://127.0.0.1:8000"

const api = axios.create({
    baseURL: API_BASE
})

export function getMovies() {
    return api.get("/api/movies")
}
export function getMovieStatistics(movieName) {
    return api.get(`/api/movies/${movieName}/statistics`)
}
export function getMovieComments(movieName, params = {}) {
    return api.get(`/api/movies/${movieName}/comments`, { params })
}