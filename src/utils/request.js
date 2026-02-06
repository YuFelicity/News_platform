import axios from 'axios'//引入axios库,用来像后端发送与接受请求
import { ElMessage } from 'element-plus'
import router from '@/router'

const service =axios.create(
    {
        baseURL: import.meta.env.VITE_BASE_API,//设置基础路径,使得之后不需要大量写,import.meta是vite提供的基础元信息，env是环境变量
        timeout:10000//设置请求超时时间为10秒
    }
)
//请求拦截器
service.interceptors.request.use(
    (config)=>{
        const token =localStorage.getItem('token')//从本地获取token
        if(token)//如果token存在，那么将token设置为请求头在放行
        {
            config.headers.Authorization=token
        }
        return config
    },
    (error)=>{
        return Promise.reject(error)//请去超时的情况下返回错误信息
    }
)
//响应拦截器
service.interceptors.response.use(
    (response)=>{//响应返回时获取数据如果返回的状态业务码不成功，在页面显示失败信息，返回失败
        const data=response.data
        if(data.code!==200)
        {
            ElMessage.error(data.message||'请求失败')
            return Promise.reject(data.message)
        }
        return data
    },
    (error)=>{//响应失败如果返回的状态码等于401页面显示登录过期，从本地删除之前的token，跳转到登陆页面重新登陆
        if(error.response.status===401)
        {
            ElMessage.error('登陆过期，请重新登录')
            localStorage.removeItem('token')
            router.push('/login')
        }
        else{
            ElMessage.error('网络异常，请稍后重试')
        }
        return Promise.reject(error)
    }

)
export default service