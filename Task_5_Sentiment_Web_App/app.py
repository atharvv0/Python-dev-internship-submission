from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)


def classify_sentiment(polarity: float) -> str:
    """Map TextBlob polarity to a simple three-class label."""
    if polarity > 0.05:
        return "Positive"
    if polarity < -0.05:
        return "Negative"
    return "Neutral"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    text = ""
    error = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            error = "Please enter some text for analysis."
        else:
            blob = TextBlob(text)
            polarity = float(blob.sentiment.polarity)
            subjectivity = float(blob.sentiment.subjectivity)
            result = {
                "label": classify_sentiment(polarity),
                "polarity": polarity,
                "subjectivity": subjectivity,
            }

    return render_template("index.html", result=result, text=text, error=error)


@app.get("/health")
def health():
    return {"status": "ok", "service": "sentiment-analysis"}


if __name__ == "__main__":
    app.run(debug=True)
