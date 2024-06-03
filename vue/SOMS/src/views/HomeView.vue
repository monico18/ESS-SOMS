<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const clickMenuOption = () => {
  const domReference = document.getElementById('buttonSidebarExpandId');
  if (domReference && window.getComputedStyle(domReference).display !== "none") {
    domReference.click();
  }
};
</script>

<template >
  <div class="about">
    <br><br>
    <h1>Welcome to SOMS</h1>
    <h3>Your very own Smart Occupancy Manager System</h3>
    <br>
    <br>
    <router-link class="nav-link btn btn-outline-secondary btn-large" :to="{ name: 'Login' }" :class="{ active: $route.name === 'Login' }" @click="clickMenuOption">
            Login
    </router-link>
  </div>
  <div class="centered-text">
    <h5>Made by :</h5>
    <h7>Pedro Manuel Pena Antunes</h7>
    <h7>Tomas Mónico Santos</h7>
    <h7>João Pedro Freitas Frutuoso Fabião Antunes</h7>
  </div>
</template>

<style scoped>
@media (min-width: 1024px) {
  .about {
    display: flex;
    align-items: center;
    flex-direction: column;
    position: absolute;
    top: 12%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
  }

  .centered-text {
    display: flex;
    flex-direction: column;
    text-align: start; 
    position: fixed;
    bottom: 20px; 
    left: 50%;
    transform: translateX(-50%);
    width: 100%; 
    margin-left: 5px;
  }
}
.image-hashkitty{
    width: 300px;
  }
.btn-large {
  padding: 20px 40px; /* Adjust padding as needed */
  font-size: 50px; /* Adjust font size as needed */
}
</style>
