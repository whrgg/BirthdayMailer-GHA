# BirthdayMailer-GHA
用于不太聪明的作者的生日提醒

# 农历生日提醒系统

这是一个基于 GitHub Actions 的自动化农历生日提醒系统。系统每天会自动检查是否有人过农历生日，如果有，则会发送邮件通知。系统支持多个模块（如家庭、朋友等），每个模块可以独立配置邮箱和生日数据。

## 功能特点

- 支持农历生日日期
- 模块化设计（家庭模块、朋友模块等）
- 每个模块独立的邮件接收列表
- 自动每日检查（北京时间早上8点）
- 邮件通知功能
- 安全的配置管理

## 配置说明

1. Fork 这个仓库到你的 GitHub 账号下

2. 在你的仓库中设置以下 GitHub Secrets：
   - `MODULES_CONFIG`: 模块配置
   - `EMAIL_FAMILY_CONFIG`: 家庭模块邮箱配置
   - `BIRTHDAYS_FAMILY_DATA`: 家庭模块生日数据
   - `EMAIL_FRIENDS_CONFIG`: 朋友模块邮箱配置
   - `BIRTHDAYS_FRIENDS_DATA`: 朋友模块生日数据

   设置方法：
   - 进入仓库的 Settings 页面
   - 点击左侧的 Secrets and variables -> Actions
   - 点击 "New repository secret"
   - 分别添加上述配置

3. 配置格式示例

   查看以下示例文件：
   - `modules.json.example`: 模块配置示例
   - `email_family.json.example`: 家庭模块邮箱配置示例
   - `birthdays_family.json.example`: 家庭模块生日数据示例
   - `email_friends.json.example`: 朋友模块邮箱配置示例
   - `birthdays_friends.json.example`: 朋友模块生日数据示例

## 运行时间

- 系统每天北京时间早上 8:00 自动运行
- 你也可以在 GitHub Actions 页面手动触发运行

## 本地测试

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 创建配置文件：
   - 复制所有 `.example` 文件并去掉 `.example` 后缀
   - 修改配置文件中的实际内容

3. 运行脚本：
   ```bash
   python check_birthdays.py
   ```

## 添加新模块

1. 在 `modules.json` 中添加新模块定义
2. 创建对应的邮箱配置文件 `email_模块名.json`
3. 创建对应的生日数据文件 `birthdays_模块名.json`
4. 在 GitHub Secrets 中添加对应的配置

## 注意事项

- 不要直接提交实际的配置文件到仓库
- 使用邮箱的应用专用密码而不是登录密码
- 定期检查 GitHub Actions 的运行日志，确保系统正常运行
- 所有配置文件都应使用 UTF-8 编码，以确保中文显示正常

## QQ邮箱配置说明

1. 开启 SMTP 服务：
   - 登录 QQ 邮箱网页版
   - 点击"设置" -> "账户"
   - 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
   - 开启"POP3/SMTP服务"
   - 按照提示验证身份后，会获得授权码

2. 配置说明：
   - SMTP 服务器：smtp.qq.com
   - SMTP 端口：465
   - 密码：使用授权码而不是QQ密码
