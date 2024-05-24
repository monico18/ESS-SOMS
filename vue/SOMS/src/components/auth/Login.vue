<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useToast } from "vue-toastification"
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user.js'

const toast = useToast()
const router = useRouter()
const userStore = useUserStore()

const credentials = ref({
      username: '',
      password: ''
  })



  const login = async () => {
  if (await userStore.login(credentials.value)) {
    toast.success('Username ' + userStore.user.username + ' has entered the application.')
    if(userStore.user.type == 'admin'){
      router.push({name: 'AdminDashboard'})
    }else{
     router.push({name: 'Dashboard'})
    }
    
  } else {
    credentials.value.password = ''
  }
}

const clickMenuOption = () => {
  const domReference = document.getElementById('buttonSidebarExpandId');
  if (domReference && window.getComputedStyle(domReference).display !== "none") {
    domReference.click();
  }
};
</script>
<template>
  <div class="center-container" style="margin-top: 50px;">
    <div class="p-card p-shadow-2 p-mb-4 p-border-rounded" style="width: 100%; max-width: 360px;">
      <div class="text-center p-mb-5">
        <h1> SOMS </h1>
        <h2>Smart Occupancy Management System</h2>
        <br>
        <div class="text-3xl p-font-weight-bold p-mb-3">Welcome Back</div>
        <span class="text-600">Don't have an account?</span>
        <router-link :to="{ name: 'Register' }" :class="{ active: $route.name === 'Register' }" @click="clickMenuOption">
          <a href="#" class="p-font-weight-bold p-ml-2 p-text-blue p-cursor-pointer">Create today!</a>
        </router-link>
      </div>
      <br>
      <form @submit.prevent="signIn">
        <div class="form-group">
          <input type="text" class="form-control bg-dark custom-text-color" placeholder="Username" v-model="credentials.username" required autofocus>
        </div>
        <br>
        <div class="form-group">
          <input type="password" class="form-control bg-dark custom-text-color" placeholder="Password" v-model="credentials.password" required>
        </div>
        <br>
        <!-- 

          Remember me ??

        -->
        <button type="submit" class="btn btn-secondary" @click="login">Sign In</button>
      </form>
    </div>
  </div>
</template>

<style>
.center-container {
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;
  height: 50vh; 
}
.custom-text-color::placeholder {
  color: white;
}

.custom-text-color {
  color: white;
}
.form-control:focus {
  color: white;
}
</style>
