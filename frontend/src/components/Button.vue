<template>
    <button :class="buttonClass" @click="handleClick">
      {{ buttonText }}
    </button>
  </template>
  
  <script>
  export default {
    props: {
      buttonText: {
        type: String,
        required: true
      },
      color: {
        type: String,
        default: 'blue' // Default color if no prop is passed
      }
    },
    computed: {
      buttonClass() {
        return `btn-${this.color}`;
      }
    },
    methods: {
      handleClick() {
        this.$emit('click');
      }
    }
  }
  </script>
  
  <style scoped>
  button {
    padding: 10px 15px;
    font-size: 16px;
    height: 3rem;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    opacity: 0.8;
  }
  
  /* Add specific colors based on the color prop */
  .btn-blue {
   
    background-color: #007bff;
  }
  
  .btn-green {
    background-color: #28a745;
  }
  
  </style>
  