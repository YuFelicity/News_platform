<template>
  <div class="favorites">
    <div class="header">
      <h2>我的收藏</h2>
      <el-button
        type="danger"
        @click="handleClearAll"
        v-if="lrNewsList.length > 0"
      >
        清空所有收藏
      </el-button>
    </div>
    
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      加载中...
    </div>
    
    <div v-else-if="favoriteList.length > 0" class="news-items">
      <div
        v-for="news in favoriteList"
        :key="news.id"
        class="news-card"
      >
        <div class="card-header">
          <h3 @click="goToNews(news.id)" class="clickable">{{ news.title }}</h3>
          <el-button
            size="small"
            type="danger"
            text
            @click="handleRemoveFavorite(news.id)"
          >
            移除
          </el-button>
        </div>
        <p class="news-summary">{{ truncateText(news.summary, 100) }}</p>
        <div class="card-footer">
          <span class="text-muted">{{ formatTime(news.collectedTime) }}</span>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-icon">⭐</div>
      <p>暂无收藏记录，快去收藏喜欢的新闻吧</p>
    </div>
    
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getFavoriteList, removeFavorite, clearFavorites } from '@/api/favorite'
import { formatTime, truncateText } from '@/utils/format'

const router = useRouter()
const favoriteList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loadFavorites = async () => {
  loading.value = true
  try {
    const response = await getFavoriteList(currentPage.value, pageSize.value)
    favoriteList.value = response.data || []
    total.value = response.total || 0
  } catch (error) {
    // 错误已处理
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadFavorites()
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadFavorites()
}

const goToNews = (newsId) => {
  router.push(`/news/${newsId}`)
}

const handleRemoveFavorite = async (newsId) => {
  try {
    await removeFavorite(newsId)
    ElMessage.success('已移除收藏')
    loadFavorites()
  } catch (error) {
    // 错误已处理
  }
}

const handleClearAll = () => {
  ElMessageBox.confirm(
    '确定要清空所有收藏吗？操作无法撤销。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await clearFavorites()
      ElMessage.success('已清空所有收藏')
      currentPage.value = 1
      loadFavorites()
    } catch (error) {
      // 错误已处理
    }
  }).catch(() => {
    // 用户取消
  })
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped lang="scss">
.favorites {
  h2 {
    margin-bottom: 16px;
    font-size: 18px;
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.news-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.news-card {
  background: white;
  padding: 16px;
  border-radius: 4px;
  border: 1px solid #eee;
  transition: all 0.3s;
  
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

.card-header {
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
  }
}

.clickable {
  cursor: pointer;
  
  &:hover {
    color: #0084ff;
  }
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

.card-footer {
  margin-top: 8px;
  font-size: 12px;
}

.text-muted {
  color: #999;
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
  text-align: center;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}
</style>
