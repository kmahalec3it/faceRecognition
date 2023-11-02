import os
from azure.storage.blob import BlobServiceClient
from PIL import Image
import io
from recognition.NamecardAnalyzer import analyze_name_cards
# from recognition.NamecardAnalyzer import analyze_name_cards

from recognition.match_Image import match_faces_in_image

# Get namecard JSON and extract firstname, lastname and photo
def face_recog() :
 
 json_data = analyze_name_cards()
 print("RETURNED JSON : ", json_data)

 if json_data.get("NameCards"):
        name_cards = json_data["NameCards"]
        for name_card in name_cards:
            if name_card.get("CanProcess") == "true" :
                first_name = name_card.get("FirstName", "")
                last_name = name_card.get("LastName", "")
                profile_photo = name_card.get("ProfilePhoto", "")
              #   result = (first_name, last_name, profile_photo)
                break
        print("COMPLETE STATUS ", first_name, last_name, profile_photo)

#  output_folder = "Images/Processed_Images"
 image_folder = "Images/Known_Images"
 image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

# Loop through each image file
 for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
 # Call the match_faces_in_image function for the current image
       #  output_image_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + "_output.jpg")

        new_json_file = match_faces_in_image(image_path, json_data)

 return(new_json_file)

# return("Successful")


