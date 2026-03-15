import os
from flask import Flask, render_template_string
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = os.environ.get("BUCKET_NAME", "bucket_gem_challenge")
FILE_NAME = "GeminiChallenge.tsx"

@app.route('/')
def index():
    try:

        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_NAME)
        

        code_content = blob.download_as_text()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>UI Navigator</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background-color: #1a1a1a; color: white; padding: 40px; }
                .container { max-width: 900px; margin: auto; border-top: 5px solid #EC111A; background: #2d2d2d; padding: 20px; border-radius: 8px; }
                h1 { color: #EC111A; }
                pre { background: #000; padding: 15px; border-radius: 5px; overflow-x: auto; color: #00ff00; font-family: 'Consolas', monospace; }
                .status { font-size: 0.9em; color: #aaa; margin-bottom: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>UI Navigator - Latest Build</h1>
                <p class="status">Source: Google Cloud Storage | File: {{ filename }}</p>
                <hr>
                <h3>Generated React Native Code:</h3>
                <pre>{{ code }}</pre>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, code=code_content, filename=FILE_NAME)
    except Exception as e:
        return f"Error loading build: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))