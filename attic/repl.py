# pip install flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    filename = data.get("filename", "")
    input_text = data.get("input", "")

    # Simulate processing based on inputs
    output = f"Received filename '{filename}' and input '{input_text}'"
    probe_a = f"Probe A processed '{filename}'"
    probe_b = f"Probe B analyzed '{input_text}'"
    probe_c = f"Probe C ran diagnostics on '{filename}'"
    errors = "" if filename and input_text else "Please provide both filename and input."

    return jsonify({
        "output": output,
        "probeA": probe_a,
        "probeB": probe_b,
        "probeC": probe_c,
        "errors": errors
    })

if __name__ == '__main__':
    app.run(debug=True)
