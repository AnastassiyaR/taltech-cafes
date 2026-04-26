import os
from flask import Flask
from flask_cors import CORS
from api.routes import api
from web.routes import web


app = Flask(__name__)
app.secret_key = "fallback-only-for-dev"
CORS(app)

app.register_blueprint(api)
app.register_blueprint(web)


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    from flask import jsonify
    return jsonify({"error": str(e.description)}), e.code


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
