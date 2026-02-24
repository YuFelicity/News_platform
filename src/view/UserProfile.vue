<template>
  <div class="user-profile">
    <h2>个人信息</h2>
    
    <el-form
      :model="form"
      label-width="100px"
      class="profile-form"
    >
      <el-form-item label="用户名">
        <el-input disabled :model-value="form.username" />
      </el-form-item>
      
      <el-form-item label="昵称">
        <el-input
          v-model="form.nickname"
          placeholder="请输入昵称"
        />
      </el-form-item>
      
      <el-form-item label="性别">
        <el-select v-model="form.gender">
          <el-option label="男" value="male" />
          <el-option label="女" value="female" />
          <el-option label="其他" value="other" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="手机号">
        <el-input
          v-model="form.phone"
          placeholder="请输入手机号"
        />
      </el-form-item>
      
      <el-form-item label="个人简介">
        <el-input
          v-model="form.bio"
          type="textarea"
          rows="4"
          placeholder="请输入个人简介"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleUpdate" :loading="loading">
          保存修改
        </el-button>
        <el-button @click="handleChangePassword">修改密码</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 修改密码弹窗 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="400px"
    >
      <el-form
        :model="passwordForm"
        label-width="100px"
      >
        <el-form-item label="当前密码">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            placeholder="请输入当前密码"
          />
        </el-form-item>
        
        <el-form-item label="新密码">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码"
          />
        </el-form-item>
        
        <el-form-item label="确认密码">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="handlePasswordSubmit" :loading="passwordLoading">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { getUserInfo, updateUserInfo, changePassword } from '@/api/user'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()
const form = ref({
  username: '',
  nickname: '',
  gender: '',
  phone: '',
  bio: ''
})
const loading = ref(false)
const showPasswordDialog = ref(false)
const passwordLoading = ref(false)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const loadUserInfo = async () => {
  try {
    const response = await getUserInfo()
    const user = response.data
    form.value = {
      username: user.username,
      nickname: user.nickname || '',
      gender: user.gender || '',
      phone: user.phone || '',
      bio: user.bio || ''
    }
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  }
}

const handleUpdate = async () => {
  loading.value = true
  try {
    await updateUserInfo({
      nickname: form.value.nickname,
      gender: form.value.gender,
      phone: form.value.phone,
      bio: form.value.bio
    })
    
    ElMessage.success('修改成功')
  } catch (error) {
    ElMessage.error('修改失败')
  } finally {
    loading.value = false
  }
}

const handleChangePassword = () => {
  showPasswordDialog.value = true
}

const handlePasswordSubmit = async () => {
  if (!passwordForm.value.oldPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
    ElMessage.error('请填写所有字段')
    return
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  passwordLoading.value = true
  try {
    await changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    
    ElMessage.success('密码修改成功，请重新登录')
    userStore.clearUser()
    router.push('/login')
  } catch (error) {
    ElMessage.error('密码修改失败')
  } finally {
    passwordLoading.value = false
  }
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped lang="scss">
.user-profile {
  h2 {
    margin-bottom: 24px;
    font-size: 18px;
  }
}

.profile-form {
  max-width: 500px;
}
</style>
