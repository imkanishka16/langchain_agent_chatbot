import os
import shutil
import requests
from data_store import register

def extract_file_id(drive_url):
    """
    Extract the file ID from a Google Drive URL.
    """
    return drive_url.split('/d/')[1].split('/')[0]

def construct_direct_download_url(file_id):
    """
    Construct a direct download URL from a Google Drive file ID.
    """
    return f'https://drive.google.com/uc?export=download&id={file_id}'

def download_image(download_url, output_path):
    """
    Download the image from the given URL and save it to the output path.
    """
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Image successfully downloaded: {output_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def get_user_by_nic(register, nic):
    """
    Find the user in the register by NIC number.
    """
    for person in register['registered']:
        if person['NIC'] == nic:
            return person
    return None

def clear_download_folder(folder_path):
    """
    Remove all files in the specified folder.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def final_output(user_nic):
    
    # Find the user by NIC
    user = get_user_by_nic(register, user_nic)
    
    if user:
        # Extract the Google Drive link
        id_image_link = user.get('id_image')
        if id_image_link:
            # Extract the file ID and construct the download link
            file_id = extract_file_id(id_image_link)
            download_url = construct_direct_download_url(file_id)
            
            # Clear the download folder
            download_folder = 'download'
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            clear_download_folder(download_folder)
            
            # Download the image
            output_path = os.path.join(download_folder, 'download_image.jpg')
            download_image(download_url, output_path)
        else:
            print("ID image link not found for this user.")
    else:
        print("User not found with the given NIC number.")

