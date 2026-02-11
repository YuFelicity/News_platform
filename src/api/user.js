import request from'@/utils.request'
import { id } from 'element-plus/es/locale/index.mjs'
export function login(data)
{
    return request.post(`/user/login`,data)
}
export function register(data){
    return request.post(`/user/register`,data)
}
export function getUserInfo()
{
    return request.get(`/user/info`)
}
export function updateUser(data)
{
    return request.put(`/user/update`,data)

}
export function updatePassword(data)
{
    return request.put(`/user/password`,data)
}