from flask import Flask, request, jsonify
from PIL import Image
import google.generativeai as genai
from io import BytesIO
import base64
from flask_cors import CORS 
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app, resources={r"/describe-images": {"origins": "http://localhost:3000"}}) 

genai.configure(api_key=process.env.gemeni_key)
model = genai.GenerativeModel("gemini-2.0-flash")  

@app.route('/describe-images', methods=['POST'])
def describe_images():
    try:
        if 'images' not in request.files:
            return jsonify({"error": "No images provided"}), 400

        images = request.files.getlist('images')
        
        print(images)

        if not images:
            return jsonify({"error": "No valid images were found"}), 400

        image_data = []
        for image in images:
            try:
                img = Image.open(image)
                img = img.convert("RGB") 
                buffered = BytesIO()
                img.save(buffered, format="JPEG") 
                img_str = base64.b64encode(buffered.getvalue()).decode()  
                image_data.append({"mime_type": "image/jpeg", "data": img_str})
            except Exception as e:
                return jsonify({"error": f"Error processing image: {str(e)}"}), 400

        prompt = "Give me a combined description of the following images in a single paragraph. Don't use '**' or any markdown symbols."

        response = model.generate_content([prompt] + image_data)

        if not response.text:
            return jsonify({"error": "Failed to generate description"}), 500

        return jsonify({"description": response.text}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@app.route('/verify-description', methods=['POST'])
@cross_origin(origins="http://localhost:3000") 
def verify_description():
    try:
        if 'image' not in request.files or 'description' not in request.form:
            return jsonify({"error": "No image or description provided"}), 400

        image = request.files['image']
        description = request.form['description']

        try:
            img = Image.open(image)
            img = img.convert("RGB")
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            prompt = f"Check if the image is real and matches the description. Image: {img_str}. Description: {description}. If the description is accurate and the image appears authentic, return 'real', otherwise 'fake'."
            
            response = model.generate_content([prompt])

            if not response.text:
                return jsonify({"error": "Failed to verify description"}), 500

            description_verification_result = "real" if "real" in response.text.lower() else "fake"

            return jsonify({
                "image_verification": "real", 
                "description_verification": description_verification_result
            }), 200

        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)














# import os
# from PIL import Image
# import google.generativeai as genai

# genai.configure(api_key=process.env.gemeni_key)
# # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-2.0-flash") 

# image_path = "c.jpg"

# try:
#     image = Image.open(image_path)
#     response = model.generate_content(
#         [image, "Give me the description of this image. Dont use '**' this type of symbol. only give description in a paragraph."],  
#     )
#     print(response.text)
# except FileNotFoundError:
#     print(f"Error: Image file not found at {image_path}")
# except Exception as e:
#     print(f"An error occurred: {e}")

# import os
# from PIL import Image
# import google.generativeai as genai

# genai.configure(api_key=process.env.gemeni_key)  

# model = genai.GenerativeModel("gemini-2.0-flash")

# image_paths = ["c.jpg", "test.png"] 

# try:
#     images = []
#     for image_path in image_paths:
#         try:
#             image = Image.open(image_path)
#             images.append(image)
#         except FileNotFoundError:
#             print(f"Error: Image file not found at {image_path}")
#             raise 

#     if not images: 
#         raise FileNotFoundError("No valid images were found.")

#     combined_prompt = "Give me a combined description of the following images. Don't use '**' this type of symbol. Only give the description in a single paragraph.\n\n"
#     contents = images + [combined_prompt]

#     response = model.generate_content(contents)
#     print(response.text)

# except FileNotFoundError as e:
#     print(f"An error occurred: {e}")
# except Exception as e:
#     print(f"An error occurred: {e}")
