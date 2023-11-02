import face_recognition
import cv2
import os
import json
from flask import jsonify
import numpy as np

def match_faces_in_image(known_image_path, json_data_file):
    # Load the known image
    known_image = face_recognition.load_image_file(known_image_path)

    # Encode the known image (create a face encoding)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Extract the name from the file name (assuming the image file is named after the person)
    known_image_name = os.path.splitext(os.path.basename(known_image_path))[0]

    # Define the target folder where target images are present
    target_folder = "Images/Event_Images"

    # data = json.loads(json_data_file.read())

    # Loop through each target image in the target folder
    for target_image_file in os.listdir(target_folder):
        # Load the target image
        target_image = face_recognition.load_image_file(os.path.join(target_folder, target_image_file))

        # Find all face locations and face encodings in the target image
        face_locations = face_recognition.face_locations(target_image)
        face_encodings = face_recognition.face_encodings(target_image, face_locations)

        min_confidence = 1.0

        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Calculate the distance (confidence) between the known face encoding and the detected face encoding
            confidence = face_recognition.face_distance([known_face_encoding], face_encodings[i])[0]

            if confidence < min_confidence:
                min_confidence = confidence

        print(known_image_name)
        # Add the target image name and confidence to the "EventPhotos" section of the NameCard
        for namecard in json_data_file["NameCards"]:
            print(namecard["ProfilePhoto"])
            if namecard["ProfilePhoto"] == (known_image_name + ".jpg") :
              event_photo = {
                    "FileName": target_image_file,
                    "Confidence": f"{(1 - min_confidence) * 100:.0f}%"
                }
              namecard["EventPhotos"].append(event_photo)
              print(event_photo)

    # Save the updated JSON data back to the file
    # with open(json_data_file, 'w') as json_file:
    #     json.dump(data, json_file, indent=4)
    # namecards = data.get('NameCards')
    # for namecard in namecards :
    #   if namecard.get('ProfilePhoto') == known_image_name :
    #       namecard.get('EventPhotos').append(
    #           {
    #                "FileName": "",
    #                 "Confidence": "61%"
    #           }
    #       )       
    # data = jsonify(json_data_file)
    return(json_data_file)
