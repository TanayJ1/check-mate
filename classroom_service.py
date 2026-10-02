from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build

import os
import pickle


SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def _secret_path(name):
    path = f"/etc/secrets/{name}"
    return path if os.path.exists(path) else name

def get_classroom_service():
    creds = Credentials.from_authorized_user_file(
        _secret_path("token.json"), SCOPES
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("classroom", "v1", credentials=creds)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build(
        "classroom",
        "v1",
        credentials=creds
    )

    return service


def get_courses():

    service = get_classroom_service()

    response = service.courses().list(
        pageSize=100
    ).execute()

    return response.get(
        "courses",
        []
    )


def get_coursework(course_id):

    service = get_classroom_service()

    response = (
        service
        .courses()
        .courseWork()
        .list(
            courseId=course_id,
            pageSize=100
        )
        .execute()
    )

    return response.get(
        "courseWork",
        []
    )


def get_submissions(
    course_id,
    coursework_id
):

    service = get_classroom_service()

    response = (
        service
        .courses()
        .courseWork()
        .studentSubmissions()
        .list(
            courseId=course_id,
            courseWorkId=coursework_id,
            pageSize=100
        )
        .execute()
    )

    return response.get(
        "studentSubmissions",
        []
    )

def get_student_name(
    course_id,
    user_id
):

    service = get_classroom_service()

    student = (
        service
        .courses()
        .students()
        .get(
            courseId=course_id,
            userId=user_id
        )
        .execute()
    )

    profile = student.get(
        "profile",
        {}
    )

    name = profile.get(
        "name",
        {}
    )

    return name.get(
        "fullName",
        "Unknown Student"
    )

if __name__ == "__main__":

    courses = get_courses()

    if not courses:
        print("No courses found.")
    
    else:
        for course in courses:

            course_id = course.get("id")
            course_name = course.get("name")

            print("\n==============================")
            print("COURSE")
            print("Name:", course_name)
            print("Course ID:", course_id)

            coursework = get_coursework(course_id)

            if not coursework:
                print("No assignments found.")

            else:
                for assignment in coursework:

                    assignment_id = assignment.get("id")
                    assignment_title = assignment.get("title")

                    print(
                        "   Assignment:",
                        assignment_title
                    )

                    print(
                        "   Assignment ID:",
                        assignment_id
                    )