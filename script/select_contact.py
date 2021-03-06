import pymysql
import csv, sys
import html
import requests
import secrete as secrete
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from helpers import valid_notification
def ESM_amount(ele):
    return int(ele[4])

def Noti_amount(ele):
    return ele["count"]

contact_list = []
notification_list = []

db = pymysql.connect(secrete.db_url,secrete.user_name,secrete.password,secrete.db)


cursor = db.cursor()

mobileID = sys.argv[1]
# mobileID = "869124021392335"

cursor.execute("SELECT user_id FROM deviceID WHERE device_id ="+mobileID)
uid = str(cursor.fetchall()[0][0])
print("User id: ",uid)

cursor.execute("SELECT name,Q4,Q9,Q2_1,Q3 FROM contact WHERE uid ="+uid) #Q4: relationship, Q9: closeness, Q2_1: interruptibility, Q3: response,
contact_questionniare= cursor.fetchall()

cursor.execute("SELECT * FROM notification WHERE device_id  ="+mobileID)
notifications = cursor.fetchall()

for noti in notifications:
    if(valid_notification(noti[7],noti[11],noti[8],noti[10],noti[9]) == False):
        #print(noti)
        continue
    contained_in_list = False
    for contact_noti in notification_list:
        if(noti[8] == contact_noti["name"]):
            contact_noti["count"] += 1
            contained_in_list = True
            break
    if(contained_in_list == False):
        data = {"name":noti[8],"count":1,"selected": False}
        notification_list.append(data)

sql = "SELECT * FROM esm_data WHERE user = " + mobileID

