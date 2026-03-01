import request from '@/utils/request'

// 用户注册
export function register(username, password) {
  return request.post('user/register', { username, password })
}

// 用户登录
export function login(username, password) {
  return request.post('user/login', { username, password })
}

// 获取用户信息
export function getUserInfo() {
  return request.get('user/info')
}

// 更新用户信息
export function updateUserInfo(data) {
  return request.put('user/info', data)
}

// 修改密码
export function changePassword(oldPassword, newPassword) {
  return request.post('user/password', { oldPassword, newPassword })
}
