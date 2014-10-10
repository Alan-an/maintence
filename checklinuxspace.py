#!/usr/bin/python
#coding=gbk
#coding=utf-8
import re
import os
import smtplib
from email.MIMEText import MIMEText
mailto_list=["ezio_shi@adata.com.cn"]
mail_host="192.168.170.170"  #���÷�����
mail_user="ezio_shi"    #�û���
#mail_pass="296701298a!"   #����
mail_postfix="adata.com.cn"  #������ĺ�׺

def send_mail(to_list,sub,content):  #to_list���ռ��ˣ�sub�����⣻content���ʼ�����
    me="LinuxSpace Warnning"+"<"+mail_user+"@"+mail_postfix+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
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

def checkspace(ipaddress,alert):
    #fp=os.popen('ssh '+ipaddress +  ' \'df -h |awk \'{if ($1==$NF){a=$1;printf $a}else{print $0}}\'\'')
    fp=os.popen('ssh '+ipaddress +  ' df -h |awk \'{if ($1==$NF){printf $1}else{print $0}}\'')
    k=1
    #print ipaddress+'\n'+fp.read()
    for i in fp:
        j=i.split()
        if k>1:
            #print j[4]
            if int(j[4][:-1])> 80:
               alertcontent='The Space of '+j[0]+' on '+ipaddress+' is '+j[4]+' Used!'
               alert=alert+alertcontent
               #print alert
               k+k+1
        else:
            k=k+1
    return alert

if __name__ == '__main__':
    alert=''
    ip=open(r'/root/linuxip.txt','r')
    for ipaddress in ip:
        ipaddress=ipaddress.strip()
        alert=checkspace(ipaddress,alert)
    #print alert
    if alert != '':
        send_mail(mailto_list,"LinixSpace Warnning",alert)
