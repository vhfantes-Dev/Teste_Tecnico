<template>
    <header class="header">
      <h1>Busca GOV</h1>
      <nav>
        <ul>
          <li> <router-link to="/">Busca Razão Social</router-link></li>
          <li> <router-link to="/buscaAns">Busca ANS</router-link></li>
          <li> <router-link to="/buscaCnpj">Busca CNPJ</router-link></li>
        </ul>
        
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: 'HeaderComponent',
  };
  </script>
  
  <style scoped>
  .header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5rem;
    background-color: #333;
    color: white;
  }
  nav ul {
    list-style: none;
    display: flex;
    gap: 1rem;
    padding: 0;
  }
  nav a {
    color: white;
    text-decoration: none;
  }
  </style>
  