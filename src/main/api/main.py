from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from io import BytesIO
from separater import Separater
import os


app = Flask(__name__, static_folder=None)
CORS(app)

separater = Separater()


@app.route('/api/ready', methods=['GET'])
def ready():
    status = separater.load_model(
        path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/model.th')
    )
    if status is True:
        return jsonify({"status": "ok", "code": 200, "message": "ok"})
    else:
        return jsonify({"status": "error", "code": 500, "message": "some error occured."})


@app.route('/api/separate', methods=['POST'])
def separate():

    if separater.model is None:
        return jsonify({"status": "error", "code": 500, "message": "some error occured."})

    request_audio_buffer = BytesIO(request.files["file"].stream.read())
    source_zip_buffer = separater(request_audio_buffer)

    res = make_response(source_zip_buffer.getvalue())
    source_zip_buffer.close()

    res.headers['Content-Type'] = 'application/zip'
    res.headers['Content-Disposition'] = 'attachment; filename=sounds.zip'
    return res


if __name__ == "__main__":
    app.run(debug=True, port=3001)
