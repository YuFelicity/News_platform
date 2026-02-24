<template>
    <div class='home'>
      <el-menu mode="horizontal" :default-active="activeCategory"><!--//设置导航栏模式为横向,动态绑定激活的菜单项-->
        <!--使用v-for渲染导航栏,再点击的时候调用函数-->
        <el-menu-item 
        v-for="item in categories" 
        :key="item.id"
        :index="String(item.id)"
        @click="changeCategory(item.id)"
        >
        {{item.name}}
        </el-menu-item>
      </el-menu>
      <!--新闻列表
      //使用v-for渲染,点击卡片时跳转到对应的详情页，卡片中展示新闻的标题，概述，发布时间-->
     <News 
       v-for="news in newsList"
       :key="news.id"
       :news="news"/>
      <!--//分页-->
      <el-pagination 
       v-model:current-page="page"
       v-model:page-size="pageSize"
      :total="total"
      @current-change="loadList"
      @size-change="loadList"
      />

      

    </div>
</template>
<script setup>
    import {ref,onMounted} from 'vue'
    import {getCategoryList,getNewsList} from '@/api/news'
    import {useRouter} from 'vue-router'
    import News from '@/components/News.vue'
    const categories=ref([])//动态绑定导航栏，初始为数组
    const newsList=ref([])//动态绑定新闻列表
    const activeCategory=ref('')//动态绑定高亮的值
    const page=ref(1)
    const pageSize=ref(10)
    const total=ref(0)
    const router=useRouter()//创建router实例
    const loadCategory=async ()=>{//加载导航栏，使用异步，只有当从后端获取到数据时才会传入
        const res=await getCategoryList()
        categories.value=res.data
    }
    const loadList = async () => {//获取从后端传来的参数值并传入到参数中
    const res = await getNewsList({
    categoryId: activeCategory.value,
    page: page.value,
    pageSize: pageSize.value
    })
     newsList.value = res.data.records
     total.value = res.data.total
    }
const changeCategory = (id) => {//在改变分类时高亮的值改变，重置页码为第一页，重新加载新闻列表
  activeCategory.value = String(id)
  page.value = 1
  loadList()
}

// const goDetail = (id) => {//根据传过来的id使用router实例挂上参数
//   router.push(`/news/${id}`)
// }

onMounted(() => {
  loadCategory()
  loadList()
})
</script>
<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 导航栏样式优化 */
.home .el-menu {
  margin-bottom: 30px;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  padding: 0 20px;
}

.home .el-menu-item {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  height: 56px;
  line-height: 56px;
}

.home .el-menu-item.is-active {
  color: #409eff !important; /* Element Plus 主色 */
  border-bottom: 2px solid #409eff !important;
}

/* 新闻列表容器 */
.news-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 分页居中 */
.home .el-pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

/* 响应式：小屏幕下导航栏紧凑 */
@media (max-width: 768px) {
  .home {
    padding: 15px;
  }

  .home .el-menu {
    padding: 0 10px;
  }

  .home .el-menu-item {
    font-size: 14px;
    padding: 0 10px !important;
  }
}
</style>