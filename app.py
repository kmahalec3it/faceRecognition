from flask import Flask,request,jsonify,render_template
# import CE.main as main
# import CE.sections as sec
from recognition.faceRecog import face_recog
from recognition.NamecardAnalyzer import analyze_name_cards
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/recognitions', methods=['GET'])
def get_sec():
    # Call the face_recog function from faceRecog.py
    try:
        result = face_recog()
        response = {'message': result}
        return response
    except Exception as ex:
        print("error in face recog : ", ex)
        return render_template('error.html')

@app.route('/namecard', methods=['GET'])
def get_card():
    # Call the face_recog function from faceRecog.py
    result = analyze_name_cards()
    
    response = result
    return jsonify(response)
    # return response


# @app.route("/")
# def title_page():
#     return render_template('index.html')

# @app.route('/sections', methods = ['GET'])
# def get_sec():
#     sections = sec.fixed_section_list
#     response = {'sections':sections}
#     return render_template('sections.html',response=response)

# @app.route('/api/sections', methods = ['GET'])
# def get_sections():
#     try:
#         # sections = ["SELLERS' WARRANTIES AND UNDERTAKINGS", "SELLERS' INDEMNITIES", "BUYER'S WARRANTIES", "TERM AND TERMINATION"]
#         # sections = sec.get_all_sections()
#         # sections = sec.fixed_section_list
#         sections = sec.get_sections_list()
#         response = {'sections':sections}
#         return jsonify(response)
#     except Exception as ex:
#         print("Exception: ",ex)
#         return {"error",ex}
#     # ngrok http 5030 -host-header="localhost:5030"

# @app.route('/api/sectionData', methods = ['POST'])
# def section_data():
#     try:
#         data = request.get_json()
#         print("In /api/sectionData 11")
#         section = data.get('section',"")
#         print("In /api/sectionData 22")
#         sectionData = main.get_section_data(sectionName=section)
#         response = {'sectionData':sectionData}
#         return jsonify(response)
#     except Exception as ex:
#         print("Error: ",ex)
#         return("error: ",ex)


if __name__ == '__main__':
    app.run(debug=True,port=5030)
    



# @app.route('/api/rfq', methods=['POST'])
# def get_query():
#     user_question = str(request.form['question'])

#     try:
#         response = rfq.get_documents_results(user_question=user_question)
#         print("Response before sending to index file", response)
#         res = Markup(response)
#         return render_template('index.html', result=res, question=user_question)
#     except Exception as ex:
#         print("Error is : ",ex)
#         return render_template('error.html')  