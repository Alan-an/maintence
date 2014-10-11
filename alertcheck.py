#!/usr/bin/python
#coding=gbk
#coding=utf-8
import smtplib
import os
import time
from email.MIMEText import MIMEText
mailto_list=["ezio_shi@adata.com.cn"]
mail_host="192.168.170.170"  #���÷�����
mail_user="ezio_shi"    #�û���
mail_postfix="adata.com.cn"  #������ĺ�׺

def send_mail(to_list,sub,content):  #to_list���ռ��ˣ�sub�����⣻content���ʼ�����
    me="OracleAlert"+"<"+mail_user+"@"+mail_postfix+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #����һ��ʵ������������Ϊhtml��ʽ�ʼ�
    msg['Subject'] = sub    #��������
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #����smtp������
        #s.set_debuglevel(1)
        s.helo()
        #s.starttls()
        #s.login(mail_user,mail_pass)  #��½������
        s.sendmail(me, to_list, msg.as_string())  #�����ʼ�
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    result=os.popen('tail -n 1000 /oracle/admin/ADATAMES/bdump/alert_ADATAMES1.log | awk  \'/Error/\' || \'/failed/\' {print $0}').read()
    if result != '':
        send_mail(mailto_list,"OracleAlert",result)
    else:
	print ' there are  no  errors on oracle at '+ time.strftime("%d/%m/%Y %H:%M:%S")

