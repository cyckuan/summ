#! /usr/bin/env python

def send_mail(me,you,subject,message_string):
	""" sends quick email alert
	"""
	
	import smtplib
	from email.mime.text import MIMEText

	msg = MIMEText(message_string)
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = you

	s = smtplib.SMTP('localhost')
	s.sendmail(me, [you], msg.as_string())
	s.quit()