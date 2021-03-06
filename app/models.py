from flask_login import UserMixin
from . import db
from flask import Flask
from datetime import datetime
import dateutil.parser


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    self_q_completed = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.now)
    in_progress = db.Column(db.Boolean)
    is_student = db.Column(db.Boolean)
    is_male = db.Column(db.Boolean)
    num_of_noti = db.Column(db.SmallInteger)
    num_of_contacts = db.Column(db.SmallInteger)
    age = db.Column(db.SmallInteger)
    is_valid = db.Column(db.Boolean)
    test = db.Column(db.Boolean)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_type = db.Column(db.String(256))
    user = db.Column(db.String(256)) # device_id
    r_id = db.Column(db.Integer)
    raw = db.Column(db.Text)
    date = db.Column(db.DateTime) # time of getting sensor data in cellphone
    created_at = db.Column(db.DateTime, default=datetime.now) # time of uploading data to server

    def __init__(self, r):
        self.r_type = r['type']
        self.user = r['user']
        self.r_id = r['id']
        self.raw = r['raw']
        self.date = dateutil.parser.parse(r['date'])

    def __repr__(self):
        return '<Result %r>' % self.id


class ContactQuestionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(50))
    contact_name_line = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_group = db.Column(db.Boolean) # deprecated
    completed = db.Column(db.Boolean)
    data = db.Column(db.Text)


class GpsLabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    label = db.Column(db.String(256))


class DeviceID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    device_id = db.Column(db.String(30))
    is_active = db.Column(db.Boolean)


class ESMCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.now)
    name = db.Column(db.String(30))
    app = db.Column(db.String(10))


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.now)
    timestamp = db.Column(db.String(16))
    datetime = db.Column(db.DateTime)
    latitude  = db.Column(db.String(16))
    longitude = db.Column(db.String(16))
    app = db.Column(db.String(128))
    title = db.Column(db.String(128)) # usually sender name
    sub_text = db.Column(db.String(32)) # idk, usually none
    text = db.Column(db.Text) # text
    ticker_text = db.Column(db.Text) # text shown on screen (sender+text)
    send_esm = db.Column(db.Boolean) # if esm is sent

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, default=datetime.now)
    EndDate = db.Column(db.DateTime, default=datetime.now)
    Status = db.Column(db.String(128))
    IPAddress = db.Column(db.String(128))
    Progress = db.Column(db.String(128))
    Duration= db.Column(db.String(128))
    Finished= db.Column(db.String(128))
    RecordedDate= db.Column(db.String(128))
    ResponseId= db.Column(db.String(128))
    RecipientLastName= db.Column(db.String(128))
    RecipientFirstName= db.Column(db.String(128))
    RecipientEmail= db.Column(db.String(128))
    ExternalReference= db.Column(db.String(128))
    LocationLatitude= db.Column(db.String(128))
    LocationLongitude= db.Column(db.String(128))
    DistributionChannel= db.Column(db.String(128))
    UserLanguage= db.Column(db.String(128))
    Q2_1= db.Column(db.String(128))
    Q3= db.Column(db.String(128))
    Q4= db.Column(db.String(128))
    Q4_11_TEXT= db.Column(db.String(128))
    Q5_1= db.Column(db.String(128))
    Q6= db.Column(db.String(128))
    Q7= db.Column(db.String(128))
    Q8= db.Column(db.String(128))
    Q9= db.Column(db.String(128))
    Q10_1= db.Column(db.String(128))
    Q10_2= db.Column(db.String(128))
    Q10_3= db.Column(db.String(128))
    Q10_4= db.Column(db.String(128))
    Q10_5= db.Column(db.String(128))
    Q10_6= db.Column(db.String(128))
    Q10_7= db.Column(db.String(128))
    Q10_8= db.Column(db.String(128))
    Q10_9= db.Column(db.String(128))
    Q10_10= db.Column(db.String(128))
    Q10_11= db.Column(db.String(128))
    Q10_12= db.Column(db.String(128))
    Q11_1= db.Column(db.String(128))
    Q11_2= db.Column(db.String(128))
    Q11_3= db.Column(db.String(128))
    Q11_4= db.Column(db.String(128))
    Q11_5= db.Column(db.String(128))
    Q11_6= db.Column(db.String(128))
    Q11_7= db.Column(db.String(128))
    Q12_1= db.Column(db.String(128))
    Q12_2= db.Column(db.String(128))
    Q12_3= db.Column(db.String(128))
    Q12_4= db.Column(db.String(128))
    Q12_5= db.Column(db.String(128))
    Q12_6= db.Column(db.String(128))
    Q12_7= db.Column(db.String(128))
    Q12_8= db.Column(db.String(128))
    Q12_9= db.Column(db.String(128))
    Q13_1= db.Column(db.String(128))
    Q13_2= db.Column(db.String(128))
    Q13_3= db.Column(db.String(128))
    Q13_4= db.Column(db.String(128))
    Q13_5= db.Column(db.String(128))
    Q13_6= db.Column(db.String(128))
    Q14_1= db.Column(db.String(128))
    Q14_2= db.Column(db.String(128))
    Q14_3= db.Column(db.String(128))
    Q14_4= db.Column(db.String(128))
    Q14_5= db.Column(db.String(128))
    Q14_6= db.Column(db.String(128))
    name= db.Column(db.String(128))
    uid= db.Column(db.String(128))
    cid= db.Column(db.String(128))

