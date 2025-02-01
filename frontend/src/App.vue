<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>

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
  overflow: hidden; 
}

main{
  width:100%;
  height: 100%;
  min-width: 100vh;
  min-height: 100vh;
}
</style>