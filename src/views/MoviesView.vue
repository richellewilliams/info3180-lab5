<template>
  <div class="about container">
    <h2 class="pb-4">Movies</h2>
    <div>
        <div v-for="movie in movies" :key="movie.id" class="card">
      <img :src="movie.poster" alt="Movie Poster" class="card-img-top">
      <div class="card-body">
        <h3 class="card-title">{{ movie.title }}</h3>
        <p class="card-text">{{ movie.description }}</p>
      </div>
    </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
let movies = ref([]);

function fetchMovies(){
    fetch('/api/v1/movies')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        movies.value = data;
    })
    .catch((error) => {
        console.log(error);
    })
}

onMounted(()=> {
    fetchMovies()
});
</script>