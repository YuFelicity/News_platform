<!-- src/views/NotFound.vue -->
<template>
  <div style="padding: 60px; text-align: center; color: #666;">
    <h1>404</h1>
    <h2>页面未找到 😢</h2>
    <p>你访问的页面尚未开发或不存在。</p>
    <el-button type="primary" @click="$router.push('/')">
      返回首页
    </el-button>
  </div>
</template>

<script setup>
// 可选：记录错误日志
console.warn('用户访问了未定义的路由:', location.pathname)
</script>