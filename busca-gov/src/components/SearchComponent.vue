<template>
    <div class="search-container">
    <input
      type="text"
      v-model="searchQuery"
      class="search-input"
      placeholder="Pesquise algo..."
    />
    <button @click="search" class="search-button">
        <img src="../assets/ic--baseline-search.svg" alt="" srcset="" class="search-icon">
    </button>
  </div>

  <div class="table-container" v-if="results.length > 0">
      <table class="results-table">
        <thead>
          <tr>
            <th>ANS</th>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Modalidade</th>
            <th>Endereço</th>
            <th>Número</th>
            <th>Cidade</th>
            <th>UF</th>
            <th>Telefone</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="index">
            <td>{{ item.Registro_ANS }}</td>
            <td>{{ item.CNPJ }}</td>
            <td>{{ item.Razao_Social }}</td>
            <td>{{ item.Nome_Fantasia }}</td>
            <td>{{ item.Modalidade }}</td>
            <td>{{ item.Logradouro }}, {{ item.Numero }}</td>
            <td>{{ item.Numero }}</td>
            <td>{{ item.Cidade }}</td>
            <td>{{ item.UF }}</td>
            <td>{{ item.Telefone !== 'nan' ? item.Telefone : 'N/D' }}</td>
            <td>{{ item.Endereco_eletronico }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <p class="message-error" v-else-if="results.length === 0">Nenhum resultado encontrado.</p>
</template>

<script>
import SearchService from '../service/SearchService';
export default {
  name: "SearchComponent",
  props:{
    searchType: String,
    required: true,
  },
  data() {
    return {
      searchQuery: "",
      results: [],
    };
  },
  methods: {
    search() {
      console.log(`Buscando por: ${this.searchQuery}, Tipo: ${this.searchType}`);

      let searchMethod;
      if (this.searchType === "razaoSocial") {
        searchMethod = SearchService.getByRazaoSocial;  
      } else if (this.searchType === "ans") {
        searchMethod = SearchService.getByANS;  
      } else if (this.searchType === "cnpj") {
        searchMethod = SearchService.getByCNPJ;  
      } else {
        console.error("Tipo de busca inválido!");
        return;
      }

    // chamando a requisição com base no tipo
      searchMethod(this.searchQuery)
        .then((response) => {
          this.results = response.data;
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Erro ao buscar dados:", error);
        });
    },
  },
};
</script>

<style scoped>
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
}
.search-input {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 25px;
  border: 1px solid #ccc;
  outline: none;
  transition: border-color 0.3s ease;
  width: 300px;
}
.search-input:focus {
  border-color: #4caf50;
}
.search-button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  margin-left: 0.5rem;
  transition: background-color 0.3s ease;
}
.search-button:hover {
  background-color: #45a049;
}
.search-icon{
    display: flex;
    justify-content: center;
}
.message-error{
    display: flex;
    justify-content: center;
}
.table-container{
    padding: 2rem;
}
.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.results-table th,
.results-table td {
  padding: 6px;
  text-align: left;
  border: 1px solid #000;
}

.results-table th {
  background-color: #cfcfcf;
  font-weight: bold;
}

/* Melhorando a responsividade */
@media (max-width: 768px) {
  .search-input {
    width: 200px;
  }
  .search-button {
    font-size: 0.9rem;
  }
}
</style>