<template>
  <div class="news-detail-container">
    <!-- 加载中 -->
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      加载中...
    </div>
    
    <!-- 新闻详情 -->
    <div v-else-if="news" class="news-detail">
      <div class="news-title">{{ news.title }}</div>
      
      <div class="news-meta">
        <span>作者: {{ news.author }}</span>
        <span>分类: {{ news.category }}</span>
        <span>{{ formatTime(news.publishTime) }}</span>
        <span>浏览: {{ news.views }}</span>
      </div>
      
      <div class="action-buttons">
        <el-button
          :type="isFavorite ? 'danger' : 'default'"
          @click="handleFavorite"
        >
          {{ isFavorite ? '已收藏' : '收藏' }}
        </el-button>
      </div>
      
      <div class="news-content" v-html="news.content"></div>
      
      <!-- 相关新闻 -->
      <div v-if="relatedNews.length > 0" class="related-news">
        <h3>相关新闻</h3>
        <div class="related-list">
          <div
            v-for="item in relatedNews"
            :key="item.id"
            class="related-item"
            @click="goToNews(item.id)"
          >
            <p>{{ truncateText(item.title, 50) }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 错误 -->
    <div v-else class="empty-state">
      <p>未找到该新闻</p>
      <el-button @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getNewsDetail, addHistory } from '@/api/news'
import { checkFavorite, addFavorite, removeFavorite } from '@/api/favorite'
import { useCacheStore } from '@/stores/cacheStore'
import { useUserStore } from '@/stores/userStore'
import { formatTime, truncateText } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const cacheStore = useCacheStore()

const news = ref(null)
const relatedNews = ref([])
const loading = ref(false)
const isFavorite = ref(false)

const loadNews = async () => {
  const newsId = route.params.id
  
  // 先检查缓存
  const cached = cacheStore.getNewsDetailCache(newsId)
  if (cached) {
    news.value = cached
    return
  }
  
  loading.value = true
  try {
    const response = await getNewsDetail(newsId)
    news.value = response.data
    relatedNews.value = response.data.relatedNews || []
    
    // 缓存
    cacheStore.setNewsDetailCache(newsId, news.value)
    
    // 添加浏览记录
    if (userStore.isLoggedIn) {
      try {
        await addHistory(newsId)
      } catch (error) {
        // 忽略错误
      }
    }
    
    // 检查收藏状态
    if (userStore.isLoggedIn) {
      try {
        const fav = await checkFavorite(newsId)
        isFavorite.value = fav.data.isFavorite
      } catch (error) {
        // 忽略错误
      }
    }
  } catch (error) {
    // 错误已处理
  } finally {
    loading.value = false
  }
}

const handleFavorite = async () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  try {
    if (isFavorite.value) {
      await removeFavorite(news.value.id)
      isFavorite.value = false
      ElMessage.success('已取消收藏')
    } else {
      await addFavorite(news.value.id)
      isFavorite.value = true
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    // 错误已处理
  }
}

const goToNews = (newsId) => {
  router.push(`/news/${newsId}`)
}

onMounted(() => {
  loadNews()
})
</script>

<style scoped lang="scss">
.news-detail-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.news-detail {
  background: white;
  padding: 32px;
  border-radius: 4px;
}

.news-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
  line-height: 1.4;
}

.news-meta {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.action-buttons {
  margin-bottom: 24px;
  display: flex;
  gap: 12px;
}

.news-content {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  margin-bottom: 32px;
  
  img {
    max-width: 100%;
    height: auto;
    margin: 16px 0;
    border-radius: 4px;
  }
  
  p {
    margin-bottom: 16px;
  }
  
  h2, h3 {
    margin: 24px 0 16px 0;
    font-weight: bold;
  }
}

.related-news {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #eee;
  
  h3 {
    margin-bottom: 16px;
    font-size: 18px;
  }
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.related-item {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: #f0f0f0;
    color: #0084ff;
  }
  
  p {
    margin: 0;
    font-size: 14px;
  }
}

.empty-state {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 4px;
  
  p {
    margin-bottom: 16px;
    color: #999;
  }
}

.loading {
  text-align: center;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}
</style>
