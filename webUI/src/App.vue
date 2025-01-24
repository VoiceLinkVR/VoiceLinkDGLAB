<template>
    <configPage/>
  </template>
  
  <script>
  import configPage from './components/config-page.vue'
  
  export default {
    name: 'App',
    components: {
        configPage
    }
  }
  </script>
  
  <style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
  </style>
  