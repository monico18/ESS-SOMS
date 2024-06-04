<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import io from 'socket.io-client';


const apiKey = 'c321147f32bb6d31e61b897e4d724a3e';
const city = ref('Leiria');

const weatherDescription = ref('');
const temperature = ref('');
const humidity = ref('');
const freeSpaces = ref(0);
const photo = ref("");
const showVideoFeed = ref(true);
const weatherIconClass = ref("")
const weatherIcons = {
  'Clear': 'bi bi-sun', 
  'Rain': 'bi bi-cloud-rain',
  'Clouds': 'bi bi-cloud',
  'Snow': 'bi bi-snow',
  'Mist': 'bi bi-cloud'
};
let intervalId = null;
let videoBuffer = [];
const bufferSize = 30; 
let frameIntervalId = null;


const fetchWeather = async () => {
  const baseUrl = 'https://api.openweathermap.org/data/2.5/weather';
  const params = new URLSearchParams({
    q: city.value,
    appid: apiKey,
    units: 'metric'
  });

  try {
    const response = await fetch(`${baseUrl}?${params.toString()}`);
    if (response.ok) {
      const weatherData = await response.json();
      weatherDescription.value = weatherData.weather[0].main;
      temperature.value = weatherData.main.temp;
      humidity.value = weatherData.main.humidity;
      weatherIconClass.value = weatherIcons[weatherDescription.value] || 'bi bi-question';
    } else {
      console.error(`Error: Failed to retrieve weather data (HTTP ${response.status})`);
    }
  } catch (error) {
    console.error(`Error: ${error}`);
  }
};

const startFetching = () => {
  if (!intervalId) {
    fetchWeather();
    intervalId = setInterval(fetchWeather, 30000); 
  }
};

const stopFetching = () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
};

onMounted(startFetching);
onUnmounted(stopFetching);

const videoUrl = ref('http://10.0.0.5:5000/video_ipl');
const socket = io('http://10.0.0.5:5000'); 

socket.on('free_spaces_live', (data) => {
  freeSpaces.value = data.free_spaces;
  const base64Image_live = 'data:image/jpeg;base64,' + data.image;
  if (videoBuffer.length < bufferSize) {
    videoBuffer.push(base64Image_live);
  } else {
    videoBuffer.shift();
    videoBuffer.push(base64Image_live);
  }
});

socket.on('free_spaces', (data) => {
  freeSpaces.value = data.free_spaces;
  photo.value = 'data:image/jpeg;base64,' + data.image;
});

const showCurrentPhoto = () => {
  showVideoFeed.value = false;
};

const showLive = () => {
  showVideoFeed.value = true;
  startFrameInterval();
};

const startFrameInterval = () => {
  if (!frameIntervalId) {
    frameIntervalId = setInterval(() => {
      if (videoBuffer.length > 0) {
        photo.value = videoBuffer.shift();
      }
    }, 1000 / 30); 
  }
};

const stopFrameInterval = () => {
  if (frameIntervalId) {
    clearInterval(frameIntervalId);
    frameIntervalId = null;
  }
};

</script>   
<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-6 mb-3">
        <div class="card bg-dark text-gray same-height">
          <div class="card-body text-center">
            <h3 class="card-title text-gray">Weather in {{ city }}</h3>
            <div v-if="loading" class="spinner-border text-primary" role="status">
              <span class="sr-only">Loading...</span>
            </div>
            <div v-else>
              <div class="weather-description mb-2">
                <span>{{ weatherDescription }}&nbsp;</span>
                <i :class="weatherIconClass" class="ml-2"></i>
              </div>
              <p class="card-text">Temperature: {{ temperature }} °C</p>
              <p class="card-text">Humidity: {{ humidity }}%</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6 mb-3">
        <div class="card bg-dark text-gray same-height">
          <div class="card-body text-center">
            <h3 class="card-title text-gray">Video</h3>
            <p class="card-text">Free Spaces: {{ freeSpaces }}</p>
            <button v-if="showVideoFeed" class="btn btn-secondary" @click="showCurrentPhoto" aria-label="Show Current Photo">Show Current Photo</button>
            <button v-if="!showVideoFeed" class="btn btn-secondary" @click="showLive" aria-label="Show Live Feed">Show Live Feed</button>
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex justify-content-center">
      <div v-if="showVideoFeed">
        <img :src="videoUrl" alt="Live Stream" class="live-stream">
      </div>
      <div v-else>
        <img :src="photo" alt="Current Photo" class="live-stream">
      </div>
    </div>
  </div>
</template>
<style>
body {
  background-color: #121212; 
  color: #c0c0c0; 
}

.form-select-bg-position {
  width: 250px;
}
.form-selectmultiple-bg-position {
  width: 650px;
  height: 150px;
}
.move-input {
  margin-right: 350px;
  width: 300px;
}
.move-textarea {
  width: 650px;
  height: 200px;
}
.algorithms {
  display: flexbox;
  flex-direction: row;
}
.weather-info {
  text-align: center;
  margin-top: 20px;
}
.live-stream {
  width: 1080px;
  height: 560px;
}
.weather-description {
  transition: all 0.3s ease;
}
.weather-description i {
  margin-left: 5px;
  transition: transform 0.3s ease;
}
.weather-description:hover i {
  transform: scale(1.2);
}
.card {
  background-color: #1e1e1e; /* Darker card background */
  color: #c0c0c0; /* Gray text color */
}
.text-gray {
  color: #c0c0c0;
}
.form-control.bg-dark {
  background-color: #1e1e1e; 
  color: #c0c0c0; 
}
.same-height {
  height: 100%;
}
</style>
