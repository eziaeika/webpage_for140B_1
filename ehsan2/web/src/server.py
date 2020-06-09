from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

from pyramid.session import SignedCookieSessionFactory

import mysql.connector as mysql
import os
import json

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

#GET HTML PAGE REQUESTS
def get_home(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'home';")
  db.commit()
  #cursor.execute("select * from Page_Analytics;")
  #[print(x) for x in cursor]
  if 'user' in req.session:
    user = req.session['user']
    cursor.execute(f"SELECT count(userID) FROM Page_Users WHERE page = 'home' AND userID ='"+user+"';")
    exists = cursor.fetchone()
    if not exists[0]:
      cursor.execute(f"INSERT INTO Page_Users (userID , page) VALUE ('"+user+"', 'home');")
      #cursor.execute("select * from Page_Users;")
      #[print(x) for x in cursor]
      db.commit()
    db.close()
    return render_to_response('templates/landing.html', {'login' : 'true'} , request=req)
  else:
    db.close()
    return render_to_response('templates/landing.html', {'login' : ''} , request=req)

def get_about(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'about';")
  db.commit()
  #cursor.execute("select * from Page_Analytics;")
  #[print(x) for x in cursor]
  if 'user' in req.session:
    user = req.session['user']
    cursor.execute(f"SELECT count(userID) FROM Page_Users WHERE page = 'about' AND userID ='"+user+"';")
    exists = cursor.fetchone()
    if not exists[0]:
      cursor.execute(f"INSERT INTO Page_Users (userID , page) VALUE ('"+user+"', 'about');")
      cursor.execute("select * from Page_Users;")
      [print(x) for x in cursor]
      db.commit()
    db.close()
    return render_to_response('templates/about.html', {'login' : 'true'} , request=req)
  else:
    db.close()
    return render_to_response('templates/about.html', {'login' : ''} , request=req)
  
def get_pricing(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'pricing';")
  db.commit()
  #cursor.execute("select * from Page_Analytics;")
  #[print(x) for x in cursor]
  if 'user' in req.session:
    user = req.session['user']
    cursor.execute(f"SELECT count(userID) FROM Page_Users WHERE page = 'pricing' AND userID ='"+user+"';")
    exists = cursor.fetchone()
    if not exists[0]:
      cursor.execute(f"INSERT INTO Page_Users (userID , page) VALUE ('"+user+"', 'pricing');")
      #cursor.execute("select * from Page_Users;")
      #[print(x) for x in cursor]
      db.commit()
    db.close()
    return render_to_response('templates/pricing.html', {'login' : 'true'} , request=req)
  else:
    db.close()
    return render_to_response('templates/pricing.html', {'login' : ''} , request=req)

def get_signup(req):
  if 'user' in req.session:
    return HTTPFound(req.route_url("get_dashboard"))
  else:
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'register';")
    db.commit()
    db.close()
    return render_to_response('templates/signup.html', {'login' : 'true'} , request=req)

def get_features(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'features';")
  db.commit()
  #cursor.execute("select * from Page_Analytics;")
  #[print(x) for x in cursor]
  if 'user' in req.session:
    user = req.session['user']
    cursor.execute(f"SELECT count(userID) FROM Page_Users WHERE page = 'features' AND userID ='"+user+"';")
    exists = cursor.fetchone()
    if not exists[0]:
      cursor.execute(f"INSERT INTO Page_Users (userID , page) VALUE ('"+user+"', 'features');")
      #cursor.execute("select * from Page_Users;")
      #[print(x) for x in cursor]
      db.commit()
    db.close()
    return render_to_response('templates/features.html', {'login' : 'true'} , request=req)
  else:
    db.close()
    return render_to_response('templates/features.html', {'login' : ''} , request=req)

def get_login(req):
  if 'user' in req.session:
    return HTTPFound(req.route_url("get_dashboard"))
  else:
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'login';")
    db.commit()
    db.close()
    error = req.session.pop_flash('login_error')
    error = error[0] if error else ''
    return render_to_response('templates/login.html', {'error': error} , request=req)

def post_login(req):
  email = None
  password = None
  if req.method == "POST":
    email = req.params['email']
    password = req.params['password']
  # Connect to the database and try to retrieve the user
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = "SELECT email, password FROM Users WHERE email='%s';" % email
  cursor.execute(query)
  user = cursor.fetchone() # will return a tuple (email, password) if user is found and None otherwise
  db.close()
  if user is not None and user[1] == password:
    req.session['user'] = user[0] # set the session variable
    return HTTPFound(req.route_url("get_dashboard"))
  else:
    req.session.invalidate() # clear session
    req.session.flash('Invalid login attempt. Please try again.', 'login_error')
    return HTTPFound(req.route_url("get_login"))

def get_dashboard(req):
  if 'user' in req.session:
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("UPDATE Page_Analytics SET count = count + 1 WHERE page = 'dashboard';")
    db.commit()
    user = req.session['user']
    cursor.execute(f"SELECT count(userID) FROM Page_Users WHERE page = 'dashboard' AND userID ='"+user+"';")
    exists = cursor.fetchone()
    if not exists[0]:
      cursor.execute(f"INSERT INTO Page_Users (userID , page) VALUE ('"+user+"', 'dashboard');")
      db.commit()
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    cursor.execute("SELECT p.page, ANY_VALUE(p.count), COUNT(u.userID) AS u_unique FROM Page_Analytics AS p LEFT JOIN Page_Users AS u USING (page) GROUP BY p.page;")
    metrics = cursor.fetchall()
    db.close()
    return render_to_response('templates/dashboard.html', {'metrics' : metrics} , request=req)
  else:
    return render_to_response('templates/login.html', {} , request=req)

def signup_submit(req):
  firstname = req.POST['first_name']
  lastname = req.POST['last_name']
  email = req.POST['email']
  password = req.POST['password']
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"SELECT count(id) FROM Users WHERE email = '"+email+"';")
  exists = cursor.fetchone()
  if not exists[0]:
    cursor.execute(f"INSERT INTO Users (first_name, last_name, email, password) VALUE ('"+firstname+"', '"+lastname+"', '"+email+"' , '"+password+"');")
    db.commit()
  db.close()
  return render_to_response('templates/login.html', {} , request=req)

def post_logout(req):
  req.session.invalidate() 
  return HTTPFound(req.route_url("get_login"))

def get_act_user_count(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"SELECT count(*) FROM Users;")
  count = cursor.fetchone()
  db.close()
  print(count[0])
  return Response(str(count[0]))

def getNewsFeed(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM News ORDER BY id DESC;")
  records = cursor.fetchall()
  db.close()
  return {'news' :records} 

def getMetrics(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute(f"SELECT * FROM Metrics ORDER BY id DESC LIMIT 1;")
  records = cursor.fetchall()
  db.close()
  print(records)
  return {'metrics' :records} 


''' Route Configurations '''
if __name__ == '__main__':
  config = Configurator()

  config.include('pyramid_jinja2')
  config.add_jinja2_renderer('.html')

  config.add_route('get_home', '/')
  config.add_view(get_home, route_name='get_home')

  config.add_route('get_about', '/about')
  config.add_view(get_about, route_name='get_about')

  config.add_route('get_features', '/features')
  config.add_view(get_features, route_name='get_features')

  config.add_route('get_pricing', '/pricing')
  config.add_view(get_pricing, route_name="get_pricing")

  config.add_route('get_act_user_count', '/active_count')
  config.add_view(get_act_user_count, route_name='get_act_user_count' , request_method='GET')

  config.add_route('getNewsFeed' ,'/getNewsFeed')
  config.add_view(getNewsFeed , route_name='getNewsFeed', request_method='GET' ,  renderer='json')

  config.add_route('getMetrics' ,'/getMetrics')
  config.add_view(getMetrics , route_name='getMetrics', request_method='GET' ,  renderer='json')

  config.add_route("get_dashboard", '/dashboard')
  config.add_view(get_dashboard , route_name='get_dashboard')

  config.add_route('get_login' , '/login')
  config.add_view(get_login, route_name='get_login')

  config.add_route('post_logout' , '/logout')
  config.add_view(post_logout , route_name='post_logout')

  config.add_route('post_login' , '/post_login')
  config.add_view(post_login , route_name="post_login")

  config.add_route('get_signup', '/signup')
  config.add_view(get_signup, route_name="get_signup")
  config.add_view(signup_submit, route_name='get_signup', request_method="POST")

  config.add_static_view(name='/', path='./public', cache_max_age=3600)

  session_factory = SignedCookieSessionFactory(os.environ['SESSION_SECRET_KEY'])
  config.set_session_factory(session_factory)

  app = config.make_wsgi_app()
  server = make_server('0.0.0.0', 6000, app)
  server.serve_forever()