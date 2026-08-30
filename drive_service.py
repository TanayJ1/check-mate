from classroom_service import get_classroom_service

from googleapiclient.discovery import build


def get_drive_service():

    classroom_service = get_classroom_service()

    credentials = classroom_service._http.credentials

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return service

def get_file(file_id):

    service = get_drive_service()

    file = service.files().get(
        fileId=file_id,
        fields="id,name,mimeType,size"
    ).execute()

    return file

from googleapiclient.http import MediaIoBaseDownload

import io


def download_file(file_id, output_path):

    service = get_drive_service()

    request = service.files().get_media(
        fileId=file_id
    )

    with open(
        output_path,
        "wb"
    ) as file:

        downloader = MediaIoBaseDownload(
            file,
            request
        )

        done = False

        while not done:

            status, done = downloader.next_chunk()

            if status:

                print(
                    f"Download: "
                    f"{int(status.progress() * 100)}%"
                )