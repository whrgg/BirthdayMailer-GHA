# BirthdayMailer-GHA
用于不太聪明的作者的生日提醒

# 农历生日提醒系统

这是一个基于 GitHub Actions 的自动化农历生日提醒系统。系统每天会自动检查是否有人过农历生日，如果有，则会发送邮件通知。

## 功能特点

- 支持农历生日日期
- 自动每日检查
- 邮件通知功能
- 安全的配置管理

## 配置说明

1. Fork 这个仓库到你的 GitHub 账号下

2. 在你的仓库中设置以下 GitHub Secrets：
   - `EMAIL_CONFIG`: 邮箱配置（参考 email.json.example）
   - `BIRTHDAY_DATA`: 生日数据（参考 birthday.json.example）

   设置方法：
   - 进入仓库的 Settings 页面
   - 点击左侧的 Secrets and variables -> Actions
   - 点击 "New repository secret"
   - 分别添加 EMAIL_CONFIG 和 BIRTHDAY_DATA

3. 配置格式

   EMAIL_CONFIG 格式：
   ```json
   {
       "sender": {
           "email": "your_email@example.com",
           "password": "your_app_password",
           "smtp_server": "smtp.example.com",
           "smtp_port": 587
       },
       "recipients": [
           "recipient1@example.com",
           "recipient2@example.com"
       ]
   }
   ```

   BIRTHDAY_DATA 格式：
   ```json
   {
       "birthdays": [
           {
               "name": "张三",
               "lunar_date": {
                   "month": 2,
                   "day": 15
               }
           }
       ]
   }
   ```

## 运行时间

- 系统每天 UTC 0:00（北京时间 8:00）自动运行
- 你也可以在 GitHub Actions 页面手动触发运行

## 本地测试

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 创建配置文件：
   - 复制 `email.json.example` 为 `email.json` 并填写实际配置
   - 复制 `birthday.json.example` 为 `birthday.json` 并填写实际数据

3. 运行脚本：
   ```bash
   python check_birthdays.py
   ```

## 注意事项

- 不要直接提交 `email.json` 和 `birthday.json` 到仓库
- 使用邮箱的应用专用密码而不是登录密码
- 定期检查 GitHub Actions 的运行日志，确保系统正常运行
