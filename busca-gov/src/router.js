import { createRouter, createWebHistory } from 'vue-router'
import BuscaRazaoSocial from './views/BuscaRazaoSocial.vue'
import BuscaCNPJ from './views/BuscaCNPJ.vue'
import BuscaANS from './views/BuscaANS.vue'

const routes = [
  { path: '/', component: BuscaRazaoSocial },
  { path: '/buscaCnpj', component: BuscaCNPJ },
  { path: '/buscaAns', component: BuscaANS }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
