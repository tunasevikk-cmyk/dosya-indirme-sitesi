from flask import Flask, request, render_template, send_from_directory, url_for
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")  # Çoklu dosya al
        links = []

        for file in uploaded_files:
            if file:
                filename = f"{uuid.uuid4().hex}_{file.filename}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                download_link = url_for('download_file', filename=filename, _external=True)
                links.append(download_link)

        return render_template("result.html", links=links)

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)