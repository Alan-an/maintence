#!/usr/bin/python
#coding=gbk
#coding=utf-8
import re
import os
import smtplib
import linecache
from email.mime.text import MIMEText
mailto_list=["ezio_shi@adata.com.cn"]
mail_host="192.168.170.170"  #���÷�����
mail_user="ezio_shi"    #�û���
#mail_pass="296701298a!"   #����
mail_postfix="adata.com.cn"  #������ĺ�׺
def send_mail(to_list,sub,content):  #to_list���ռ��ˣ�sub�����⣻content���ʼ�����
    me="ServerSpaceAlert"+"<"+mail_user+"@"+mail_postfix+">"   #�����hello�����������ã��յ��ź󣬽�����������ʾ
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #����һ��ʵ������������Ϊhtml��ʽ�ʼ�
    msg['Subject'] = sub    #��������
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #����smtp������
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        #s.login(mail_user,mail_pass)  #��½������
        s.sendmail(me, to_list, msg.as_string())  #�����ʼ�
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False



def disktype(ipaddress):
    disknum=1
    diskcount=[]
    fp1=os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.2')
    for i in fp1:
        if 'hrStorageFixedDisk' in i:
            diskcount.append(disknum)
        disknum=disknum+1
    fp1.close()
    return diskcount
def disklabel(ipaddress,diskcount):
    labelname=[]
    j=1
    fp2=os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.3')
    for i in fp2:
        if j in diskcount:
            k=re.findall('(?<= STRING: )\S',i)
            labelname.append(k)
            j=j+1
        else:
            j=j+1
    return labelname
def diskunits(ipaddress,diskcount):
    unitsize=[]
    j=1
    fp3=os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.4')
    for i in fp3:
        if j in diskcount:
            k=re.findall('(?<= INTEGER: )\d+',i)
            unitsize.append(k)
            j=j+1
        else:
            j=j+1
    return unitsize
def disktotalsize(ipaddress,diskcount):
    disksize=[]
    j=1
    fp4=os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.5')
    for i in fp4:
        if j in diskcount:
            k=re.findall('(?<= INTEGER: )\d+',i)
            disksize.append(k)
            j=j+1
        else:
            j=j+1
    return disksize
    
def diskusedsize(ipaddress,diskcount):
    diskused=[]
    j=1
    fp5=os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.6')
    for i in fp5:
        if j in diskcount:
            k=re.findall('(?<= INTEGER: )\d+',i)
            diskused.append(k)
            j=j+1
        else:
            j=j+1
    return diskused
def diskfailuresnum(ipaddress,diskcount):
    diskfailures = []
    j = 1
    fp6 =os.popen('snmpwalk -v 2c -c public '+ ipaddress +' 1.3.6.1.2.1.25.2.3.1.7')
    for i in fp6:
        if j in diskcount:
            k=re.findall('(?<= INTEGER: )\d+',i)
            diskfailures.append(k)
            j=j+1
        else:
            j=j+1
    return diskfailures
def result(ipaddress,diskcount,alert):
    leng=len(diskcount)
    k=1
    for k in range(1, leng + 1):
        totalspace=(int(unitsize[k-1][0]) * int(disksize[k-1][0]))/1024/1024/1024
        #print 'The Total Size of  '+ labelname[k-1][0] +' Dirver on '+ipaddress+' is ' + str(totalspace)+' G'
        freespace = (int(unitsize[k - 1][0]) * int(disksize[k - 1][0])) / 1024 / 1024 / 1024 - (int(unitsize[k - 1][0]) * int(diskused[k - 1][0])) / 1024 / 1024 / 1024
        print 'The Free Space of  '+ labelname[k-1][0] +' Dirver on '+ ipaddress+' is  ' + str(freespace)+' G'
        diskusage=float(totalspace-freespace)/float(totalspace)*100
        alertcontent='Be Careful, The Usage of '+ labelname[k-1][0]+' Driver on '+ipaddress+' is '+ str(diskusage)+' Used'
        if diskusage>=90:
            alert=alert+alertcontent
    return alert
if __name__ == '__main__':
    ip=open(r'/root/ipaddress.txt','r')
    alert=''
    for ipaddress in ip:
        ipaddress=ipaddress.strip()
        diskcount=disktype(ipaddress)
        labelname=disklabel(ipaddress,diskcount)
        unitsize=diskunits(ipaddress,diskcount)
        disksize=disktotalsize(ipaddress,diskcount)
        diskused = diskusedsize(ipaddress,diskcount)
        diskfailures=diskfailuresnum(ipaddress,diskcount)
        alert=result(ipaddress,diskcount,alert)
    if alert!='':
    	send_mail(mailto_list,"ServerSpaceAlert",alert)
    ip.close()
