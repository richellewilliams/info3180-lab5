<template>
    <div class="about container">
        <h2 class="pb-4">Movie Form</h2>
        <form @submit.prevent="saveMovie" id="movieForm">
            <div class="form-group">
                <div class="form-group pb-4">
                    <label for="title" class="form-label">Movie Title</label>
                    <input type="text" name="title" class="form-control"/>
                </div>
                
                <div class="form-group pb-4">
                    <label for="description" class="form-label">Description</label>
                    <textarea type="text" name="description" class="form-control"></textarea>
                </div>

                <div class="form-group pb-4">
                    <label for="poster" class="form-label">Photo Upload</label>
                    <input type="file" name="poster" class="form-control"/>
                </div>
                <button class="btn btn-primary" type="submit">Submit</button>
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
let csrf_token = ref("");

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    })
}

onMounted(() => {
    getCsrfToken();
});

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        // display a success message
        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
    });
};
</script>

<style>
    textarea {
        height: 200px
    }
</style>