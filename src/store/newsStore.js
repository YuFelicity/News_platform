import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCache, setCache } from '@/utils/auth'

export const useNewsStore = defineStore('news', () => {
  const categories = ref([])
  const newsList = ref([])
  const currentCategory = ref('热点')
  const currentPage = ref(1)
  const pageSize = ref(10)
  const total = ref(0)

  // 设置分类
  function setCategories(data) {
    categories.value = data
    setCache('categories', data, 7200000) // 2小时过期
  }

  // 获取缓存分类
  function getCachedCategories() {
    return getCache('categories')
  }

  // 设置新闻列表
  function setNewsList(data, total = 0) {
    newsList.value = data
    this.total = total
  }

  // 设置当前分类
  function setCurrentCategory(category) {
    currentCategory.value = category
    currentPage.value = 1
  }

  // 设置分页信息
  function setPagination(page, size) {
    currentPage.value = page
    pageSize.value = size
  }

  return {
    categories,
    newsList,
    currentCategory,
    currentPage,
    pageSize,
    total,
    setCategories,
    getCachedCategories,
    setNewsList,
    setCurrentCategory,
    setPagination
  }
})
