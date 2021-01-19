from flask import render_template, url_for, flash, redirect, request, Blueprint,session,Flask
from meetin.init import sql_connection,app,cursor
from meetin.models import User
from meetin.forms import LoginForm, RegisterForm,EventForm,UpdateProfileform,EnrollForm,SimpleForm,choice
import re
import hashlib 
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date
import mysql.connector
from meetin.database import category_event_count,get_all_event,subscribers_count_event,get_all_category,get_all_university,add_university,create_category,get_user,create_user,get_user_detail,get_enrollment,get_user_event,get_event,create_event,update_event,delete_event,delete_user,update_user_detail,add_enrollment,delete_enrollment,update_enrollment

def hash(password):
    key = hashlib.md5(password.encode())
    return key.hexdigest()


def auth():
    if current_user.is_authenticated:
        return True
    else:
        return False
@app.errorhandler(404)
def page_not_found(e):
    if(auth()):
        usr = get_user_detail(current_user.id)
        return render_template('404.html',usr = usr), 404
    else:
        return redirect(url_for('login'))
@app.route('/',methods=['GET'])
@app.route('/home',methods=['GET'])
def home():
    if(auth()):
        usr = get_user_detail(userId = current_user.id)
        categories = category_event_count()
        events = get_all_event()
        today=date.today()
        for each in events:
            if( each['eventdate']<today):
                each['happened'] = True
            else:
                each['happened'] = False
        return render_template('home.html',usr = usr,categories=categories,events = events)
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
        
    if auth():
        return redirect(url_for('home'))

   
    form = LoginForm(request.form)
    if form.is_submitted():
        print ("submitted")

    if form.validate():
        print("valid")
    if form.validate_on_submit():
        print('aaaaa')
        account = get_user(username = form.username.data)

        if account:
            if(hash(form.password.data)==account['password']):

                account = User(account)
                
                login_user(account,remember = form.remember.data)
                
                next_page = request.args.get('next')
                flash('Logged In','success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Verification failed. Please check username and password', category='danger')
               
        else:
            flash('There isn\'t an account in that username.','danger')


    return render_template('login.html',form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
        
    if auth():
        return redirect(url_for('home'))

   
    form = RegisterForm()
    if form.validate_on_submit():
        print(get_user(username = form.username.data))
        if(get_user(username = form.username.data)):
            flash('Username already in use','danger')
        elif(get_user(email = form.email.data)):
            flash('Email already in use','danger')
        else:
            passs = hash(form.password.data)
            user_obj = create_user(username = form.username.data,email = form.email.data,password = passs)
            try:
                
                login_user(user_obj,remember=True)
                next_page = request.args.get('next')
                flash('Logged In','success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            except:
                flash('Failed to create account. Please try again later','danger')

    
    return render_template('register.html',form = form)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logged Out','success')
    return redirect(url_for('login'))

@app.route("/profile/<string:username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    detail = get_user_detail(username=username)
    usr = get_user_detail(userId = current_user.id)
    enrolled = get_enrollment(userId = detail['userId'])
    user_event = get_user_event(userId = detail['userId'])
    today = date.today()
    for each in enrolled:
      
        if( each['eventdate']<today):
            each['happened'] = True
        else:
            each['happened'] = False


    for each in user_event:
        if( each['eventdate']<today):
            each['happened'] = True
        else:
            each['happened'] = False
    print(type(today))
    return render_template('profile.html',usr = usr,detail = detail,enrolled=enrolled,user_event = user_event,today=today)

@app.route("/edit_account",methods = ['GET','POST'])
@login_required
def edit_account():
    usr = get_user_detail(current_user.id)
    form = UpdateProfileform()
    form.university.choices =choice(get_all_university())
    if form.validate_on_submit():
        
        try:
            
            update_user_detail(usr['userId'],form)
            flash('Updated profile','success')
            return redirect(url_for('profile',username = usr['username']))
        except:
            flash('Failed to update. Please try again','danger')
    
    form.university.default = usr['universityId']
    form.bio.default = usr['bio']
    form.birthDate.default = usr['birthDate']
    form.urlInstagram.default = usr['urlInstagram']
    form.urlTwitter.default = usr['urlTwitter']
    form.urlFacebook.default = usr['urlFacebook']
    form.occupation.default = usr['occupation']
    if(usr['gender']=='Female'):
        form.gender.default = 2
    elif(usr['gender']=='Male'):
        form.gender.default = 1
    elif(usr['gender']=='Other'):
        form.gender.default = 3
    
    form.process()
    photo = usr['photoUrl']
    return render_template('edit_profile.html',usr = usr,form = form,photo = photo)

@app.route("/delete_my_account",methods = ['POST'])
@login_required
def delete_my_account():
    id_user = current_user.id
    
    logout_user()
    delete_user(id_user)
    try:
        delete_user(id_user)
        return redirect(url_for('register'))
    except:
        flash('Failed to delete your account. Log in and try again','danger')
        return redirect(url_for('login'))


@app.route("/event/<int:eventId>", methods=['GET', 'POST'])
@login_required
def event(eventId):
    
    usr= get_user_detail(userId=current_user.id)
    today = date.today()
    event = get_event(eventId = eventId)
    
    
    if(not event):
        return redirect(url_for('open_event'))
    subs = subscribers_count_event(event['eventId'])
    event['sub_count'] = subs['c']
    owner = get_user_detail(userId = event['adminId'])
    enrolled = get_enrollment(eventId = eventId)
    if( event['eventdate']<today):
        event['happened'] = True
    else:
        event['happened'] = False

    
    return render_template('event.html',usr = usr,enrolled=enrolled,event = event,today =today,owner=owner )

@app.route("/open_event", methods=['GET', 'POST'])
@login_required
def open_event():
   
    usr= get_user_detail(userId=current_user.id)
    form =  EventForm()
    form.category.choices = choice(get_all_category())
    if form.validate_on_submit():
        
        
        try:
            event_id = create_event(usr['userId'],form)
            flash('Event creted','success')
            return redirect(url_for('event',eventId = event_id))
        except:
            flash('Failed to create event','danger')
    
    photo = 'img/event_photo/dummy.jpg'
    return render_template('open_event.html',usr = usr,form = form,title='Create',photo=photo,action = url_for('open_event') )


@app.route("/edit_event/<int:eventId>", methods=['GET', 'POST'])
@login_required
def edit_event(eventId):
   
    usr= get_user_detail(userId=current_user.id)
    today = date.today()
    event = get_event(eventId = eventId)
    
    print(event)
    if(event['adminId']!= usr['userId']):
        return redirect(url_for('event',eventId = event['eventId']))

    form =  EventForm()
    form.category.choices = choice(get_all_category())
    if form.validate_on_submit():
        
        try:
            update_event(event['eventId'],form)
            flash('Event updated','success')
            return redirect(url_for('event',eventId = eventId))
        except:
            flash('Failed to edit event','danger')
    form.eventName.default = event['eventName']
    form.eventLink.default = event['eventLink']
    form.description.default = event['description']
    form.category.default = event['categoryId']
    form.eventdate.default = event['eventdate']
    form.process()
    photo = event['eventPhotoUrl']
    return render_template('open_event.html',usr = usr,form = form,photo=photo,title='Edit',action = url_for('edit_event',eventId = eventId) )

@app.route("/delete_event/<int:eventId>",methods=['POST'])
@login_required
def event_delete(eventId):
    usr= get_user_detail(userId=current_user.id)
    event = get_event(eventId = eventId)
  
    if(event['adminId']!= usr['userId']):
        return redirect(url_for('event',eventId = event['eventId']))
    
    try:
        delete_event(eventId)
        flash('Event deleted','success')
        return redirect(url_for('home'))
    except:
        flash('Failed to delete event','danger')
        return redirect(url_for('event',eventId = eventId))

@app.route("/subscribe/<int:eventId>",methods=['GET','POST'])
@login_required
def enroll(eventId):
    usr = get_user_detail(userId = current_user.id)
    enrollment = get_enrollment(eventId = eventId,userId = usr['userId'])
    form = EnrollForm()
    if form.validate_on_submit():
        if(enrollment):
            
            update_enrollment(enrollment['enrollmentId'],form.reason.data)
            try:
                flash('Updated enrollment','success')
                return redirect(url_for('event',eventId = eventId))
            except:
                flash('Failed to update','danger')
        else:
            try:
                add_enrollment(userId = usr['userId'],eventId = eventId,reason=form.reason.data)
                flash('You enrolled to event','success')
                return redirect(url_for('event',eventId = eventId))
            except:
                flash('Failed to enroll','danger')
    if(enrollment):
        form.reason.data = enrollment['reason']
    return render_template('enroll.html',usr = usr,form=form,eventId = eventId)

@app.route("/profile/subscribed_events/<string:username>",methods = ['GET','POST'])
@login_required
def profile_subscribed_events(username):
    usr = get_user_detail(userId = current_user.id)
    profile =  get_user_detail(username= username)
    enrolled = get_enrollment(userId = profile['userId'])
    today = date.today()
    for each in enrolled:
        if( each['eventdate']<today):
            each['happened'] = True
        else:
            each['happened'] = False
    return render_template('subscribed.html',usr = usr,profile=profile,enrolled = enrolled,title = 'SUBSCRIBED')

@app.route("/profile/events/<string:username>",methods = ['GET','POST'])
@login_required
def profile_events(username):
    usr = get_user_detail(userId = current_user.id)
    profile =  get_user_detail(username= username)
    events = get_user_event(userId = profile['userId'])
    today = date.today()
    for each in events:
        if( each['eventdate']<today):
            each['happened'] = True
        else:
            each['happened'] = False
    return render_template('subscribed.html',usr = usr,profile=profile,enrolled = events,title = 'HAS')

@app.route("/unsubscribe/<int:enrollmentId>",methods=['POST'])
@login_required
def unsubscribe(enrollmentId):
    usr = get_user_detail(userId = current_user.id)
    enrollment = get_enrollment(enrollmentId = enrollmentId)
    if(enrollment['userId']==usr['userId']):
        try:
            delete_enrollment(enrollmentId = enrollmentId)
            flash('Unsubscribed','success')
            return redirect(url_for('event',eventId = enrollment['eventId']))
        except:
            flash('Failed to unsubscribe','danger')

@app.route("/add_category", methods=['GET', 'POST'])
@login_required
def add_category():
   
    usr= get_user_detail(userId=current_user.id)
    form =  SimpleForm()
    if form.validate_on_submit():
        
        
        try:
            create_category(form.field.data)
            flash('Category creted','success')
            return redirect(url_for('open_event'))
        except:
            flash('Failed to create category','danger')
    
    
    return render_template('category.html',usr = usr,form = form)

@app.route("/university_add", methods=['GET', 'POST'])
@login_required
def university_add():
   
    usr= get_user_detail(userId=current_user.id)
    form =  SimpleForm()
    if form.validate_on_submit():
        
        
        try:
            add_university(form.field.data)
            flash('University creted','success')
            return redirect(url_for('edit_account'))
        except:
            flash('Failed to create university','danger')
    
    
    return render_template('university.html',usr = usr,form = form)