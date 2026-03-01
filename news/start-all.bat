@echo off
REM SuperNews 项目启动脚本 (Windows 版本)
REM 用法: start-all.bat [option]

setlocal enabledelayedexpansion

title SuperNews 项目启动
color 0A
cls

echo ════════════════════════════════════════════════════════════════
echo 蜘蛛 SuperNews 项目启动脚本
echo ════════════════════════════════════════════════════════════════

REM 检查参数
if "%1"=="" (
    echo 用法: start-all.bat [option]
    echo.
    echo 选项:
    echo   frontend   - 启动前端应用
    echo   gateway    - 启动网关服务
    echo   all        - 启动所有服务（默认）
    echo   help       - 显示帮助信息
    echo.
    pause
    exit /b 0
)

set TYPE=%1

REM 启动前端
if "%TYPE%"=="frontend" goto start_frontend
if "%TYPE%"=="all" goto start_all
if "%TYPE%"=="gateway" goto start_gateway
if "%TYPE%"=="help" goto show_help
goto invalid_option

:start_frontend
echo.
echo ━ 启动前端应用 (Vue 3 + Vite)
if not exist "SuperNews_frontend" (
    echo 错误: 找不到 SuperNews_frontend 目录
    pause
    exit /b 1
)

cd SuperNews_frontend

if not exist "node_modules" (
    echo 安装依赖中...
    call npm install
)

echo 启动开发服务器...
start cmd /k npm run dev
echo ✓ 前端运行在 http://localhost:5173
cd ..
pause
exit /b 0

:start_gateway
echo.
echo ━ 启动网关服务 (Spring Cloud Gateway)
if not exist "SpringCloudGateway_CanaryRelease" (
    echo 错误: 找不到 SpringCloudGateway_CanaryRelease 目录
    pause
    exit /b 1
)

cd SpringCloudGateway_CanaryRelease

where java >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Java 环境，请先安装 JDK
    cd ..
    pause
    exit /b 1
)

echo 构建项目中...
call mvn clean package -DskipTests > nul 2>&1

echo 启动网关服务...
start cmd /k mvn spring-boot:run
echo ✓ 网关运行在 http://localhost:8080
cd ..
pause
exit /b 0

:start_all
echo.
echo ━ 启动所有服务

where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 npm，请先安装 Node.js
    pause
    exit /b 1
)

where java >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 Java，请先安装 JDK
    pause
    exit /b 1
)

echo 启动网关服务...
cd SpringCloudGateway_CanaryRelease
if not exist "node_modules" (
    echo 构建项目中...
    call mvn clean package -DskipTests
)
start cmd /k mvn spring-boot:run
cd ..

timeout /t 3 /nobreak

echo 启动前端应用...
cd SuperNews_frontend
if not exist "node_modules" (
    echo 安装依赖中...
    call npm install
)
start cmd /k npm run dev
cd ..

echo.
echo ════════════════════════════════════════════════════════════════
echo ✓ 所有服务已启动！
echo ════════════════════════════════════════════════════════════════
echo.
echo 服务地址:
echo   前端:  http://localhost:5173
echo   网关:  http://localhost:8080
echo.
echo 关闭此窗口或按 Ctrl+C 停止启动脚本
pause
exit /b 0

:show_help
echo SuperNews 项目启动脚本
echo.
echo 用法: start-all.bat [option]
echo.
echo 选项:
echo   frontend  - 启动前端应用
echo   gateway   - 启动网关服务
echo   all       - 启动所有服务
echo   help      - 显示此帮助信息
echo.
echo 示例:
echo   start-all.bat frontend  # 启动前端
echo   start-all.bat gateway   # 启动网关
echo   start-all.bat all       # 启动全部
pause
exit /b 0

:invalid_option
echo 错误: 未知选项 "%TYPE%"
echo 使用 'start-all.bat help' 查看帮助
pause
exit /b 1
