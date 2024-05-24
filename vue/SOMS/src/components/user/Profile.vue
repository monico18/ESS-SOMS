<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useUserStore } from '../../stores/user.js'
import { useToast } from "vue-toastification"



const props = defineProps({
  errors: {
    type: Object,
    required: false,
  },
});

const userStore = useUserStore()
const toast = useToast()
const confirmationLeaveDialog = ref(null)
const editShow = ref(false)
const saving = ref(false);

const oldPassword = ref('');
const newPassword = ref('');
const confirmNewPassword = ref('');

let originalValueStr = ''
const editingUser = ref(Object.assign({},userStore.user) )


const userTitle = computed(()=>{
  if (!editingUser.value) {
    return ''
  }
  return saving.value ? 'Saving...' : 'Profile of ' + editingUser.value.username;
})

const save = async () => {
    saving.value = true;
    try {
        const userToSave = editingUser.value;
        const response = await axios.put(`/profile`, {
        email: userToSave.email,
        });
        editingUser.value.email = response.data.email;
        toast.success('User #' + editingUser.value.username + ' was updated successfully.');
    } catch (error) {
        console.error('Error saving user:', error);
        toast.error('Error saving user. Please try again.');
    } finally {
        saving.value = false;
    }
}

const cancel = () => {
  originalValueStr = JSON.stringify(editingUser.value)
  editShow.value = false
}

const savePasswordChanges = async () => {
  try {
      if(newPassword.value != confirmNewPassword.value){
        throw e
      }
        await axios.put(`/profile/password`, {
          oldPassword: oldPassword.value,
          newPassword: newPassword.value
        });
        toast.success('User #' + editingUser.value.username + ' has updated their password successfully.');
    } catch (error) {
        console.error('Error password user:', error);
        toast.error('Error password user. Please try again.');
    }
};
</script>
<template>
    <br>
    <br>
    <form class="row g-3 needs-validation" novalidate @submit.prevent="save">
    <h2 class="mt-5 mb-3">{{ userTitle }}</h2>
    <hr/>
    <div>
      <div class="w-75 pe-4">
        <div class="mb-3 px-1">
            <label for="inputName" class="form-label">Username</label> <br>
            <input
              type="text"
              class="form-control edit_input"
              placeholder="Username"
              disabled
              style="background-color: #3d3939;"
              v-model="editingUser.username"
            />
          </div>
          <div class="mb-3 px-1">
            <label for="inputEmail" class="form-label">Email</label> <br>
            <input
              type="email"
              class="form-control edit_input"
              :class="{ 'is-invalid': errors ? errors['email'] : false }"
              placeholder="Email"
              required
              v-model="editingUser.email"
              v-if="editShow"
            />
            <field-error-message :errors="errors" fieldName="email"></field-error-message>

            <input
              v-if="!editShow"
              type="text"
              class="form-control edit_input"
              placeholder="Username"
              disabled
              style="background-color: #3d3939;"
              v-model="editingUser.email"
            />
          </div>
        </div>
      </div>
        <div class="d-flex justify-content-start">
          <button type="button" class="btn btn-outline-info px-5 mx-2" v-if="editShow" @click="save">Save</button>
          <button type="button" class="btn btn-outline-secondary px-5 mx-2" v-if="editShow" @click="cancel">Cancel</button>
          <button type="button" class="btn btn-outline-secondary px-5 mx-2" v-if="!editShow" @click="editShow=!editShow">Edit</button>
          <button type="button" class="btn btn-outline-secondary px-5 mx-2" v-if="!editShow" data-bs-toggle="modal" data-bs-target="#changePass">Change Password</button>
        </div>
        <div class="modal fade" id="changePass" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="changePassLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content bg-dark">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="changePassLabel">Change Password</h1>
              <button type="button" class="btn-close" style="background-color: lightgray;" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <label for="inputEmail" class="form-label">Old Password</label> <br>
                <input
                v-if="!editShow"
                type="password"
                class="form-control edit_pass"
                placeholder="Old Password"
                required
                v-model="oldPassword"
                />
                <br>
              <label for="inputEmail" class="form-label">New Password</label> <br>
                <input
                  v-if="!editShow"
                  type="password"
                  class="form-control edit_pass"
                  placeholder="New Password"
                  required
                  v-model="newPassword"
                  />
                  <br>
              <label for="inputEmail" class="form-label">Confirm New Password</label> <br>
                <input
                  v-if="!editShow"
                  type="password"
                  class="form-control edit_pass"
                  placeholder="Confirm New Password"
                  required
                  v-model="confirmNewPassword"
                />
              <br>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-info" @click="savePasswordChanges()">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
      </form>
</template>
<style>
.edit_input{
    color:lightgray;
    background-color: #3d3939;
    width: 500px;
}
.edit_input:focus {
  background-color: #3d3939;
  outline: none; 
}
.edit_pass{
  color:lightgray !important;
  background-color: #3d3939;
}
.edit_pass::placeholder{
  color: lightgray;
}
.edit_pass:focus {
  background-color: #3d3939;
  outline: none; 
}
</style>