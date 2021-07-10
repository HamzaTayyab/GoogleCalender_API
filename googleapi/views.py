import os
from django.shortcuts import render, redirect
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapi.googleapifunctions import API_1, schedule_event
import json
import pickle
from django import forms
from googleapi.models import teachers
from googleapi.forms import OauthForm
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapi.models import teachers

# Create your views here.


# def API_1(name, Email, subj, onset, dur):
# credentials2 = pickle.load(open("marc_token.pkl", "rb"))
# credentials3 = pickle.load(open("andrew_token.pkl", "rb"))

# # Dictionary for Subjects and their relevant teachers
# subject_dict = {'Calculations': ['Zachary Piracha', 'Marc Berman'],
#                 'Clinical Pharmacy': ['Zachary Piracha', 'Andrew Piracha'],
#                 'Pharmacy Law': ['Zachary Piracha', 'Andrew Piracha'],
#                 'Compounding Exam': ['Zachary Piracha', 'Andrew Piracha'],
#                 'General Pharmacology': ['Zachary Piracha', 'Andrew Piracha']}
# # Dictionary for Authors and their access tokens
# Author_dict = {'Zachary Piracha': [credentials1, "https://i.ibb.co/3BcnXzh/Image-from-i-OS-1.jpg"],
#                'Marc Berman': [credentials2, "https://i.ibb.co/hZMxW4J/20210617-154244.jpg"],
#                'Andrew Piracha': [credentials3, "https://i.ibb.co/rvTJ9x5/Image-from-i-OS.jpg"]}
# Student_name = name
# Student_email = Email
# Subject = subj
# Onset = onset
# Event_duration = dur
# free_slot = []
# for key in subject_dict:
#     if (key == subj):
#         for obj in subject_dict[key]:
#             for index, auth in enumerate(Author_dict):
#                 if (obj == auth):
#                     service = build("calendar", "v3",
#                                     credentials=Author_dict[auth][0])
#                     auth_img = Author_dict[auth][1]
#                     free_slot.insert(index, free_slots_1(
#                         Onset, Event_duration, service, auth, auth_img))
# return ({'Author_details': free_slot}, {'Subject': Subject}, {'Email': Student_email})


class API1(APIView):
    def post(self, request):
        try:
            data = request.data
            Name = data["name"]
            Email = data["email"]
            Subject = data["subject"]
            Onset = int(data["onset"])
            Duration = int(data["duration"])
            res = API_1(Name, Email, Subject, Onset, Duration)

            return Response(data=res)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class API2(APIView):
    def post(self, request):

        try:
            data = request.data
            Start = data["start"]
            End = data["end"]
            Subject = data["subject"]
            Author = data["author"]
            Email = data["email"]
            Auth_imgLink = data["imgLink"]
            Fee = data["fee"]
            res = schedule_event(Start, End, Author,
                                 Auth_imgLink, Fee, Subject, Email)
            return Response(data=res)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


def file_handler(file):
    data_file = open('test.json', "wb+")
    data_file.write(file)


def modelCreateView(request, id):
    context = {}
    context['form'] = OauthForm()
    json_fie = None

    if request.POST:
        form = OauthForm(request.POST, request.FILES)

        if form.is_valid():
            json_file = request.FILES["json_uploader"]
            json = json_file.read()
            file_handler(json)

            scopes = ['https://www.googleapis.com/auth/calendar']
            path_file = os.getcwd()
            flow = InstalledAppFlow.from_client_secrets_file(
                path_file + "\\test.json", scopes=scopes)

            cred = flow.run_local_server()
            path = "pickles/"+id+".pkl"
            pickle.dump(cred, open(path, "wb"))

            # print(cred.__dict__)

            # context['cre'] = "/admin/googleapi/teachers/"
            x = teachers.objects.filter(id=id).update(credentials=path)
            return redirect('/admin/googleapi/teachers')
    return render(request, "ext.html", context)
