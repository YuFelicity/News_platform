// 时间格式化
export function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

// 截断文本
export function truncateText(text, length = 50) {
  return text && text.length > length ? text.slice(0, length) + '...' : text
}

// 保留两位小数
export function formatNumber(num) {
  return Number(num).toFixed(2)
}
