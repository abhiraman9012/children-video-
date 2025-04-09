# 1. Required libraries - these should be installed using requirements.txt before running
# Do not attempt installation here to avoid issues with exec()
# If you need to install these libraries, use:
# pip install -r requirements.txt

# Check if we're in a Colab environment
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Only attempt system installations in Colab environment
if IN_COLAB:
    import subprocess
    try:
        subprocess.check_call(['apt-get', '-qq', '-y', 'install', 'espeak-ng'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Installed system dependencies")
    except Exception as e:
        print(f"Warning: Could not install system dependencies: {e}")


# 2. Import libraries
import os
import re
import json
import mimetypes
import tempfile
import datetime
import base64
import subprocess
import numpy as np
import soundfile as sf
import requests
from google import genai
from google.genai import types # Need types for Content/Part/Config/SafetySetting
from IPython.display import display, Image, Audio, HTML
from PIL import Image as PILImage
from kokoro import KPipeline
