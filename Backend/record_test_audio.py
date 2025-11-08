import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import os
import time

# Settings for the recording
duration = 5  # seconds
sample_rate = 44100  # Hz
channels = 1  # mono audio

# Get the assets folder path (same as used in Milestone1)
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")
output_file = os.path.join(assets_dir, "test_recording.wav")

print("\n🎙️ Recording will start in:")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("\n🔴 Recording... (speak for 5 seconds)")
recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=channels,
    dtype=np.int16
)
sd.wait()  # Wait until recording is done

print("\n✅ Recording finished!")

# Save the recording
wavfile.write(output_file, sample_rate, recording)
print(f"\n💾 Saved to: {output_file}")
print("\nNow you can run Milestone1(STT).py to test speech recognition!")