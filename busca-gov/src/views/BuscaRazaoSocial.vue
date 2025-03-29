<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import SearchComponent from '../components/SearchComponent.vue';
</script>

<template>
    <HeaderComponent></HeaderComponent>
    <h2>Aqui a busca está sendo feita atráve da Razão Social</h2>
    <SearchComponent searchType="razaoSocial"></SearchComponent>
</template>

<style scoped>
h2 {
    display: flex;
    justify-content: center;
}
</style>