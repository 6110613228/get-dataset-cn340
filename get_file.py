import os
import io
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
base_dir = 'credential'
token_file = os.path.join(base_dir, 'token.json')

output_dir = 'dataset'

def main():

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(base_dir, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credential/token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)

    data = pd.read_csv('Data Collection CN340 1_64 (Responses) - Data Collection.csv')

    for i, row in data.iterrows():
        out_dir = os.path.join(output_dir, str(row['รหัสนักศึกษา']))
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        with open(os.path.join(out_dir, 'info.txt'), 'w') as f:
            f.write(str(row['รหัสนักศึกษา']) + '\n')
            f.write(row['ชื่อ(ไทย)'] + '\n')
            f.write(row['นามสกุล(ไทย)'] + '\n')
            f.write(row['ชื่อเล่น(ไทย)'] + '\n')
            f.close()
        
        face_only_dir = os.path.join(out_dir, 'face_only')
        if not os.path.exists(face_only_dir):
            os.mkdir(face_only_dir)
        face_only_fileId = row['upload your file'].split('id=')[1]
        request = drive_service.files().get_media(fileId=face_only_fileId)
        fh = io.FileIO(face_only_dir + '/' + str(row['รหัสนักศึกษา']) + '-face.mp4', 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %s %d%%." % (face_only_dir + '/' + str(row['รหัสนักศึกษา']), int(status.progress() * 100)))
        
        face_id_dir = os.path.join(out_dir, 'face_id')
        if not os.path.exists(face_id_dir):
            os.mkdir(face_id_dir)
        face_id_fileId = row['upload your file.1'].split('id=')[1]
        request = drive_service.files().get_media(fileId=face_id_fileId)
        fh = io.FileIO(face_id_dir + '/' + str(row['รหัสนักศึกษา']) + '-face_id.mp4', 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %s %d%%." % (face_id_dir + '/' + str(row['รหัสนักศึกษา']), int(status.progress() * 100)))
        
        id_only_dir = os.path.join(out_dir, 'id_only')
        if not os.path.exists(id_only_dir):
            os.mkdir(id_only_dir)
        id_only_fileId = row['upload your image'].split('id=')[1]
        request = drive_service.files().get_media(fileId=id_only_fileId)
        fh = io.FileIO(id_only_dir + '/' + str(row['รหัสนักศึกษา']) + '-id.jpeg', 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %s %d%%." % (id_only_dir + '/' + str(row['รหัสนักศึกษา']), int(status.progress() * 100)))

if __name__ == "__main__":
    main()
    print('Finished!')