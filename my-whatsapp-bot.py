import requests

# Define some constants for the hall options
HALL_OPTIONS = {
    "1": "Eastern Region",
    "2": "Northern Region",
    "3": "Southern Region",
}

# Define supported languages
LANGUAGES = {
    "en": "eng_Latn",
    "zu": "zul_Latn"
}

# Store user language preferences
user_languages = {}

# Endpoint URL for Vulavula API
VULAVULA_API_URL = 'https://vulavula-services.lelapa.ai/api/v1/translate/process'
VULAVULA_API_KEY = 'your_actual_client_token_here'  # Replace with your actual client token

def translate_text(text, target_language):
    headers = {
        'Content-Type': 'application/json',
        'X-CLIENT-TOKEN': VULAVULA_API_KEY
    }
    data = {
        "input_text": text,
        "source_lang": "eng_Latn",
        "target_lang": LANGUAGES.get(target_language, "eng_Latn")  # Default to English if language not found
    }
    try:
        response = requests.post(VULAVULA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('translated_text', text)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.text)  # Print response content for more details
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return text

def handle_message(incoming_msg, user_phone):
    global user_languages
    response = ""

    # Handle language selection
    if 'hi' in incoming_msg or 'hello' in incoming_msg:
        user_languages[user_phone] = 'en'  # Default to English
        response = "Welcome to the City of Ekurhuleni Venue Booking Bot!\n\n" \
                   "Please choose a language to continue:\n" \
                   "1. English\n" \
                   "2. isiZulu\n" \
                   "Reply with the number corresponding to your choice."
    
    elif incoming_msg in ['1', '2']:
        language_code = 'en' if incoming_msg == '1' else 'zu'
        user_languages[user_phone] = language_code
        response = translate_text(
            "You have selected a language. Please choose an option from the menu below:\n"
            "1. Book in Eastern Region \n"
            "2. Book in Northern Region \n"
            "3. Book in Southern Region \n"
            "Reply with the number corresponding to your choice.",
            language_code
        )

    elif incoming_msg in HALL_OPTIONS:
        hall_name = HALL_OPTIONS[incoming_msg]
        lang = user_languages.get(user_phone, 'en')
        response = translate_text(
            f"You have selected {hall_name}.\n\n"
            "Please reply with your name and contact number to complete the booking.",
            lang
        )

    elif 'name' in incoming_msg and 'contact' in incoming_msg:
        lang = user_languages.get(user_phone, 'en')
        response = translate_text(
            "Thank you! Your booking request has been received.\n"
            "We will get back to you shortly to confirm the booking.\n\n"
            "If you have any other queries, please reply here.",
            lang
        )

    else:
        lang = user_languages.get(user_phone, 'en')
        response = translate_text(
            "Sorry, I didn't understand that. Please reply with 'Hi' to see the menu options.",
            lang
        )

    return response

# Example usage with a loop for user input
if __name__ == "__main__":
    print("Starting the bot. Type 'exit' to end the program.")
    
    while True:
        # Read incoming message from the user
        incoming_message = input("Enter your message: ").strip().lower()
        
        if incoming_message == 'exit':
            print("Exiting the bot. Goodbye!")
            break
        
        # Simulate user phone number for this session
        user_phone = "+1234567890"  # Replace with an actual phone number if needed

        # Handle the incoming message
        response = handle_message(incoming_message, user_phone)
        print(f"Response: {response}")
        print("-" * 40)
