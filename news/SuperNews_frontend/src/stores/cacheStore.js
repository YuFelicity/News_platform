import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCacheStore = defineStore('cache', () => {
  const newsDetailCache = ref(new Map())
  const listCache = ref(new Map())

  // 设置新闻详情缓存
  function setNewsDetailCache(newsId, data) {
    newsDetailCache.value.set(newsId, {
      data,
      time: Date.now()
    })
  }

  // 获取新闻详情缓存
  function getNewsDetailCache(newsId) {
    const item = newsDetailCache.value.get(newsId)
    if (!item) return null
    
    // 1小时过期
    if (Date.now() - item.time > 3600000) {
      newsDetailCache.value.delete(newsId)
      return null
    }
    return item.data
  }

  // 清空缓存
  function clearCache() {
    newsDetailCache.value.clear()
    listCache.value.clear()
  }

  return {
    newsDetailCache,
    listCache,
    setNewsDetailCache,
    getNewsDetailCache,
    clearCache
  }
})