class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, default=datetime.now)
    EndDate = db.Column(db.DateTime, default=datetime.now)
    Status = db.Column(db.String(128))
    IPAddress = db.Column(db.String(128))
    Progress = db.Column(db.String(128))
    Duration= db.Column(db.String(128))
    Finished= db.Column(db.String(128))
    RecordedDate= db.Column(db.String(128))
    ResponseId= db.Column(db.String(128))
    RecipientLastName= db.Column(db.String(128))
    RecipientFirstName= db.Column(db.String(128))
    RecipientEmail= db.Column(db.String(128))
    ExternalReference= db.Column(db.String(128))
    LocationLatitude= db.Column(db.String(128))
    LocationLongitude= db.Column(db.String(128))
    DistributionChannel= db.Column(db.String(128))
    UserLanguage= db.Column(db.String(128))
    Q2_1= db.Column(db.String(128))
    Q2_2= db.Column(db.String(128))
    Q2_3= db.Column(db.String(128))
    Q2_4= db.Column(db.String(128))
    Q2_5= db.Column(db.String(128))
    Q2_6= db.Column(db.String(128))
    Q2_7= db.Column(db.String(128))
    Q2_8= db.Column(db.String(128))
    Q2_9= db.Column(db.String(128))
    Q2_10= db.Column(db.String(128))
    Q2_11= db.Column(db.String(128))
    Q2_12= db.Column(db.String(128))
    Q2_13= db.Column(db.String(128))
    Q2_14= db.Column(db.String(128))
    Q2_15= db.Column(db.String(128))
    Q2_16= db.Column(db.String(128))
    Q2_17= db.Column(db.String(128))
    Q2_18= db.Column(db.String(128))
    Q2_19= db.Column(db.String(128))
    Q3_1 = db.Column(db.String(128))
    Q3_2= db.Column(db.String(128))
    Q3_3= db.Column(db.String(128))
    Q3_4= db.Column(db.String(128))
    Q3_5= db.Column(db.String(128))
    Q3_6= db.Column(db.String(128))
    Q3_7= db.Column(db.String(128))
    Q3_8= db.Column(db.String(128))
    Q3_9= db.Column(db.String(128))
    Q3_10= db.Column(db.String(128))
    Q3_11	= db.Column(db.String(128))
    Q3_12	= db.Column(db.String(128))
    Q3_13	= db.Column(db.String(128))
    Q3_14	= db.Column(db.String(128))
    Q3_15	= db.Column(db.String(128))
    Q3_16	= db.Column(db.String(128))
    Q3_17	= db.Column(db.String(128))
    Q3_18	= db.Column(db.String(128))
    Q3_19	= db.Column(db.String(128))
    Q3_20	= db.Column(db.String(128))
    Q4_1	= db.Column(db.String(128))
    Q4_2	= db.Column(db.String(128))
    Q4_3	= db.Column(db.String(128))
    Q4_4	= db.Column(db.String(128))
    Q4_5	= db.Column(db.String(128))
    Q4_6	= db.Column(db.String(128))
    Q4_7	= db.Column(db.String(128))
    Q4_8	= db.Column(db.String(128))
    Q4_9	= db.Column(db.String(128))
    Q4_10	= db.Column(db.String(128))
    name	= db.Column(db.String(128))
    uid	= db.Column(db.String(128))
    name_Topics= db.Column(db.String(128))


class DailyCheck(db.Model):
    __tablename__ = 'daily_check'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date)
    send_esm_count = db.Column(db.Integer)
    esm_done_count = db.Column(db.Integer)
    accessibility = db.Column(db.Boolean)
    no_result_lost = db.Column(db.Boolean)
    im_notification_count = db.Column(db.Integer)
    all_valid = db.Column(db.Boolean)
    fail_list = db.Column(db.String(128))
    result_incomplete = db.Column(db.String(512))
    time_list = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)


class APPState(db.Model):
    __tablename__ = 'app_state'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(30))
    state_accessibility = db.Column(db.DateTime)
    state_main = db.Column(db.DateTime)
    state_esm_done = db.Column(db.DateTime)
    state_esm_create = db.Column(db.DateTime)
    state_bootcomplete = db.Column(db.DateTime)
    state_notification_listen = db.Column(db.DateTime)
    state_notification_sent_esm = db.Column(db.DateTime)
    state_wifi_upload = db.Column(db.DateTime)
    state_stream = db.Column(db.DateTime)
    state_gps = db.Column(db.DateTime)
    state_version = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.now)
