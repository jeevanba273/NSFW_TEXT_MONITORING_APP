from flask import Flask, render_template, request, jsonify
import pickle
import logging

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Load models safely
try:
    with open("hatespeech/saved_models/lr_model.pkl", 'rb') as f:
        hate_model = pickle.load(f)
    with open("hatespeech/saved_models/vectorizer.pkl", 'rb') as f:
        hate_vect = pickle.load(f)
    logging.info("Models loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load models: {str(e)}")
    raise FileNotFoundError("Model files not found.")

def ishate(string: str) -> bool:
    string = [string]
    sen_trans = hate_vect.transform(string)
    prediction = hate_model.predict(sen_trans)[0]  # 0 -> normal, 1 -> toxic

    return prediction == 0  # ✅ If 0 (Normal), return False; If 1 (Toxic), return True



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/check_hate', methods=['POST'])
def check_hate():
    if not request.is_json:
        return jsonify({"error": "Invalid content type. Application/json required."}), 400

    try:
        data = request.get_json()
        received_text = data.get('text')

        if received_text:
            result = bool(ishate(received_text))  # ✅ Ensure the result is a Python bool
            return jsonify({"result": result})  # ✅ JSON serialization works
        else:
            return jsonify({"error": "No text received"}), 400
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
