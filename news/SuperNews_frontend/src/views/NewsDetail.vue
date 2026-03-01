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
        <span>浏览: {{ news.views }}</span>
      </div>
      
      <div class="action-buttons">
        <el-button
          :type="isFavorite ? 'danger' : 'default'"
          @click="handleFavorite">
          {{ isFavorite ? '已收藏' : '收藏' }}
        </el-button>
      </div>

      <div class="news-body">
        <!-- 左侧：新闻图片 -->
        <div class="news-image-side" v-if="news.image">
          <img :src="news.image" :alt="news.title" />
        </div>

        <!-- 右侧：新闻内容（富文本） -->
        <div class="news-content-side" v-html="news.content"></div>
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

/* 核心：左右布局容器 */
.news-body {
  display: flex;
  gap: 24px; /* 图和文之间的间距 */
  align-items: flex-start; /* 顶部对齐 */
}

/* 左侧：图片区 */
.news-image-side {
  flex: 0 0 360px; /* 固定宽度，不拉伸 */
  border-radius: 8px;
  overflow: hidden;
}

.news-image-side img {
  width: 100%;
  height: auto;
  object-fit: cover; /* 保持比例，不拉伸 */
}


.news-content-side {
  flex: 1; /* 占满剩余空间 */
  font-size: 16px;
  line-height: 1.8;
  color: #333;

  /* 内容内部样式保持不变 */
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

/* 适配：无图时，内容占满整行 */
.news-detail:not(:has(.news-image-side)) .news-content-side {
  flex: 1 1 100%;
}

.news-cover {
  width: 100%;
  max-height: 400px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 24px;
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
