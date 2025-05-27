from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import csv
import tempfile
import shutil
from zipfile import ZipFile
from moviepy.editor import *
import qrcode

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return "YouTube Shorts Backend is Live!"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        # Create temp workspace
        workspace = tempfile.mkdtemp()
        output_dir = os.path.join(workspace, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Get uploaded files
        csv_file = request.files.get("csv")
        logo_file = request.files.get("logo")
        product_image_file = request.files.get("product")
        audio_file = request.files.get("audio")

        # Save inputs
        csv_path = os.path.join(workspace, "input.csv")
        logo_path = os.path.join(workspace, "logo.png")
        product_path = os.path.join(workspace, "product.png")
        audio_path = os.path.join(workspace, "music.mp3")

        csv_file.save(csv_path)
        logo_file.save(logo_path)
        product_image_file.save(product_path)
        audio_file.save(audio_path)

        # Process CSV
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                part = row.get("Part", f"Item {i}")
                price = row.get("Price", "$0.00")
                url = row.get("URL", "https://www.example.com")

                # Make QR code
                qr = qrcode.make(url)
                qr_path = os.path.join(workspace, f"qr_{i}.png")
                qr.save(qr_path)

                # Create video clip with product image
                product_clip = ImageClip(product_path).set_duration(10).resize(height=720).set_position("center")
                logo_clip = ImageClip(logo_path).set_duration(10).resize(height=100).set_position(("left", "top"))
                qr_clip = ImageClip(qr_path).set_duration(10).resize(height=120).set_position(("right", "bottom"))

                txt_clip = TextClip(f"{part} - {price}", fontsize=40, color='white', font='Arial-Bold').set_duration(10).set_position("bottom")

                final = CompositeVideoClip([product_clip, logo_clip, qr_clip, txt_clip])

                # Add audio
                audio_bg = AudioFileClip(audio_path).subclip(0, min(10, final.duration))
                final = final.set_audio(audio_bg)

                # Export video
                video_path = os.path.join(output_dir, f"short_{i+1}.mp4")
                final.write_videofile(video_path, fps=24)

        # Zip it
        zip_filename = os.path.join(workspace, "shorts.zip")
        with ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, arcname=file)

        return send_file(zip_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Required by Render to bind to the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
