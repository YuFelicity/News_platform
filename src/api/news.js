import request from '@/utils/request'

// 获取新闻分类
export function getCategories() {
  return request.get('/news/categories')
}

// 获取新闻列表
export function getNewsList(category, page = 1, pageSize = 10) {
  return request.get('/news/list', {
    params: { category, page, pageSize }
  })
}

// 获取新闻详情
export function getNewsDetail(newsId) {
  return request.get(`/news/${newsId}`)
}

// 添加浏览记录
export function addHistory(newsId) {
  return request.post('/history/add', { newsId })
}

// 获取浏览历史
export function getHistory(page = 1, pageSize = 10) {
  return request.get('/history/list', {
    params: { page, pageSize }
  })
}

// 删除单条历史
export function deleteHistory(historyId) {
  return request.delete(`/history/${historyId}`)
}

// 清空历史
export function clearHistory() {
  return request.delete('/history/clear')
}
