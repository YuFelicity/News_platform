import request from '@/utils/request'

// 用户注册
export function register(username, password) {
  return request.post('/auth/register', { username, password })
}

// 用户登录
export function login(username, password) {
  return request.post('/auth/login', { username, password })
}

// 获取用户信息
export function getUserInfo() {
  return request.get('/users/info')
}

// 更新用户信息
export function updateUserInfo(data) {
  return request.put('/users/info', data)
}

// 修改密码
export function changePassword(oldPassword, newPassword) {
  return request.post('/users/password', { oldPassword, newPassword })
}
