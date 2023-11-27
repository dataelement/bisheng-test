import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def email_util(att=None, content=None, subject=None,):
    """发送邮件的工具方法"""
    username = 'from@dataelem.com'  # 待替换
    password = '*****'
    receiver = 'to@dataelem.com'  # 接收邮箱
    content = content

    output_path = os.environ.get('OUTPUT_PATH', '/app/output')
    # 不带附件的
    if att is None:  
        message = MIMEText(content)
        message['subject'] = subject
        message['from'] = username
        message['to'] = receiver
    else:
        # 带附件发送
        message = MIMEMultipart()
        txt = MIMEText(content, _charset='utf-8', _subtype="html")
        part = MIMEApplication(open('%s/%s' % (output_path, att), 'rb').read())
        part.add_header(
            'Content-Disposition', 'attachment', filename=att.split('\\')[-1])
        message['subject'] = subject
        message['from'] = username
        message['to'] = receiver
        message.attach(txt)
        message.attach(part)

    # 登录smtp服务器
    smtpserver = 'smtp.163.com'
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(username, receiver, message.as_string())
    smtp.quit()


if __name__ == '__main__':
    email_util(
        content="<i>测试发送邮件测试报告内容</i>", 
        subject="测试发送邮件-主题", 
        att='data/images/result.jpeg')
