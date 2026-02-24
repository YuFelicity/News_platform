<template>
  <div class="home-container">
    <div class="news-list">
      <h2>{{ newsStore.currentCategory }} 新闻</h2>
      
      <!-- 加载中 -->
      <div v-if="loading" class="loading">
        <el-spinning />
      </div>
      
      <!-- 新闻列表 -->
      <div v-else-if="newsList.length > 0" class="news-items">
        <div
          v-for="news in newsList"
          :key="news.id"
          class="news-card"
          @click="goToDetail(news.id)"
        >
          <div class="news-header">
            <h3>{{ news.title }}</h3>
            <span v-if="isFavorite(news.id)" class="favorite-badge">已收藏</span>
          </div>
          <p class="news-summary">{{ truncateText(news.summary, 100) }}</p>
          <div class="news-footer">
            <span class="news-meta">
              <span>{{ news.author }} | </span>
              <span>{{ formatTime(news.publishTime) }} | </span>
              <span>{{ news.views }} 浏览</span>
            </span>
            <el-tag size="small">{{ news.category }}</el-tag>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div v-else class="empty-state">
        <div class="empty-icon">📰</div>
        <p>暂无新闻</p>
      </div>
      
      <!-- 分页 -->
      <el-pagination
        v-if="total > 0"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[10, 20, 50]"
        @current-change="handlePageChange"
        @size-change="handlePageSizeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useNewsStore } from '@/stores/newsStore'
import { useCacheStore } from '@/stores/cacheStore'
import { getNewsList, getCategories } from '@/api/news'
import { checkFavorite } from '@/api/favorite'
import { formatTime, truncateText } from '@/utils/format'

const router = useRouter()
const newsStore = useNewsStore()
const cacheStore = useCacheStore()

const newsList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const favoriteIds = ref(new Set())

const loadNews = async () => {
  loading.value = true
  try {
    const response = await getNewsList(
      newsStore.currentCategory,
      currentPage.value,
      pageSize.value
    )
    
    newsList.value = response.data || []
    total.value = response.total || 0
    
    // 检查收藏状态
    for (const news of newsList.value) {
      try {
        const fav = await checkFavorite(news.id)
        if (fav.data.isFavorite) {
          favoriteIds.value.add(news.id)
        }
      } catch (error) {
        // 忽略错误，不中断流程
      }
    }
  } catch (error) {
    // 错误已在请求拦截器处理
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadNews()
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadNews()
}

const goToDetail = (newsId) => {
  router.push(`/news/${newsId}`)
}

const isFavorite = (newsId) => {
  return favoriteIds.value.has(newsId)
}

// 监听分类变化
watch(() => newsStore.currentCategory, () => {
  currentPage.value = 1
  loadNews()
})

onMounted(() => {
  loadNews()
})
</script>

<style scoped lang="scss">
.home-container {
  width: 100%;
  max-width: 800px;
}

.news-list {
  h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
    border-bottom: 2px solid #0084ff;
    padding-bottom: 10px;
  }
}

.news-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.news-card {
  background: white;
  padding: 16px;
  border-radius: 4px;
  border: 1px solid #eee;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 12px;
  
  h3 {
    font-size: 16px;
    margin: 0;
    color: #333;
    flex: 1;
    line-height: 1.4;
  }
}

.favorite-badge {
  background: #fef0f0;
  color: #f56c6c;
  padding: 2px 8px;
  border-radius: 3px;
  font-size: 12px;
  white-space: nowrap;
}

.news-summary {
  margin: 8px 0;
  color: #666;
  font-size: 13px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.news-meta {
  display: flex;
  gap: 4px;
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #999;
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}
</style>
