import request from '@/utils/request'

// 检查收藏状态
export function checkFavorite(newsId) {
  return request.get(`/favorites/check/${newsId}`)
}

// 添加收藏
export function addFavorite(newsId) {
  return request.post('/favorites/add', { newsId })
}

// 取消收藏
export function removeFavorite(newsId) {
  return request.delete(`/favorites/${newsId}`)
}

// 获取收藏列表
export function getFavoriteList(page = 1, pageSize = 10) {
  return request.get('/favorites/list', {
    params: { page, pageSize }
  })
}

// 清空所有收藏
export function clearFavorites() {
  return request.delete('/favorites/clear')
}
