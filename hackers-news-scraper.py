import requests # http requests

from bs4 import BeautifulSoup # web scraping
# send the email
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime
now = datetime.datetime.now()

# email content placeholder

content = '' # global variable


# extracting hacker news stories


def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories: </b>\n' + '<br>' + '-' *50+ '<br>')
    response = requests.get(url)
    content = response.content # local variable content is diffrent from the method .content
    soup = BeautifulSoup(content, 'html.parser')
    for i,tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign' : ''})):
        cnt += ((str(i+1) + ' :: ' + str(tag) + '\n' + '<br>') 
        if str(tag) != 'More' else '')
        # print(tag.prettify) #find all('span', attrs={'class': 'sitestr'})
    return(cnt)


cnt = extract_news('https://news.ycombinator.com')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')


# lets send the email

print('Composing email...')

# update your email details

SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM = '*****@gmail.com' # "your from email id"
TO = '*****@gmail.com' # "your to email ids" # can be a list
PASS = '*****' #"your email id´s password"

# fp = open(file_name 'rb')
# Create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP SSL('smtp.gmail.com', 465)
server.set_debuglevel(1) # 1 to show error mesages or 0 to not show error mesages
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
