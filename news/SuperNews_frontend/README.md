# SuperNews Frontend - Vue 3 前端应用

## 📂 项目概述

这是一个基于 **Vue 3 + Vite** 的超级新闻系统前端应用，提供新闻浏览、用户管理、收藏和历史记录等功能。

## 🚀 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

应用默认运行在 `http://localhost:5173`

### 3. 构建生产版本
```bash
npm run build
```

### 4. 预览生产版本
```bash
npm run preview
```

## 📁 项目结构

```
SuperNews_frontend/
├── public/                          # 静态资源
├── src/
│   ├── api/                         # API 请求封装
│   │   ├── user.js                  # 用户接口
│   │   ├── news.js                  # 新闻接口
│   │   └── favorite.js              # 收藏接口
│   ├── assets/
│   │   └── styles.scss              # 全局样式
│   ├── components/                  # 公共组件
│   ├── hooks/                       # 自定义钩子
│   ├── layouts/
│   │   └── MainLayout.vue           # 主布局
│   ├── router/
│   │   └── index.js                 # 路由配置
│   ├── stores/                      # Pinia 状态管理
│   │   ├── userStore.js
│   │   ├── newsStore.js
│   │   └── cacheStore.js
│   ├── utils/                       # 工具函数
│   │   ├── request.js               # Axios 封装
│   │   ├── auth.js                  # 认证相关
│   │   └── format.js                # 格式化工具
│   ├── views/                       # 页面组件
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Home.vue
│   │   ├── NewsDetail.vue
│   │   ├── UserCenter.vue
│   │   ├── UserProfile.vue
│   │   ├── Favorites.vue
│   │   ├── History.vue
│   │   └── NotFound.vue
│   ├── App.vue
│   └── main.js
├── index.html
├── vite.config.js
└── package.json
```

## 🔧 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 快速构建工具
- **Vue Router 4** - 页面路由
- **Pinia** - 状态管理
- **Axios** - HTTP 请求库
- **Element Plus** - 饱和组件库
- **SCSS** - 样式预处理器

## 📖 主要功能

### 1. 用户管理
- ✅ 用户注册（用户名、密码校验）
- ✅ 用户登录（令牌存储和认证）
- ✅ 个人信息编辑（昵称、性别、手机号等）
- ✅ 密码修改

### 2. 新闻浏览
- ✅ 新闻分类获取和展示
- ✅ 按分类筛选新闻列表
- ✅ 分页查看（10/20/50条）
- ✅ 新闻详情页面
- ✅ 浏览量统计

### 3. 收藏功能
- ✅ 添加/取消收藏
- ✅ 收藏列表展示
- ✅ 清空所有收藏

### 4. 历史记录
- ✅ 自动记录浏览历史
- ✅ 历史列表展示
- ✅ 删除单条/清空所有历史

### 5. 缓存管理
- ✅ 本地缓存新闻数据
- ✅ 缓存过期自动刷新
- ✅ 登出自动清空缓存

## 🔐 认证机制

- 令牌存储在 `localStorage`
- 所有请求贵携带 `Authorization: Bearer {token}`
- 401 错误自动跳转到登录页
- 支持路由守卫进行权限校验

## 🎨 样式规范

- **主色**: #0084ff (蓝色)
- **辅助色**: #f0f0f0 (浅灰)
- **字体**: 系统字体栈，14px 默认大小
- **间距**: 8px, 16px, 24px 三级间距

## 🌐 响应式适配

- 支持最小宽度 1280px
- PC 端优先设计
- 移动端基础适配
- 侧边栏在窄屏幕下折叠

## ⚙️ 配置说明

### 后端 API 代理

在 `vite.config.js` 中配置：
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '/api')
  }
}
```

### 缓存策略

- **新闻分类**: 2 小时过期
- **新闻列表**: 30 分钟过期
- **新闻详情**: 1 小时过期
- **用户历史**: 1 小时过期

## 🐛 常见问题

### Q: 登录后页面刷新令牌丢失？
A: 令牌存储在 `localStorage`，刷新不会丢失。检查浏览器是否禁用了存储。

### Q: 请求 API 时 CORS 错误？
A: 确保后端已启用 CORS，或者在 `vite.config.js` 中配置正确的代理。

### Q: 页面加载很慢？
A: 使用 `npm run build` 构建生产版本，使用 CDN 加速静态资源。

## 📦 部署

### 使用 npm 托管
```bash
npm run build
# 上传 dist 文件夹到服务器
```

### 使用 Docker
```dockerfile
FROM node:16 AS build
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

## 📝 注意事项

1. 代码遵循 ESLint 规范
2. 组件使用 `<script setup>` 语法
3. 样式使用 `<style scoped>` 避免污染
4. 状态管理集中在 Pinia 中
5. API 请求统一在 api/ 目录下

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License
