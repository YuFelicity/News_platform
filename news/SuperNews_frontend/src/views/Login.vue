<template>
  <div class="login-container">
    <div class="login-box">
      <h2>登录</h2>
      
      <el-form
        :model="form"
        @submit.prevent="handleLogin"
        class="login-form"
      >
        <el-form-item label="用户名">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="handleLogin"
            :loading="loading"
            class="login-btn"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <p>没有账号？<router-link to="/register">点击注册</router-link></p>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/user'
import { useUserStore } from '@/stores/userStore'
import { setToken } from '@/utils/auth'

const router = useRouter()
const userStore = useUserStore()
const form = ref({
  username: '',
  password: ''
})
const loading = ref(false)

const handleLogin = async () => {
  // 简单验证
  if (!form.value.username || !form.value.password) {
    ElMessage.error('请输入用户名和密码')
    return
  }
  
  loading.value = true
  try {
    const response = await login(form.value.username, form.value.password)
    
    // 存储令牌
    setToken(response.data.token)
    userStore.setTokenValue(response.data.token)
    
    // 存储用户信息
    userStore.setUser({
      username: form.value.username,
      id: response.data.userId
    })
    
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  
  h2 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px;
    color: #333;
  }
}

.login-form {
  .login-btn {
    width: 100%;
  }
}

.form-footer {
  text-align: center;
  font-size: 14px;
  
  p {
    margin: 0;
  }
  
  a {
    color: #0084ff;
    cursor: pointer;
  }
}

@media (max-width: 600px) {
  .login-box {
    width: 90%;
    padding: 20px;
  }
}
</style>
