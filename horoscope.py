import swisseph as swe
import datetime
import math
import pytz
import openai

# ---------------- OpenAI API Key ----------------
openai.api_key = "YOUR-OPEN-AI-API-KEY"

# ---------------- Location ----------------
latitude = 27.7172   # Kathmandu
longitude = 85.3240
timezone = 5.75      # NPT = UTC+5:45

# ---------------- Date ----------------
date = datetime.date.today()

# ---------------- Sunrise Calculation ----------------
def calculate_sunrise(lat, lon, date, tz_offset):
    """Approximate sunrise calculation in local time"""
    N = date.timetuple().tm_yday
    decl = 23.45 * math.pi/180 * math.sin(2 * math.pi * (284 + N)/365)
    lat_rad = math.radians(lat)
    ha = math.acos((math.cos(math.radians(90.833)) / (math.cos(lat_rad)*math.cos(decl)) - math.tan(lat_rad)*math.tan(decl)))
    ha_hours = math.degrees(ha) / 15
    solar_noon = 12 - (lon / 15)
    sunrise_utc = solar_noon - ha_hours
    sunrise_local = sunrise_utc + tz_offset
    hr = int(sunrise_local)
    mn = int((sunrise_local - hr) * 60)
    return datetime.datetime(date.year, date.month, date.day, hr, mn)

sunrise_local = calculate_sunrise(latitude, longitude, date, timezone)
np_tz = pytz.timezone("Asia/Kathmandu")
sunrise_local = np_tz.localize(sunrise_local)
sunrise_utc = sunrise_local.astimezone(datetime.timezone.utc)

# ---------------- Julian Day ----------------
jd_ut = swe.julday(
    sunrise_utc.year, sunrise_utc.month, sunrise_utc.day,
    sunrise_utc.hour + sunrise_utc.minute/60 + sunrise_utc.second/3600
)

# ---------------- Swiss Ephemeris Setup ----------------
swe.set_ephe_path("/tmp")
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ---------------- Planetary Positions ----------------
planets = {
    "सूर्य": swe.SUN,
    "चन्द्र": swe.MOON,
    "बुध": swe.MERCURY,
    "शुक्र": swe.VENUS,
    "मंगल": swe.MARS,
    "बृहस्पति": swe.JUPITER,
    "शनि": swe.SATURN,
    "राहु": swe.MEAN_NODE,
}

planet_positions = {}
for name, planet in planets.items():
    lon = swe.calc_ut(jd_ut, planet)[0][0]
    planet_positions[name] = lon

planet_positions["केतु"] = (planet_positions["राहु"] + 180) % 360

# ---------------- Panchang Calculations ----------------
sun_lon = planet_positions["सूर्य"]
moon_lon = planet_positions["चन्द्र"]

diff = (moon_lon - sun_lon) % 360
tithi_num = int(diff // 12) + 1
paksha = "शुक्ल" if tithi_num <= 15 else "कृष्ण"

nakshatra_num = int(moon_lon // (360/27)) + 1
yoga_sum = (sun_lon + moon_lon) % 360
yoga_num = int(yoga_sum // (360/27)) + 1
karana_num = int((diff % 12) // 6) + 1
rashi_num = int(moon_lon // 30) + 1

# ---------------- Names ----------------
tithi_names = [
    "प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पञ्चमी",
    "षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी",
    "एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","पूर्णिमा",
    "प्रतिपदा","द्वितीया","तृतीया","चतुर्थी","पञ्चमी",
    "षष्ठी","सप्तमी","अष्टमी","नवमी","दशमी",
    "एकादशी","द्वादशी","त्रयोदशी","चतुर्दशी","अमावस्या"
]

nakshatra_names = [
    "अश्विनी","भरणी","कृत्तिका","रोहिणी","मृगशीर्ष",
    "आर्द्रा","पुनर्वसु","पुष्य","आश्रेषा","मघा",
    "पूर्वफल्गुनी","उत्तरफल्गुनी","हस्त","चित्रा","स्वाति",
    "विशाखा","अनुराधा","ज्येष्ठा","मूला","पूर्वाषाढ़ा",
    "उत्तराषाढ़ा","श्रवण","श्रविष्ठा","शतभिषा","पूर्वभाद्रपद",
    "उत्तरभाद्रपद","रेवती"
]

yoga_names = [
    "विश्वकर्मा","प्रिति","आयुष्मान","सौभाग्य","शोभना",
    "अतिगण्ड","सुकर्मा","ध्रुव","व्याघात","हर्षण",
    "वज्र","सिद्धि","व्यास","धृति","शूल",
    "गण्ड","वृद्धि","ध्रुवसिद्धि","व्याघातसिद्धि","हर्षणसिद्धि",
    "वज्रसिद्धि","सिद्धिवृद्धि","व्याघातवृद्धि","हर्षवृद्धि","वज्रवृद्धि",
    "सिद्धिव्याघात","व्याघातवज्र"
]

karana_names = [
    "वणिज","बालव","कौलव","तैतिल","गरज",
    "वणिज","बालव","कौलव","तैतिल","गरज",
    "वणिज","बालव","कौलव","तैतिल","गरज",
    "विष्टि/भद्र","शकुनि","चतुष्पद","नाग","किमस्तुग्न"
]

rashi_names = [
    "मेष","वृष","मिथुन","कर्कट","सिंह","कन्या",
    "तुला","वृश्चिक","धनु","मकर","कुम्भ","मीन"
]

# ---------------- ChatGPT Integration ----------------
def generate_rashifal_chatgpt(moon_rashi_name):
    prompt = f"""
तपाईं एक अनुभवी नेपाली ज्योतिषी हुनुहुन्छ। आजको राशिफल बनाउनुहोस्।
महत्त्वपूर्ण जानकारी:
- राशि: {moon_rashi_name}
- तिथि: {tithi_num} ({paksha})
- नक्षत्र: {nakshatra_names[nakshatra_num-1]}
- योग: {yoga_names[yoga_num-1]}
- करण: {karana_names[karana_num-1]}
- ग्रहहरूको स्थिती: {planet_positions}

कृपया Nepali भाषामा दैनिक राशिफल बनाउनुहोस्। स्वास्थ्य, धन, प्रेम, करियरका सल्लाह समावेश गर्नुहोस्। छोटकरीमा 2-3 वाक्यमा लेख्नुहोस्।
"""
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "तपाईं एक अनुभवी नेपाली ज्योतिषी हुनुहुन्छ।"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    return response.choices[0].message.content

# ---------------- Generate Rashifal for All Moon Rashis ----------------
print(f"सूर्योदय (काठमाडौँ): {sunrise_local.time()}")
print("ग्रहहरूको स्थिती (Longitude in degrees):")
for name, lon in planet_positions.items():
    print(f"  {name}: {lon:.2f}")

print("\n--- दैनिक राशिफल ---")
for i in range(12):
    moon_rashi_name = rashi_names[i]
    rashifal = generate_rashifal_chatgpt(moon_rashi_name)
    print(f"\n{moon_rashi_name} राशिफल:\n{rashifal}")
