import os
import torch
from PIL import Image
from googletrans import Translator
from transformers import BlipProcessor, BlipForConditionalGeneration


current_folder = os.path.dirname(os.path.abspath(__file__))

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base").to(device)

translator = Translator()


def get_image_paths(folder):
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

    return [
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith(valid_extensions)
    ]


def generate_caption(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_length=50)

    return processor.decode(out[0], skip_special_tokens=True)


def translate_text(text, dest_language="ru"):
    try:
        return translator.translate(text, dest=dest_language).text

    except Exception as e:
        print(f"Ошибка перевода: {e}")

        return text


def rename_images(folder):
    image_paths = get_image_paths(folder)

    for i, image_path in enumerate(image_paths):
        try:
            caption = generate_caption(image_path)
            translated_caption = translate_text(caption)
            new_filename = f"{translated_caption}.jpg"

            new_path = os.path.join(folder, new_filename)

            # Если имя уже существует, добавляем индекс
            counter = 1

            while os.path.exists(new_path):
                new_filename = f"{translated_caption} ({counter}).jpg"
                new_path = os.path.join(folder, new_filename)
                counter += 1

            os.rename(image_path, new_path)
            print(f"{os.path.basename(image_path)} → {new_filename}")

        except Exception as e:
            print(f"Ошибка обработки {image_path}: {e}")


rename_images(current_folder)
