// 令牌管理
export function setToken(token) {
  localStorage.setItem('token', token)
}

export function getToken() {
  return localStorage.getItem('token')
}

export function removeToken() {
  localStorage.removeItem('token')
}

// 缓存管理
export function setCache(key, value, expireTime = 3600000) {
  const data = {
    value,
    expireTime: Date.now() + expireTime
  }
  localStorage.setItem(key, JSON.stringify(data))
}

export function getCache(key) {
  const data = localStorage.getItem(key)
  if (!data) return null
  
  try {
    const parsed = JSON.parse(data)
    if (parsed.expireTime > Date.now()) {
      return parsed.value
    } else {
      localStorage.removeItem(key)
      return null
    }
  } catch {
    return null
  }
}

export function removeCache(key) {
  localStorage.removeItem(key)
}

export function clearAllCache() {
  localStorage.clear()
}
