import html

from flask import Flask, request, jsonify
import spacy
from flask_cors import CORS

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
CORS(app)


@app.route("/process-text", methods=["POST"])
def process_text():
    text = request.json["text"]
    doc = nlp(text)

    tags = set()
    highlighted_text = text

    if "NE" in request.json:
        for ent in doc.ents:
            tags.add(ent.label_)
            html_entity = f"<{ent.label_}>{html.escape(ent.text)}</{ent.label_}>"
            highlighted_text = highlighted_text.replace(ent.text, html_entity)

    if "POS" in request.json:
        for token in doc:
            tags.add(token.pos_)
            if token.pos_:
                html_token = f"<{token.pos_}>{html.escape(token.text)}</{token.pos_}>"
                highlighted_text = highlighted_text.replace(token.text, html_token)

    print(highlighted_text)
    return jsonify({"tags": list(tags), "highlightedText": highlighted_text})


if __name__ == "__main__":
    app.run()
