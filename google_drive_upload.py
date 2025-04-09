    # --- Google Drive API Integration ---
    if output_path and os.path.exists(output_path):
        try:
            print("\n--- Saving Video to Google Drive using API ---")

            # Import necessary libraries for Google Drive API
            try:
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload
                from google.oauth2 import service_account
                import io
                import json

                # Download and use credentials from Google Drive link instead of hardcoding them
                credentials_file_id = "152LtocR_Lvll37IW3GXJWAowLS02YBF2"
                credentials_file_path = os.path.join(temp_dir, "drive_credentials.json")
                
                print("u23f3 Downloading Google Drive API credentials from the provided link...")
                try:
                    # Function to download file by ID from Google Drive without authentication
                    def download_file_from_google_drive(file_id, destination):
                        import requests
                        
                        # Create the direct download URL
                        url = f"https://drive.google.com/uc?id={file_id}&export=download"
                        
                        # Make the initial request to get the download link
                        session = requests.Session()
                        response = session.get(url, stream=True)
                        
                        # Handle potential confirmation page (for large files)
                        for key, value in response.cookies.items():
                            if key.startswith('download_warning'):
                                url = f"{url}&confirm={value}"
                                response = session.get(url, stream=True)
                        
                        # Save the file
                        with open(destination, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=32768):
                                if chunk:
                                    f.write(chunk)
                        
                        return destination
                    
                    # Download the credentials file
                    download_file_from_google_drive(credentials_file_id, credentials_file_path)
                    print(f"u2705 Credentials file downloaded to: {credentials_file_path}")
                    
                    # Set up credentials from the downloaded file
                    credentials = service_account.Credentials.from_service_account_file(
                        credentials_file_path,
                        scopes=['https://www.googleapis.com/auth/drive']
                    )
                    print("u2705 Successfully loaded credentials from downloaded file")
                    
                except Exception as e:
                    print(f"u26a0ufe0f Error downloading or loading credentials: {e}")
                    print("Attempting to continue with alternative methods...")
                    raise

                drive_service = build('drive', 'v3', credentials=credentials)

                # Create main folder if it doesn't exist
                main_folder_name = 'GeminiStories'
                main_folder_id = None

                # Check if main folder exists
                query = f"name='{main_folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
                results = drive_service.files().list(q=query).execute()
                items = results.get('files', [])

                if not items:
                    # Create main folder
                    print(f"Creating main folder '{main_folder_name}'...")
                    folder_metadata = {
                        'name': main_folder_name,
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    main_folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
                    main_folder_id = main_folder.get('id')
                else:
                    main_folder_id = items[0]['id']

                print(f"u2705 Using main folder: {main_folder_name} (ID: {main_folder_id})")

                # Generate a timestamp for the folder name
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                story_folder_name = f"{timestamp}_story"

                # Create a folder for this story
                story_folder_metadata = {
                    'name': story_folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [main_folder_id]
                }

                story_folder = drive_service.files().create(body=story_folder_metadata, fields='id').execute()
                story_folder_id = story_folder.get('id')
                print(f"u2705 Created story folder: {story_folder_name} (ID: {story_folder_id})")

                # Generate SEO metadata if needed
                if 'metadata' not in locals() or not metadata:
                    metadata = generate_seo_metadata(story_text, image_files, prompt_text)

                # Generate thumbnail if needed
                if 'thumbnail_path' not in locals() or not thumbnail_path:
                    thumbnail_path = generate_thumbnail(image_files, story_text, metadata)

                # Upload video
                print("u23f3 Uploading video to Google Drive...")
                video_metadata = {
                    'name': 'video.mp4',
                    'parents': [story_folder_id]
                }

                media = MediaFileUpload(output_path, mimetype='video/mp4', resumable=True)
                video_file = drive_service.files().create(
                    body=video_metadata,
                    media_body=media,
                    fields='id'
                ).execute()

                print(f"u2705 Video uploaded successfully (File ID: {video_file.get('id')})")

                # Helper function to upload text files to Google Drive
                def upload_text_file_to_drive(content, filename, parent_folder_id):
                    """Upload a text file to Google Drive using a temporary file approach.
                    
                    Args:
                        content: The text content to upload
                        filename: The name of the file in Google Drive
                        parent_folder_id: The ID of the parent folder
                        
                    Returns:
                        The file ID of the uploaded file
                    """
                    # Create file metadata
                    file_metadata = {
                        'name': filename,
                        'parents': [parent_folder_id]
                    }
                    
                    # Create a temporary file
                    temp_file_path = os.path.join(temp_dir, filename)
                    with open(temp_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Upload the file directly
                    file_media = MediaFileUpload(temp_file_path, mimetype='text/plain', resumable=False)
                    file = drive_service.files().create(
                        body=file_metadata,
                        media_body=file_media,
                        fields='id'
                    ).execute()
                    
                    return file.get('id')
                
                # Upload metadata files
                # Title
                title_content = metadata['title']
                title_file_id = upload_text_file_to_drive(title_content, 'title.txt', story_folder_id)

                # Description
                desc_content = metadata['description']
                desc_file_id = upload_text_file_to_drive(desc_content, 'description.txt', story_folder_id)

                # Tags
                tags_content = '\n'.join(metadata['tags'])
                tags_file_id = upload_text_file_to_drive(tags_content, 'tags.txt', story_folder_id)

                # Upload thumbnail if available
                if thumbnail_path and os.path.exists(thumbnail_path):
                    thumb_metadata = {
                        'name': 'thumbnail.jpg',
                        'parents': [story_folder_id]
                    }

                    thumb_media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg', resumable=True)
                    thumb_file = drive_service.files().create(
                        body=thumb_metadata,
                        media_body=thumb_media,
                        fields='id'
                    ).execute()

                    print(f"u2705 Thumbnail uploaded successfully (File ID: {thumb_file.get('id')})")

                # Get a direct link to the folder
                folder_link = f"https://drive.google.com/drive/folders/{story_folder_id}"
                print(f"\nu2705 All files uploaded successfully to Google Drive!")
                print(f"ud83dudcc1 Folder link: {folder_link}")

                # Display a summary of the uploaded content
                print("\n--- Upload Summary ---")
                print(f"• Video: video.mp4")
                print(f"• Title: {metadata['title']}")
                print(f"• Description: {len(metadata['description'])} characters")
                print(f"• Tags: {len(metadata['tags'])} tags")
                if thumbnail_path and os.path.exists(thumbnail_path):
                    print(f"• Thumbnail: thumbnail.jpg")
                    
                # Important: Completely stop execution after successful upload
                print("\nu2705u2705u2705 Upload to Google Drive successful! Script execution will stop now to prevent unnecessary retries.")
                print("ud83duded1 Terminating script execution...")
                
                # Force exit the script with success code
                import sys
                sys.exit(0)

            except ImportError as ie:
                print(f"u26a0ufe0f Required libraries for Google Drive API not installed: {ie}")
                print("ud83dudca1 To use Google Drive API, install these packages:")
                print("   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2")
                print("\nud83dudca1 You can manually download the video from the temporary location:")
                print(f"   {output_path}")

        except Exception as e:
            print(f"u26a0ufe0f Error uploading to Google Drive: {e}")
            print("ud83dudca1 You can manually download the video from the temporary location:")
            print(f"   {output_path}")
