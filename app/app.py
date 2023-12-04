from flask import Flask, request, jsonify, render_template
from services import convert_to_pdf_service

app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    return jsonify(
        status = 'UP'
    )

@app.route("/convert", methods=['POST'])
def convert():
    try:
        data = request.get_json(silent=True)
        filename, output_base64 = convert_to_pdf_service(data)
        return jsonify(
            status = 'Success',
            message = 'Converted to PDF',
            filename = filename,
            output_base64 = output_base64
        )
    except Exception as e:
            return jsonify(
                status = 'Error',
                message = str(e)
            ) , 400

# @app.route('/answer', methods=['POST'])
# async def answer():
#     if request.method == 'POST':
#         try:
#             data = request.get_json(silent=True)
#             message_id = data['message_id'] if 'message_id' in data else None
#             await send_answer(data['bot_token'], data['chat_id'], message_id, data['response_text'])
#             return jsonify(
#                 status = 'Success',
#                 message = 'Send answer',
#             ) , 200
#         except Exception as e:
#             return jsonify(
#                 status = 'Error',
#                 message = str(e)
#             ) , 400

if __name__ == "__main__":
    print('Run service...')
    app.run(host='0.0.0.0', port=5000, debug=True)