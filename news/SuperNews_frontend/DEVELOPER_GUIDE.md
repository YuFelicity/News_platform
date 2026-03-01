开发者指南

## 快速开始

### 第一步：安装依赖
```bash
cd SuperNews_frontend
npm install
```

### 第二步：启动开发服务器
```bash
npm run dev
```

访问 http://localhost:5173

### 第三步：修改 API 地址
在 `vite.config.js` 中修改后端服务地址：
```javascript
proxy: {
  '/api': {
    target: 'http://your-backend-url:8080',
    changeOrigin: true
  }
}
```

## 项目目录说明

### /src/api - API 请求层
- user.js：用户相关 API（登录、注册、获取信息等）
- news.js：新闻相关 API（获取列表、详情、历史等）
- favorite.js：收藏相关 API

### /src/utils - 工具函数
- request.js：Axios 封装，包含请求/响应拦截器
- auth.js：认证和缓存工具
- format.js：数据格式化工具

### /src/stores - 状态管理（Pinia）
- userStore.js：用户信息状态
- newsStore.js：新闻分类和列表状态
- cacheStore.js：缓存管理

### /src/layouts - 布局组件
- MainLayout.vue：主布局（包含导航栏、侧边栏等）

### /src/views - 页面组件
- Login.vue：登录页
- Register.vue：注册页
- Home.vue：首页新闻列表
- NewsDetail.vue：新闻详情页
- UserCenter.vue：用户中心
- UserProfile.vue：个人信息编辑
- Favorites.vue：收藏列表
- History.vue：浏览历史
- NotFound.vue：404 页面

## 主要特性

### 1. 简洁的架构
- 组件化设计，易于维护扩展
- API 层分离，业务逻辑清晰
- Pinia 状态管理，全局状态易管理

### 2. 完整的功能
- 用户认证（登录、注册、个人资料编辑）
- 新闻浏览（列表、分类、详情）
- 收藏管理（添加、删除、列表）
- 历史记录（自动记录、删除、清空）

### 3. 良好的用户体验
- 加载动画反馈
- 错误提示处理
- 缓存优化性能
- 响应式设计

### 4. 安全认证
- 令牌存储和传递
- 路由守卫权限控制
- 401 错误自动登出

## 常用命令

```bash
# 开发
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# ESLint 检查代码
# npm run lint（需自行配置）
```

## 代码规范

### 命名规范
- 组件文件：大驼峰（UserProfile.vue）
- 函数/变量：小驼峰（getUserInfo）
- 常量：大写（API_URL）

### 文件结构
- 单文件组件使用 <script setup> 语法
- 样式使用 <style scoped> 避免全局污染
- 所有 API 请求在 api/ 目录

### 注释规范
```javascript
// 简单说明
const userName = 'xxx'

// 复杂逻辑需要注释
// 1. 先获取用户信息
// 2. 再检查收藏状态
// 3. 最后更新界面
```

## 调试技巧

### 1. 使用 Vue DevTools
- Chrome 扩展，安装后自动识别 Vue 应用
- 可查看组件树、Pinia 状态等

### 2. Network 标签页
- 检查 API 请求和响应
- 查看请求头中的 Authorization 令牌

### 3. localStorage 调试
```javascript
// 在控制台查看存储的令牌
console.log(localStorage.getItem('token'))

// 清空所有存储
localStorage.clear()
```

### 4. 断点调试
- 在 Sources 标签页设置断点
- 使用 debugger 语句

## 常见开发场景

### 添加新的 API 请求
1. 在 /src/api/ 中创建函数
```javascript
export function getNewAPI(params) {
  return request.get('/endpoint', { params })
}
```

2. 在组件中调用
```javascript
import { getNewAPI } from '@/api/news'
const response = await getNewAPI()
```

### 添加新的全局状态
1. 在 /src/stores/ 创建 store
```javascript
import { defineStore } from 'pinia'
export const useMyStore = defineStore('my', () => {
  const state = ref({})
  return { state }
})
```

2. 在组件中使用
```javascript
const myStore = useMyStore()
```

### 添加新的路由
1. 在 /src/router/index.js 添加路由
```javascript
{
  path: '/new-page',
  component: () => import('@/views/NewPage.vue')
}
```

2. 创建对应的页面文件

## 性能优化

1. **代码分割**：使用 const component = () => import() 动态导入
2. **图片优化**：压缩图片，使用 webp 格式
3. **缓存策略**：合理设置缓存过期时间
4. **懒加载**：列表使用虚拟滚动（大数据量时）

## 常见问题解决

### 页面刷新后令牌丢失
- 检查是否在 app 初始化时从 localStorage 恢复令牌
- initializeUser() 在 main.js 中调用

### API 请求 CORS 错误
- 后端需要正确设置 CORS 头
- 或在 vite.config.js 中配置代理

### 样式污染
- 确保使用 <style scoped>
- 验证全局样式是否覆盖了组件样式

### 状态更新不生效
- 使用响应式 API（ref, reactive）
- 避免直接修改数组，使用 push、splice 等方法

## 下一步学习

1. **Vue 3 文档**：https://vuejs.org/
2. **Vite 文档**：https://vitejs.dev/
3. **Pinia 文档**：https://pinia.vuejs.org/
4. **Element Plus 文档**：https://element-plus.org/
5. **Axios 文档**：https://axios-http.com/

## 联系方式

有问题或建议，欢迎反馈！
