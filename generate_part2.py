        try:
            # Flag to determine if we should use streaming or fallback approach
            use_streaming = True

            try:
                # Wrap the API call in the retry mechanism
                def attempt_stream_generation():
                    return client.models.generate_content_stream(
                        model=model,
                        contents=contents,
                        config=generate_content_config,
                    )

                stream = retry_api_call(attempt_stream_generation)

            except json.decoder.JSONDecodeError as je:
                print(f"⚠️ JSON decoding error during stream creation: {je}")
                print("Trying fallback to non-streaming API call...")
                use_streaming = False

                # Fallback to non-streaming version
                try:
                    # Wrap the fallback API call in the retry mechanism
                    def attempt_non_stream_generation():
                        return client.models.generate_content(
                            model=model,
                            contents=contents,
                            config=generate_content_config,
                        )

                    response = retry_api_call(attempt_non_stream_generation)

                    # Process the non-streaming response
                    print("Using non-streaming response instead")
                    image_found = False

                    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                image_found = True
                                inline_data = part.inline_data
                                image_data = inline_data.data
                                mime_type = inline_data.mime_type

                                # Save image to a temporary file
                                img_path = os.path.join(temp_dir, f"image_{len(image_files)}.jpg")
                                with open(img_path, "wb") as f:
                                    f.write(image_data)
                                image_files.append(img_path)

                                print(f"\n\n🖼️ --- Image Received ({mime_type}) ---")
                                display(Image(data=image_data))
                                print("--- End Image ---\n")
                            elif hasattr(part, 'text') and part.text:
                                print(part.text)
                                story_text += part.text

                    # Skip the streaming loop since we already processed the response
                    print("✅ Non-streaming processing complete.")
                    if not image_found:
                        print("⚠️ No images were found in the non-streaming response.")

                    # Continue with audio and video processing
                    image_found = True  # Set this to true to prevent early exit

                except Exception as e:
                    print(f"⚠️ Fallback API call also failed: {e}")
                    return

            except Exception as e:
                print(f"⚠️ Error creating stream: {e}")
                return

            # Only enter the streaming loop if we're using streaming
            if use_streaming:
                image_found = False
                print("--- Response Stream ---")

                # Track JSON parsing errors to decide when to fallback
                json_errors = 0
                max_json_errors = 5  # Allow up to 5 errors before giving up on streaming

                # Check for Image Description text instead of actual images
                contains_image_description = False

                try:
                    for chunk in stream:
                        try:
                            # If we get a raw string instead of parsed content
                            if isinstance(chunk, str):
                                print(chunk, end="")
                                story_text += chunk
                                # Check for image descriptions
                                if "**Image Description:**" in chunk:
                                    contains_image_description = True
                                continue

                            # Check if chunk has candidates
                            if not hasattr(chunk, 'candidates') or not chunk.candidates:
                                # Try to extract as much as possible from the chunk
                                if hasattr(chunk, 'text') and chunk.text:
                                    print(chunk.text, end="")
                                    story_text += chunk.text
                                    # Check for image descriptions
                                    if "**Image Description:**" in chunk.text:
                                        contains_image_description = True
                                continue

                            if not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                                if hasattr(chunk, 'text') and chunk.text:
                                    print(chunk.text, end="")
                                    story_text += chunk.text
                                    # Check for image descriptions
                                    if "**Image Description:**" in chunk.text:
                                        contains_image_description = True
                                continue

                            part = chunk.candidates[0].content.parts[0]

                            if hasattr(part, 'inline_data') and part.inline_data:
                                image_found = True
                                inline_data = part.inline_data
                                image_data = inline_data.data
                                mime_type = inline_data.mime_type

                                # Save image to a temporary file
                                img_path = os.path.join(temp_dir, f"image_{len(image_files)}.jpg")
                                with open(img_path, "wb") as f:
                                    f.write(image_data)
                                image_files.append(img_path)

                                print(f"\n\n🖼️ --- Image Received ({mime_type}) ---")
                                display(Image(data=image_data))
                                print("--- End Image ---\n")
                            elif hasattr(part,'text') and part.text:
                                print(part.text, end="")
                                story_text += part.text
                                # Check for image descriptions
                                if "**Image Description:**" in part.text:
                                    contains_image_description = True
                        except json.decoder.JSONDecodeError as je:
                            print(f"\n⚠️ JSON decoding error in chunk: {je}")
                            json_errors += 1
                            if json_errors >= max_json_errors:
                                print(f"Too many JSON errors ({json_errors}), falling back to non-streaming mode...")
                                # Try to extract any text that might be in the raw response
                                try:
                                    if hasattr(chunk, '_response') and hasattr(chunk._response, 'text'):
                                        raw_text = chunk._response.text
                                        # Extract text content between markdown or code blocks if possible
                                        story_text += re.sub(r'```.*?```', '', raw_text, flags=re.DOTALL)
                                        print(f"Extracted {len(raw_text)} characters from raw response")
                                except Exception:
                                    pass
                                break  # Exit the streaming loop and use the fallback
                            continue  # Skip this chunk and continue with next
                        except Exception as e:
                            print(f"\n⚠️ Error processing chunk: {e}")
                            continue  # Skip this chunk and continue with next
                except Exception as e:
                    print(f"⚠️ Error in stream processing: {e}")
                    # If streaming failed completely, try the non-streaming fallback
                    if not story_text.strip() and json_errors > 0:
                        print("Stream processing failed, trying non-streaming fallback...")
                        try:
                            response = client.models.generate_content(
                                model=model,
                                contents=contents,
                                config=generate_content_config,
                            )

                            if response.candidates and response.candidates[0].content:
                                for part in response.candidates[0].content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        story_text += part.text

                            print("✅ Non-streaming fallback successful")
                        except Exception as fallback_error:
                            print(f"⚠️ Non-streaming fallback also failed: {fallback_error}")
        except Exception as e:
            print(f"⚠️ Error in stream creation: {e}")
            return

        print("\n" + "-"*20)
        if not image_found:
             print("⚠️ No images were found in the stream.")
        print("✅ Stream processing complete.")

        if not image_found or contains_image_description:
            if contains_image_description:
                print("\n⚠️ Model generated text descriptions instead of actual images. Restarting generation...")
                # Restart the entire generation process by recursively calling generate
                return generate(use_prompt_generator=use_prompt_generator, prompt_input=prompt_input)
            elif not image_found:
                print("⚠️ No images were found in the stream.")
        print("✅ Stream processing complete.")
