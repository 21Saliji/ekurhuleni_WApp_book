import requests

# Endpoint URL
url = 'https://vulavula-services.lelapa.ai/api/v1/translate/process'

# Replace '<INSERT_TOKEN>' with your actual client token
headers = {
    'Content-Type': 'application/json',
    'X-CLIENT-TOKEN': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQxZDkwNTU4YTg2NjQwOGNiMzM1MzQ5ZTk2MjM4MjEyIiwiY2xpZW50X2lkIjoxNTYsInJlcXVlc3RzX3Blcl9taW51dGUiOjAsImxhc3RfcmVxdWVzdF90aW1lIjpudWxsfQ.z2nJX2BJeRF5hpUPd7yRHiGBhStNypck46aMB-2JHtk'  # Your actual client token here
}

# Request body
data = {
    "input_text": "Hello, how are you?",
    "source_lang": "eng_Latn",  # English
    "target_lang": "zul_Latn"   # isiZulu
}

def translate_text():
    try:
        # Sending POST request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Printing response
        translation_result = response.json()
        return translation_result
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return None

# Example usage
translated_text = translate_text()
if translated_text:
    print(f"Translated Text: {translated_text}")
