import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from zhdate import ZhDate

def get_today_lunar_date():
    # 获取今天的公历日期
    today = datetime.now()
    # 转换为农历日期
    lunar_date = ZhDate.from_datetime(today)
    return lunar_date

def format_lunar_date(month, day):
    lunar_months = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
    return f"农历{lunar_months[month-1]}月{day}日"

def send_birthday_email(birthday_people, email_config):
    try:
        # 创建邮件内容
        msg = MIMEMultipart()
        msg['From'] = email_config['sender']['email']
        msg['To'] = ', '.join(email_config['recipients'])
        msg['Subject'] = f'农历生日提醒 - {datetime.now().strftime("%Y-%m-%d")}'

        # 获取今天的农历日期
        lunar_today = get_today_lunar_date()
        lunar_date_str = format_lunar_date(lunar_today.month, lunar_today.day)

        # 构建邮件正文
        body = f'今天是{lunar_date_str}，以下人员过农历生日：\n\n'
        for name in birthday_people:
            body += f'- {name}\n'
        body += '\n祝他们生日快乐！'

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 连接SMTP服务器并发送邮件
        with smtplib.SMTP(email_config['sender']['smtp_server'], 
                         email_config['sender']['smtp_port']) as server:
            server.starttls()
            server.login(email_config['sender']['email'], 
                        email_config['sender']['password'])
            server.send_message(msg)
        
        print('生日提醒邮件已发送成功！')
        
    except Exception as e:
        print(f'发送邮件时出错：{str(e)}')

def check_birthdays():
    try:
        # 读取birthday.json文件
        with open('birthday.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 读取email.json文件
        with open('email.json', 'r', encoding='utf-8') as file:
            email_config = json.load(file)
        
        # 获取今天的农历日期
        lunar_today = get_today_lunar_date()
        lunar_date_str = format_lunar_date(lunar_today.month, lunar_today.day)
        
        # 检查今天是否有人过生日
        birthday_people = []
        for person in data['birthdays']:
            lunar_date = person['lunar_date']
            if lunar_date['month'] == lunar_today.month and lunar_date['day'] == lunar_today.day:
                birthday_people.append(person['name'])
        
        # 输出结果
        if birthday_people:
            print(f'今天是{lunar_date_str}，以下人员过农历生日：')
            for name in birthday_people:
                print(f'- {name}')
            
            # 发送生日提醒邮件
            send_birthday_email(birthday_people, email_config)
        else:
            print(f'今天是{lunar_date_str}，没有人过农历生日。')
            
    except FileNotFoundError as e:
        if 'birthday.json' in str(e):
            print('错误：找不到 birthday.json 文件')
        elif 'email.json' in str(e):
            print('错误：找不到 email.json 文件')
    except json.JSONDecodeError as e:
        print(f'错误：JSON 文件格式不正确 - {str(e)}')
    except Exception as e:
        print(f'发生错误：{str(e)}')

if __name__ == '__main__':
    check_birthdays() 