#!/bin/bash

# SuperNews 项目启动脚本
# 用法: bash start-all.sh

echo "════════════════════════════════════════════════════════════════"
echo "🚀 SuperNews 项目启动"
echo "════════════════════════════════════════════════════════════════"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否有参数
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}用法:${NC}"
    echo "  bash start-all.sh [option]"
    echo ""
    echo -e "${YELLOW}选项:${NC}"
    echo "  frontend     - 只启动前端"
    echo "  gateway      - 只启动网关"
    echo "  all          - 启动所有服务（默认）"
    echo "  dev          - 开发模式（前端 + 网关）"
    echo "  help         - 显示帮助信息"
    echo ""
    exit 0
fi

TYPE=${1:-all}

# 检查必要的命令
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}错误: 未找到 $1 命令${NC}"
        return 1
    fi
    return 0
}

# 启动前端
start_frontend() {
    echo -e "\n${BLUE}─ 启动前端应用${NC} (Vue 3 + Vite)"
    
    # 检查目录
    if [ ! -d "SuperNews_frontend" ]; then
        echo -e "${RED}错误: 找不到 SuperNews_frontend 目录${NC}"
        return 1
    fi
    
    cd SuperNews_frontend
    
    # 检查dependencies
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}安装依赖中...${NC}"
        npm install
    fi
    
    echo -e "${GREEN}✓ 启动开发服务器...${NC}"
    npm run dev &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ 前端运行在 http://localhost:5173${NC}"
    echo -e "${GREEN}✓ 进程 ID: $FRONTEND_PID${NC}"
    
    cd ..
    return 0
}

# 启动网关
start_gateway() {
    echo -e "\n${BLUE}─ 启动网关服务${NC} (Spring Cloud Gateway)"
    
    # 检查目录
    if [ ! -d "SpringCloudGateway_CanaryRelease" ]; then
        echo -e "${RED}错误: 找不到 SpringCloudGateway_CanaryRelease 目录${NC}"
        return 1
    fi
    
    cd SpringCloudGateway_CanaryRelease
    
    # 检查 Java
    if ! check_command java; then
        return 1
    fi
    
    echo -e "${YELLOW}构建项目中...${NC}"
    mvn clean package -DskipTests > /dev/null 2>&1
    
    echo -e "${GREEN}✓ 启动网关服务...${NC}"
    mvn spring-boot:run &
    GATEWAY_PID=$!
    echo -e "${GREEN}✓ 网关运行在 http://localhost:8080${NC}"
    echo -e "${GREEN}✓ 进程 ID: $GATEWAY_PID${NC}"
    
    cd ..
    return 0
}

# 启动所有服务
case $TYPE in
    frontend)
        start_frontend
        ;;
    gateway)
        start_gateway
        ;;
    all|dev)
        check_command npm || exit 1
        check_command java || exit 1
        
        # 并行启动
        start_gateway &
        sleep 3
        start_frontend &
        
        echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}✓ 所有服务已启动！${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${BLUE}服务地址:${NC}"
        echo -e "  前端: ${GREEN}http://localhost:5173${NC}"
        echo -e "  网关: ${GREEN}http://localhost:8080${NC}"
        echo ""
        echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"
        
        wait
        ;;
    help)
        echo -e "${BLUE}SuperNews 项目启动脚本${NC}"
        echo ""
        echo "用法: bash start-all.sh [option]"
        echo ""
        echo "选项:"
        echo "  frontend   - 只启动前端应用"
        echo "  gateway    - 只启动网关服务"
        echo "  all/dev    - 启动所有服务"
        echo "  help       - 显示此帮助信息"
        echo ""
        echo "示例:"
        echo "  bash start-all.sh frontend  # 启动前端"
        echo "  bash start-all.sh gateway   # 启动网关"
        echo "  bash start-all.sh all       # 启动全部"
        ;;
    *)
        echo -e "${RED}未知选项: $TYPE${NC}"
        echo "使用 'bash start-all.sh help' 查看帮助"
        exit 1
        ;;
esac
