        # After generating story and images, create audio
        if story_text and image_files:
            print("\n--- Starting Text-to-Speech Generation with Kokoro ---")
            try:
                # First collect and clean the complete story
                complete_story = collect_complete_story(story_text)

                # Check if we have enough segments for a complete story
                story_segments = collect_complete_story(story_text, return_segments=True)
                print(f"Story has {len(story_segments)} segments")

                # Check if we have matching image count (each segment should have one image)
                segments_count = len(story_segments)
                images_count = len(image_files)

                print(f"Story segments: {segments_count}, Images: {images_count}")

                # If we don't have enough segments or have mismatched images, try to regenerate
                retry_count = 0
                max_retries = 1000
                min_segments = 6  # Require at least 6 segments for a complete story

                # Define conditions for regeneration
                needs_regeneration = (segments_count < min_segments) or (images_count < segments_count)

                while needs_regeneration and retry_count < max_retries:
                    retry_count += 1

                    if segments_count < min_segments:
                        print(f"\nu26a0ufe0f Story has only {segments_count} segments, which is less than the required {min_segments}.")

                    if images_count < segments_count:
                        print(f"\nu26a0ufe0f Mismatch between story segments ({segments_count}) and images ({images_count}).")

                    print(f"Attempting to regenerate a more detailed story with complete images (attempt {retry_count}/{max_retries})...")

                    # Modify prompt to encourage a complete story with images for each segment
                    enhanced_prompt = prompt_text
                    if "with at least 6 detailed scenes" not in enhanced_prompt:
                        # Add more specific instructions to generate a longer story with images
                        enhanced_prompt = enhanced_prompt.replace(
                            "Generate a story about",
                            "Generate a detailed story with at least 6 scenes about"
                        )
                    if "with one image per scene" not in enhanced_prompt:
                        enhanced_prompt += " Please create one clear image for each scene in the story."

                    # Retry with the enhanced prompt
                    retry_contents = [
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_text(text=enhanced_prompt),
                            ],
                        ),
                    ]

                    # Clear previous results
                    story_text_retry = ""
                    image_files_retry = []

                    try:
                        # Try non-streaming for retries as it's more reliable
                        # Wrap the regeneration API call in the retry mechanism
                        def attempt_retry_generation():
                            return client.models.generate_content(
                                model=model,
                                contents=retry_contents,
                                config=generate_content_config,
                            )

                        retry_response = retry_api_call(attempt_retry_generation)

                        if retry_response.candidates and retry_response.candidates[0].content:
                            for part in retry_response.candidates[0].content.parts:
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    inline_data = part.inline_data
                                    image_data = inline_data.data
                                    mime_type = inline_data.mime_type

                                    # Save image to a temporary file
                                    img_path = os.path.join(temp_dir, f"image_retry_{len(image_files_retry)}.jpg")
                                    with open(img_path, "wb") as f:
                                        f.write(image_data)
                                    image_files_retry.append(img_path)

                                    print(f"\n\nud83duddbcufe0f --- Retry Image Received ({mime_type}) ---")
                                    display(Image(data=image_data))
                                    print("--- End Image ---\n")
                                elif hasattr(part, 'text') and part.text:
                                    print(part.text)
                                    story_text_retry += part.text

                        # Check if the retry generated enough content AND enough images
                        if story_text_retry:
                            story_segments = collect_complete_story(story_text_retry, return_segments=True)
                            segments_count = len(story_segments)
                            images_count = len(image_files_retry)

                            print(f"Retry generated {segments_count} segments and {images_count} images")

                            # Verify that we have sufficient segments AND images
                            if segments_count >= min_segments and images_count >= segments_count * 0.8:  # Allow for some missing images (80% coverage)
                                story_text = story_text_retry
                                if image_files_retry:
                                    image_files = image_files_retry
                                complete_story = collect_complete_story(story_text)
                                print("u2705 Successfully regenerated a more detailed story with images")
                                needs_regeneration = False
                            else:
                                print("u26a0ufe0f Regenerated story still doesn't meet requirements")

                                # If we have good segment count but poor image count, keep trying
                                if segments_count >= min_segments and images_count < segments_count * 0.8:
                                    print("Generated enough segments but not enough images. Retrying...")
                                    # We'll continue the loop to try again
                    except Exception as retry_error:
                        print(f"u26a0ufe0f Error during story regeneration: {retry_error}")

                print("u23f3 Converting complete story to speech...")
                print("Story to be converted:", complete_story[:100] + "...")

                # Initialize Kokoro pipeline
                pipeline = KPipeline(lang_code='a')

                try:
                    # Generate audio for the complete story
                    print("Full story length:", len(complete_story), "characters")
                    generator = pipeline(complete_story, voice='af_heart')

                    # Save the complete audio file
                    audio_path = os.path.join(temp_dir, "complete_story.wav")

                    # Process and save all audio chunks
                    all_audio = []
                    for _, (gs, ps, audio) in enumerate(generator):
                        all_audio.append(audio)

                    # Combine all audio chunks
                    if all_audio:
                        combined_audio = np.concatenate(all_audio)
                        sf.write(audio_path, combined_audio, 24000)
                        print(f"u2705 Complete story audio saved to: {audio_path}")
                        print("ud83dudd0a Playing complete story audio:")
                        display(Audio(data=combined_audio, rate=24000))

                except Exception as e:
                    print(f"u26a0ufe0f Error in text-to-speech generation: {e}")
                    return

                bark_audio_success = False

            except Exception as e:
                print(f"u26a0ufe0f Error in text-to-speech generation: {e}")
                return
