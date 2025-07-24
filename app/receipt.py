import io
import pandas as pd
from PIL import Image
import json
from datetime import datetime

def process_image(gemini_model, image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        prompt = '''Extract the store name, store address, receipt date, receipt time, item details (item name, quantity, price and total), receipt subtotal, 
        taxes details (tax name, percent, amount) and receipt total from this receipt image.
        Provide the output as a JSON object with eight keys: "store_name", "store_address", "date", "time", "items", "subtotal", "taxes" and "total".
        The value of "date" should be the date of the receipt in DD-MM-YYYY format.
        The value of "time" should be the time of the receipt in HH-MM-SS format (in 24 hours format).
        The value of "items" should be a list of JSON objects, where each object represents an item and has the keys "item_name", "quantity", "price", and "total".
        The value of "taxes" should be a list of JSON objects, where each object represents a tax and has the keys "tax_name", "percent", and "amount".
        For example:
        {
          "store_name": "Lucky Karyana Store",
          "store_address": "Model Town, Ludhiana",
          "date": "27-10-2023",
          "time": "15:20:22",
          "items": [
            {
              "item_name": "Example Item",
              "quantity": 1,
              "price": 10.00,
              "total": 10.00
            }
          ],
          "subtotal": 117.00,
          "taxes": [
            {
              "tax_name": "GST",
              "percent": 8.375,
              "amount": 20.00,
            }
          ],
          "total": 137.00
        }
        Do not include any other text or formatting in the response, only the JSON object.
        '''
        response = gemini_model.generate_content([prompt, image])

        extracted_data = None
        if response.text:
            json_start = response.text.find("```json")
            json_end = response.text.rfind("```")

            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_string = response.text[json_start + len("```json"):json_end].strip()
                try:
                    extracted_data = json.loads(json_string)
                    print("JSON loaded successfully.")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
                    print("String that caused the error:")
                    print(json_string)
            else:
                print("Could not find JSON block within ```json and ``` markers.")
        else:
            print("Received empty response from Gemini API. Data not saved.")
        return extracted_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    