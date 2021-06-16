# Importing all the required packages
import pickle
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime,date,timedelta
import pytz

# Importing Credential to all authors' calenders
credentials1 = pickle.load(open("zach_token.pkl", "rb"))
credentials2 = pickle.load(open("marc_token.pkl", "rb"))
credentials3 = pickle.load(open("andrew_token.pkl", "rb"))

# Dictionary for Subjects and their relevant teachers
subject_dict = {'Calculations':['Zach','Marc'],'Clinical':['Zach','Andrew'],'Concept Prep':['Zach','Andrew'],
                'Compounding Exam': ['Zach','Andrew'],'General Pharmacology': ['Zach','Andrew']}
# Dictionary for Authors and their access tokens
Author_dict = {'Zach':credentials1,'Marc':credentials2,'Andrew':credentials3}

def API_1(name,Email,subj,onset,dur):
    Student_name = name
    Student_email = Email
    Subject = subj
    Onset = onset
    Event_duration = dur
    free_slot = list()
    for key in subject_dict:
        if (key==subj):
            for obj in subject_dict[key]:
                for index,auth in enumerate(Author_dict):
                    if (obj==auth):
                        service = build("calendar", "v3", credentials=Author_dict[auth])
                        free_slot.insert(index,free_slots_1(Onset,Event_duration,service,auth))
    return (free_slot,Subject,Student_email)

def busy_schedule_1(Min, Max, service):
    # Getting the scheduled events from the calendar
    calendar_list = service.events().list(calendarId='primary',
                                          timeMin=Min, timeMax=Max, timeZone='US/Eastern', singleEvents="TRUE",
                                          orderBy="startTime").execute()
    # Creating a list to save start, endtime and date for all events
    Busy_schedule = list()
    # Getting the start and End time element off all the events from calendars
    for index, obj in enumerate(calendar_list['items']):
        Start = obj['start']['dateTime']
        End = obj['end']['dateTime']
        Busy_schedule.insert(index, [Start, End])
    # Busy_schedule.insert(2,['21:00','22:00','2021-05-10'])
    return (Busy_schedule)

# THIS FUNCTION HELPS IN ROUNDING OFF THE MINUTES & SECONDS TO NEXT HOUR
def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta

# THIS FUNCTION IS USED TO RETURN MINIMUM AND MAXIMUM DATE DEPENDING UPON DAYS PARAM
def time_Min_Max(days):
    timezone = pytz.timezone('US/Eastern')
    # ------------ MinTime ---------------
    if (days == 1):
        today = datetime.now(timezone)
        days = 2
    elif (days == 7):
        today = datetime.now(timezone) + timedelta(days=1)
        # today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    Mintime = today.strftime('%Y-%m-%dT%H:%M:%S') + '-0400'
    # ------------- MaxTime ---------------
    today = datetime.now(timezone)
    Maxtime = today.replace(hour=0, minute=0, second=0, microsecond=0)
    Maxtime = Maxtime + timedelta(days)
    Maxtime = Maxtime.strftime('%Y-%m-%dT%H:%M:%S') + '-0400'
    Maxtime
    return Mintime, Maxtime

# THIS FUNCTION IS USED TO RETURN THE FEE FOR EACH SESSION
def sub_fee(dur):
    if (dur == 1):
        Fee = 40
    else:
        Fee = 80
    return (Fee)


##############################
# DET: DESIRED EVENT TIME
# DEET: DESIRED EVENT END TIME
#
# ET: EVENT TIME
# EET: EVENT END TIME
###############################
# THIS FUNCTION WILL RETURN THE FREE SLOTS FROM THE CALENDER
def free_slots_1(onset, dur, service, auth):
    Onset = onset
    Event_duration = dur
    Fee = sub_fee(dur)

    # Extracting Free time to schedule an event
    tobe_scheduled = list()
    DET2 = datetime.now(pytz.timezone('US/Eastern'))
    DET2 = ceil_dt(DET2.replace(tzinfo=None), timedelta(minutes=60))

    DEET2 = (DET2 + timedelta(hours=Event_duration))
    DEET2 = ceil_dt(DEET2.replace(tzinfo=None), timedelta(minutes=60))
    eventEnd_time = DEET2.strftime("%H")

    # Getting the busy schedule w.r.t onset value. Onset=1 means within 1 day & Onset=2 means within a week
    schedule = list()
    if (Onset == 1):
        time = time_Min_Max(1)
        schedule = busy_schedule_1(time[0], time[1], service)
    elif (Onset == 2):
        time = time_Min_Max(7)
        schedule = busy_schedule_1(time[0], time[1], service)

    start_date = DET2.date()

    # Iterating over the schedule to get free slots
    for index, obj in enumerate(schedule):
        Start_obj = datetime.strptime(obj[0], '%Y-%m-%dT%H:%M:%S%z')
        End_obj = datetime.strptime(obj[1], '%Y-%m-%dT%H:%M:%S%z')

        ET2 = Start_obj
        EET2 = End_obj

        # Need to compare dates instead of simplying updating it on index. declare a variable start date and store the date
        # of the first event in it then keeps on comparing it with the other events and update it when it doesn't matches.

        # print((DET2.date()-start_date).days,start_date,DET2.date())
        if (DET2.hour < ET2.hour):
            # print(1,DET2.hour,DEET2.hour,ET2.hour,EET2.hour,DET2)
            if (DEET2.hour <= ET2.hour):
                break
            else:
                DET2 = EET2
                DEET2 = DET2 + timedelta(hours=Event_duration)
        elif (DET2.hour > ET2.hour):
            # print(2,DET2.hour,DEET2.hour,ET2.hour,EET2.hour,DET2)
            if (DEET2.hour > EET2.hour):
                break
            else:
                DET2 = EET2
                DEET2 = DET2 + timedelta(hours=Event_duration)
                # print(DET,DEET)
        elif (DET2.hour == ET2.hour):
            # print(3,DET2.hour,DEET2.hour,ET2.hour,EET2.hour,DET2)
            DET2 = EET2
            DEET2 = DET2 + timedelta(hours=Event_duration)

    if (onset == 1 and (DET2.date() - start_date).days > 1):
        DET2 = "Not Available"
        DEET2 = "Not Available"
        Fee = 'NA'
    elif (onset == 2 and (DET2.date() - start_date).days > 7):
        DET2 = "Not Available"
        DEET2 = "Not Available"
        Fee = 'NA'
    else:
        DET2 = DET2.strftime('%Y-%m-%dT%H:%M:%S') + '-0400'
        DEET2 = DEET2.strftime('%Y-%m-%dT%H:%M:%S') + '-0400'

    return DET2, DEET2, auth, Fee;

# STARTING API2 PART
def schedule_event(Start,End, Author,Subject_name,Student_email):
    event = {
      'summary': Subject_name + ' Class',
      'location': 'Google hangout',
      'start': {
        'dateTime': Start,
        'timeZone': 'America/New_York',
      },
      'end': {
        'dateTime': End,
        'timeZone': 'America/New_York',
      },
      'conferenceData': {
        'createRequest': {
        'conferenceSolutionKey': {
          'type': 'hangoutsMeet'
        },
        'requestId': "some-random-string"
      }
        },
      'attendees': [
        {'email': Student_email},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    # print (event)
    service = build("calendar", "v3", credentials=Author_dict[Author])
    event = service.events().insert(calendarId='primary',conferenceDataVersion=1, body=event).execute()
    Meeting_link = event.get('hangoutLink')

    return (Meeting_link, Start, End,Author);