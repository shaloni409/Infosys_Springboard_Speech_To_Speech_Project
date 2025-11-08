try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None
    _deep_translator_missing = True
else:
    _deep_translator_missing = False

# Ensure stdout uses UTF-8 on platforms where the default encoding cannot print emoji (Windows CP1252)
import sys
try:
    # Python 3.7+ has reconfigure
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    # ignore if reconfigure isn't available
    pass

# File paths (use project-relative paths)
import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "Data")

# Create Data directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

input_file = os.path.join(data_dir, "text.txt")
output_file = os.path.join(data_dir, "translated.txt")

# Check if input file exists
if not os.path.isfile(input_file):
    print(f"\nERROR: Input file not found: {input_file}")
    print("\nPlease create a text.txt file in the Backend/Data folder with the text to translate.")
    print("Example content for text.txt:")
    print('    Hello, this is a test message.')
    print('    How are you today?')
    print(f"\nCreated folder: {data_dir}")
    sys.exit(1)

# Azure-supported languages (for both Translation + Text-to-Speech)
language_options = {
    "English": "English",
    "hi": "Hindi",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "pt-PT": "Portuguese (Portugal)",
    "pt-BR": "Portuguese (Brazil)",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "ar": "Arabic",
    "tr": "Turkish",
    "th": "Thai",
    "nl": "Dutch",
    "sv": "Swedish",
    "pl": "Polish",
    "ta": "Tamil"
}

# Ask user for language choice
print("🌍 Available languages (Azure TTS compatible):")
for code, name in language_options.items():
    print(f"{code} → {name}")

user_choice = input("\nEnter the language code you want to translate to: ").strip()

if user_choice not in language_options:
    print("❌ Invalid language code. Please try again.")
    exit()

if globals().get("_deep_translator_missing", False):
    sys.stderr.write("ERROR: Missing required Python package 'deep-translator'.\n")
    sys.stderr.write("Install it with:\n    pip install deep-translator\nOr install all project dependencies:\n    pip install -r requirements.txt\n")
    sys.exit(1)

# Translate and output only translated text
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        text = line.strip()
        if not text:
            continue

        try:
            translated_text = GoogleTranslator(source='auto', target=user_choice).translate(text)
            print(translated_text)  # only translated text
            outfile.write(translated_text + "\n")
        except Exception as e:
            outfile.write("Translation Error\n") 