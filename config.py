import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Yandex Cloud
    FOLDER_ID = os.getenv('YANDEX_CLOUD_FOLDER_ID')
    YANDEX_OAUTH_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')
    IAM_TOKEN = os.getenv('IAM_TOKEN')
    
    # Настройки
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5242880))  # 5MB
    SUPPORTED_FORMATS = os.getenv('SUPPORTED_FORMATS', 'jpg,jpeg,png').split(',')
    
    # Vision API
    VISION_API_URL = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"
    
    # IAM токен
    IAM_TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    
    @classmethod
    def validate(cls):
        """Проверка конфигурации"""
        errors = []
        
        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN не установлен")
        
        if not cls.FOLDER_ID:
            errors.append("YANDEX_CLOUD_FOLDER_ID не установлен")
        
        if not cls.YANDEX_OAUTH_TOKEN and not cls.IAM_TOKEN:
            errors.append("Необходим YANDEX_OAUTH_TOKEN или IAM_TOKEN")
        
        if errors:
            raise ValueError(f"Ошибки конфигурации:\n" + "\n".join(errors))
