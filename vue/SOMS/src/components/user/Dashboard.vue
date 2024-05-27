<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const apiKey = 'c321147f32bb6d31e61b897e4d724a3e';
const city = ref('Leiria');

const weatherDescription = ref('');
const temperature = ref('');
const humidity = ref('');

let intervalId = null;

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
      weatherDescription.value = weatherData.weather[0].description;
      temperature.value = weatherData.main.temp;
      humidity.value = weatherData.main.humidity;
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

const videoUrl = ref('http://10.0.0.5:5000/video_feed');

</script>   
<template>
    <br>
    <br>
    <div class="d-flex justify-content-center">
      <h1>Welcome User</h1>
    </div>
    <div class="weather-info">
      <h3>Weather in {{ city }}:</h3>
      <h6>Description: {{ weatherDescription }}</h6>
      <h6>Temperature: {{ temperature }} °C</h6>
      <h6>Humidity: {{ humidity }}%</h6>
    </div>
    <br>
    <div class="d-flex justify-content-center">
      <h3>Live Feed</h3>
    </div>
    <div class="d-flex justify-content-center">
      <img :src="videoUrl" alt="Live Stream" class="live-stream">
    </div>

</template>
<style>
.form-select-bg-position {
  width: 250px;
}
.form-selectmultiple-bg-position{
    width: 650px;
    height: 150px;
}
.move-input{
    margin-right: 350px;
    width: 300px;
}
.move-textarea{
    width: 650px;
    height: 200px;
}
.algorithms{
    display: flexbox;
    flex-direction: row;
}
.weather-info {
  text-align: center;
  margin-top: 20px;
}
.live-stream {
  width: 640px;
  height: 480px;
}
</style>