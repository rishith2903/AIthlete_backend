from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-08-23T00:00:00',
        'models_loaded': {
            'pose_estimation': True,
            'nutrition': True,
            'workout': True,
            'chatbot': True
        }
    })

if __name__ == '__main__':
    # Bind to all interfaces so the backend can reach it at localhost
    app.run(host='0.0.0.0', port=5000)
