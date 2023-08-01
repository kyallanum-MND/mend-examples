import requests
import json
import sys
import os

# Purpose: Close all open pending tasks in an organization
# Requirements:
#   Environment Variables:
#       MEND_URL
#       WS_APIKEY
#       MEND_USER_KEY


REQUEST_HEADERS = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
}

def get_result_from_api_response(response: dict, object_to_get: str) -> list:
    return_object = []
    if object_to_get in response:
        return_object = response[object_to_get]

    return return_object

def check_api_error(response: dict):
    if "errorCode" in response:
        print(f"Error Running Request: {json.dumps(response, indent=4)}")
        sys.exit(-1)

def send_api_1_4_request(base_url: str, request: dict) -> dict:
    payload = json.dumps(request)

    if "/api" not in base_url:
        base_url = f"{base_url}/api/v1.4"

    response = requests.post(base_url, headers=REQUEST_HEADERS, data=payload)
    response_object = response.json()

    return response_object


def create_get_domain_pending_tasks_request(org_token: str, user_key: str):
    request_object = {
        "requestType": "getDomainPendingTasks",
        "orgToken": org_token,
        "userKey": user_key,
    }

    return request_object

def create_close_pending_task_request(org_token: str, user_key: str, task_uuid: str) -> dict:
    request_object = {
        "requestType": "closePendingTask",
        "orgToken": org_token,
        "userKey": user_key,
        "taskUUID": task_uuid
    }

    return request_object

def main():
    mend_url = os.getenv("MEND_URL")
    mend_user_key = os.getenv("MEND_USER_KEY")
    mend_orgtoken = os.getenv("WS_APIKEY")

    print("Getting all pending tasks from an organization")
    get_pending_task_request = create_get_domain_pending_tasks_request(mend_orgtoken, mend_user_key)
    get_pending_task_response_object = send_api_1_4_request(mend_url, get_pending_task_request)
    check_api_error(get_pending_task_response_object)
    pending_task_info = get_result_from_api_response(get_pending_task_response_object, "pendingTaskInfos")

    for pending_task in pending_task_info:
        print(f"Closing Pending Task for artifact: {pending_task['artifact']}... ", end="")
        close_pending_task_request = create_close_pending_task_request(mend_orgtoken, mend_user_key, pending_task["uuid"])
        close_pending_task_response_object = send_api_1_4_request(mend_url, close_pending_task_request)
        check_api_error(close_pending_task_response_object)
        print("Closed")

    print("All requests closed")

if __name__ == "__main__":
    main()