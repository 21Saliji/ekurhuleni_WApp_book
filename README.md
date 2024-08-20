# Ekurhuleni Smart Bot README

Welcome to the Ekurhuleni Smart Bot project! This bot helps users book venues and manage their bookings via SMS, integrating with Google Calendar for event management. Below is a guide to set up, run, and understand the bot.

## Overview

The Ekurhuleni Smart Bot is a Flask-based application that interacts with users through Twilio SMS. It uses spaCy for natural language processing and integrates with Google Calendar to manage venue bookings. The bot supports multiple languages and provides an intuitive booking experience.

## Features

- **Language Support:** English, IsiZulu, Sesotho
- **Region Selection:** Duduza, Tsakane, KwaThema
- **Venue Booking:** Book various venues in the selected region
- **Google Calendar Integration:** Creates events on Google Calendar for confirmed bookings
- **Rate Limiting:** Prevents abuse by limiting requests

## Requirements

- Python 3.6 or higher
- Flask
- spaCy
- Twilio
- Flask-Limiter
- python-dotenv
- Google API client libraries

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/ekurhuleni-smart-bot.git
   cd ekurhuleni-smart-bot
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following variables:

   ```plaintext
   GOOGLE_CLIENT_ID=<your-google-client-id>
   GOOGLE_CLIENT_SECRET=<your-google-client-secret>
   TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
   TWILIO_PHONE_NUMBER=<your-twilio-phone-number>
   ```

5. **Download and install spaCy language model:**

   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Set up Google API credentials:**

   - Create a project in the Google Developers Console.
   - Enable the Google Calendar API.
   - Download the `credentials.json` file and place it in the `.credentials` directory.

## Running the Application

1. **Start the Flask server:**

   ```bash
   python chantel.py
   ```

2. **Set up a webhook in Twilio:**

   Configure Twilio to send incoming SMS messages to `http://your-server-url/webhook`.

## Code Explanation

- **Google Calendar Integration:**
  - `initialize_google_calendar()`: Sets up the Google Calendar API client.
  - `create_event()`: Creates an event on Google Calendar.

- **spaCy Integration:**
  - `analyze_message()`: Analyzes user messages to extract details.

- **Flask Routes:**
  - `/webhook`: Handles incoming SMS messages, guides the user through the booking process, and creates calendar events.

- **Rate Limiting:**
  - Prevents abuse by limiting requests to 50 per minute.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


Happy coding! 🎉