import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export default {
    getByRazaoSocial(query) {
        return axios.get(`${API_URL}/razao-social`, {
          params: {
            query: query, // Passando o parâmetro 'query'
          },
        });
      },
    getByANS(query) {
        return axios.get(`${API_URL}/registro-ans`, {
            params: {
              query: query, 
            },
          });
    },
    getByCNPJ(query) {
        return axios.get(`${API_URL}/cnpj`, {
            params: {
              query: query,
            },
          });
    },
};
