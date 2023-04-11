<template>
    <div class="about container">
        <h2 class="pb-4">Movie Form</h2>
        
        <div v-if="successMessage" class="alert alert-success" role="alert">{{ successMessage }}</div>
        <div v-if="errors.length > 0">
            <div v-for="error in errors" :key="error.field">
                <li class="alert alert-danger" role="alert">Error in {{ error.field }} - {{ error.message }}</li>
            </div>
        </div>

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
                    <label for="poster" class="form-label">Poster Photo Upload</label>
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
let successMessage = ref("");
let errors = ref([]);

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
        if (data.errors && data.errors.length > 0) {
            errors.value = data.errors;
        } else {
            successMessage.value = "File Upload Successful";
            errors.value = "";
        }
        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
        errors.value = error.data;
    });
};
</script>

<style>
    textarea {
        height: 200px
    }
</style>