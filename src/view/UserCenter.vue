<template>
    <div class="user-center">
        <!--通过设置router与index可以实现跳转类似于@click-->
        <el-menu 
        class="menu"
        router
        default-active="/user/favorite"
        >
        <el-menu-item index="/user/profile">个人信息</el-menu-item>
        <el-menu-item index="/user/favorite">我的收藏</el-menu-item>
        <el-menu-item index="/user/history">浏览历史</el-menu-item>
        </el-menu>
          <div class="component">
           <router-view/>

          </div>
    </div>
  
</template>
<script>

</script>
<style scoped>
.user-center {
  display: flex;
}
.menu {
  width: 200px;
  min-height: 100vh;
  border-right: 1px solid #eee;
}
.content {
  flex: 1;
  padding: 16px;
}
</style>
