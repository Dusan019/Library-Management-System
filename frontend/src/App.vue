<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
/* Ensure the entire page takes up the full height and width of the viewport */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  min-width: 100vh;
  min-height: 100vh;
}

#app {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0;
  box-sizing: border-box;
  overflow: hidden; /* Prevent horizontal scroll */
}

main{
  width:100%;
  height: 100%;
  min-width: 100vh;
  min-height: 100vh;
}
</style>