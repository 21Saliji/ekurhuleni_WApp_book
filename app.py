import spacy
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import logging
import requests  # For API calls

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app
)

# Initialize user state and language
user_state = {}
user_language = {}
user_details = {}

# Sample date availability (replace with database in production)
booked_dates = {}  # {'venue_name': ['YYYY-MM-DD', ...]}

# Language options
LANGUAGES = {
    '1': 'English',
    '2': 'IsiZulu',
    '3': 'Sesotho'
}

# Regions and Venues
REGIONS = {
    '1': 'Duduza',
    '2': 'Tsakane',
    '3': 'KwaThema'
}

VENUES = {
    'Duduza': ['Multipurpose Centre', 'Resource Centre', 'Duduza Church Hall'],
    'Tsakane': ['Tsakane Hall', 'Tsakane Sports Ground'],
    'KwaThema': ['KwaThema Hall', 'KwaThema Stadium']
}

# Calendar API integration (placeholder)
CALENDAR_API_URL = "https://example.com/calendar"  # Replace with actual API

# Function to get translated text based on language
def get_translated_text(lang, text):
    translations = {
        'welcome': {
            'English': "Welcome to the Ekurhuleni Smart Bot!",
            'IsiZulu': "Siyakwamukela kuBot ehlakaniphile yase-Ekurhuleni!",
            'Sesotho': "Rea u amohela ho Bot e bohlale ea Ekurhuleni!"
        },
        'choose_language': {
            'English': "Please choose your language:\n1. English\n2. IsiZulu\n3. Sesotho",
            'IsiZulu': "Sicela ukhethe ulimi lwakho:\n1. English\n2. IsiZulu\n3. Sesotho",
            'Sesotho': "Ka kopo khetha puo ea hau:\n1. English\n2. IsiZulu\n3. Sesotho"
        },
        'main_menu': {
            'English': "Main Menu:\n1. Book a Venue\n2. Check Booking Status\n3. Contact Support",
            'IsiZulu': "Imenyu Enkulu:\n1. Bhuka Indawo\n2. Hlola Isimo Sokubhuka\n3. Xhumana Nenkxaso",
            'Sesotho': "Lenane le Leholo:\n1. Booka Sebaka\n2. Hlahloba Boemo ba Booking\n3. Ikopanye le Tšehetso"
        },
        'choose_region': {
            'English': "Please choose a region:\n1. Duduza\n2. Tsakane\n3. KwaThema",
            'IsiZulu': "Sicela ukhethe isifunda:\n1. Duduza\n2. Tsakane\n3. KwaThema",
            'Sesotho': "Ka kopo khetha sebaka:\n1. Duduza\n2. Tsakane\n3. KwaThema"
        },
        'choose_venue': {
            'English': "You have selected {}. Please choose a date (YYYY-MM-DD):\n{}",
            'IsiZulu': "Ukhethe {}. Sicela ukhethe usuku (YYYY-MM-DD):\n{}",
            'Sesotho': "U khethile {}. Ka kopo khetha letsatsi (YYYY-MM-DD):\n{}"
        },
        'ask_details': {
            'English': "Please reply with your:\n1. Name\n2. Address\n3. Contact Number",
            'IsiZulu': "Sicela uphendule nge:\n1. Igama lakho\n2. Ikheli\n3. Inombolo yakho yocingo",
            'Sesotho': "Ka kopo araba ka:\n1. Lebitso la hau\n2. Aterese\n3. Nomoro ea hau ea mohala"
        },
        'confirm_booking': {
            'English': "Thank you, {}! Your booking request has been received. We will get back to you shortly to confirm the booking. Choose payment method:\n1. Pay online\n2. Pay at local municipality\n3. Get EFT details",
            'IsiZulu': "Ngiyabonga, {}! Isicelo sakho sokubhuka samukelwe. Sizokubuyela kuwe maduze ukuqinisekisa ukubhuka. Khetha indlela yokukhokha:\n1. Khokha online\n2. Khokha eMaspala wendawo\n3. Thola imininingwane ye-EFT",
            'Sesotho': "Kea leboha, {}! Kopo ea hau ea ho booka e amohetsoe. Re tla khutlela ho uena haufinyane ho netefatsa booking. Khetha mokhoa oa ho patala:\n1. Patala inthaneteng\n2. Patala ka masepala oa lehae\n3. Fumana lintlha tsa EFT"
        },
        'eft_details': {
            'English': "Please use the following EFT details:\n\nBank: XYZ Bank\nAccount Number: 1234567890\nReference: VENUE_BOOKING",
            'IsiZulu': "Sicela usebenzise imininingwane ye-EFT elandelayo:\n\nIbhange: XYZ Bank\nInombolo ye-akhawunti: 1234567890\nIsalathiso: VENUE_BOOKING",
            'Sesotho': "Ka kopo sebelisa lintlha tse latelang tsa EFT:\n\nBanka: XYZ Bank\nNomoro ea Ak'haonte: 1234567890\nReference: VENUE_BOOKING"
        },
        'payment_method': {
            'English': "Choose payment method:\n1. Pay online\n2. Pay at local municipality\n3. Get EFT details",
            'IsiZulu': "Khetha indlela yokukhokha:\n1. Khokha online\n2. Khokha eMaspala wendawo\n3. Thola imininingwane ye-EFT",
            'Sesotho': "Khetha mokhoa oa ho patala:\n1. Patala inthaneteng\n2. Patala ka masepala oa lehae\n3. Fumana lintlha tsa EFT"
        }
    }
    return translations[text].get(lang, translations[text]['English'])

