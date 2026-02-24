import request from '@/utils/request'//导入axios
//新闻分类
export function getCategoryList(){
    return request.get(`/news/categories/list`)//与基础路径产生关联
}
//新闻列表
export function getNewsList(params){
    return request.get(`/news/list`,params)
}//params是传给后端的查询参数，将参数拼接到查询字符串上
//新闻详情
export function getNewsDetail(id){
    return request.get(`news/detail/${id}`)
}
//添加收藏
export function addFavorite(id) {
  return request.post(`/favorite/add/${id}`)
}
// 取消收藏
export function cancelFavorite(id) {
  return request.delete(`/favorite/remove/${id}`)
}
//收藏列表
export function getFavoriteList()
{
    return request.post(`/favorite/list`)
}
//历史列表
export function getHistoryList()
{
    return request.get(`/history/list`)
}
//删除历史
export function removeHistory()
{
    return request.delete(`/history/delete/${id}`)
}