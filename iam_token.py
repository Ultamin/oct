import json
import time
import requests
from config import Config

class IAMToken:
    """Класс для работы с IAM токеном Yandex Cloud"""
    
    def __init__(self):
        self._token = None
        self._expires_at = 0
    
    def get_token(self) -> str:
        """Получение валидного IAM токена"""
        if self._token and time.time() < self._expires_at:
            return self._token
        
        # Если токен указан вручную в .env
        if Config.IAM_TOKEN:
            self._token = Config.IAM_TOKEN
            self._expires_at = time.time() + 3600  # Предполагаем, что срок действия 1 час
            return self._token
        
        # Получаем новый токен через OAuth токен
        if not Config.YANDEX_OAUTH_TOKEN:
            raise ValueError("YANDEX_OAUTH_TOKEN не установлен для получения IAM токена")
        
        return self._request_new_token()
    
    def _request_new_token(self) -> str:
        """Запрос нового IAM токена"""
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "yandexPassportOauthToken": Config.YANDEX_OAUTH_TOKEN
            }
            
            response = requests.post(
                Config.IAM_TOKEN_URL,
                headers=headers,
                json=data,
                timeout=10
            )
            
            response.raise_for_status()
            
            token_data = response.json()
            self._token = token_data.get("iamToken")
            self._expires_at = time.time() + float(token_data.get("expiresAt", 0))
            
            if not self._token:
                raise ValueError("IAM токен не получен в ответе")
            
            print(f"IAM токен получен, действителен до: {token_data.get('expiresAt')}")
            return self._token
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка получения IAM токена: {str(e)}")

# Создаем глобальный экземпляр
iam_token = IAMToken()
