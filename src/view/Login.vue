<template>
    <div class="login">
        <el-card class="login-card">
            <h2>用户登录</h2>
            <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
                <el-form-item label="账号" prop="username">
                    <el-input v-model="form.username" placeholder="请输入账号"/>
                </el-form-item>
                 <el-form-item>
                    <el-input v-model="form.password" placeholder="请输入密码"/>
                </el-form-item>
              
                 <el-form-item>
                    <el-button type="primary" @click="onSubmit">登录
                    </el-button>
                </el-form-item>
            </el-form>
<!--:model的作用是告诉表单检验时使用form作为数据源，：rules的作用是声明检验规则，ref是获取表单实例，prop是对应rules中的username规则-->
        </el-card>

    </div>
</template>
<script setup>
import{ref} from 'vue'
import{useRouter} from 'vue-router'
import{ElMessage} from'element-plus'
import {login} from '@/api/user'
const form={
    username:'',
    password:''
}//表单数据
const rules={
    username:[{required:true,message:'请输入账号',trigger:'blur'}],
    password:[{required:true,message:'请输入密码',trigger:'blur'}]
}//规则，账户和密码必须填写，失焦时检验
const formRef=ref(null)//表单实例
const router= useRouter()
const onSubmit=async()=>{
    await formRef.value.validate()//在提交时触发检验
    const res=await login(form.value)

localStorage.set('token',res.data.token)//保存token
ElMessage.success('登陆成功')
router.push('/')//登录成功后进入首页
}
</script>
<style scoped>
.login{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-card {
  width: 360px;
}
</style>