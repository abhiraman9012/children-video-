    # --- Direct Download Option ---
    # Skip this section if we already uploaded to Google Drive
    # This section is only for when Google Drive upload was not available or failed
    if 'drive_service' not in locals() and output_path and os.path.exists(output_path):
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
        try:
            print("u26a0ufe0f Video file is too large for direct download in notebook.")
            print(f"Video size: {file_size_mb:.1f} MB")
            print("Please download it from the location shown above.")
        except Exception as e:
            print(f"u26a0ufe0f Could not create download button: {e}")
            print("Please download the video from the path shown above.")
