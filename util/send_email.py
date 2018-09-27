
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class SendEmail:
    global send_user
    global email_host
    global password

    def send_mail(self, user_list, title, content,file=None, filename=None):
        user = "Xdchen" + "<" + "cxdtotsj@163.com" + ">"

        server = smtplib.SMTP()
        server.connect("smtp.163.com")
        server.login("cxdtotsj@163.com", "cxd19900527")

        '''设置邮件标题、发送者、发送对象、发送内容、发送附件'''
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = user
        msg['To'] = ";".join(user_list)
        # 邮件内容
        text = MIMEText(content, _subtype='html', _charset='utf-8')
        msg.attach(text)
        # 邮件附件
        att = MIMEApplication(open(file, 'rb').read())
        att['Content-Type'] = 'application/octet-stream'
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(att)

        server.sendmail(user, user_list, msg.as_string())
        server.close()

    def send_main(self, result_file,report_name):
        file = open(result_file, 'r',encoding='utf-8')
        html_content = file.read()
        file.close()
        '''
        report_file : 要发送的附件文件
        report_name : 要发送的附件名称
        '''
        report_file = result_file

        user_list = ['1183008543@qq.com']
        title = "接口自动化测试报告"

        self.send_mail(user_list, title, html_content,report_file, report_name)
