#!/usr/bin/python
#coding=gbk
#coding=utf-8
import os
import time
import smtplib
from email.MIMEText import MIMEText
mailto_list=["ezio_shi@adata.com.cn","lin_gao@adata.com.cn","mark_zhang@adata.com.cn"]
mail_host="192.168.170.170"  #���÷�����
mail_user="ezio_shi"    #�û���
#mail_pass="296701298a!"   #����
mail_postfix="adata.com.cn"  #������ĺ�׺

def send_mail(to_list,sub,content):  #to_list���ռ��ˣ�sub�����⣻content���ʼ�����
    me="Tablespace Warnning"+"<"+mail_user+"@"+mail_postfix+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #����һ��ʵ������������Ϊhtml��ʽ�ʼ�
    msg['Subject'] = sub    #��������
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #����smtp������
        #s.set_debuglevel(1)
        s.ehlo()
        #s.starttls()
        #s.login(mail_user,mail_pass)  #��½������
        s.sendmail(me, to_list, msg.as_string())  #�����ʼ�
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
values={}
#fp=open(r'c:\re.txt','rb')
fp=os.popen('/home/oracle/db_check/tab_spa.sh')
k=1
for i in fp:
    if k>3 and k<33:
        j= i.split()
        values['name']=j[0]
        values['usage']=j[3]
        values['fusage']=float(j[3][:-1])
        if values['fusage']>95:
            result='Be careful,the space of '+values['name'] +' is ' +values['usage']+' Used'
            send_mail(mailto_list,"Tablespace Warnning",result)
    k=k+1
