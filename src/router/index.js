import {createRouter,createWebHistory} from 'vue-router'//导入vue-router中的api,前者用于创建路由实例，后者用于开启“HTML5 History 模式”的路由
import {useUserStore} from '@/store/userStore'//导入pinia状态管理库，用于鉴定登录，使用useUserStore可以获取仓库实例
import { KeepAlive } from 'vue'
//懒加载，用来减少每次加载页面都要重新导入的开销，只在真正使用的时候加载js代码
const Login=()=>import('@/view/login/index.vue')
const Register=()=>import('@/view/register/index.vue')
const Home = () => import('@/views/Home/index.vue')
const NewsDetail = () => import('@/views/NewsDetail/index.vue')
const UserCenter = () => import('@/views/UserCenter/index.vue')
const Profile = () => import('@/views/UserCenter/Profile/index.vue')
const Favorite = () => import('@/views/UserCenter/Favorite/index.vue')
const History = () => import('@/views/UserCenter/History/index.vue')
const NotFound = () => import('@/views/NotFound/index.vue')
//创建路由实例
const router=createRouter({
    history:createWebHistory(),
    routes:[
        {
            path:'/',
            redirect:'/home'//路由重定向，用于首页当访问'/'时候，自动跳转到'/hoe'
        },
        {
            path:'/login',
            component:Login,//当访问'/login'时，渲染login组件，
            meta:{requireAuth:false}//路由元信息，通过meta附加的信息，与路由守卫连用,这一步写的是是否需要登录才能访问

        },
        {
            path:'/register',
            component:Register,
            meta:{requireAuth:false}
        },
        {
            path:'/home',
            component:Home,
            meta:{KeepAlive:true}//打上需要缓存的标签，作用是如果到了这个页面直接从内存中拿组件，不必重新渲染，与<keeo-alive>连用
        },
        {
            path:'/news/：id',//进入此页时带上id
            component:NewsDetail,
             meta: { keepAlive: false }
        },
        {
            path:'/user',
            component:UserCenter,
            meta: { requiresAuth: true },
            redirect: '/user/profile',
                children: [
        {
          path: 'profile',
          component: Profile,
          meta: { keepAlive: true }
        },
        {
          path: 'favorite',
          component: Favorite,
          meta: { keepAlive: true }
        },
        {
          path: 'history',
          component: History,
          meta: { keepAlive: true }
        }
      ]//子路由
        },
        {
            path:'/notfound',
            component:NotFound
        }
    ]

})
//全局前置路由守卫，用于检查是否登录过
router.beforeEach(
    (to,from,next)=>{
        const store=useUserStore()
        const token=store.token||localStorage.getItem('token')//token 可以是来自store中的也可以是来自本地存储中
        if(to.meta.requireAuth&&!token)
        {
            next({
                path:'/login',
                query:{redirect:to.fullpath}
            })
        }
        else{
            next()
        }//逻辑：如果想要去的页面需要登录或者登录过，那么就跳转到登陆页面，完成后在回到之前的页面，否则的话直接放行
    }
)
export default router//把创建好的路由对象导出挂载到vue上
