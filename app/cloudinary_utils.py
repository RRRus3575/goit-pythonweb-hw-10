import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

load_dotenv()

# Проверка переменных
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    raise ValueError("❌ Cloudinary API credentials не заданы в .env")

# Настройка Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# Загрузка изображения
def upload_image(image_url, public_id):
    upload_result = cloudinary.uploader.upload(image_url, public_id=public_id)
    return upload_result["secure_url"]

