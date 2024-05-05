from application.workers import celery_app
from celery.schedules import crontab
from jinja2 import Template
import sqlalchemy as sa
from sqlalchemy import or_
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from application.models import User, show, bookings, theatre
import datetime, csv, requests

SMTP_SERVER_HOST='localhost'
SMTP_SERVER_PORT='1025'
SENDER_ADDRESS='admin@admin.com'
SENDER_PASSWORD='1234'

def send_email(to_address, sub, message):
    msg=MIMEMultipart()
    msg["From"]=SENDER_ADDRESS
    msg["To"]=to_address
    msg["Subject"]=sub

    msg.attach(MIMEText(message,"html"))

    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True

def format_message(template_file, data={}):
   with open(template_file) as file_:
      template=Template(file_.read())
      return template.render(data=data)

@celery_app.on_after_finalize.connect
def automated_task(sender, **kwargs):
    sender.add_periodic_task(10, daily_reminders.s(), name='daily reminder task') # task scheduled for everyday at 5:30 PM
    sender.add_periodic_task(30,monthly_user_reports.s(), name='monthly report task') #task scheduled at the start of the month at 8:00 AM

@celery_app.task()
def daily_reminders():
    time_now=datetime.datetime.now()
    date_today=time_now.strftime("%d/%m/%Y")
    print(date_today)
    user_list=User.query.filter(or_(User.last_booking_date != date_today, User.last_booking_date == sa.null())).all()
    #print(user_list)
    user_list=user_list[1:]
    #print(user_list)
    if user_list != []:
        for u in user_list:
            #print(u.last_booking_date)
            send_email(to_address=u.email, sub="Ticket New", message="It seems like you haven't booked anything today. Book Tickets for your favourite show TODAY at TicketNew website.")
        return "All Daily Reminder Mails have been sent Successfully to users who haven't booked a ticket."
    else:
        return "All users have booked Today."

@celery_app.task()
def monthly_user_reports():
    user_details=User.query.all()
    user_details=user_details[1:]
    for u in user_details:
        user_data={}
        user_bookings=bookings.query.filter(bookings.user_id == u.id).all()
        user_data["username"]=u.username
        user_data["no_of_tickets"]=0
        user_data["show_names"]=[]
        for s in user_bookings:
            user_data["no_of_tickets"]+=s.tickets_booked
            show_deets=show.query.filter(show.show_id == s.show_id).first()
            user_data["show_names"].append((show_deets.show_name,show_deets.show_tags,s.tickets_booked,s.booked_on))
        #send email using this data 
        # template file in templates folder as monthly_report.html 
        msg=format_message("./templates/monthly_report.html",data=user_data)
        send_email(to_address=u.email, sub="Monthly Entertainment Report", message=msg)
    return "All reports have been successfully sent to the users."
    

@celery_app.task()
def theatre_report(t_id):
    theatre_details=theatre.query.filter(theatre.theatre_id == t_id).first()
    show_details=show.query.filter(show.theatre_id == t_id).all()
    csv_header=["Show Name", "Show Timings", "Show tags", "Ticket Price", "Tickets sold", "Revenue Generated"]
    csv_data=[]
    #showname, timings, tags, price, no of tickets sold ,revenue generated 
    for s in show_details:
        entry=[s.show_name, s.show_start_timing, s.show_tags, s.price]
        booking_details=bookings.query.filter(bookings.show_id == s.show_id).all()
        count_tickets=0
        for b in booking_details:
            count_tickets+=b.tickets_booked
        entry.append(count_tickets)
        revenue_generated= count_tickets*s.price
        entry.append(revenue_generated)
        csv_data.append(entry)
        entry=[]
    time_now=datetime.datetime.now()
    date_today=time_now.strftime("%d-%m-%Y")
    theatre_name_str=theatre_details.theatre_name.replace(" ","_")
    #filedir="./static/reports/"+ date_today +"_" + theatre_name_str +"_report.csv"
    with open("./static/reports/Theatre_report.csv",'w') as file_:
        csv_file=csv.writer(file_)
        csv_file.writerow(["Theatre name", theatre_name_str])
        csv_file.writerow(csv_header)
        csv_file.writerows(csv_data)
    #requests.get("http://127.0.0.1:8080/send_csv_file")
    return "Theatre Report has been genareted successfully."