import os
import uuid
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
def upload_avatar(image_file, public_id=None):
    if not public_id:
        public_id = str(uuid.uuid4())  # Генерируем уникальный ID
    try:
        upload_result = cloudinary.uploader.upload(image_file, public_id=f"avatars/{public_id}", overwrite=True)
        return upload_result["secure_url"]
    except Exception as e:
        print(f"❌ Ошибка загрузки изображения: {e}")
        raise ValueError("Ошибка при загрузке изображения.")



