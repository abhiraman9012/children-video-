                    # Run the enhanced command
                    try:
                        result = subprocess.run(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                        print("u2705 Enhanced video with effects created successfully!")
                    except subprocess.CalledProcessError as e:
                        # If enhanced command fails, try the fallback
                        print("u26a0ufe0f Enhanced video creation failed, trying fallback method...")
                        print(f"Error: {e.stderr.decode() if hasattr(e.stderr, 'decode') else str(e)}")
                        result = subprocess.run(
                            [
                                'ffmpeg', '-y',
                                '-f', 'concat',
                                '-safe', '0',
                                '-i', image_list_path,
                                '-i', audio_path,
                                '-c:v', 'libx264',
                                '-c:a', 'aac',
                                '-pix_fmt', 'yuv420p',
                                '-shortest',
                                output_path
                            ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                        print("u2705 Video created successfully with basic method")

                    print(f"u2705 Video created at: {output_path}")
                    # Display the video
                    print("ud83cudfac Playing the created video:")
                    display(HTML(f"""
                    <video width="640" height="360" controls>
                        <source src="file://{output_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    """))

                    # Save video to Google Drive using the API rather than mounting
                    # The API-based saving functionality is implemented below outside of this function
                    print("\n--- Video will be saved to Google Drive using API ---")
                    print("ud83dudca1 Check the output below for Google Drive upload status")

                    # Add option to download directly in the notebook
                    try:
                        print("\n--- Download Video ---")
                        # Get file size in MB
                        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

                        if file_size_mb < 50:  # Only try data URL method for files under 50MB
                            with open(output_path, "rb") as video_file:
                                video_data = video_file.read()
                                b64_data = base64.b64encode(video_data).decode()
                                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                display(HTML(f"""
                                <a href="data:video/mp4;base64,{b64_data}"
                                   download="gemini_story_{timestamp}.mp4"
                                   style="
                                       display: inline-block;
                                       padding: 10px 20px;
                                       background-color: #4CAF50;
                                       color: white;
                                       text-decoration: none;
                                       border-radius: 5px;
                                       font-weight: bold;
                                       margin-top: 10px;
                                   ">
                                   Download Video ({file_size_mb:.1f} MB)
                                </a>
                                """))
                        else:
                            print("u26a0ufe0f Video file is too large for direct download in notebook.")
                            print(f"Video size: {file_size_mb:.1f} MB")
                            print("Please download it from the location shown above.")
                    except Exception as e:
                        print(f"u26a0ufe0f Could not create download button: {e}")
                        print("Please download the video from the path shown above.")

                except subprocess.CalledProcessError as e:
                    print(f"ud83duded1 Error creating video: {e}")
                    print(f"FFmpeg stderr: {e.stderr.decode()}")

                    # If FFmpeg is not installed or fails, just display the images
                    print("\nu26a0ufe0f Video creation failed. Displaying images instead:")
                    for img_path in resized_images:
                        display(Image(filename=img_path))
            else:
                print("u26a0ufe0f No images available for video creation.")

    except Exception as e:
        print(f"\nud83duded1 An error occurred during streaming or processing: {e}")
        import traceback
        traceback.print_exc()
