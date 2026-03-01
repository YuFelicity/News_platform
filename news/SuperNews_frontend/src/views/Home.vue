<template>
  <div class="home-container">
    <div class="news-list">
      <h2>{{ newsStore.currentCategory?.name }} 新闻</h2>
      
      <!-- 加载中 -->
      <div v-if="loading" class="loading">
        <el-skeleton :rows="5" animated />
      </div>
      
      <!-- 新闻列表 -->
      <div v-else-if="newsList.length > 0" class="news-items">
        <div
          v-for="news in newsList"
          :key="news.id"
          class="news-card"
          @click="goToDetail(news.id)">

          <div class="news-header">
            <h3>{{ news.title }}</h3>
          </div>

          <div class="news-image" v-if="news.image">
          <img :src="news.image" :alt="news.title" />
          </div>

          <p class="news-summary">{{ truncateText(news.description, 100) }}</p>

          <div class="news-footer">
            <span class="news-meta">
              <span>{{ news.author }} | </span>
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
      newsStore.currentCategory?.id,
      currentPage.value,
      pageSize.value
    )
    
    newsList.value = response.data?.list || []
    total.value = response.total?.to || 0
    
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
  max-width: 1200px;
  margin: 0 auto; /* 让整个内容区在页面中居中 */
  padding: 0 20px; /* 防止贴边 */
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
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  /* 新增：限制最大宽度，并水平居中 */
  max-width: 900px; /* 这个宽度可以根据你的视觉效果微调 */
  margin: 0 auto 30px; /* 上下间距，左右自动居中 */
}

.news-card {
  /* 核心：设置宽高比 1:1，实现正方形 */
  aspect-ratio: 1 / 1;
  /* 内部垂直布局 */
  display: flex;
  flex-direction: column;
  /* 美化 */
  background: white;
  padding: 12px;
  border-radius: 8px; /* 卡片整体圆角 */
  border: 1px solid #eee;
  cursor: pointer;
  transition: all 0.3s;
  /* 隐藏超出正方形的内容 */
  overflow: hidden;
}

.news-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
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


/* 图片容器：在正方形卡片中间，圆角，不遮挡文字 */
.news-image {
  width: 100%;
  height: 40%; /* 占卡片高度的40%，留出空间给文字 */
  border-radius: 6px; /* 图片圆角，更美观 */
  overflow: hidden;   /* 让圆角生效 */
  margin-bottom: 8px; /* 和下面的描述文字保持间距 */
}

/* 图片本身：填充容器，保持比例不变形 */
.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 核心：按比例裁剪，不会拉伸变形 */
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
