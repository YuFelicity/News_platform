# SuperNews 项目 - 总体说明

欢迎使用 SuperNews 项目！这是一个完整的、生产级别的新闻应用系统，包含后端灰度发布网关和 Vue 3 前端应用。

## 🎯 项目概览

本项目包含两个独立的、完整的子项目：

### 1. **Spring Cloud Gateway 灰度发布网关** 
一个企业级的微服务网关，支持多种灰度发布策略，用于控制不同用户或流量分配到不同版本的后端服务。

**特点**：
- 🎯 四种灰度策略：用户ID、IP段、请求头、流量百分比
- 🔄 动态配置管理，无需重启
- 🔍 灰度规则实时监控
- 🐳 Docker 容器化部署支持
- 📊 完整的 API 管理接口

### 2. **SuperNews 前端应用** （Vue 3 + Vite）
一个现代化的新闻应用前端，使用最新的 Vue 3 技术栈，提供用户认证、新闻浏览、收藏、历史记录等完整功能。

**特点**：
- 👤 用户认证系统（登录、注册、个人资料）
- 📰 新闻管理（分类、列表、详情、分页）
- ⭐ 收藏功能（添加、删除、列表管理）
- 📋 浏览历史（自动记录、清除）
- 💾 智能缓存（带过期时间）
- 📱 响应式设计（PC + 移动端）
- ⚡ 性能优化（路由懒加载、缓存）

## 📁 项目结构

```
qianwen/
├── SpringCloudGateway_CanaryRelease/    # 后端网关项目
├── SuperNews_frontend/                   # 前端应用项目
├── DELIVERY_SUMMARY.md                   # 交付总结
├── PROJECT_CHECKLIST.md                  # 项目清单
├── start-all.sh                          # 快速启动脚本（Linux/Mac）
└── start-all.bat                         # 快速启动脚本（Windows）
```

## 🚀 快速开始

### 前置条件

**后端要求**：
- Java JDK 11 或更高版本
- Maven 3.6.0 或更高版本

**前端要求**：
- Node.js 16.0.0 或更高版本
- npm 8.0.0 或更高版本

**可选**：
- Docker 和 Docker Compose（用于容器化部署）

### 启动方式一：使用启动脚本（推荐）

#### Windows 用户：
```bash
# 启动所有服务
start-all.bat all

# 查看帮助
start-all.bat help
```

#### Linux/Mac 用户：
```bash
# 启动所有服务
bash start-all.sh all

# 查看帮助
bash start-all.sh help
```

### 启动方式二：手动启动

#### 1. 启动前端应用

```bash
cd SuperNews_frontend
npm install
npm run dev
```

浏览器访问：http://localhost:5173

#### 2. 启动网关服务

```bash
cd SpringCloudGateway_CanaryRelease
mvn clean package
mvn spring-boot:run
```

访问：http://localhost:8080

## 📖 项目文档

### 后端网关文档
- [README](SpringCloudGateway_CanaryRelease/README.md) - 项目概况和功能说明
- [快速开始](SpringCloudGateway_CanaryRelease/GETTING_STARTED.md) - 部署和运行指南
- [API 示例](SpringCloudGateway_CanaryRelease/EXAMPLES.md) - 详细的 API 使用示例
- [配置示例](SpringCloudGateway_CanaryRelease/CONFIG_EXAMPLES.md) - 生产环境配置方案

### 前端应用文档
- [README](SuperNews_frontend/README.md) - 项目说明
- [开发指南](SuperNews_frontend/DEVELOPER_GUIDE.md) - 开发者必读
- [项目总结](SuperNews_frontend/PROJECT_SUMMARY.md) - 功能和技术总结

### 总体文档
- [交付总结](DELIVERY_SUMMARY.md) - 两个项目的交付成果
- [项目清单](PROJECT_CHECKLIST.md) - 详细的完成情况

## ✨ 核心功能

### 后端功能
| 功能 | 描述 | 状态 |
|------|------|------|
| 用户ID灰度 | 指定用户总是路由到灰度版本 | ✅ |
| IP段灰度 | 指定IP段的用户路由到灰度版本 | ✅ |
| 请求头灰度 | 带特定请求头的请求路由到灰度版本 | ✅ |
| 流量灰度 | 按比例将部分流量路由到灰度版本 | ✅ |
| 动态配置 | 通过 API 动态配置灰度规则 | ✅ |
| 服务发现 | Eureka 服务发现和注册 | ✅ |

### 前端功能
| 功能 | 描述 | 状态 |
|------|------|------|
| 用户认证 | 登录、注册、个人资料等 | ✅ |
| 新闻浏览 | 分类、列表、详情、分页 | ✅ |
| 收藏功能 | 添加、删除、查看收藏 | ✅ |
| 历史记录 | 自动记录、查看、删除历史 | ✅ |
| 本地缓存 | 智能缓存，带过期时间 | ✅ |
| 响应式设计 | PC 和移动端完全适配 | ✅ |

