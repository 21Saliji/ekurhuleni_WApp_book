```markdown
# Ekurhuleni WhatsApp Booking System

## Overview
This project integrates Vonage's API to send WhatsApp messages. Follow the steps below to set up and run the project.

## Prerequisites

1. **Python 3.x:** Ensure Python 3 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **Git:** Make sure Git is installed for version control. You can download it from [git-scm.com](https://git-scm.com/downloads).

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/21Saliji/ekurhuleni_WApp_book.git
cd ekurhuleni_WApp_book
```

### 2. Create and Activate a Virtual Environment

Set up a virtual environment to manage dependencies:

- **On Windows:**

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **On macOS/Linux:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Required Packages

Install the necessary packages using the `requirements.txt` file:

```bash
pip freeze > requirements.txt

pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```plaintext
VONAGE_API_KEY=your_api_key
VONAGE_API_SECRET=your_api_secret
```

Replace `your_api_key` and `your_api_secret` with your actual Vonage API key and secret. 

To obtain your Vonage API key and secret, sign up or log in to the Vonage API Dashboard[https://www.vonage.com/communications-apis/].

### 5. Run the Script

Once everything is set up, you can run the `my-whatsapp-bot.py` script:

```bash
python my-whatsapp-bot.py  # Or use `python3` if necessary
```

## Troubleshooting

- **Missing Packages:** Ensure all required packages are listed in `requirements.txt` and installed in your virtual environment.
- **Environment Variables:** Verify that the `.env` file is correctly set up with the correct API key and secret.
- **Script Errors:** Review any error messages in the terminal to identify and fix issues. Common issues might include typos or configuration problems.

