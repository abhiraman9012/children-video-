def retry_api_call(retry_function, *args, **kwargs):
    """
    Retries API calls when the Gemini model server is unavailable or encounters errors.

    Args:
        retry_function: The function to retry (either generate_prompt or the model API call)
        *args, **kwargs: Arguments to pass to the function

    Returns:
        The result of the successful function call, or None after maximum retries
    """
    import time

    max_consecutive_failures = 1000  # Effectively keep trying indefinitely
    retry_delay = 10  # seconds
    attempt = 0

    while attempt < max_consecutive_failures:
        attempt += 1
        try:
            print(f"⏳ API call attempt {attempt}...")
            result = retry_function(*args, **kwargs)

            # For generate function, check if we got story and images
            if retry_function.__name__ == 'generate_content_stream' or retry_function.__name__ == 'generate_content':
                # Success criteria - we need to check the response for both text and images
                if result:
                    # Check if the result contains "**Image Description:**" which indicates
                    # the model generated text descriptions instead of actual images

                    # For non-streaming responses
                    if hasattr(result, 'candidates') and result.candidates:
                        for candidate in result.candidates:
                            if hasattr(candidate, 'content') and candidate.content:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'text') and part.text and "**Image Description:**" in part.text:
                                        print(f"⚠️ Model generated text descriptions instead of images on attempt {attempt}, retrying in {retry_delay} seconds...")
                                        time.sleep(retry_delay)
                                        continue

                    # For streaming responses, we can't easily check the content before consuming the stream
                    # So we'll rely on the subsequent processing to detect this issue

                    print(f"✅ API call successful on attempt {attempt}")
                    return result
                else:
                    print(f"⚠️ API returned empty result on attempt {attempt}, retrying in {retry_delay} seconds...")
            else:
                # For other functions like generate_prompt, just check if result is not None
                if result is not None:
                    print(f"✅ API call successful on attempt {attempt}")
                    return result

        except Exception as e:
            print(f"🔴 API error on attempt {attempt}: {e}")

        print(f"🔄 Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

    print(f"⚠️ Maximum consecutive failures ({max_consecutive_failures}) reached. Giving up.")
    return None

def retry_story_generation(use_prompt_generator=True, prompt_input="Create a unique children's story with a different animal character, setting, and adventure theme."):
    """
    Persistently retries story generation when image loading fails or JSON errors occur.
    This function will keep retrying every 7 seconds until all conditions are met:
    1. No JSON errors in stream processing
    2. Images are properly loaded
    3. At least 6 story segments are generated
    
    Args:
        use_prompt_generator: Whether to use the prompt generator
        prompt_input: The prompt input to guide story generation
        
    Returns:
        The result of the successful generation
    """
    import time
    import threading
    
    # Set initial state
    success = False
    max_retries = 1000  # Set a reasonable limit
    retry_count = 0
    retry_delay = 7  # Run every 7 seconds as specified
    
    # Create a container for results
    results = {"story_text": None, "image_files": [], "output_path": None, "thumbnail_path": None, "metadata": None}
    
    # Create a global temp directory for flag files
    import tempfile
    import os
    temp_dir = tempfile.mkdtemp()
    
    def check_generation_status():
        # This helper function checks if the generation was successful
        # Based on the presence of images and sufficient story segments
        nonlocal success
        
        if not results["story_text"] or not results["image_files"]:
            return False
        
        # Check if we have at least 6 story segments
        try:
            story_segments = collect_complete_story(results["story_text"], return_segments=True)
            if len(story_segments) < 6:
                print(f"⚠️ Insufficient story segments: {len(story_segments)} (need at least 6)")
                return False
                
            # Check if we have sufficient images
            if len(results["image_files"]) < 6:
                print(f"⚠️ Insufficient images: {len(results['image_files'])} (need at least 6)")
                return False
            
            # NEW: Check if video was successfully generated
            if results["output_path"] and os.path.exists(results["output_path"]):
                print(f"✅ Video successfully generated: {results['output_path']}")
                # Note: We don't need to check for a flag file anymore since we use sys.exit()
                # after successful Google Drive upload
                
            # If we get here, generation was successful
            success = True
            return True
        except Exception as e:
            print(f"⚠️ Error checking generation status: {e}")
            return False
    
    # Define a wrapper function that will capture the results
    def generation_wrapper():
        nonlocal results
        try:
            # Create a clean temporary directory for each attempt
            import tempfile
            import os
            temp_dir = tempfile.mkdtemp()
            
            # Call the main generate function
            print(f"\n🔄 Retry attempt #{retry_count+1} for story generation...")
            print(f"⏳ Starting generation with prompt: {prompt_input[:50]}...")
            
            # This is a wrapper that will call the actual generate function
            # but will capture its outputs for our status checks
            result = generate(use_prompt_generator=use_prompt_generator, prompt_input=prompt_input)
            
            # Capture variables from the generate function's scope if possible
            if 'story_text' in locals() and locals()['story_text']:
                results["story_text"] = locals()['story_text']
            if 'image_files' in locals() and locals()['image_files']:
                results["image_files"] = locals()['image_files']
            if 'output_path' in locals() and locals()['output_path']:
                results["output_path"] = locals()['output_path']
            if 'thumbnail_path' in locals() and locals()['thumbnail_path']:
                results["thumbnail_path"] = locals()['thumbnail_path']
            if 'metadata' in locals() and locals()['metadata']:
                results["metadata"] = locals()['metadata']
                
            # Check if generation was successful
            check_generation_status()
        except Exception as e:
            print(f"⚠️ Error in generation attempt: {e}")
            import traceback
            traceback.print_exc()
    
    # Main retry loop
    while not success and retry_count < max_retries:
        retry_count += 1
        
        # Start generation in current thread (blocking)
        generation_wrapper()
        
        # If successful, break the loop
        if success:
            print(f"✅ Story generation successful after {retry_count} attempts!")
            break
            
        # If not successful, wait and retry
        print(f"⚠️ Generation attempt #{retry_count} failed or incomplete.")
        print(f"🔄 Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)
    
    if not success:
        print(f"⚠️ Maximum retry attempts ({max_retries}) reached without success.")
    
    # Return the results regardless of success state
    # This allows partial results to be used if available
    return results
