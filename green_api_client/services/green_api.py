import logging
import requests

logger = logging.getLogger(__name__)

class GreenAPIService:
    BASE_URL = "https://api.green-api.com/waInstance{idInstance}/{method}/{apiTokenInstance}"

    @classmethod
    def call_api(cls, method, id_instance, api_token, payload=None, http_method="GET"):
        url = cls.BASE_URL.format(idInstance=id_instance, method=method, apiTokenInstance=api_token)
        headers = {}
        if payload is not None:
            headers['Content-Type'] = 'application/json'
            
        try:
            if http_method == "GET":
                response = requests.get(url, timeout=15)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            logger.error(f"Green API Error ({method}): {e}")
            error_data = {"error": str(e)}
            if hasattr(e, 'response') and getattr(e, 'response', None) is not None:
                try:
                    error_data["details"] = e.response.json()
                except ValueError:
                    error_data["details"] = e.response.text
            return error_data, str(e)

    @classmethod
    def get_settings(cls, id_instance, api_token):
        return cls.call_api("getSettings", id_instance, api_token, http_method="GET")

    @classmethod
    def get_state_instance(cls, id_instance, api_token):
        return cls.call_api("getStateInstance", id_instance, api_token, http_method="GET")

    @classmethod
    def send_message(cls, id_instance, api_token, chat_id, message):
        payload = {"chatId": chat_id, "message": message}
        return cls.call_api("sendMessage", id_instance, api_token, payload=payload, http_method="POST")

    @classmethod
    def send_file_by_url(cls, id_instance, api_token, chat_id, url_file, file_name=None):
        if not file_name:
            file_name = url_file.split('/')[-1] if '/' in url_file else 'file'
        payload = {"chatId": chat_id, "urlFile": url_file, "fileName": file_name}
        return cls.call_api("sendFileByUrl", id_instance, api_token, payload=payload, http_method="POST")
