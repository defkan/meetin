from meetin.init import cursor,app,sql_connection
from meetin.models import User
from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets

def photo_save_profile(photo):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(photo.filename)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(photo)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def photo_save_event(photo):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(photo.filename)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/event_photo', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(photo)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def get_user(userId = None, username = None,email=None):
    if(userId):
        sql = 'SELECT * FROM user where userId = %s'
        values = (userId,)
    elif(username):
        sql = 'SELECT * FROM user WHERE username = %s'
        values = (username,)
    elif(email):
        sql = 'SELECT * FROM user WHERE email = %s'
        values = (email,)
    else:
        return None

    cursor.execute(sql,values)
    return cursor.fetchone()

def get_user_detail(userId=None,username = None):
    if(userId):
        sql = '''SELECT date_format(userdetail.birthDate,'%d/%m/%y') as birthdate,user.*, userdetail.*,university.* 
        FROM userdetail 
        INNER JOIN user ON user.userId = userdetail.userId 
        LEFT JOIN university ON university.universityId = userdetail.universityId
        WHERE userdetail.userId = %s'''
        cursor.execute(sql,(userId,))
        return cursor.fetchone()
    elif(username):
        sql = '''SELECT date_format(userdetail.birthDate,'%d/%m/%y') as birthdate,user.*, userdetail.*,university.* 
        FROM userdetail 
        INNER JOIN user ON user.userId = userdetail.userId 
        LEFT JOIN university ON university.universityId = userdetail.universityId
        WHERE user.username = %s
        '''
        cursor.execute(sql,(username,))
        return cursor.fetchone()

    else:
        return None
    

def update_user_detail(userId,form):
    temp = get_user_detail(userId)
    sql = '''
    UPDATE userdetail
    SET universityId = %s,
    photoUrl = %s,
    birthDate = %s,
    bio  =%s,
    urlInstagram = %s,
    urlTwitter = %s,
    urlFacebook = %s,
    occupation = %s
    WHERE userId = %s
    '''
    if(form.photoUrl.data):
        photoUrl = 'img/profile/' + photo_save_profile(form.photoUrl.data)
    else:
        photoUrl = temp['photoUrl']

    values = (form.university.data,photoUrl,form.birthDate.data,form.bio.data,form.urlInstagram.data,form.urlTwitter.data,form.urlFacebook.data,form.occupation.data,userId )
    cursor.execute(sql,values)
    sql_connection.commit()
def create_user(username,email,password):
    photo = 'img/profile/dummy.png'
    sql = 'INSERT INTO user(username,email,password) VALUES(%s,%s,%s)'
    cursor.execute(sql,(username,email,password))
    id_user= cursor.lastrowid
    sql = 'INSERT INTO userdetail(userId,urlInstagram,urlTwitter,urlFacebook,photoUrl) VALUES(%s,%s,%s,%s,%s)'
    cursor.execute(sql,(id_user,'instagram','twitter','facebook',photo))
    sql_connection.commit()
    user_info = {
        "userId": id_user,
        "username": username,
        "email": email
    }
    return User(user_info)

def delete_user(userId):
    sql = 'DELETE FROM user WHERE userId = %s'
    cursor.execute(sql,(userId,))
    sql_connection.commit()


def get_all_category():
    sql = 'SELECT * FROM category'
    cursor.execute(sql)
    return cursor.fetchall()

def create_category(categoryName):
    sql = 'INSERT INTO category(categoryName) VALUES(%s)'
    cursor.execute(sql,(categoryName,))
    sql_connection.commit()
    

def get_all_event():
    sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,user.*,userdetail.*,category.*,event.* 
            FROM event
            INNER JOIN user on user.userId = event.adminId
            INNER JOIN userdetail on userdetail.userId = event.adminId
            LEFT JOIN category on category.categoryId = event.categoryId
            ORDER BY event.eventdate desc
             '''
    cursor.execute(sql)
    return cursor.fetchall()

def get_user_event(userId):
    sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,event.*,category.* from event 
        LEFT JOIN category ON category.categoryId = event.categoryId
        WHERE event.adminId = %s ORDER BY event.eventdate desc'''

    cursor.execute(sql,(userId,))
    return cursor.fetchall()

def get_event(eventId):
    sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,event.*,category.* from event 
        LEFT JOIN category ON category.categoryId = event.categoryId
        WHERE event.eventId = %s ORDER BY event.eventdate desc'''

    cursor.execute(sql,(eventId,))
    return cursor.fetchone()
def subscribers_count_event(eventId):
    sql = 'SELECT count(userId) as c from enrollment WHERE eventId = %s'
    cursor.execute(sql,(eventId,))
    return cursor.fetchone()
def category_event_count():
    sql ='''
    SELECT category.categoryName,count(event.categoryId) as c from event 
