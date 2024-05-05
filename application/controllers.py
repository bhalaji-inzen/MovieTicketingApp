from flask import render_template, redirect, request, url_for, send_file, jsonify
from flask_security import roles_required, login_required, auth_required, current_user
from flask import current_app as app
import json, datetime
from application.models import *
from application.tasks import *
from main import cache

####CACHED Functions####
@cache.cached(timeout=1, key_prefix='all_theatres')
def get_theatres():
  theatre_shows=theatre.query.all()
  return theatre_shows

@cache.memoize(5)
def get_a_theatre(t_id):
  t=theatre.query.filter(theatre.theatre_id == t_id).first()
  return t

@cache.memoize(10)
def get_shows_of_theatre(t_id):
  shows_list=show.query.filter(show.theatre_id == t_id).all()
  return shows_list

####CACHED####
@app.route('/theatre_shows')
@auth_required("token")
@cache.cached(timeout=5, key_prefix="theatre_shows")
def theatre_shows():
  all_theatres=get_theatres()
  theatre_shows=[]
  d={}
  for t in all_theatres :
    d['theatre_id']=t.theatre_id
    d['theatre_name']=t.theatre_name
    d['theatre_place']=t.place
    d['theatre_location']=t.location
    shows_of_theatre=get_shows_of_theatre(t.theatre_id)
    d['shows']=[]
    p={}
    for s in shows_of_theatre:
      p['show_id']=s.show_id
      p['show_name']=s.show_name
      p['show_start_timing']=s.show_start_timing
      d['shows'].append(p)
      p={}
    theatre_shows.append(d)
    d={}
  return json.dumps(theatre_shows)
####CACHED####

####CACHED Functions####

# @app.route('/current_user')
# @auth_required('token')
# def current_user():
#   print(type(current_user))
#   return current_user.find_role


@app.route('/')
@login_required
def index():
  return render_template('index.html')

@app.route('/create_theatre')
@login_required
@roles_required('admin')
def create_theatre():
  return render_template('create_theatre.html')


@app.post('/create_theatre')
@auth_required("token")
@roles_required('admin')
def create_t():
  theatre_data=get_theatres()
  theatre_names=[t.theatre_name for t in theatre_data]
  if request.json['theatre_name'] not in theatre_names or theatre_names == []:
    new_theatre=theatre(theatre_name=request.json['theatre_name'], place=request.json['theatre_place'], location=request.json['theatre_location'], capacity=request.json['theatre_capacity'])
    db.session.add(new_theatre)
    db.session.commit()
    return "Theatre has been created successfully."
  else:
    return "Theatre name is already taken. Try a new name. <a href='/create_theatre'>Create Again</a>"

@app.route('/edit_theatre/<int:t_id>')
@login_required
@roles_required('admin')
def edit_theatre(t_id):
  return render_template('edit_theatre.html')

@app.post('/edit_theatre/<int:t_id>')
@auth_required("token")
@roles_required("admin")
def edit_t(t_id):
  old_t=get_a_theatre(t_id)
  old_t.theatre_name=request.json['theatre_name'] 
  old_t.place=request.json['theatre_place'] 
  old_t.location=request.json['theatre_location']
  old_t.capacity=request.json['theatre_capacity']
  db.session.commit()
  return "Theatre information has been edited successfully."


@app.route('/delete_theatre/<int:t_id>')
@auth_required("token")
@roles_required("admin")
def delete_theatre(t_id):
  del_theatre=get_a_theatre(t_id)
  del_shows=get_shows_of_theatre(t_id)
  for d in del_shows:
    db.session.delete(d)
    del_books=bookings.query.filter(bookings.show_id == d.show_id).all()
    for d in del_books:
      db.session.delete(d)
  db.session.delete(del_theatre)
  db.session.commit()
  return "Theatre, shows and its bookings  have been deleted successfully."

@app.route('/<int:t_id>/create_show')
@login_required
@roles_required('admin')
def create_show(t_id):
  return render_template('create_show.html')

@app.post('/<int:t_id>/create_show')
@auth_required("token")
@roles_required('admin')
def create_s(t_id):
  new_show=show(show_name=request.json['show_name'],show_start_timing=request.json['show_timing'], show_tags=request.json['show_tags'], price=request.json['price'], theatre_id=t_id)
  db.session.add(new_show)
  db.session.commit()
  return "A show has been successfully created for this theatre."

@app.route('/<int:t_id>/edit_show/<int:s_id>')
@login_required
@roles_required('admin')
def edit_show(t_id,s_id):
  return render_template('edit_show.html')

@app.post('/<int:t_id>/edit_show/<int:s_id>')
@auth_required("token")
@roles_required('admin')
def edit_s(t_id,s_id):
  e_show=show.query.filter(show.show_id == s_id and show.t_id == t_id ).first()
  e_show.show_name=request.json['show_name']
  e_show.show_start_timing=request.json['show_timing']
  e_show.show_tags=request.json['show_tags']
  e_show.price=request.json['price']
  db.session.commit()
  return "The show details has been edited successfully."


@app.route('/<int:t_id>/delete_show/<int:s_id>')
@auth_required("token")
@roles_required('admin')
def delete_show(t_id,s_id):
  del_show=show.query.filter(show.show_id == s_id and show.theatre_id == t_id).first()
  del_books=bookings.query.filter(bookings.show_id == s_id).all()
  for d in del_books:
    db.session.delete(d)
  db.session.delete(del_show)
  db.session.commit()
  return "The show and its corresponding bookings have been deleted successfully."

