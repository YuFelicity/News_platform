<template>
<div>
      <el-card 
      class="news-card"
      @click="goDetail(news.id)">
      <div class="heaer">
        <h3>{{news.title}}</h3>
         <!-- 用于当点击的收藏按钮的时候不会直接进入详情
         内容通过布尔值判断是否收藏过
         -->
        <el-button
         size="small"
         type="warning"
         @click.stop="onToggleFavorite"
         >
         {{isFavorite?'取消收藏':'收藏'}}
        </el-button>

      </div>
      
       <p>{{ news.summary }}</p>
      <span>{{ news.publishTime }}</span>
      </el-card>
</div>
</template>
<script setup>
import{useRouter}  from 'vue-router'
import {ref} from 'vue'
import{addFavorite,cancelFavorite}from '@/api/news'
import {ElMessage} from 'element-plus'

const props=defineProps({//调用vue内置宏
    news:{//定义一个prop名为news
        type:Object,//传入的类型必须是js对象
        required:true//强制必须传递
    }
  
})
const isFavorite=ref(false)
const router=useRouter()
const goDetail=()=>{
    router.push('/newsDetail/${props.news.id}')
}
const onToggleFavorite=async()=>{//点击按钮时要判断是否收藏过
  if(isFavorite.value===true)
  {
    await cancelFavorite(props.news.id)
    ElMessage.success('已取消收藏')
  }
  else{
    await addFavorite(props.news.id)
    ElMessage.success('已收藏')
  }

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
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
    
</style>