<template>
<div class="news-deteil"> 
    <h2>{{detail.title}}</h2>//新闻标题，插值表达式用于动态渲染
    <p class="publishtime">发布时间：{{detail.publishtime}}</p>
   <div class="content" v-html="detail.content"></div>//新闻内容
</div>
  
</template>

<script setup>
import {ref,onMounted} from 'vue'
import {getNewsDetail} from '@/api/news'
import { useRoute, useRouter } from 'vue-router'
const route=useRoute()//创建获取路由信息的对象
const router=useRouter()//创建控制路由的对象
const detail=ref({})
const loadDetail= async()=>{
    const id=route.params.id//从路由中获取id
    const content= await getNewsDetail(id)//根据id获取内容对象
    detail.value=content.data

}
onMounted(()=>
    {
        loadDetail()//通过钩子函数在页面的html渲染之后，自动加载内容

    }
)

</script>


<style scoped>
.news-detail {
  padding: 16px;
}
.time {
  color: #999;
  margin: 8px 0 16px;
}
.content {
  line-height: 1.8;
}
</style>
