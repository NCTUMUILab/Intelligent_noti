from app.models import DailyCheck, ESMCount
from app.helpers.valid_notification import valid_notification
from datetime import datetime
from json import dumps, loads

class Check:
    """
    check record for each day of each user
    """
    def __init__(self, name, user_id, user_created_at, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        
        self.name = name
        self.user_id = user_id
        self.device_id = ''
        self.day = (datetime.now().date() - user_created_at.date()).days + 1
        self.send_esm_count = 0
        self.esm_done_count = 0
        self.im_notification_count = 0
        self.accessibility = False
        self.no_result_lost = True
        self.all_valid = True
        self.warning = False
        self.fail_list = []
    
    
    def count_esm_done(self):
        """
        filter condition: 1. device_id  2. in the time slot 
        """
        self.esm_done_count = ESMCount.query.filter_by(device_id=self.device_id).filter(ESMCount.created_at > self.start_time).filter(ESMCount.created_at <= self.end_time).count()
    
    def count_send_esm(self, noti_day_query):
        self.send_esm_count = noti_day_query.filter_by(send_esm=True).count()
    
    def count_im_noti(self, noti_day_query):
        for each_noti in noti_day_query.filter_by(send_esm=False).all():
            if valid_notification(each_noti.app, each_noti.ticker_text, each_noti.title, each_noti.text, each_noti.sub_text):
                self.im_notification_count += 1
    
    def check_data(self, day_all_result):
        time_list = [ 0 for i in range(24) ]
        for each_result in day_all_result:
            hour = int(each_result.date.strftime("%H"))
            time_list[hour] += 1
            if loads(each_result.raw).get("Accessibility"):
                self.accessibility = True
        print('\t{}'.format(time_list))
        if self.day == 1: # must lost some data in day one, so ignore it
            return
        zero_start = False
        result_exist = False
        for each_count in time_list:
            if each_count != 0:
                result_exist = True
            if each_count == 0:
                zero_start = True
            elif each_count != 0 and zero_start:
                print('\terror in result')
                self.no_result_lost = False
                return
        if not result_exist:
            self.no_result_lost = False
    
    
    def check_valid(self):
        if self.im_notification_count <= 10:
            self.all_valid = False
            self.fail_list.append('im_notification_count')
        if self.send_esm_count < 5 and self.send_esm_count >= self.esm_done_count:
            self.all_valid = False
            self.fail_list.append('send_esm_count')
        if self.esm_done_count < 5 and self.day > 1:
            self.all_valid = False
            self.fail_list.append('esm_done_count')
        if not self.accessibility:
            self.all_valid = False
            self.fail_list.append('accessibility')
        if not self.no_result_lost:
            self.all_valid = False
            self.fail_list.append('no_result_lost')
        
        if not self.all_valid:
            last_check = DailyCheck.query.filter_by(user_id=self.user_id).order_by(DailyCheck.date.desc()).first()
            if last_check and not last_check.all_valid:
                self.warning = True
            else:
                self.warning = False
        
    
def is_today_checked():
    last_check = DailyCheck.query.order_by(DailyCheck.created_at.desc()).first()
    if last_check and last_check.created_at.date() == datetime.now().date():
        return True
    return False