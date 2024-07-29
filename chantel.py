import spacy
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import datetime
from quickstart import initialize_google_calendar, create_event  # Import the create_event function

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize Limiter with get_remote_address as key function
limiter = Limiter(
    get_remote_address,
    app=app
)

# Initialize user state and language
user_state = {}
user_language = {}
user_details = {}

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
            'English': "You have selected {}. Please choose a venue:\n{}",
            'IsiZulu': "Ukhethe {}. Sicela ukhethe indawo:\n{}",
            'Sesotho': "Ukhethile {}. Ka kopo khetha sebaka:\n{}"
        },
        'ask_details': {
            'English': "Please reply with your:\n1. Name\n2. Address\n3. Contact Number",
            'IsiZulu': "Sicela uphendule nge:\n1. Igama lakho\n2. Ikheli\n3. Inombolo yakho yocingo",
            'Sesotho': "Ka kopo araba ka:\n1. Lebitso la hau\n2. Aterese\n3. Nomoro ea hau ea mohala"
        },
        'ask_date': {
            'English': "Please provide the booking date in YYYY-MM-DD format.",
            'IsiZulu': "Sicela unikeze usuku lokubhuka ngefomethi ethi YYYY-MM-DD.",
            'Sesotho': "Ka kopo fana ka letsatsi la ho booka ka mokhoa oa YYYY-MM-DD."
        },
        'invalid_date': {
            'English': "Invalid date format or date in the past. Please provide a future date in YYYY-MM-DD format.",
            'IsiZulu': "Ifomethi yosuku engalungile noma usuku lwedlule. Sicela unikeze usuku lwesikhathi esizayo ngefomethi ethi YYYY-MM-DD.",
            'Sesotho': "Mokhoa oa letsatsi o fosahetseng kapa letsatsi le fetileng. Ka kopo fana ka letsatsi la kamoso ka mokhoa oa YYYY-MM-DD."
        },
        'confirm_booking': {
            'English': "Thank you, {}! Your booking request for {} at {} on {} has been confirmed. Please proceed to payment options.",
            'IsiZulu': "Ngiyabonga, {}! Isicelo sakho sokubhuka sika-{} e-{} ngomhla ka-{} siqinisekisiwe. Sicela uqhubekele kuzinketho zokukhokha.",
            'Sesotho': "Kea leboha, {}! Kopo ea hau ea ho booka bakeng sa {} ho {} ka {} e netefalitsoe. Ka kopo tsoela pele ho khetho ea tefo."
        },
        'payment_method': {
            'English': "Choose payment method:\n1. Pay online\n2. Pay at local municipality\n3. Get EFT details",
            'IsiZulu': "Khetha indlela yokukhokha:\n1. Khokha online\n2. Khokha eMaspala wendawo\n3. Thola imininingwane ye-EFT",
            'Sesotho': "Khetha mokhoa oa ho patala:\n1. Patala inthaneteng\n2. Patala ka masepala oa lehae\n3. Fumana lintlha tsa EFT"
        },
        'eft_details': {
            'English': "Please use the following EFT details:\n\nBank: XYZ Bank\nAccount Number: 1234567890\nReference: VENUE_BOOKING",
            'IsiZulu': "Sicela usebenzise imininingwane ye-EFT elandelayo:\n\nIbhange: XYZ Bank\nInombolo ye-akhawunti: 1234567890\nIsalathiso: VENUE_BOOKING",
            'Sesotho': "Ka kopo sebelisa lintlha tse latelang tsa EFT:\n\nBanka: XYZ Bank\nNomoro ea Ak'haonte: 1234567890\nReference: VENUE_BOOKING"
        }
    }
    return translations[text].get(lang, translations[text]['English'])

# Function to analyze user input with spaCy
def analyze_message(message):
    doc = nlp(message)
    return doc

@app.route('/webhook', methods=['POST'])
@limiter.limit("50/minute")  # Increased rate limit to 50 requests per minute
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
            user_details[from_number] = {'region': selected_region}
            venue_list = "\n".join([f"{i + 1}. {venue}" for i, venue in enumerate(VENUES[selected_region])])
            user_state[from_number] = "venue_selection"
            msg.body(get_translated_text(lang, 'choose_venue').format(selected_region, venue_list))
        else:
            msg.body(get_translated_text(lang, 'choose_region'))
    
    elif state == "venue_selection":
        selected_region = user_details[from_number]['region']
        venue_list = VENUES[selected_region]
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= len(venue_list):
            selected_venue = venue_list[int(incoming_msg) - 1]
            user_details[from_number]['venue'] = selected_venue
            user_state[from_number] = "details_collection"
            msg.body(get_translated_text(lang, 'ask_details'))
        else:
            venue_list = "\n".join([f"{i + 1}. {venue}" for i, venue in enumerate(venue_list)])
            msg.body(get_translated_text(lang, 'choose_venue').format(selected_region, venue_list))
    
    elif state == "details_collection":
        doc = analyze_message(incoming_msg)
        if doc:
            user_details[from_number]['details'] = incoming_msg
            user_state[from_number] = "date_selection"
            msg.body(get_translated_text(lang, 'ask_date'))
        else:
            msg.body(get_translated_text(lang, 'ask_details'))
    
    elif state == "date_selection":
        try:
            booking_date = datetime.datetime.strptime(incoming_msg, '%Y-%m-%d').date()
            if booking_date >= datetime.date.today():
                user_details[from_number]['date'] = booking_date
                name = user_details[from_number].get('details', 'Customer').split("\n")[0]  # Extracting name
                venue = user_details[from_number]['venue']
                region = user_details[from_number]['region']
                msg.body(get_translated_text(lang, 'confirm_booking').format(name, venue, region, booking_date))
                user_state[from_number] = "payment_method"
                msg.body(get_translated_text(lang, 'payment_method'))

                # Call create_event function to create Google Calendar event
                calendar_service = initialize_google_calendar()
                summary = f"Booking: {name} - {venue}"
                location = venue
                description = f"Booking made by {name} for {venue} at {region}"
                start_datetime = f"{booking_date}T09:00:00Z"  # Adjust time as needed
                end_datetime = f"{booking_date}T10:00:00Z"    # Adjust time as needed
                create_event(calendar_service, summary, location, description, start_datetime, end_datetime)

            else:
                msg.body(get_translated_text(lang, 'invalid_date'))
        except ValueError:
            msg.body(get_translated_text(lang, 'invalid_date'))
    
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
def ratelimit_handler(e):
    return "Rate limit exceeded. Please try again in a minute.", 429

if __name__ == "__main__":
    app.run(debug=True)
