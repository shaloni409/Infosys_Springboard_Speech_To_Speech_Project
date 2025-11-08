import os
import sys
import time
import azure.cognitiveservices.speech as speechsdk

# Base project directory (use current script's location)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))  # Go up two levels to project root
input_folder = os.path.join(script_dir, "assets")

# Create assets directory if it doesn't exist
os.makedirs(input_folder, exist_ok=True)

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Speech Configuration
speech_key = os.getenv("Speech_key")
service_region = os.getenv("Speech_region")

print("Speech Key:", speech_key)  # (for testing only, remove later)
print("Region:", service_region)
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Auto language detection (Hindi + English)
auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    languages=["hi-IN", "en-IN"]
)

# Check for WAV files in the assets directory
wav_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
if not wav_files:
    print(f"\nNo .wav files found in {input_folder}")
    print("Please add .wav files to this directory and run the script again.")
    sys.exit(0)

for file in wav_files:
        input_file = os.path.join(input_folder, file)
        audio_input = speechsdk.AudioConfig(filename=input_file)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_input,
            auto_detect_source_language_config=auto_detect_source_language_config
        )

        all_text = []
        done_flag = {"done": False}

        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = evt.result.text.strip()
                if text:
                    all_text.append(text)

        def stop_cb(evt):
            done_flag["done"] = True

        recognizer.recognized.connect(recognized_handler)
        recognizer.session_stopped.connect(stop_cb)
        recognizer.canceled.connect(stop_cb)

        recognizer.start_continuous_recognition()

        timeout = 60
        start_time = time.time()
        while not done_flag["done"] and time.time() - start_time < timeout:
            time.sleep(0.5)

        recognizer.stop_continuous_recognition()

        if all_text:
            print(" ".join(all_text))