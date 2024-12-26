from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/play_sound', methods=['POST'])
def play_sound():
    data = request.get_json()
    intent_name = data["request"]["intent"]["name"]

    if intent_name == "PlayDoorSoundIntent":
        # Lógica para reproducir el sonido
        print("Reproduciendo sonido de la puerta.")
        response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Reproduciendo el sonido de la puerta."
                },
                "shouldEndSession": True
            }
        }
        return jsonify(response)

    return jsonify({"error": "Intento desconocido"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
