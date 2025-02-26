import os
import subprocess
import threading

PIPER_PATH = "./piper/piper"
VOICE_MODEL = "./piper_voices/en-us-glados-high.onnx"

def speak(text, speed=0.75):
    """
    Uses Piper for TTS.
    """
    try:
        process = subprocess.Popen(
            [PIPER_PATH, "--model", VOICE_MODEL, "--output_raw", "--quiet"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        sox_process = subprocess.Popen(
            ["play", "-t", "raw", "-r", "22050", "-e", "signed", "-b", "16", "-c", "1", "-"],
            stdin=process.stdout,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        process.stdin.write(text.encode("utf-8"))
        process.stdin.close()
        sox_process.wait()
    except Exception as e:
        print(f"Error: {e}")

def speak_threaded(text, speed=0.75):
    threading.Thread(target=speak, args=(text, speed)).start()
