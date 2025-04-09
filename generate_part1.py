# Generate function
def generate(use_prompt_generator=True, prompt_input="Create a unique children's story with a different animal character, setting, and adventure theme."):
    # Initialize variables that might be used later
    output_path = None
    story_text = None
    image_files = []

    try:
        client = genai.Client(
             api_key=os.environ.get("GEMINI_API_KEY"),
        )
        print("u2705 Initializing client using genai.Client...")
    except AttributeError:
        print("ud83dudd34 FATAL ERROR: genai.Client is unexpectedly unavailable.")
        return
    except Exception as e:
        print(f"ud83dudd34 Error initializing client: {e}")
        return
    print("u2705 Client object created successfully.")

    model = "gemini-2.0-flash-exp-image-generation"

    # --- Modified Prompt ---
    if use_prompt_generator:
        print("ud83eudde0 Using prompt generator model first...")
        # Use retry mechanism for generate_prompt
        generated_prompt = retry_api_call(generate_prompt, prompt_input)
        if generated_prompt and generated_prompt.strip():
            prompt_text = generated_prompt
            print("u2705 Using AI-generated prompt for story and image creation")
        else:
            print("u26a0ufe0f Prompt generation failed or returned empty, using default prompt")
            prompt_text = """Generate a story about a white baby goat named Pip going on an adventure in a farm in a highly detailed 3d cartoon animation style. For each scene, generate a high-quality, photorealistic image **in landscape orientation suitable for a widescreen (16:9 aspect ratio) YouTube video**. Ensure maximum detail, vibrant colors, and professional lighting."""
    else:
        prompt_text = """Generate a story about a white baby goat named Pip going on an adventure in a farm in a highly detailed 3d cartoon animation style. For each scene, generate a high-quality, photorealistic image **in landscape orientation suitable for a widescreen (16:9 aspect ratio) YouTube video**. Ensure maximum detail, vibrant colors, and professional lighting."""
    # --- End Modified Prompt ---

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["image", "text"],
        response_mime_type="text/plain",
        safety_settings=safety_settings,
    )

    print(f"u2139ufe0f Using Model: {model}")
    print(f"ud83dudcdd Using Prompt: {prompt_text}") # Show the modified prompt
    print(f"u2699ufe0f Using Config (incl. safety): {generate_content_config}")
    print("u23f3 Calling client.models.generate_content_stream...")

    try:
        # Create a temporary directory to store images and audio
        temp_dir = tempfile.mkdtemp()

        # Variables to collect story and images
        story_text = ""
        image_files = []
