from GoogleApi import API_1, schedule_event
from flask import Flask, request,jsonify
import json
app = Flask(__name__)

# @app.route('/API2',methods=["GET"])
# def API2():
#     try:
#         Start = request.args.get("Start")
#         End = request.args.get("End")
#         Subject = request.args.get("sub")
#         Author = request.args.get("Author")
#         email = request.args.get("Email")
#         # return json.dumps([Start,End,Author,Subject,email]);
#         res = schedule_event(Start,End,Author,Subject,email)
#         return (json.dumps(res));
#     except:
#         return "Please try again with correct arguments"

# JSON FORMAT FOR CALLING API-1
# {
#     "subject": "Calculations",
#     "name": "Tobe Ony",
#     "email": "tobe@gmail.com",
#     "onset": 1,
#     "duration": 1
# }
@app.route('/API-1',methods=["POST"])
def API1():
    try:
        data = request.get_json()
        Name = data["name"]
        Email = data["email"]
        Subject = data["subject"]
        Onset = int(data["onset"])
        Duration = int(data["duration"])
        res = API_1(Name, Email, Subject, Onset, Duration)

        return jsonify(res)
    except:
        return "Bad Request!"

# JSON FORMAT FOR CALLING API-2
# {
#     "subject": "Calculations",
#     "author": "Zach",
#     "email": "tobe@gmail.com",
#     "start": 1,
#     "end": 1
# }
@app.route('/API-2',methods=["POST"])
def API2():
    try:
        data = request.get_json()
        Start = data["start"]
        End = data["end"]
        Subject = data["subject"]
        Author = data["author"]
        Email = data["email"]
        res = schedule_event(Start,End,Author,Subject,Email)
        return jsonify(res)
    except:
        return "Bad Request!"

if __name__ == '__main__':
    app.run()