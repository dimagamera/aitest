from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
from rembg import remove

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Перевірте, чи є дані у запиті
        data = request.get_json()
        if 'body' not in data:
            return jsonify({'error': 'No body in request'}), 400

        # Отримання зображення з запиту
        base64_image = data['body']
        image_bytes = base64.b64decode(base64_image)
        input_image = Image.open(BytesIO(image_bytes))
        input_image = input_image.convert("RGBA")

        # Видалення фону
        output_image = remove(input_image)

        # Збереження результату в буфер
        output_buffer = BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        output_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return jsonify({'body': output_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
