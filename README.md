Nepali Rashifal Generator (Astrological Horoscope)

This Python script performs traditional Vedic (sidereal) astrological calculations (Panchang) for a specified location (defaulting to Kathmandu, Nepal) at the moment of local sunrise. It then leverages the Gemini API to generate a personalized, culturally-aware daily horoscope (Rashifal) for each of the 12 Moon signs in the Nepali language.

🌟 Features

Accurate Planetary Calculation: Uses the swisseph library (Swiss Ephemeris) for precise planetary longitudes, including the Sun, Moon, and other planets, at the moment of local sunrise (Suryodaya).

Panchang Elements: Calculates the Tithi, Nakshatra, Yoga, Karana, and Moon Rashi (sign) for the day.

ChatGPT API Integration: Generates detailed predictions for health, wealth, love, and career advice, tailored to the unique astrological conditions of the day.

Nepali Language Output: All generated horoscopes are provided in Nepali.

🚀 Getting Started

Follow these steps to set up and run the Rashifal Generator on your machine.

Prerequisites

You need Python 3.8+ installed and an OpenAI API Key to run the horoscope generation using the LLM.

1. Installation

First, clone the repository and install the required dependencies:

# Clone the repository (if not already done)
git clone [https://github.com/Mosin0Ali/ai-rashifal-horoscope--generator.git](https://github.com/Mosin0Ali/ai-rashifal-horoscope--generator.git)
cd ai-rashifal-horoscope--generator

# Create and activate a virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate

# Install required Python packages
pip install -r requirements.txt


2. Configure API Key

Open your main Python script (e.g., rashifal_generator.py) and replace the placeholder with your actual OpenAI API Key:

# ---------------- OpenAI API Key ----------------
openai.api_key = "YOUR - OPEN-AI-API-KEY"


Note: The provided code uses the openai library. If you are integrating with the Google Gemini models, ensure you are using the correct client library and API endpoint.

3. Run the Script

Execute the main file. It will print the sunrise time, planetary positions, and the generated horoscopes for all 12 rashis to your console.

python3 your_script_name.py


⚙️ Configuration

You can easily adjust the primary settings at the beginning of the script:

Variable

Description

Default Value

latitude

Geographical latitude of the calculation point.

27.7172 (Kathmandu)

longitude

Geographical longitude of the calculation point.

85.3240 (Kathmandu)

timezone

Timezone offset from UTC in hours (e.g., NPT is UTC+5.75).

5.75

date

The date for which the Rashifal is calculated.

datetime.date.today()