cursor.execute(sql)
results = cursor.fetchall()
with open(mobileID+".csv", 'w', newline='') as f:
    writer = csv.writer(f)
    title = [["time","app","傳送者","內容","你有沒有在手機上感受或注意到通知來的瞬間","你如何感知到這則通知(複選)","在感受到通知的當下，你有沒有猜是誰傳的訊息？","請問你是否有猜對?","請問你剛剛猜的是誰？(請填你猜的人在通訊軟體上的名稱)","你是不是因為你所猜的那個人，而決定看不看這則通知？","你覺得這則通知的干擾程度(1:完全沒干擾；5:非常干擾)","你覺得這個時機點送這則通知如何","你有沒有立即去看這則通知？","這則訊息你預計什麼時候回覆？","這個通知的內容","這個通知的時效性(有急迫性)","你們的關係最可以用下列何者圖示表示","你當時正在做什麼事？","你當時正在做什麼事？-其他","你當時做這件事的專注(投入)程度？(1:非常不投入；5: 非常投入)","你當下在你身邊互動的有多少人？(不包含傳訊息、打電話等等)","你當下在你身邊互動的有誰？(選擇所有符合的身份)","你當下在你身邊互動的有誰?(選擇所有符合的身份)-其他"]]
    writer.writerows(title)
    for row in results:
        if(row[7] == "False"):
            continue
        time = row[44]
        app = row[39]
        contact_name = row[40]
        text = row[41]
        Q1 = row[18]
        Q2 = row[19]
        Q2_2 = row[27]
        Q2_2_other = row[28]
        Q3 =row[20]
        Q4 =row[21]
        Q5 =row[22]
        Q6 =row[23]
        Q7 =row[24]
        Q8 =row[25]
        Q9 =row[26]
        Q10 =row[29]
        Q11 = row[30]
        Q12 = row[31]
        Q13 =row[32]
        Q14 =row[33]
        Q15 =row[34]
        Q15_other=row[35]
        Q16 =row[36]
        Q17 =row[37]
        Q17_other =row[38]
        in_list = False

        """
        contact = ["name",interruptibility, respond, percept_count, total ESM, 立即回覆, 在數分鐘之內,在半小時以內,一小時以內,隔數小時之後，但會在當天回覆,不會在當天回覆,不會回覆,沒有預計,closeness, importance, urgence, timing]

        """

        data = [[time,app,contact_name,text,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q15_other,Q16,Q17,Q17_other]]
        writer.writerows(data)


        if(Q10 == ""):
            #print(Q1)
            continue
        """
        if(Q1 == "沒有，但已經在其他裝置上看到內容"):
            continue
        """
        for contact in contact_list:
            if(contact_name == contact[0]):
                #print("exist contact: ",contact_name)
                if(Q7 != ''):
                    contact[1] += int(Q7)
                    contact[3] += 1
                contact[4] +=1
                contact[13] += int(Q13) #closeness
                if(Q11 == "沒看到沒有任何影響"):
                    contact[14] += 1 #importance
                elif(Q11 == "沒看到不會有太大影響"):
                    contact[14] += 2
                elif(Q11 == "沒看到會有影響"):
                    contact[14] += 3
                elif(Q11 == "沒看到會有明顯的影響"):
                    contact[14] += 4
                elif(Q11 == "非常重要，一定要看到的訊息"):
                    contact[14] += 5

                if(Q12 == "無論什麼時候看到都可以"):
                    contact[15] += 1 #urgence
                elif(Q12 == "當下沒看到不會有太大的影響"):
                    contact[15] += 2
                elif(Q12 == "如果當下沒有看到，會有一點的影響"):
                    contact[15] += 3
                elif(Q12 == "如果當下沒有看到，會有明顯的影響"):
                    contact[15] += 4
                elif(Q12 == "一定當下看到，完全不能延遲"):
                    contact[15] += 5

                if(Q10=="立即回覆"):
                    contact[5]+=1
                elif(Q10=="在數分鐘之內"):
                    contact[6]+=1
                elif(Q10=="在半小時以內"):
                    contact[7]+=1
                elif(Q10=="一小時以內"):
                    contact[8]+=1
                elif(Q10=="隔數小時之後，但會在當天回覆"):
                    contact[9]+=1
                elif(Q10=="不會在當天回覆"):
                    contact[10]+=1
                elif(Q10=="不會回覆"):
                    contact[11]+=1
                elif(Q10=="沒有預計"):
                    contact[12]+=1

                if(Q8 == "現在是個非常好的時機"):
                    contact[16] += 5
                elif(Q8 == "現在是個好時機"):
                    contact[16] += 4
                elif(Q8 == "現在的時機還好"):
                    contact[16] += 3
                elif(Q8 == "現在時機不好"):
                    contact[16] += 2
                elif(Q8 == "現在時機非常不好"):
                    contact[16] += 1

                in_list = True
        if(in_list == False):
            #print("add contact: ",contact_name)
            data = [contact_name,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if(Q7 != ''):
                data[1] += int(Q7)
                data[3] += 1
            data[4] += 1
            data[13] += int(Q13)
            if(Q11 == "沒看到沒有任何影響"):
                data[14] += 1 #importance
            elif(Q11 == "沒看到不會有太大影響"):
                data[14] += 2
            elif(Q11 == "沒看到會有影響"):
                data[14] += 3
            elif(Q11 == "沒看到會有明顯的影響"):
                data[14] += 4
            elif(Q11 == "非常重要，一定要看到的訊息"):
                data[14] += 5

            if(Q12 == "無論什麼時候看到都可以"):
                data[15] += 1
            elif(Q12 == "當下沒看到不會有太大的影響"):
                data[15] += 2
            elif(Q12 == "如果當下沒有看到，會有一點的影響"):
                data[15] += 3
            elif(Q12 == "如果當下沒有看到，會有明顯的影響"):
                data[15] += 4
            elif(Q12 == "一定當下看到，完全不能延遲"):
                data[15] += 5

            if(Q10=="立即回覆"):
                data[5]+=1
            elif(Q10=="在數分鐘之內"):
                data[6]+=1
            elif(Q10=="在半小時以內"):
                data[7]+=1
            elif(Q10=="一小時以內"):
                data[8]+=1
            elif(Q10=="隔數小時之後，但會在當天回覆"):
                data[9]+=1
            elif(Q10=="不會在當天回覆"):
                data[10]+=1
            elif(Q10=="不會回覆"):
                data[11]+=1
            elif(Q10=="沒有預計"):
                data[12]+=1
                #print(data)
            if(Q8 == "現在是個非常好的時機"):
                data[16] += 5
            elif(Q8 == "現在是個好時機"):
                data[16] += 4
            elif(Q8 == "現在的時機還好"):
                data[16] += 3
            elif(Q8 == "現在時機不好"):
                data[16] += 2
            elif(Q8 == "現在時機非常不好"):
                data[16] += 1

            contact_list.append(data)

    blank = [[]]
    writer.writerows(blank)
    writer.writerows(blank)
    writer.writerows(blank)


    result = [["時間", "經緯度", "App", "title", "sub_text", "text", "ticker_text"]]
    writer.writerows(result)

    cursor.execute("SELECT * From notification WHERE device_id=\"{0}\" and send_esm=1 and esm_done=0;".format(mobileID)) #Q4: relationship, Q9: closeness, Q2_1: interruptibility, Q3: response,


    esm_not_done_list = cursor.fetchall()

    for e in esm_not_done_list:
        map_url = "https://www.google.com.tw/maps/@{0},{1},16.32z".format(e[6], e[5])
        writer.writerows( [[e[4], map_url] + list(e[7:12])]  )

    writer.writerows(blank)
    writer.writerows(blank)
    writer.writerows(blank)

    final_self_closeness = 0
    final_self_response = 0
    final_self_inter = 0
    questionniare_count = 0
    answered_questionniare = 0

    final_closeness = 0
    final_inter = 0
    final_resp = 0
    final_timing = 0
    final_percept = 0
    final_ESM_count = 0
    final_contact_5 = 0
    final_contact_6 = 0
    final_contact_7 = 0
    final_contact_8 = 0
    final_contact_9 = 0
    final_contact_10 = 0
    final_contact_11 = 0
    final_contact_12 = 0
    final_motivation_count = 0

    final_importance = 0
    final_urgence = 0
    final_notification_count = 0


    result = [["name","notification 總量","關係","Contact Questionnaire 自評資料( Closeness, Interruptibility, 回覆動機)", "total ESM","ESM 資料( Closeness, Interruptibility, 回覆動機, 重要程度, 緊急程度)","自評 Closeness","自評 Interruptibility","自評 回覆動機","Closeness","Interruptibility","Timing","回覆動機","重要程度","緊急程度", "立即回覆", "在數分鐘之內","在半小時以內","一小時以內","隔數小時之後，但會在當天回覆","不會在當天回覆","不會回覆","沒有預計"]]
    writer.writerows(result)

    #contact = ["name",interruptibility, respond, percept_count, total ESM, 立即回覆, 在數分鐘之內,在半小時以內,一小時以內,隔數小時之後，但會在當天回覆,不會在當天回覆,不會回覆,沒有預計,closeness, importance, urgence, timing]

    contact_list.sort(reverse=True, key=ESM_amount)
    for contact in contact_list:
        if(float(contact[3]) != 0):
            avg_intr = str(round(float(contact[1])/float(contact[3]),2))
            avg_timing = str(round(float(contact[16])/float(contact[3]),2))
            final_closeness += float(contact[13])
            final_percept += float(contact[3])

        else:
            avg_intr = "no data"
            avg_timing = "no data"
        avg_closeness = str(round(float(contact[13])/float(contact[4]),2))
        motivation_sum = contact[5]+ contact[6]+contact[7]+contact[8]+contact[9]+contact[10]+contact[11]
        contact_5 = str(contact[5])+" ("+str(float(contact[5])/float(contact[4])*100)+"%)"
        contact_6 = str(contact[6])+" ("+str(float(contact[6])/float(contact[4])*100)+"%)"
        contact_7 = str(contact[7])+" ("+str(float(contact[7])/float(contact[4])*100)+"%)"
        contact_8 = str(contact[8])+" ("+str(float(contact[8])/float(contact[4])*100)+"%)"
        contact_9 = str(contact[9])+" ("+str(float(contact[9])/float(contact[4])*100)+"%)"
        contact_10 = str(contact[10])+" ("+str(float(contact[10])/float(contact[4])*100)+"%)"
        contact_11 = str(contact[11])+" ("+str(float(contact[11])/float(contact[4])*100)+"%)"
        contact_12 = str(contact[12])+" ("+str(float(contact[12])/float(contact[4])*100)+"%)"

        avg_importance = round(float(contact[14])/float(contact[4]),2)
        avg_urgence = round(float(contact[15])/float(contact[4]),2)


        if(motivation_sum == 0):
            response_motivation = "no data"
        else:
            response_motivation = round(7 * float(contact[5])/float(motivation_sum) + 6 * float(contact[6])/float(motivation_sum) + 5 * float(contact[7])/float(motivation_sum) + 4 * float(contact[8])/float(motivation_sum) + 3 * float(contact[9])/float(motivation_sum) + 2 * float(contact[10])/float(motivation_sum) + 1 * float(contact[11])/float(motivation_sum), 2)
            final_resp += 7 * float(contact[5]) + 6 * float(contact[6])+ 5 * float(contact[7])+ 4 * float(contact[8]) + 3 * float(contact[9])+ 2 * float(contact[10]) + 1 * float(contact[11])
            final_motivation_count += motivation_sum

        final_inter += float(contact[1])
        final_timing += float(contact[16])
        final_ESM_count += float(contact[4])
        final_contact_5 += int(contact[5])
        final_contact_6 += int(contact[6])
        final_contact_7 += int(contact[7])
        final_contact_8 += int(contact[8])
        final_contact_9 += int(contact[9])
        final_contact_10 += int(contact[10])
        final_contact_11 += int(contact[11])
        final_contact_12 += int(contact[12])

        final_importance += int(contact[14])
        final_urgence += int(contact[15])

        relationship = ""
        self_closeness = ""
        self_interr = ""
        self_response = ""
        noti_count = 0
        for questionniare in contact_questionniare:
            if(questionniare[0] == contact[0]):
                relationship = questionniare[1]
                self_closeness = questionniare[2]
                self_interr = questionniare[3]
                self_response = questionniare[4]
                final_self_inter += float(questionniare[3])

                if(self_response=="通常立即回覆"):
                    self_response="7-通常立即回覆"
                    final_self_response += 7
                elif(self_response=="通常間隔數分鐘"):
                    self_response="6-通常間隔數分鐘"
                    final_self_response += 6
                elif(self_response=="通常半小時以內"):
                    self_response="5-通常半小時以內"
                    final_self_response += 5
                elif(self_response=="通常一小時以內"):
                    self_response="4-通常一小時以內"
                    final_self_response += 4
                elif(self_response=="通常幾小時內（當天）"):
                    self_response="3-通常幾小時內（當天）"
                    final_self_response += 3
                elif(self_response=="通常沒有在當天回覆"):
                    self_response="2-通常沒有在當天回覆"
                    final_self_response += 2
                elif(self_response=="通常不回覆"):
                    self_response="1-通常不回覆"
                    final_self_response += 1
                final_self_closeness += float(questionniare[2])
                questionniare_count += 1
        print(contact[0])
        for data in notification_list:
            if (data["name"] == contact[0]):
                data["selected"] = True
                noti_count = data["count"]
                break

        self_report_data = str(self_closeness).ljust(15) +str(self_interr).ljust(15) +str(self_response).ljust(15)
        esm_data = str(avg_closeness).ljust(15)+str(avg_intr).ljust(15)+str(response_motivation).ljust(15)+"      "+str(avg_importance).ljust(15)+str(avg_urgence).ljust(15)
        final_notification_count += noti_count
        result_data = [[contact[0],noti_count,relationship,self_report_data, contact[4], esm_data,self_closeness,self_interr,self_response,avg_closeness, avg_intr, avg_timing,response_motivation,avg_importance,avg_urgence,contact_5,contact_6,contact_7,contact_8,contact_9,contact_10,contact_11,contact_12]]
        writer.writerows(result_data)

    notification_list.sort(reverse=True, key=Noti_amount)
    for data in notification_list:
        if (data["selected"] == False):
            print(data["name"])
            final_notification_count += data["count"]
            writer.writerows([[data["name"],data["count"]]])

    print("questionnarie conact: ",str(questionniare_count))
    if(questionniare_count==0):
        questionniare_count = 1
    final_self_report_data = str(round(final_self_closeness/questionniare_count, 2)).ljust(15)+str(round(float(final_self_inter)/questionniare_count,2)).ljust(15)+str(round(float(final_self_response)/questionniare_count,2))
    final_esm_data = str(round(final_closeness/final_ESM_count,2)).ljust(15)+str(round(final_inter/final_percept,2)).ljust(15)+str(round(final_resp/final_motivation_count,2)).ljust(15)+"            "+str(round(float(final_importance)/final_ESM_count,2)).ljust(15)+str(round(float(final_urgence)/final_ESM_count,2)).ljust(15)


    final_data = [["Total",round(final_notification_count, 2),"",final_self_report_data,int(final_ESM_count),final_esm_data,round(final_self_closeness/questionniare_count, 2),round(float(final_self_inter)/questionniare_count,2),round(float(final_self_response)/questionniare_count,2),round(final_closeness/final_ESM_count,2),round(final_inter/final_percept,2),round(final_timing/final_percept,2),round(final_resp/final_motivation_count,2),round(float(final_importance)/final_ESM_count,2),round(float(final_urgence)/final_ESM_count,2), str(final_contact_5)+" ("+str(float(final_contact_5)/float(final_ESM_count)*100)+"%)",str(final_contact_6)+" ("+str(float(final_contact_6)/float(final_ESM_count)*100)+"%)",str(final_contact_7)+" ("+str(float(final_contact_7)/float(final_ESM_count)*100)+"%)",str(final_contact_8)+" ("+str(float(final_contact_8)/float(final_ESM_count)*100)+"%)",str(final_contact_9)+" ("+str(float(final_contact_9)/float(final_ESM_count)*100)+"%)",str(final_contact_10)+" ("+str(float(final_contact_10)/float(final_ESM_count)*100)+"%)",str(final_contact_11)+" ("+str(float(final_contact_11)/float(final_ESM_count)*100)+"%)",str(final_contact_12)+" ("+str(float(final_contact_12)/float(final_ESM_count)*100)+"%)" ]]
    writer.writerows(final_data)

    writer.writerows(blank)
    writer.writerows(blank)
    writer.writerows(blank)

    contact_title = [["name","IOS(1-7)","URCS(1-7)","Depandance(1-5)","Mobile Maintainace(1-5)","Interruptibility(1-5)","Obligation To Answer(1-5)","Ansering Expectation(1-5)"]]
    writer.writerows(contact_title)

    final_IOS = 0
    final_URCS = 0
    final_depandance = 0
    final_mobile_maintainace = 0
    final_obligation_to_answer = 0
    final_answering_expectation = 0
    final_interruptibility = 0
    contact_count = 0


    selected_contact_list_data = []

    cursor.execute("SELECT DISTINCT contact_name FROM contact_questionnaire WHERE user_id ="+uid)
    selected_contact_list_data = cursor.fetchall()

    cursor.execute("SELECT DISTINCT contact_name_line FROM contact_questionnaire WHERE user_id ="+uid)
    selected_contact_list_data += cursor.fetchall()

    selected_contact_list = [0]*len(selected_contact_list_data)

    print("selected contact:")
    for i in range(len(selected_contact_list_data)):
        selected_contact_list[i] = selected_contact_list_data[i][0]

    print("after:")
    for contact_item in selected_contact_list:
        print(contact_item)

    cursor.execute("SELECT * FROM contact WHERE uid ="+uid)  #26:IOS    #27~38: URCS       #39~45:depandance      #46~54:mobile mantainace      #55~60: obligation to answer       #61~66: expection to answer
    contact_list = cursor.fetchall()

    for contact in contact_list:
        contact_count+=1
        name = contact[67]
        print(name)
        if(name in selected_contact_list):
            selected_contact_list.remove(name)
            print("name exist: ",name)
        depandance = 0
        for i in range(39, 46):
            if(i == 41 or i==45):
                depandance += float((int(contact[i])-6)*(-1))
            else:
                depandance += float(contact[i])

        depandance /= 7
        final_depandance += depandance

        mobile_maintainace = 0
        for i in range(46,55):
            mobile_maintainace += float(contact[i])

        mobile_maintainace /= 9
        final_mobile_maintainace += mobile_maintainace

        answering_expectation = 0
        for i in range(61,67):
            answering_expectation += float(contact[i])

        answering_expectation /= 6
        final_answering_expectation += answering_expectation


        obligation_to_answer = 0
        for i in range(55,61):
            obligation_to_answer += float(contact[i])

        obligation_to_answer /= 6
        final_obligation_to_answer += obligation_to_answer

        IOS = int(contact[26])
        final_IOS += IOS
        URCS = 0
        for i in range(27,39):
            URCS += float(contact[i])
        URCS /= 12
        final_URCS += URCS

        interruptibility = int(contact[18])
        final_interruptibility += interruptibility

        #print(interruptibility)
        contact_data = [[name,round(IOS, 2),round(URCS, 2),round(depandance, 2),round(mobile_maintainace, 2),round(interruptibility, 2),round(obligation_to_answer, 2),round(answering_expectation, 2)]]
        writer.writerows(contact_data)

        """
        Interruptibility_list.append(interruptibility)
        Obligation_to_answer_list.append(obligation_to_answer)
        Answering_expectation_list.append(answering_expectation)
        Mobile_maintainace_list.append(mobile_maintainace)
        Depandance_list.append(depandance)
        IOS_list.append(IOS)
        URCS_list.append(URCS)
        """

    for selected_contact_name in selected_contact_list:
        writer.writerows([[selected_contact_name]])
    if(contact_count == 0):
        contact_count = 1

    final_IOS = round(float(final_IOS)/contact_count, 2)
    final_URCS = round(float(final_URCS)/contact_count, 3)
    final_depandance = round(float(final_depandance)/contact_count, 2)
    final_mobile_maintainace = round(float(final_mobile_maintainace)/contact_count, 2)
    final_obligation_to_answer = round(float(final_obligation_to_answer)/contact_count, 2)
    final_answering_expectation = round(float(final_answering_expectation)/contact_count, 2)
    final_interruptibility = round(float(final_interruptibility)/contact_count, 2)
    total_contact_data = [["Total",final_IOS,final_URCS,final_depandance,final_mobile_maintainace,final_interruptibility,final_obligation_to_answer,final_answering_expectation]]
    writer.writerows(total_contact_data)

db.close()
