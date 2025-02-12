import sys
from PIL import Image
import ollama

def generate_text(instruction, file_path):
    try:
        # Generate text response
        result = ollama.generate(
            model='llava:latest',
            prompt=instruction,
            images=[file_path],
            stream=False
        ).get('response', '')

        # Resize and display the image
        img = Image.open(file_path)
        img = img.resize(tuple(int(i / 1.2) for i in img.size))

        # Print result efficiently
        sys.stdout.write(result.replace('.', ''))
        sys.stdout.flush()
    
    except Exception as e:
        print(f"Error: {e}")

instruction = "Give me the description of this image"
file_path = './test.png'
generate_text(instruction, file_path)
