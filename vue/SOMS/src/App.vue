<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useToast } from "vue-toastification"


const toast = useToast()
const router = useRouter();


const clickMenuOption = () => {
  const domReference = document.getElementById('buttonSidebarExpandId');
  if (domReference && window.getComputedStyle(domReference).display !== "none") {
    domReference.click();
  }
};

</script>

<template>
  <div>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark sticky-top flex-md-nowrap shadow">
      <div class="svg-container" style="margin-left: 0.8rem;">
        <p>ola</p>
      </div>
    <div class="collapse navbar-collapse justify-content-start" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
            Dashboard
        </li>
      </ul>
    </div>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
            Sign In
        </li>
      </ul>
    </div>
</nav>
    <main class="container">
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<style scoped>
@import "./assets/dashboard.css";

.svg-container {
  width: 200px; /* Adjust width as needed */
  height: auto; /* Adjust height as needed */
}
.navbar{
  padding-top: 10px ;
  padding-bottom: 10px;
  width: 100%;
}


.nav-link.active {
  background-color: rgba(76, 67, 67, 0);
}
</style>
