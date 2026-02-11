<<template >
    <div class="profile">
    <el-card>
    <h2>个人信息</h2>


    <el-form :model="form" label-width="100px">
       <el-form-item label="用户名">
          <el-input v-model="form.username" disabled />
        </el-form-item>

        <el-form-item label="昵称">
          <el-input v-model="form.nickname" />
        </el-form-item>

        <el-form-item label="性别">
          <el-select v-model="form.gender" placeholder="请选择">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>

        <el-form-item label="头像URL">
          <el-input v-model="form.avatar" placeholder="请输入头像链接" />
        </el-form-item>

        <el-form-item label="个人简介">
          <el-input v-model="form.bio" type="textarea" :rows="3" />
        </el-form-item>
          <el-form-item>
          <el-button type="primary" @click="saveProfile">
            保存修改
          </el-button>
        </el-form-item>
    </el-form>
    <el-divider/>
        <h3>修改密码</h3>
      <el-form :model="pwdForm" label-width="100px">
        <el-form-item label="原密码">
          <el-input v-model="pwdForm.oldPassword" type="password" />
        </el-form-item>

        <el-form-item label="新密码">
          <el-input v-model="pwdForm.newPassword" type="password" />
        </el-form-item>

        <el-form-item>
          <el-button type="warning" @click="changePassword">
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    

    


        
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserInfo, updateUserInfo, updatePassword } from '@/api/user'
import userRouter from 'vue-router'

const router=userRouter()
const form = ref({
  id: '',
  username: '',
  nickname: '',
  avatar: '',
  gender: '',
  bio: ''
})


const pwdForm = ref({
  oldPassword: '',
  newPassword: ''
})



const loadUserInfo = async () => {
    const res = await getUserInfo()
    form.value = res.data

}

const saveProfile = async () => {

    await updateUserInfo({
      nickname: form.value.nickname,
      avatar: form.value.avatar,
      gender: form.value.gender,
      bio: form.value.bio
    })
    ElMessage.success('个人信息更新成功')
    loadUserInfo()

}

const changePassword = async () => {
 
    await updatePassword({
      oldPassword: pwdForm.value.oldPassword,
      newPassword: pwdForm.value.newPassword
    })
    ElMessage.success('密码修改成功，请重新登录')
    localStorage.removeItem('token')
    router.push('/login')//修改密码后删除本地的token跳转到登录页面
}

onMounted(loadUserInfo)
</script>

<style scoped>
.profile {
  max-width: 700px;
  margin: 20px auto;
}
</style>