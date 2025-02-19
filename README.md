# 动态微信群二维码管理系统  Dynamic Group QR Code Management System

[English Documentation](README_EN.md)

这是一个用于管理微信群（其他群也支持）二维码的Web应用，可以自动切换显示不同群的二维码，当一个群满员后使用下一个新群的二维码。

## 功能特点

- 支持上传多个微信群二维码
- 动态二维码， 永不过期的群二维码，永久二维码
- 每个群都有两个二维码：原始群二维码和永久链接二维码
- 群满员前，管理员后台更新群二维码为新群二维码（ TODO： 自动切换到下一个可用的群二维码）
- 提供管理界面和展示界面
- 展示页面自动刷新，确保二维码始终是最新的
- 支持 HTTPS，确保生产环境下的安全访问

动态二维码的功能，管理后台需要登陆，登陆的用户名密码在 .env 中配置。 每个二维码的专属链接可以匿名访问。

在管理后台中，每个群会显示两个二维码：
1. 原始群二维码 - 上传的实际群二维码
2. 永久链接二维码 - 指向该群专属链接的永久二维码，可以长期使用

在 .env 文件中的配置项：
- URL_PREFIX=qrcode - URL 前缀配置
- PREFERRED_URL_SCHEME=https - URL 协议配置（生产环境使用 https，本地开发使用 http）

使用 Flask Blueprint 来实现 URL 前缀功能
将除了 /group/<display_code> 之外的所有路由移到带前缀的 Blueprint 中

更新了所有 url_for 调用以使用新的 Blueprint 路由名称.

现在的URL结构如下：
/qrcode/ - 重定向到管理后台
/qrcode/group_adm_dna - 管理后台（需要登录）
/qrcode/login - 登录页面
/qrcode/logout - 登出
/group/<display_code> - 显示特定的二维码（保持不变，无前缀）

## 界面预览

### 登录界面
![登录界面](/images/login.png)

### 管理后台
![管理后台](/images/qrcode_admin.png)

## 安装说明

1. 确保已安装 Python 3.10 或更高版本
2. 克隆此仓库到本地
3. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动应用：
   ```bash
   python app.py
   ```

2. 打开浏览器访问：
   - 管理界面：http://localhost:5000/{qrcode}/group_adm_dna
   - 单个二维码的展示界面：http://localhost:5000/group/xxxx

{qrcode} 是 .env 文件中 URL_PREFIX 配置的值， 默认是 qrcode

3. 在管理界面中：
   - 上传新的群二维码
   - 设置群名称和最大成员数
   - 设置显示顺序
   - 管理群成员数量（增加/减少）
   - 删除不需要的二维码

4. 展示界面会自动显示当前活跃的群二维码，并每60秒自动刷新一次

## 注意事项

- 请确保上传的二维码图片清晰可用
- 建议定期检查群成员数量，确保数据准确
- 可以通过调整显示顺序来控制群二维码的切换顺序
- 展示页面建议使用全屏显示，以获得最佳展示效果 