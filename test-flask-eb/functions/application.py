from flask import Flask, request, jsonify
import pickle
import numpy as np
from testemail import send_email
from notification import *
from studentUpdates import *
from books import *
import firebase_admin
from firebase_admin import credentials, storage
from getFinancialAid import *
from datetime import datetime, timedelta
from stats import *
import os
from check_video import *
from detect_face import *
app = Flask(__name__)

cred = credentials.Certificate("serviceKeyv2.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sih1-7632c.appspot.com'
})
bucket = storage.bucket()

@app.route("/getCareerRecommendation", methods=['GET', 'POST'])
def get_career_recommendation():
    with open('model.pkl', 'rb') as file:
        mlp_classifier= pickle.load(file)
    json_data = request.get_json()
    feature = json_data['list']
    feature = feature.split(",")
    def preprocess_user_input(user_input):
        user_input_encoded = [1 if answer.lower() == 'yes' else 0 for answer in user_input]
        return np.array(user_input_encoded).reshape(1, -1)
    
    ans = mlp_classifier.predict(preprocess_user_input(feature))
    response = {'prediction': ans.tolist()}
    return jsonify(response)

@app.route("/sendOTPtoEmail", methods=['GET', 'POST'])
def sendOtpToEmail():
    otp = send_email("chintan222005@gmail.com")
    return jsonify(otp)

@app.route("/sendNotification", methods=['GET', 'POST'])
def sendNotification():
    return send_push_notification()

@app.route('/getUpdates', methods=['GET'])
def getUpdates():
    result = scrape_scholarship_info()
    if isinstance(result, list):
        return jsonify({'data': result}), 200
    else:
        return jsonify({'error': result}), 500
    
@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    url = "https://jobs-api14.p.rapidapi.com/list"
    headers = {
        "X-RapidAPI-Key": "31f9f38f67msh61dc71a007fa815p1d2c63jsnf6de091561b4",
        "X-RapidAPI-Host": "jobs-api14.p.rapidapi.com"
    }
    query = request.args.get('query')
    location = request.args.get('location')
    distance = request.args.get('distance', '1.0')
    language = request.args.get('language', 'en_GB')
    remote_only = request.args.get('remoteOnly', 'false')
    date_posted = request.args.get('datePosted', 'month')
    employment_types = request.args.get('employmentTypes', 'fulltime;parttime;intern;contractor')
    querystring = {"query": query,"location": location,"distance": distance,"language": language,"remoteOnly": remote_only,"datePosted": date_posted,"employmentTypes": employment_types,"index": "0"}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch job listings.'}), 500
    
@app.route('/downloadAndStore', methods=['GET'])
def download_and_store():
    class_num = request.args.get('class')
    medium_type = request.args.get('medium')
    subject_type = request.args.get('subject')
    file_name = form_download_query_param(class_num, medium_type, subject_type)
    if not file_name:
        return jsonify({'message': 'Invalid parameters'}), 400
    url = "https://books.ebalbharati.in/pdfs/" + file_name
    if download_file(url, file_name):
        file_path = f"textbooks/{class_num}/{medium_type}/{subject_type}.pdf"
        blob = bucket.blob(file_path)
        blob.upload_from_filename(file_name)
        download_url = blob.generate_signed_url(version="v4", expiration=datetime.utcnow() + timedelta(hours=1), method="GET")
        return jsonify({'message': 'PDF downloaded and stored successfully', 'download_url': download_url}), 200
    else:
        return jsonify({'message': 'Failed to download PDF'}), 500
    
@app.route("/getGovtSchemeData", methods=['GET', 'POST'])
def getGovtSchemeData():
    if request.is_json:
        request_data = request.json
        filterType = request_data.get("filterType")
        searchParam = request_data.get("searchParam")
        result_list = []
        if(filterType.upper() == "SCHOLARSHIP"):
            result_list = get_scholarship_info(27, searchParam)
        elif(filterType.upper() == "APPRENTICESHIP"):
            result_list = get_apprenticeship_info(6, searchParam)
        elif(filterType.upper() == "JOB"):
            result_list = get_job_info(20, searchParam)
        elif(filterType.upper() == "VOLUNTEER"):
            result_list = get_volunteer_info(4, searchParam)
        else:
            result_list = get_all(searchParam)
        return jsonify(result_list), 200
    else:
        return jsonify({'error': 'Request body must be JSON'}), 400

@app.route("/getStats", methods = ["GET", "POST"])
def getStats():
    request_data = request.json
    return gen_stats(request_data.get("width"), request_data.get("height"))

@app.route("/proofreadVideo", methods=['GET', 'POST'])
def proofReadVideo():
    video_file = request.files['video']
    video_path = video_file.filename
    video_file.save(video_path)
    result = process_video(video_path)
    os.remove(video_path)

    return result
@app.route('/verify_face', methods=['POST'])
def handle_verify_face():
    image_file = request.files['image']
    image_path = image_file.filename
    image_file.save(image_path)
    result = verify_human_face(image_path)
    os.remove(image_path)
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)