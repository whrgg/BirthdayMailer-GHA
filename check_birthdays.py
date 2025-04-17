import json
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from zhdate import ZhDate
from typing import Dict, List, Any

def get_today_lunar_date():
    # 获取今天的公历日期
    today = datetime.now()
    # 转换为农历日期
    lunar_date = ZhDate.from_datetime(today)
    return {
        'month': lunar_date.lunar_month,
        'day': lunar_date.lunar_day
    }

def format_lunar_date(month, day):
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    return f"农历{lunar_months[month-1]}月{day}日"

def send_birthday_email(birthday_people: List[str], email_config: Dict[str, Any], module_name: str):
    server = None
    try:
        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = email_config['sender']['email']
        msg['To'] = ', '.join(email_config['recipients'])
        msg['Subject'] = f'{module_name}模块 - 农历生日提醒 - {datetime.now().strftime("%Y-%m-%d")}'

        # 获取今天的农历日期
        lunar_today = get_today_lunar_date()
        lunar_date_str = format_lunar_date(lunar_today['month'], lunar_today['day'])

        # 构建邮件正文
        body = f'今天是{lunar_date_str}，{module_name}模块中以下人员过农历生日：\n\n'
        for name in birthday_people:
            body += f'- {name}\n'
        body += '\n祝他们生日快乐！'

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 使用SSL连接SMTP服务器并发送邮件
        server = smtplib.SMTP_SSL(email_config['sender']['smtp_server'], 465, timeout=10)
        server.login(email_config['sender']['email'], 
                    email_config['sender']['password'])
        server.send_message(msg)
        print(f'{module_name}模块的生日提醒邮件已发送成功！')
        
    except Exception as e:
        print(f'发送{module_name}模块邮件时出错：{str(e)}')
        print('请确保：')
        print('1. QQ邮箱已开启SMTP服务')
        print('2. 使用的是正确的授权码而不是QQ密码')
        print('3. email.json中的配置信息正确')
        raise
    finally:
        # 安全关闭连接
        if server:
            try:
                server.quit()
            except (socket.error, smtplib.SMTPServerDisconnected):
                pass  # 忽略关闭连接时的错误

def check_birthdays_for_module(birthday_data: Dict[str, Any], email_config: Dict[str, Any], module_name: str):
    lunar_today = get_today_lunar_date()
    lunar_date_str = format_lunar_date(lunar_today['month'], lunar_today['day'])
    
    birthday_people = []
    for person in birthday_data.get('birthdays', []):
        lunar_date = person['lunar_date']
        if lunar_date['month'] == lunar_today['month'] and lunar_date['day'] == lunar_today['day']:
            birthday_people.append(person['name'])
    
    if birthday_people:
        print(f'今天是{lunar_date_str}，{module_name}模块中以下人员过农历生日：')
        for name in birthday_people:
            print(f'- {name}')
        
        send_birthday_email(birthday_people, email_config, module_name)
    else:
        print(f'今天是{lunar_date_str}，{module_name}模块中没有人过农历生日。')

def load_config(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'错误：找不到配置文件 {file_path}')
        raise
    except json.JSONDecodeError as e:
        print(f'错误：配置文件 {file_path} 格式不正确 - {str(e)}')
        raise

def main():
    try:
        # 加载模块配置
        modules_config = load_config('modules.json')
        
        # 遍历每个模块
        for module in modules_config['modules']:
            module_name = module['name']
            try:
                # 加载模块的生日数据和邮箱配置
                birthday_data = load_config(f'birthdays_{module_name}.json')
                email_config = load_config(f'email_{module_name}.json')
                
                # 检查该模块的生日
                check_birthdays_for_module(birthday_data, email_config, module_name)
                
            except Exception as e:
                print(f'处理{module_name}模块时出错：{str(e)}')
                continue
            
    except Exception as e:
        print(f'发生错误：{str(e)}')

if __name__ == '__main__':
    main() 