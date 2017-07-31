// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import VueFormGenerator from 'vue-form-generator'
import VueFormWizard from 'vue-form-wizard'

import App from './App'
import router from './router'

Vue.use(VueFormGenerator)
Vue.use(VueFormWizard)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
