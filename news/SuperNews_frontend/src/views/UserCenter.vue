<template>
  <div class="user-center">
    <div class="user-menu-side">
      <div class="menu-item"
           :class="{ active: activeTab === 'profile' }"
           @click="activeTab = 'profile'">
        个人信息
      </div>
      <div class="menu-item"
           :class="{ active: activeTab === 'favorites' }"
           @click="activeTab = 'favorites'">
        我的收藏
      </div>
      <div class="menu-item"
           :class="{ active: activeTab === 'history' }"
           @click="activeTab = 'history'">
        浏览历史
      </div>
    </div>
    
    <div class="user-content">
      <!-- 个人信息 -->
      <div v-show="activeTab === 'profile'" class="tab-content">
        <UserProfile />
      </div>
      
      <!-- 收藏列表 -->
      <div v-show="activeTab === 'favorites'" class="tab-content">
        <Favorites />
      </div>
      
      <!-- 历史记录 -->
      <div v-show="activeTab === 'history'" class="tab-content">
        <History />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import UserProfile from './UserProfile.vue'
import Favorites from './Favorites.vue'
import History from './History.vue'

const activeTab = ref('profile')
</script>

<style scoped lang="scss">
.user-center {
  display: flex;
  gap: 24px;
  width: 100%;
  background: white;
  padding: 24px;
  border-radius: 4px;
}

.user-menu-side {
  flex: 0 0 150px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  padding: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
  text-align: center;
  
  &:hover {
    background: #f0f0f0;
  }
  
  &.active {
    background: #e6f2ff;
    color: #0084ff;
    font-weight: bold;
  }
}

.user-content {
  flex: 1;
  min-width: 0;
}

.tab-content {
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .user-center {
    flex-direction: column;
  }
  
  .user-menu-side {
    flex-direction: row;
    flex: none;
  }
}
</style>
