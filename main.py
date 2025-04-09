# Import necessary modules
from setup import *
from google_drive_utils import download_file_from_google_drive, test_google_drive_api
from api_config import api_keys, selected_api_key, safety_settings
from prompt_generation import generate_prompt
from retry_mechanisms import retry_api_call, retry_story_generation
from collect_story import collect_complete_story
from seo_metadata import generate_seo_metadata, default_seo_metadata
from thumbnail_generation import generate_thumbnail

# Main generation modules are imported using exec to avoid issues with large imports
exec(open("generate_part1.py").read())
exec(open("generate_part2.py").read())
exec(open("generate_part3.py").read())
exec(open("generate_part4.py").read())
exec(open("generate_part5.py").read())
exec(open("generate_part6.py").read())
exec(open("google_drive_upload.py").read())
exec(open("direct_download.py").read())

# --- Run the function ---
print("--- Starting generation (attempting 16:9 via prompt) ---")
# You can set use_prompt_generator=True to enable the prompt generator model
# You can also customize the prompt_input to guide the prompt generator
retry_story_generation(use_prompt_generator=True)
print("--- Generation function finished ---")
