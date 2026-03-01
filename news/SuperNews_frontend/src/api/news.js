import request from '@/utils/request'

// 获取新闻分类
export function getCategories(params = {skip:0,limit:100}) {
  return request.get('news/categories',{params})
}

// 获取新闻列表
export function getNewsList(categoryId, page = 1, pageSize = 10) {
  return request.get('news/list', {
    params: { categoryId, page, pageSize }
  })
}

// 获取新闻详情
export function getNewsDetail(newsId) {
  return request.get('news/detail', {
    params: { id: newsId } // 核心：用params传参，且参数名必须是id
  })
}

// 添加浏览记录
export function addHistory(newsId) {
  return request.post('history/add', { newsId })
}

// 获取浏览历史
export function getHistory(page = 1, pageSize = 10) {
  return request.get('history/list', {
    params: { page, pageSize }
  })
}

// 删除单条历史
export function deleteHistory(historyId) {
  return request.delete(`history/${historyId}`)
}

// 清空历史
export function clearHistory() {
  return request.delete('history/clear')
}