# Function to check date availability
def is_date_available(venue, date):
    if venue not in booked_dates:
        return True
    return date not in booked_dates[venue]

# Function to analyze user input with spaCy
def analyze_message(message):
    doc = nlp(message)
    return doc

# Function to synchronize with external calendar (example placeholder)
def sync_with_calendar(event_details):
    response = requests.post(CALENDAR_API_URL, json=event_details)
    return response.status_code == 200

@app.route('/webhook', methods=['POST'])
@limiter.limit("10/minute")
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '')
    
    # Create a Twilio response object
    response = MessagingResponse()
    msg = response.message()

    # Retrieve user's state and language
    state = user_state.get(from_number, "start")
    lang = user_language.get(from_number, "English")

    # Process user input based on state
    if state == "start":
        user_state[from_number] = "language_selection"
        msg.body(get_translated_text(lang, 'welcome') + "\n" + get_translated_text(lang, 'choose_language'))
    
    elif state == "language_selection":
        if incoming_msg in LANGUAGES:
            user_language[from_number] = LANGUAGES[incoming_msg]
            user_state[from_number] = "main_menu"
            msg.body(get_translated_text(user_language[from_number], 'main_menu'))
        else:
            msg.body("Invalid selection. " + get_translated_text(lang, 'choose_language'))
    
    elif state == "main_menu":
        if incoming_msg == '1':
            user_state[from_number] = "region_selection"
            msg.body(get_translated_text(lang, 'choose_region'))
        elif incoming_msg == '2':
            msg.body("Booking status feature is under construction. " + get_translated_text(lang, 'main_menu'))
        elif incoming_msg == '3':
            msg.body("Support feature is under construction. " + get_translated_text(lang, 'main_menu'))
        else:
            msg.body("Invalid selection. " + get_translated_text(lang, 'main_menu'))
    
    elif state == "region_selection":
        if incoming_msg in REGIONS:
            selected_region = REGIONS[incoming_msg]
            venue_list = "\n".join([f"{i + 1}. {venue}" for i, venue in enumerate(VENUES[selected_region])])
            user_state[from_number] = "venue_selection"
            msg.body(get_translated_text(lang, 'choose_venue').format(selected_region, venue_list))
        else:
            msg.body(get_translated_text(lang, 'choose_region'))
    
    elif state == "venue_selection":
        selected_region = [key for key, value in REGIONS.items() if value in VENUES][0]
        venue_list = VENUES[REGIONS[selected_region]]
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= len(venue_list):
            selected_venue = venue_list[int(incoming_msg) - 1]
            user_details[from_number] = {'venue': selected_venue}
            user_state[from_number] = "date_selection"
            msg.body("Please enter the date you want to book (YYYY-MM-DD).")
        else:
            msg.body(get_translated_text(lang, 'choose_venue').format(REGIONS[selected_region], "\n".join([f"{i + 1}. {venue}" for i, venue in enumerate(venue_list)])))
    
    elif state == "date_selection":
        selected_venue = user_details[from_number].get('venue')
        if is_date_available(selected_venue, incoming_msg):
            # Add the date to booked dates
            if selected_venue not in booked_dates:
                booked_dates[selected_venue] = []
            booked_dates[selected_venue].append(incoming_msg)

            # Prepare event details for calendar synchronization
            event_details = {
                'venue': selected_venue,
                'date': incoming_msg,
                'name': user_details[from_number].get('name'),
                'address': user_details[from_number].get('address'),
                'contact': user_details[from_number].get('contact')
            }
            if sync_with_calendar(event_details):
                user_state[from_number] = "details_collection"
                msg.body(get_translated_text(lang, 'ask_details'))
            else:
                msg.body("Unable to synchronize with the calendar. Please try again.")
        else:
            msg.body("The selected date is not available. Please choose another date.")
    
    elif state == "details_collection":
        if 'name' not in user_details[from_number]:
            user_details[from_number]['name'] = incoming_msg
            msg.body(get_translated_text(lang, 'ask_details'))
        elif 'address' not in user_details[from_number]:
            user_details[from_number]['address'] = incoming_msg
            msg.body(get_translated_text(lang, 'ask_details'))
        elif 'contact' not in user_details[from_number]:
            user_details[from_number]['contact'] = incoming_msg
            msg.body(get_translated_text(lang, 'confirm_booking').format(user_details[from_number]['name']))
            user_state[from_number] = "confirm_booking"
        else:
            msg.body(get_translated_text(lang, 'ask_details'))
    
    elif state == "confirm_booking":
        if incoming_msg in ['yes', 'no']:
            if incoming_msg == 'yes':
                msg.body(get_translated_text(lang, 'payment_method'))
                user_state[from_number] = "payment_method"
            else:
                user_state[from_number] = "start"
                msg.body(get_translated_text(lang, 'welcome') + "\n" + get_translated_text(lang, 'choose_language'))
        else:
            msg.body("Please reply with 'Yes' or 'No'.")
    
    elif state == "payment_method":
        if incoming_msg == '1':
            msg.body("Please proceed to our online payment portal.")
            user_state[from_number] = "start"
        elif incoming_msg == '2':
            msg.body("Please pay at your local municipality office.")
            user_state[from_number] = "start"
        elif incoming_msg == '3':
            msg.body(get_translated_text(lang, 'eft_details'))
            user_state[from_number] = "start"
        else:
            msg.body(get_translated_text(lang, 'payment_method'))
    
    return str(response)

@app.errorhandler(429)
def ratelimit_error(e):
    return "Too many requests. Please try again later.", 429

if __name__ == "__main__":
    app.run(debug=True)