INNER JOIN category on category.categoryId = event.categoryId
group by event.categoryId
    '''

    cursor.execute(sql)
    return cursor.fetchall()
def create_event(userId,form):
    sql = 'INSERT INTO event(adminId,categoryId,eventName,description,eventPhotoUrl,eventLink,eventDate) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    if(form.eventPhotoUrl.data):
        photoUrl = 'img/event_photo/' + photo_save_event(form.eventPhotoUrl.data)
    else:
        photoUrl = 'img/event_photo/dummy.jpg'

    values = (userId, form.category.data,form.eventName.data,form.description.data,photoUrl,form.eventLink.data,form.eventdate.data)
    cursor.execute(sql,values)
    id_event = cursor.lastrowid
    sql_connection.commit()
    return id_event

def update_event(eventId,form):
    event =  get_event(eventId = eventId)
    sql = '''UPDATE event
        SET categoryId = %s,
        eventName = %s,
        description = %s,
        eventPhotoUrl = %s,
        eventLink = %s,
        eventdate = %s
        WHERE eventId = %s
     '''
    if(form.eventPhotoUrl.data):
        photoUrl = 'img/event_photo/' + photo_save_event(form.eventPhotoUrl.data)
    else:
        photoUrl = event['eventPhotoUrl']

    values = (form.category.data,form.eventName.data,form.description.data,photoUrl,form.eventLink.data,form.eventdate.data,eventId)
    cursor.execute(sql,values)

    sql_connection.commit()

def delete_event(eventId):

    sql = 'DELETE FROM event WHERE eventId = %s'
    cursor.execute(sql,(eventId,))
    sql_connection.commit()

def get_all_university():
    sql = 'SELECT * FROM university'
    cursor.execute(sql)
    return cursor.fetchall()

def add_university(universityName):
    sql = 'INSERT INTO university(universityName) values(%s)'
    cursor.execute(sql,(universityName,))
    sql_connection.commit()

def get_enrollment(userId = None,eventId = None,enrollmentId= None):
    if(enrollmentId):
        sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,userdetail.*,event.*,user.*,enrollment.enrollmentId,enrollment.reason from enrollment 
        INNER JOIN event ON event.eventId = enrollment.eventId
        INNER JOIN user ON user.userId = enrollment.userId
        INNER JOIN userdetail ON userdetail.userId = enrollment.userId
        WHERE enrollment.enrollmentId = %s
        '''
        cursor.execute(sql,(enrollmentId,))
        return cursor.fetchone()
    if(userId and eventId):
        sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,userdetail.*,event.*,user.*,enrollment.enrollmentId,enrollment.reason from enrollment 
        INNER JOIN event ON event.eventId = enrollment.eventId
        INNER JOIN user ON user.userId = enrollment.userId
        INNER JOIN userdetail ON userdetail.userId = enrollment.userId
        WHERE enrollment.userId = %s and enrollment.eventId = %s
        ORDER BY event.eventdate desc'''
        cursor.execute(sql,(userId,eventId))
        return cursor.fetchone()
    elif(userId):
        sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,userdetail.*,event.*,user.*,enrollment.enrollmentId,enrollment.reason from enrollment 
        INNER JOIN event ON event.eventId = enrollment.eventId
        INNER JOIN user ON user.userId = enrollment.userId
        INNER JOIN userdetail ON userdetail.userId = enrollment.userId
        WHERE enrollment.userId = %s
        ORDER BY event.eventdate desc
        '''

        cursor.execute(sql,(userId,))
        return cursor.fetchall()    
    elif(eventId):
        sql = '''SELECT date_format(event.eventdate,'%d/%m/%y') as date,userdetail.* ,event.*,user.*,enrollment.reason,enrollment.enrollmentId from enrollment 
        INNER JOIN event ON event.eventId = enrollment.eventId
        INNER JOIN user ON user.userId = enrollment.userId
        INNER JOIN userdetail ON userdetail.userId = enrollment.userId
        WHERE enrollment.eventId = %s
        ORDER BY event.eventdate desc
        '''

        cursor.execute(sql,(eventId,))
        return cursor.fetchall()    
    else:
        return None

def delete_enrollment(enrollmentId):
    sql = 'DELETE FROM enrollment WHERE enrollmentId = %s'
    cursor.execute(sql,(enrollmentId,))
    sql_connection.commit()

def add_enrollment(userId,eventId,reason):
    sql  = 'INSERT INTO enrollment(userId,eventId,reason) VALUES(%s,%s,%s)'
    cursor.execute(sql,(userId,eventId,reason))
    sql_connection.commit()

def update_enrollment(enrollmentId,reson):
    sql = 'UPDATE enrollment SET reason = %s WHERE enrollmentId = %s'
    cursor.execute(sql,(reson,enrollmentId))
    sql_connection.commit()

