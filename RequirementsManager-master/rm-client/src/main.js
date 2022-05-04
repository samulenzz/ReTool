import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import './plugins/vue_table_with_tree_grid.js'
// 导入全局样式表
import './assets/css/global.css'
// 导入axios
import axios from 'axios'

// 配置URL
// axios.defaults.baseURL = 'http://127.0.0.1:5000'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
