<template>
  <div class="main-layout">
    <!-- 顶部导航 -->
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <h1>SuperNews</h1>
        </div>
        
        <nav class="nav-menu">
          <ul class="categories">
            <li v-for="cat in categories" :key="cat"
                :class="{ active: cat === newsStore.currentCategory }"
                @click="changeCategory(cat)">
              {{ cat }}
            </li>
          </ul>
        </nav>
        
        <div class="header-right">
          <el-input 
            v-model="searchText"
            placeholder="搜索新闻..."
            class="search-input"
            @keyup.enter="handleSearch"
          />
          
          <div class="user-menu" v-if="userStore.isLoggedIn">
            <el-dropdown>
              <span class="user-name">{{ userStore.user?.username }}</span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="goToUserCenter">个人中心</el-dropdown-item>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          
          <div class="user-menu" v-else>
            <el-button link @click="$router.push('/login')">登录</el-button>
            <el-button link @click="$router.push('/register')">注册</el-button>
          </div>
        </div>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
    
    <!-- 底部 -->
    <footer class="footer">
      <p>&copy; 2024 SuperNews - 超级新闻系统. All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useNewsStore } from '@/stores/newsStore'
import { getCategories } from '@/api/news'

const router = useRouter()
const userStore = useUserStore()
const newsStore = useNewsStore()
const categories = ref([])
const searchText = ref('')

onMounted(async () => {
  // 获取分类
  try {
    const response = await getCategories()
    categories.value = response.data || []
    newsStore.setCategories(categories.value)
  } catch (error) {
    console.error('获取分类失败:', error)
  }
})

const changeCategory = (category) => {
  newsStore.setCurrentCategory(category)
  router.push('/')
}

const handleSearch = () => {
  if (searchText.value.trim()) {
    router.push(`/?search=${searchText.value}`)
  }
}

const goToUserCenter = () => {
  router.push('/user/profile')
}

const handleLogout = () => {
  userStore.clearUser()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: white;
}

.header {
  background: white;
  border-bottom: 1px solid #ddd;
  padding: 16px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  gap: 24px;
}

.logo h1 {
  font-size: 24px;
  color: #0084ff;
  margin: 0;
  white-space: nowrap;
}

.nav-menu {
  flex: 1;
}

.categories {
  display: flex;
  list-style: none;
  gap: 16px;
  
  li {
    cursor: pointer;
    padding: 8px 12px;
    border-radius: 4px;
    transition: all 0.3s;
    
    &:hover {
      background: #f0f0f0;
    }
    
    &.active {
      color: #0084ff;
      background: #e6f2ff;
      font-weight: bold;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  white-space: nowrap;
}

.search-input {
  width: 200px;
}

.user-menu {
  display: flex;
  gap: 12px;
  align-items: center;
  
  .user-name {
    cursor: pointer;
    &:hover {
      color: #0084ff;
    }
  }
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 24px 16px;
}

.footer {
  background: #f0f0f0;
  padding: 24px;
  text-align: center;
  color: #666;
  border-top: 1px solid #ddd;
  
  p {
    margin: 0;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-wrap: wrap;
  }
  
  .categories {
    gap: 8px;
    
    li {
      padding: 4px 8px;
      font-size: 12px;
    }
  }
  
  .search-input {
    width: 150px;
  }
}
</style>
