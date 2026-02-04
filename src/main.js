import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import {createPinia} from 'pinia'
import ElementPlus from 'element-plus'
const app=createApp(App)
app.use(router)
app.use(createPinia())
app.use(ElementPlus)
app.mount('#app')

