from telegram import ParseMode
from telegram.ext import CommandHandler, Defaults, Updater
import requests
import datetime
import time
import os
# from win10toast import ToastNotifier

TELEGRAM_TOKEN = os.environ.get("TOKEN")
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
responseNorth={}
responseSouth={}
lastRefreshTime=0
# toast = ToastNotifier()


def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello there!\n<b>Welcome to the Goa 18-45 vaccination alert bot</b>\nThis bot will alert you when there are avaiable slots for vaccinations in the age group of 18-45.\nType `/alert_district north 1` to get alerts for North Goa 1st dose\nType `/alert_district south 1` to get alerts for South Goa 1st  dose\nYou can issue multiple commands to get alerts\n <b><i>DISCLAIMER: Please do not use this bot as your only source of information. This is only meant to be an extra tool to aid you.</i></b>\n\n-TIM3LORD')

def availableAlert(update, context):
    if len(context.args) == 2:
        district = context.args[0].lower()
        dose = context.args[1]
        # toast.show_toast("Started!","Started checking",duration=20)
        context.job_queue.run_repeating(availableAlertCallback, interval=10, first=10, context=[district,dose, update.message.chat_id])
        
        response = f"⏳ I will send you a message when there are vaccination slots available in "+district+" Goa.\n"
        
    else:
        response = '⚠️ Please provide a value like `/alert_district north 1` or `/alert_district south 1`'
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def availableAlertCallback(context):
    district = context.job.context[0]
    dose = context.job.context[1]
    chat_id = context.job.context[2]

    send = False
    spots = checkAvailable(district.lower(),dose)

    if int( 'available' in spots):
        send = True

    if send:
        response = "Dose "+str(spots['dose'])+":\nThere are "+str(spots['available'])+" doses of "+str(spots['vaccine'])+" available at "+str(spots['name'])+","+str(spots['address'])+" on "+str(spots['date'])+" ! Please issue the command again to keep receiving alerts"
        # toast.show_toast("Vaccine available!",response,duration=20)
        context.job.schedule_removal()

        context.bot.send_message(chat_id=chat_id, text=response,timeout=None)

def checkJobs(update,context):
    if context.job_queue.jobs():
        for job in context.job_queue.jobs():
            context.bot.send_message(chat_id=update.effective_chat.id, text=job.name+" is "+str(job.enabled),timeout=None)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No jobs running",timeout=None)

def checkAvailable(district,dose):
    if int(time.time())-lastRefreshTime > 30:
        refreshData()
    result={}
    if district=='north':
        data = responseNorth
    elif district=='south':
        data = responseSouth
        
    for center in data['centers']:
        for session in center['sessions']:
            if int(dose) == 1:
                 if int(session['available_capacity_dose1'])>0 and int(session['min_age_limit'])==18:
                    result['dose']=1
                    result['available']=session['available_capacity_dose1']
                    result['vaccine']=session['vaccine']
                    result['name']=center['name']
                    result['address']=center['address']
                    result['date']=session['date']
            elif int(dose) == 2:
                if int(session['available_capacity_dose2'])>0 and int(session['min_age_limit'])==18:
                    result['dose']=2
                    result['available']=session['available_capacity_dose2']
                    result['vaccine']=session['vaccine']
                    result['name']=center['name']
                    result['address']=center['address']
                    result['date']=session['date']
            
    print(result)
    return result

def refreshData():
    print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"- Refreshing")
    currentDate = datetime.datetime.now().strftime("%d-%m-%Y")
    try:
        global responseNorth
        global responseSouth
        responseNorth = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=151&date="+currentDate,headers=headers).json()
        # responseNorth = requests.get("http://localhost:5000/north",headers=headers).json()
        # print(responseNorth)
        responseSouth = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=152&date="+currentDate,headers=headers).json()
        # responseSouth = requests.get("http://localhost:5000/south",headers=headers).json()
        # print(responseSouth)

        lastRefreshTime= int(time.time())       
        
    except:
        pass
    

if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', startCommand)) # Accessed via /start
    dispatcher.add_handler(CommandHandler('alert_district', availableAlert)) # Accessed via /alert_district
    dispatcher.add_handler(CommandHandler('status', checkJobs)) # Accessed via /status

    updater.start_polling() # Start the bot

    updater.idle() # Wait for the script to be stopped, this will stop the bot as well
