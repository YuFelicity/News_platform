import {defineStore} from 'pinia'//创建仓库
import {ref} from 'vue'
export const useUserStore=defineStore('user',()=>{
    const token=ref(localStorage.getItem('token'||''))//登录token
    const userInfo = ref(null)//用户信息
    const isLogin=!!localStorage.getItem('token')//判断是否登录
    const setToken = (newToken) => {
     localStorage.setItem('token', newToken)//设置token
     }
     const setUserInfo = (info) => {
    userInfo.value = info
     }//设置用户信息
     const logout = () => {
  token.value = ''
  userInfo.value = null
  localStorage.removeItem('token')
}//退出登录
return {
  token,
  userInfo,
  isLogin,
  setToken,
  setUserInfo,
  logout
}
})