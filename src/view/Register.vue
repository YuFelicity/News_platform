<template>
  <div class="register-container">
    <div class="register-box">
      <h2>注册</h2>
      
      <el-form
        :model="form"
        @submit.prevent="handleRegister"
        class="register-form"
      >
        <el-form-item label="用户名">
          <el-input
            v-model="form.username"
            placeholder="6-20位，支持字母、数字、下划线"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="8-20位，包含字母和数字"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="确认密码">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="再次输入密码"
            clearable
            @keyup.enter="handleRegister"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="handleRegister"
            :loading="loading"
            class="register-btn"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="form-footer">
          <p>已有账号？<router-link to="/login">点击登录</router-link></p>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { register } from '@/api/user'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()
const form = ref({
  username: '',
  password: '',
  confirmPassword: ''
})
const loading = ref(false)

const handleRegister = async () => {
  // 验证
  if (!form.value.username || !form.value.password || !form.value.confirmPassword) {
    ElMessage.error('请填写所有字段')
    return
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  if (form.value.username.length < 6 || form.value.username.length > 20) {
    ElMessage.error('用户名长度需6-20位')
    return
  }
  
  if (form.value.password.length < 8 || form.value.password.length > 20) {
    ElMessage.error('密码长度需8-20位')
    return
  }
  
  loading.value = true
  try {
    const response = await register(form.value.username, form.value.password)
    
    // 注册成功后自动登录
    userStore.setTokenValue(response.data.token)
    userStore.setUser({
      username: form.value.username,
      id: response.data.userId
    })
    
    ElMessage.success('注册成功，已自动登录')
    router.push('/')
  } catch (error) {
    ElMessage.error('注册失败，用户名可能已存在')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-box {
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

.register-form {
  .register-btn {
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
  }
}

@media (max-width: 600px) {
  .register-box {
    width: 90%;
    padding: 20px;
    max-width: 100%;
  }
}
</style>
