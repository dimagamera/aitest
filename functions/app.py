import io
import logging
from PIL import Image
from rembg import remove
import base64

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handler(event, context):
    try:
        # Отримання зображення з запиту
        base64_image = event['body']
        image_bytes = base64.b64decode(base64_image)
        input_image = Image.open(io.BytesIO(image_bytes))
        input_image = input_image.convert("RGBA")

        # Видалення фону
        output_image = remove(input_image)

        # Збереження результату в буфер
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return {
            'statusCode': 200,
            'body': output_base64,
            'isBase64Encoded': True,
            'headers': {
                'Content-Type': 'image/png'
            }
        }
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return {
            'statusCode': 500,
            'body': str(e)
        }
