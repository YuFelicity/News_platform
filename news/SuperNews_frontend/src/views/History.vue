<template>
  <div class="history">
    <div class="header">
      <h2>浏览历史</h2>
      <el-button
        type="danger"
        @click="handleClearAll"
        v-if="historyList.length > 0"
      >
        清空历史
      </el-button>
    </div>
    
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      加载中...
    </div>
    
    <div v-else-if="historyList.length > 0" class="news-items">
      <div
        v-for="record in historyList"
        :key="record.id"
        class="news-card"
      >
        <div class="card-header">
          <h3 @click="goToNews(record.newsId)" class="clickable">{{ record.title }}</h3>
          <el-button
            size="small"
            type="danger"
            text
            @click="handleDeleteRecord(record.id)"
          >
            删除
          </el-button>
        </div>
        <p class="news-summary">{{ truncateText(record.summary, 100) }}</p>
        <div class="card-footer">
          <span class="text-muted">浏览于: {{ formatTime(record.viewTime) }}</span>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-icon">📋</div>
      <p>暂无浏览历史</p>
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
import { getHistory, deleteHistory, clearHistory } from '@/api/news'
import { formatTime, truncateText } from '@/utils/format'

const router = useRouter()
const historyList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loadHistory = async () => {
  loading.value = true
  try {
    const response = await getHistory(currentPage.value, pageSize.value)
    historyList.value = response.data || []
    total.value = response.total || 0
  } catch (error) {
    // 错误已处理
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadHistory()
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadHistory()
}

const goToNews = (newsId) => {
  router.push(`/news/${newsId}`)
}

const handleDeleteRecord = async (recordId) => {
  try {
    await deleteHistory(recordId)
    ElMessage.success('已删除')
    loadHistory()
  } catch (error) {
    // 错误已处理
  }
}

const handleClearAll = () => {
  ElMessageBox.confirm(
    '确定要清空所有浏览历史吗？操作无法撤销。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await clearHistory()
      ElMessage.success('已清空')
      currentPage.value = 1
      loadHistory()
    } catch (error) {
      // 错误已处理
    }
  }).catch(() => {
    // 用户取消
  })
}

onMounted(() => {
  loadHistory()
})
</script>

<style scoped lang="scss">
.history {
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
