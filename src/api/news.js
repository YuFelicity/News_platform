import request from '@utils/request'//导入axios
//新闻分类
export function getCategoryList(){
    return request.get('/news/category/list')//与基础路径产生关联
}
//新闻列表
export function getNewsList(params){
    return request.get('/news/list',params)
}//params是传给后端的查询参数，将参数拼接到查询字符串上