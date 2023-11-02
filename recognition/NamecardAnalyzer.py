import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient

def analyze_name_cards():
    # Azure Form Recognizer endpoint and key
    endpoint = "https://formreconew.cognitiveservices.azure.com/"
    key = "4aedaf26c19940b6aa441b4552a4dbe2"

    # Azure Blob Storage connection string and container name
    connection_string = "DefaultEndpointsProtocol=https;AccountName=saforformrecog;AccountKey=Zq1FPqmX2bwkA4nqs+frTsNe1Qwx5tlxZ6bDB4bK44Hy3mmPbi1q3pXrPCvE7TaQPKiyCwBZyelx+ASt45QzJg==;EndpointSuffix=core.windows.net"
    container_name = "blobcontainernamecards"

    # Model ID for the trained model in Azure Form Recognizer
    model_id = "newmodelstudent"

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Create a Document Analysis client
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # List all blobs in the container
    blobs = container_client.list_blobs()

    # Initialize a list to store the content of the results in the desired format
    name_cards = []

    # Iterate through the blobs and analyze each document using the specified model
    for blob in blobs:
        blob_client = container_client.get_blob_client(blob.name)
        blob_data = blob_client.download_blob().readall()

        try:
            # Analyze the document using the specified model
            poller = document_analysis_client.begin_analyze_document(
                model_id,
                document=blob_data,
                locale="en-US"
            )
            result = poller.result()

            # Extract and transform the content into the desired format
            content = " ".join([line.content for page in result.pages for line in page.lines])

            # Check if "SerialNo" is not empty
            serial_no = content.split("First Name:")[0].strip("Sr.no:").strip().split(" ")[0]
            can_process = "true" if serial_no else "false"

            # Determine the "Reason" based on "CanProcess" value
            reason = "success" if can_process == "true" else "Name card not recognized"

            # Initialize EventPhotos as an empty list of dictionaries with empty FileName and Confidence
            event_photos = []

            name_card = {
                "SerialNo": serial_no,
                "FirstName": content.split("First Name:")[1].split("Last Name:")[0].strip(),
                "LastName": content.split("Last Name:")[1].split("Email:")[0].strip(),
                "EmailID": content.split("Email:")[1].split("Mob no:")[0].strip(),
                "ContactNo": content.split("Mob no:")[1].split("Address:")[0].strip(),
                "Address": content.split("Address:")[1].split("School Name:")[0].strip(),
                "School Name": content.split("School Name:")[1].strip(),
                "CanProcess": can_process,
                "Reason": reason,
                "ProfilePhoto": "",
                "EventPhotos": event_photos  # Initialize EventPhotos as an empty list of dictionaries
            }
            name_cards.append(name_card)
        except Exception as e:
            print(f"Error processing document: {e}")
            name_card = {
                "SerialNo": "",
                "FirstName": "",
                "LastName": "",
                "EmailID": "",
                "ContactNo": "",
                "Address": "",
                "School Name": "",
                "CanProcess": "false",
                "Reason": "Name card not recognized",
                "ProfilePhoto": "",
                "EventPhotos": event_photos  # Initialize EventPhotos as an empty list of dictionaries
            }
            name_cards.append(name_card)

    # Create a JSON object
    name_cards_json = {"NameCards": name_cards}

    # If "CanProcess" is "true," retrieve and process profile images from the "blobcantaineruserphoto" container
    profile_container_name = "blobcantaineruserphoto"
    if any(entry["CanProcess"] == "true" for entry in name_cards_json["NameCards"]):
        profile_photos = blob_service_client.get_container_client(profile_container_name).list_blobs()

        for profile_blob in profile_photos:
            profile_photo_name = profile_blob.name
            serial_no_match = profile_photo_name.split("_")[0]
            matching_name_card = next((nc for nc in name_cards_json["NameCards"] if nc["SerialNo"] == serial_no_match), None)
            if matching_name_card:
                matching_name_card["ProfilePhoto"] = profile_photo_name

    # Update "Reason" to "Profile photo not found" for entries with empty "ProfilePhoto" and "CanProcess" set to "true"
    for entry in name_cards_json["NameCards"]:
        if entry["CanProcess"] == "true" and not entry["ProfilePhoto"]:
            entry["Reason"] = "Profile photo not found"
            entry["CanProcess"] = "false"

    return name_cards_json

# Call the function to get the name_cards_json
name_cards_json = analyze_name_cards()
print("\n_________Json _________\n", name_cards_json)