## 🛠️ 技术栈

### 后端
- **框架**: Spring Boot 2.7.14 + Spring Cloud 2021.0.5
- **网关**: Spring Cloud Gateway
- **服务发现**: Eureka
- **容器化**: Docker + Docker Compose
- **构建工具**: Maven
- **Runtime**: Java JDK 11+

### 前端
- **框架**: Vue 3.3.4 + Vite 4.5.0
- **路由**: Vue Router 4.2.5
- **状态管理**: Pinia 2.1.6
- **HTTP 客户端**: Axios 1.5.0
- **UI 组件库**: Element Plus 2.4.2
- **样式**: SCSS
- **代码规范**: ESLint + Prettier
- **Runtime**: Node.js 16+

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| 总文件数 | 50+ |
| 代码行数 | 4500+ |
| API 接口数 | 15+ |
| 页面组件数 | 9 |
| 文档文件数 | 7 |
| 完成度 | 100% |

## 💡 使用场景

### 适用于
- ✅ 企业级新闻类应用
- ✅ 灰度发布需求
- ✅ 学习 Vue 3 和 Spring Cloud
- ✅ 微服务架构参考
- ✅ 生产环境部署

### 功能扩展方向
- 搜索功能（全文搜索、推荐搜索）
- 评论系统（用户评论、点赞）
- 内容推荐（个性化推荐、热门推荐）
- 用户社交（关注、粉丝、分享）
- 实时通知（Web Socket、服务端推送）
- 内容分析（阅读时长、热门内容分析）

## 🔒 安全特性

- ✅ JWT 令牌认证
- ✅ 密码加密存储
- ✅ 会话管理
- ✅ CORS 跨域配置
- ✅ 请求验证
- ✅ 错误处理

## 📈 性能指标

| 指标 | 目标 | 说明 |
|------|------|------|
| 首页加载 | < 2 秒 | 含所有资源 |
| API 响应 | < 500 ms | 平均响应时间 |
| 缓存命中率 | > 80% | 频繁访问页面 |
| 包体积 | < 500 KB | gzip 压缩后 |

## 🐛 故障诊断

### 前端无法连接后端
1. 检查 vite.config.js 中的 proxy 配置
2. 确保后端服务运行在正确的端口
3. 检查浏览器开发者工具的 Network 标签页

### 登录失败
1. 确保后端 API 服务已启动
2. 检查用户名和密码是否正确
3. 查看浏览器控制台是否有错误信息

### 灰度规则不生效
1. 检查灰度规则是否正确配置
2. 查看 Gateway 日志文件
3. 通过管理 API 查看当前配置

详见各项目的文档文件。

## 🤝 贡献指南

本项目采用标准的 Git 工作流程：
1. 从 main 分支创建开发分支
2. 在分支上进行开发和测试
3. 提交 Pull Request 进行代码审查
4. 通过审查后合并到 main

## 📞 获取帮助

### 快速查询
- 前端问题 → 查看 [`SuperNews_frontend/DEVELOPER_GUIDE.md`](SuperNews_frontend/DEVELOPER_GUIDE.md)
- 后端问题 → 查看 [`SpringCloudGateway.../GETTING_STARTED.md`](SpringCloudGateway_CanaryRelease/GETTING_STARTED.md)
- API 问题 → 查看 [`...EXAMPLES.md`](SpringCloudGateway_CanaryRelease/EXAMPLES.md)

### 常见问题
- npm 依赖安装失败 → 清除 node_modules，执行 `npm install`
- 端口被占用 → 修改配置文件中的端口
- Java 版本问题 → 确保 JDK 版本 >= 11

## 📝 许可证

本项目代码可自由使用和修改。

## 🎉 致谢

感谢使用本项目！希望它能帮助你：
- ✅ 学习现代 Web 开发技术
- ✅ 理解微服务架构设计
- ✅ 掌握灰度发布的最佳实践
- ✅ 加速你的企业应用开发

---

## 📋 快速检查清单

启动项目前：
- [ ] 安装了 Node.js 16+
- [ ] 安装了 Java JDK 11+
- [ ] 安装了 Maven 3.6+
- [ ] 克隆或下载了项目文件

启动项目后：
- [ ] 前端正常运行在 http://localhost:5173
- [ ] 后端网关正常运行在 http://localhost:8080
- [ ] 能够登录到前端应用
- [ ] 能够正常加载新闻列表

## 🚀 下一步

1. **快速启动**：运行 `start-all.sh` 或 `start-all.bat`
2. **浏览文档**：查看项目中的 README 和指南文件
3. **开始开发**：根据需要修改和扩展代码
4. **部署上线**：参考文档中的部署指南

---

**版本**：1.0.0  
**更新日期**：2026-02-06  
**状态**：✅ 生产就绪

**祝你使用愉快！** 🎊

