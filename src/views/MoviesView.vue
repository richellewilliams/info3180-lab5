<template>
  <div class="about container">
    <h2 class="pb-3">Movies</h2>

    <div class="row row-cols-2 g-4">
      <div v-for="movie in movies" :key="movie.id">
        <div class="card mb-3">
            <div class="col-md-4">
              <img :src="movie.poster" alt="Movie Poster" class="card-img-top">
            </div>

            <div class="col-md-8">
              <div class="card-body">
                <h3 class="card-title">{{ movie.title }}</h3>
                <p class="card-text">{{ movie.description }}</p>
              </div>
            </div>
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
        movies.value = data.data;
    })
    .catch((error) => {
        console.log(error);
    });
}

onMounted(()=> {
    fetchMovies();
});
</script>

<style>
.card {
    width: 600px;
    flex-direction: row;
}
</style>