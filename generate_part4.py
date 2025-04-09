            # Create video from images and audio
            print("\n--- Creating Video from Images and Audio ---")
            print("⏳ Creating video...")

            # Prepare images for FFMPEG
            # First, ensure all images are the same size (1920x1080) for YouTube HD quality
            # Then we'll downscale to 1280x720 for the final thumbnail with better quality
            resized_images = []
            for idx, img_path in enumerate(image_files):
                img = PILImage.open(img_path)
                # Use high-quality resizing with antialiasing for best quality
                resized_img = img.resize((1920, 1080), PILImage.LANCZOS)
                resized_path = os.path.join(temp_dir, f"resized_{idx}.jpg")
                # Save with high quality (95%)
                resized_img.save(resized_path, quality=95, optimize=True)
                resized_images.append(resized_path)

            # Create a text file listing all images for FFMPEG
            image_list_path = os.path.join(temp_dir, "image_list.txt")

            # Calculate approximate duration based on audio file
            try:
                # Use ffprobe to get audio duration if ffmpeg is available
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                audio_duration = float(result.stdout.strip())
            except Exception:
                # Fallback duration estimation
                if 'bark_audio_success' in locals() and bark_audio_success:
                    audio_duration = len(combined_audio) / SAMPLE_RATE
                else:
                    # gTTS fallback
                    word_count = len(story_text.split())
                    audio_duration = word_count * 0.5  # rough estimate

            # Calculate duration for each image
            if len(resized_images) > 0:
                image_duration = audio_duration / len(resized_images)

                # Create the image list file with durations
                with open(image_list_path, 'w') as f:
                    for img_path in resized_images:
                        f.write(f"file '{img_path}'\n")
                        f.write(f"duration {image_duration}\n")
                    # Write the last image path again (required by FFMPEG)
                    f.write(f"file '{resized_images[-1]}'\n")

                # Output video path
                output_path = os.path.join(temp_dir, "story_video.mp4")

                # Use advanced FFMPEG command with Frei0r effects
                print("⏳ Running FFmpeg with Frei0r effects for enhanced storytelling...")
                try:
                    # Create complex filter string for each image with effects
                    filter_complex = []

                    # Import random for selecting effects randomly
                    import random

                    # Define simple motion effects for storytelling enhancement
                    # Each effect is designed to work well with static images
                    motion_effects = [
                        # 1. Zoom In effect - slowly enlarges the image (Ken Burns effect)
                        lambda i: f"[v{i}]zoompan=z='min(zoom+0.0015,1.4)':d={int(image_duration*25)}:s=1920x1080[v{i}e];",

                        # 2. Pan Left/Right - moves horizontally across the image
                        lambda i: f"[v{i}]zoompan=z=1.2:x='iw/2-(iw/zoom/2)+((iw/zoom/2)/100)*n':d={int(image_duration*25)}:s=1920x1080[v{i}e];",

                        # 3. Pan Up/Down - moves vertically across the image
                        lambda i: f"[v{i}]zoompan=z=1.2:y='ih/2-(ih/zoom/2)+sin(n/120)*100':d={int(image_duration*25)}:s=1920x1080[v{i}e];",

                        # 4. Shake/Jitter - adds micro-movements for handheld camera feel
                        lambda i: f"[v{i}]zoompan=z=1.01:x='iw/2-(iw/zoom/2)+sin(n*5)*10':y='ih/2-(ih/zoom/2)+cos(n*5)*10':d={int(image_duration*25)}:s=1920x1080[v{i}e];",

                        # 5. Tilt - slight angular rotation
                        lambda i: f"[v{i}]rotate='0.02*sin(n/30)':fillcolor=black:c=bilinear:s=1920x1080[v{i}e];",

                        # 8. Rotate - subtle rotation to mimic dynamic camera
                        lambda i: f"[v{i}]rotate='0.01*sin(n/40)':fillcolor=black:c=bilinear:s=1920x1080[v{i}e];",

                        # 9. Scale Bounce - light zoom in/out bounce loop
                        lambda i: f"[v{i}]zoompan=z='1.05+0.05*sin(n/25)':d={int(image_duration*25)}:s=1920x1080[v{i}e];",

                        # 14. Color Pulse - subtle brightness shifts
                        lambda i: f"[v{i}]curves=all='0/0 0.5/0.55 1/1'[v{i}e];",

                        # 15. Zoom with Rotation - slight zoom while spinning slowly
                        lambda i: f"[v{i}]zoompan=z='min(zoom+0.001,1.2)':d={int(image_duration*25)}:s=1920x1080,rotate='0.008*n':fillcolor=black:c=bilinear[v{i}e];",
                    ]
