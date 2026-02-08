<template>
<div>
      <el-card 
      class="news-card"
      @click="goDetail(news.id)">
      <h3>{{news.title}}</h3>
       <p>{{ news.summary }}</p>
      <span>{{ news.publishTime }}</span>
      </el-card>
</div>
</template>
<script setup>
import{useRouter}  from 'vue-router'
const props=defineProps({//调用vue内置宏
    news:{//定义一个prop名为news
        type:Object,//传入的类型必须是js对象
        required:true//强制必须传递
    }
})
const router=useRouter()
const goDetail=()=>{
    router.push('/newsDetail/${props.news.id}')
}

</script>
<style scoped>
.news-card {
  margin: 12px 0;
  cursor: pointer;
}
.news-card:hover {
  background: #f7f7f7;
}
.title {
  font-size: 16px;
  margin-bottom: 6px;
}
.summary {
  color: #666;
  margin: 6px 0;
}
.time {
  color: #999;
  font-size: 12px;
}
    
</style>