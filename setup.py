# 1. Install required libraries
!pip install -q google-generativeai IPython
!pip install -q pillow
!pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
!pip install -q kokoro>=0.9.2 soundfile
!apt-get -qq -y install espeak-ng > /dev/null 2>&1

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