@app.route('/book_show/<int:u_id>/<int:s_id>')
@login_required
def book_s(u_id,s_id):
  if request.content_type == "application/json":
    book_show=show.query.filter(show.show_id == s_id).first()
    required_data={}
    required_data["price"]=book_show.price
    theatre_info=theatre.query.filter(theatre.theatre_id == book_show.theatre_id).first()
    required_data["theatre_capacity"]=theatre_info.capacity
    time_now=datetime.datetime.now()
    formatted_date=time_now.strftime("%d/%m/%Y")
    booked_tickets=bookings.query.filter(bookings.show_id == s_id).all()
    total_booked_tickets=0
    for t in booked_tickets:
      print(formatted_date)
      if formatted_date == t.booked_on.split(" ")[0]:
        total_booked_tickets += t.tickets_booked
      print(t.booked_on.split(" ")[0]) #IT Works this way so implement it this way in line no 171 on booked_on column or you could use like.
    required_data["available_tickets"]= required_data["theatre_capacity"] - total_booked_tickets
    if required_data["available_tickets"] == 0:
      return "HOUSEFULL", 400
    print(required_data)
    return json.dumps(required_data), 200
  return render_template('book_show.html')



@app.post('/book_show/<int:u_id>/<int:s_id>')
@auth_required("token")
def book_show(u_id,s_id):
  time_now=datetime.datetime.now()
  formatted_time=time_now.strftime("%d/%m/%Y %H:%M")
  formatted_date=time_now.strftime("%d/%m/%Y")
  user_obj=User.query.filter(User.id == u_id).first()
  user_obj.last_booking_date=formatted_date
  #print(request.json)
  new_booking=bookings(user_id=u_id, show_id=s_id, tickets_booked= request.json, booked_on=formatted_time)
  db.session.add(new_booking)
  db.session.commit()
  return "You have booked a show successfully."


@app.route('/search')
@login_required
def search():
  return render_template('search.html')
  
@app.post('/search')
@auth_required('token')
def search_result():
  search_field=request.json['search_in']
  search_term="%"+ request.json['search_term'] + "%"
  ####
  if search_field == 'theatre_name' :
    search_results=theatre.query.filter(theatre.theatre_name.like(search_term)).all()
    search_theatres=[]
    d={}
    for t in search_results :
      shows_of_theatre=get_shows_of_theatre(t.theatre_id)
      d['theatre_id']=t.theatre_id
      d['theatre_name']=t.theatre_name
      d['shows']=[]
      p={}
      for s in shows_of_theatre:
        p['show_id']=s.show_id
        p['show_name']=s.show_name
        p['show_start_timing']=s.show_start_timing
        d['shows'].append(p)
        p={}
      search_theatres.append(d)
      d={}
    return json.dumps(search_theatres)
  
  elif search_field == 'theatre_location' :
    search_results=theatre.query.filter(theatre.location.like(search_term)).all()
    search_theatres=[]
    d={}
    for t in search_results :
      shows_of_theatre=get_shows_of_theatre(t.theatre_id)
      d['theatre_id']=t.theatre_id
      d['theatre_name']=t.theatre_name
      d['theatre_location']=t.location
      d['shows']=[]
      p={}
      for s in shows_of_theatre:
        p['show_id']=s.show_id
        p['show_name']=s.show_name
        p['show_start_timing']=s.show_start_timing
        d['shows'].append(p)
        p={}
      search_theatres.append(d)
      d={}
    return json.dumps(search_theatres)
  
  elif search_field == 'show_name' :
    search_results=show.query.filter(show.show_name.like(search_term)).all()
    search_shows=[]
    d={}
    for s in search_results:
      d['show_id']=s.show_id
      d['show_name']=s.show_name
      d['show_start_timing']=s.show_start_timing
      d['show_tags']=s.show_tags
      search_shows.append(d)
    return json.dumps(search_shows)
  
  elif search_field == 'show_tags':
    search_results=show.query.filter(show.show_tags.like(search_term)).all()
    search_shows=[]
    d={}
    for s in search_results:
      d['show_id']=s.show_id
      d['show_name']=s.show_name
      d['show_start_timing']=s.show_start_timing
      d['show_tags']=s.show_tags
      search_shows.append(d)
    return json.dumps(search_shows)
    

@app.route('/bookings/<int:u_id>')
@login_required
def user_bookings(u_id):
  if request.content_type == 'application/json' :
    user_booking=bookings.query.filter(bookings.user_id == u_id).all()
    booked_shows=[]
    d={}
    for b in user_booking:
      d['show_details']={}
      show_details=show.query.filter(show.show_id == b.show_id).first()
      d['show_details']['show_id']=show_details.show_id
      d['show_details']['show_name']=show_details.show_name
      d['show_details']['show_tags']=show_details.show_tags
      d['show_details']['show_price']=show_details.price
      t=theatre.query.filter(theatre.theatre_id == show_details.theatre_id).first()
      d['show_details']['theatre_name']=t.theatre_name
      d['tickets_booked']=b.tickets_booked
      d['booked_time']=str(b.booked_on)
      booked_shows.append(d)
      d={}
    return json.dumps(booked_shows)
  return render_template("bookings.html")


#####CELERY BACKEND JOBS######

@app.route('/theatre_report/<int:t_id>')
@login_required
@roles_required("admin")
def Theatre_report(t_id):
  job=theatre_report.delay(t_id)
  return "<a href='/send_csv_file'>Download csv file</a> <br> <a href='/'>Home page</a>"


@app.route('/send_csv_file')
@login_required
@roles_required("admin")
def send_csv():
  #file_loc= request.args.get("file_location")
  #print(file_loc)
  return send_file("./static/reports/Theatre_report.csv", as_attachment=True, download_name="Theatre report.csv")

#####CELERY BACKEND JOBS######