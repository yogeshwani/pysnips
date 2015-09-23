#!/usr/bin/env python

import simplejson, urllib
from datetime import datetime  
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import smtplib
import csv
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


filename ="/home/yogesh/travel_time_at6pm.png"
csv_file = "/home/yogesh/travel_data_at6pm.csv"

longstanton = 52.280993, 0.05950
office = 52.230744,0.158977
waterbeach = 52.268294,0.193990
cottenham = 52.286757,0.126040

def get_travel_data(orig,dest):
	url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig),str(dest))
	result= simplejson.load(urllib.urlopen(url))
	driving_time = result['rows'][0]['elements'][0]['duration']['text']
	driving_value = (result['rows'][0]['elements'][0]['duration']['value'])/60.0
	return driving_value
#datess = dt.date2num(datetime.now())
#print result
#print datess
#print "Driving time:" + str(driving_time)

def csv_file_write(driving_value,location):
	b = open(csv_file,'a')
	csv_writer =csv.writer(b, delimiter=',')
	data = driving_value,location
	csv_writer.writerow(data)

def csv_file_read():
	loc_waterbeach = []
	val_waterbeach = []
	loc_cottenham = []
	val_cottenham = []
	loc_longstanton = []
	val_longstanton = []
	b = open(csv_file,'r')
	csv_reader = csv.reader(b, delimiter=',')	
	for row in csv_reader:
		print row
		if row[1] == '2':
			print "waterbeach"
			val_waterbeach.append(row[0])
			loc_waterbeach.append(row[1])
		if row[1] == '4':
			print "cottenham"
			val_cottenham.append(row[0])
			loc_cottenham.append(row[1])
		if row[1] == '6':
			print "longstanton"
			val_longstanton.append(row[0])
			loc_longstanton.append(row[1])
	print val_waterbeach
	print val_cottenham
	print val_longstanton
	print loc_waterbeach
	print loc_cottenham
	print loc_longstanton
	return val_waterbeach, val_cottenham, val_longstanton,loc_waterbeach, loc_cottenham, loc_longstanton
 		
def create_plot():
	valw,valc,vall,locw,locc,locl = csv_file_read()
	print valw
	print valc
	print vall
	print locw
	print locc
	print locl
	#print val
	#print loc
	fig,ax = plt.subplots()
	fig.autofmt_xdate()
	plt.title("Travelling estimates to home")
	#ax.set_xlim(datetime.date(2015,06,06)),dt.date2num(datetime.date(2015,06,31)))
	ax.set_ylim(9.5,30)
	ax.set_xlim(1.5,6.5)
	#ax.plot_date(datess,driving_value)
	ax.plot(locw,valw,'r*',label='waterbeach')
	ax.plot(locc,valc,'bd',label='cottenham')
	ax.plot(locl,vall,'gh',label='longstanton')
	plt.xlabel("Travel date")
	plt.ylabel("Estimated Time to reach home ")
	ax.legend()
	fig.savefig(filename)
#	plt.show()
	#plt.close(fig)

def create_send_email():
	sender = 'y.wani@samsung.com'
	receivers = ["y.wani@samsung.com","h.sawardekar@samsung.com"]
#	receivers = ["y.wani@samsung.com"]
	smtpObj = smtplib.SMTP('smtp.w1.samsung.com',25)
	print "In send email.."
	#Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Travel Time'
	msgRoot['From'] = sender
	msgRoot['To'] = "y.wani@samsung.com,h.sawardekar@samsung.com"
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	 #Encapsulate the plain and HTML versions of the message body in an 'alternative' part, so message agents can decide which they want to display.
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText("Some text")
	msgAlternative.attach(msgText)

	#We reference the image in the IMG SRC attribute by the ID we give it below
	msgText = MIMEText(' Hi <br><br> The travel Graph for travelling estimates from work location to home<br><img src="cid:image1"><br>Thanks and Regards <br> Python at your service!', 'html')
	msgAlternative.attach(msgText)

	# This example assumes the image is in the current directory
	fp = open(filename, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)
	#send the email
	smtpObj.sendmail(sender, receivers, msgRoot.as_string())

for i in [2,4,6]:
	if i == 2:
		location = 2
		driving_value = get_travel_data(office,waterbeach)
		csv_file_write(driving_value,location)
	elif i == 4:
		location = 4
		driving_value = get_travel_data(office,cottenham)
		csv_file_write(driving_value,location)
	elif i == 6:
		location = 6
		driving_value = get_travel_data(office,longstanton)
		csv_file_write(driving_value,location)
create_plot()
create_send_email()
