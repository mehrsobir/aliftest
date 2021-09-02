import smtplib
from email.message import EmailMessage
import mysql.connector
from datetime import date

# Пайвастшавӣ бо хазинаи додаҳо
def con():
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='password', database='dbname',
                                   auth_plugin='mysql_native_password')
    return mydb


# Функсия барои фиристодани паёмакҳо
def sendemail(to, suject, body):
    user = 'myemail@gmail.com'
    pas = 'myapppassword'
    ms = EmailMessage()
    ms['from'] = user
    ms['to'] = to
    ms['subject'] = suject
    ms.set_content(body)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(user, pas)
    server.send_message(ms)
    server.quit()


# Рақами ҳуҷраро истифодабаранда ворид месозад
number = int(input('Рақами ҳуҷраро ворид созед: '))
mydb = con() #пайватсшавӣ бо хазинаи додаҳо
cursor = mydb.cursor()
cursor.execute(f'SELECT * FROM rooms WHERE id={number}') #гирифтани маълумот
room = cursor.fetchall()
mydb.close()

# Санҷиши ҳолати ҳуҷра ва амал мувофиқи он
if room[0][2] == 1:
    print(f'Ҳуҷраи интихобшударо {room[0][3]} то {room[0][4]} банд кардааст!')
else:
    nom = input('ҳуҷра озод аст! Лутфан номатонро ворид созед: ')
    end_date = input('То кай мемонед?: ')
    mydb = con()
    cursor = mydb.cursor()
    cursor.execute(f'UPDATE rooms SET reserved = 1, client = "{nom}", end_date = "{end_date}" WHERE (id = {room[0][0]})')
    mydb.commit()
    cursor.close()
    mydb.close()

    imruz = date.today().isoformat()
    # Фиристодани e-mail
    sendemail('clientmail@mail.ru', 'Ҳуҷраи Шумо', f'Ҳуҷраи Шумо рақами {room[0][0]} аст. Аз {imruz} то {end_date}')
    # Фиристодани паёмак ба телефон
    sendemail('992XXXXXXXXX@sms.tj', 'Ҳуҷраи Шумо', f'Ҳуҷраи Шумо рақами {room[0][0]} аст. Аз {imruz} то {end_date}')

