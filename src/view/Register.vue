<template>
    <div class="register">
        <el-card>
            <h2>用户注册</h2>
            <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
                <el-form-items label="账号" prop="username">
                    <el-input v-model="form.username" placeholder="请输入账号"/>
                </el-form-items>
                 <el-form-items label="密码" prop="password">
                    <el-input v-model="form.password" placeholder="请输入密码"/>
                </el-form-items>
                 <el-form-items label="确认密码" prop="confirmpassword">
                    <el-input v-model="form.confirmpassword" placeholder="请确认密码"/>

                </el-form-items>
                 <el-form-items>
                    <el-button type="primary" @click="onSubmit">注册</el-button>
                    <el-button type="primary" @click="goLogin">去登陆</el-button>
                </el-form-items>
            </el-form>
        </el-card>

    </div>
</template>
<script setup>
import {ref } from 'vue'
import {ElMessage} from 'element-plus'
import {useRouter} from'vue-router'
import {register} from'@/api/user'
const form=ref({
    username:'',
    password:'',
    confirmpassword:''
})

const router=useRouter()
const validateConfirmPassword=(rule,value,callback)=>{//自定义去确认密码
    if(value!==form.value.password)
    {
        callback(new error('两次输入密码不一致'))//callback()如果括号内为空说明检验成功，括号内有错误说明检验失败
    }
    else{
        callback()
    }
}
const rules={
    username:[{required:true,message:'请输入账号',trigger:'blur'}],
    password:[{required:true,message:'请输入密码',trigger:'blur'},
        {min:6,max:20,message:'密码应在6到20位之间',trigger:'blur'}
    ],
    confirmpassword:[{required:true,message:"请确认密码",trigger:'blur'},{
        validator:validateConfirmPassword ,trigger:'blur'
    }]
}
const formRef=ref(null)
const onSubmit=async()=>{
    await formRef.value.validate()
     await register({
    username: form.value.username,
    password: form.value.password
  })

  ElMessage.success('注册成功，请登录')

  router.push('/login')
}
const goLogin = () => {
  router.push('/login')
}
 
</script>
<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.register-card {
  width: 400px;
}
</style>