
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    current_units = float(data["current_units"])
    previous_units = float(data["previous_units"])
    bill_amount = float(data["bill_amount"])

    # Calculate consumption difference
    difference = current_units - previous_units

    if previous_units > 0:
        percentage = (difference / previous_units) * 100
    else:
        percentage = 0

    # Simple next bill estimate
    if previous_units > 0:
        estimated_bill = bill_amount * (current_units / previous_units)
    else:
        estimated_bill = bill_amount

    # Telugu explanation
    if difference > 0:
        explanation = (
            f"గత నెలతో పోలిస్తే ఈ నెల విద్యుత్ వినియోగం "
            f"{difference:.0f} యూనిట్లు పెరిగింది."
        )
    elif difference < 0:
        explanation = (
            f"గత నెలతో పోలిస్తే ఈ నెల విద్యుత్ వినియోగం "
            f"{abs(difference):.0f} యూనిట్లు తగ్గింది."
        )
    else:
        explanation = "గత నెలతో పోలిస్తే విద్యుత్ వినియోగం మారలేదు."

    return jsonify({
        "current_units": current_units,
        "previous_units": previous_units,
        "difference": difference,
        "percentage": round(percentage, 2),
        "estimated_bill": round(estimated_bill, 2),
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
