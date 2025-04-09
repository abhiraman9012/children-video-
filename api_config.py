# Run the test before executing any models
print("\n--- Testing Google Drive API Integration ---")
api_test_result = test_google_drive_api()
if not api_test_result:
    print("⚠️ Warning: Google Drive API test failed. Some features related to Google Drive may not work properly.")
else:
    print("✅ Google Drive API integration is ready to use.")

# 3. --- SET API KEY IN ENVIRONMENT ---
#    Make sure this is done BEFORE running this cell.
#    e.g., os.environ['GEMINI_API_KEY'] = "YOUR_API_KEY_HERE"
# ------------------------------------

# Setting API Key - randomly selecting from available keys
# List of all available API keys
api_keys = [
    "AIzaSyAqbqE86FKFXS6t5qrpXJVj9jAf-arQ1Js",
    "AIzaSyDVmSA9ricHVEzo6v1gj-crkuaJvQD72yw",
    "AIzaSyDNeeKDXnwGF7MYhFrnFoD9VL-ecvO5mEE",
    "AIzaSyAHvAdcSoRmeXB9xJjvvdXKtXw3dHSmJiQ",
    "AIzaSyC_XqbLjFQnLXfo26J-RX_WDx59H4ql9Qs",
    "AIzaSyC8FuTNC3FxLs0Qx2ciRoLwxjOrLGqOB5A",
    "AIzaSyBL8KngLHXOY0rSk5R4awta1tfDl6xC8rM"
]

# Randomly select one API key
import random
selected_api_key = random.choice(api_keys)
os.environ['GEMINI_API_KEY'] = selected_api_key
print(f"✅ Randomly selected one of {len(api_keys)} available API keys")

# --- Check API Key ---
api_key_check = os.environ.get("GEMINI_API_KEY")
if not api_key_check:
    print("🛑 ERROR: Environment variable GEMINI_API_KEY is not set.")
    print("💡 TIP: Uncomment and set your API key above, or run this in a cell before running this script:")
    print("    os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'")
    raise ValueError("API Key not found in environment.")
else:
    print(f"✅ Found API Key: ...{api_key_check[-4:]}")
#------------------------

# Define Safety Settings
safety_settings = [
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
]
print(f"⚙️ Defined Safety Settings: {safety_settings}")
