# 动态微信群二维码管理系统

这是一个用于管理微信群二维码的Web应用，可以自动切换显示不同群的二维码，当一个群满员后自动切换到下一个群的二维码。

## 功能特点

- 支持上传多个微信群二维码
- 可以设置群的最大人数
- 自动追踪群成员数量
- 当群满员时自动切换到下一个可用的群二维码
- 提供管理界面和展示界面
- 展示页面自动刷新，确保二维码始终是最新的

## 安装说明

1. 确保已安装 Python 3.7 或更高版本
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
   - 管理界面：http://localhost:5000
   - 展示界面：http://localhost:5000/display

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