                    # Define transition effects for connecting scenes
                    transition_effects = [
                        # 6. Fade In/Out - smooth transition
                        lambda i, duration: f"[v{i}e]fade=t=in:st=0:d=0.7,fade=t=out:st={duration-0.7}:d=0.7[f{i}];",

                        # 7. Slide In/Out - moves from a direction
                        lambda i, duration: f"[v{i}e]fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.6}:d=0.6[f{i}];",

                        # 12. Blur In/Out - start blurred, sharpen over time
                        lambda i, duration: f"[v{i}e]boxblur=10:enable='lt(t,0.8)':t=max(0,1-t/{0.8})',fade=t=in:st=0:d=0.3,fade=t=out:st={duration-0.5}:d=0.5[f{i}];",

                        # 13. Glitch Effect - quick jitter & distortion
                        lambda i, duration: f"[v{i}e]hue='n*2':enable='if(lt(mod(t,1),0.1),1,0)',fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.6}:d=0.6[f{i}];",
                    ]

                    # Create combined effects pool
                    all_effects = motion_effects

                    for i in range(len(resized_images)):
                        # Add scale filter to ensure consistent size
                        filter_complex.append(f"[{i}:v]scale=1920:1080,setsar=1[v{i}];")

                        # Randomly select effects based on image count
                        # If we have N images, each image gets one of N randomly selected effects
                        total_images = len(resized_images)

                        # Calculate number of effects to use - equal to number of images
                        num_effects_to_use = min(total_images, len(all_effects))

                        # Create a deterministic but varied effect selection based on image position
                        # This ensures each image gets a different effect while maintaining consistency
                        # across multiple runs with the same number of images
                        random.seed(i + 42)  # Seed based on image position for deterministic variation
                        effect_index = i % len(all_effects)  # Cycle through effects based on image position

                        # Apply the selected effect - still maintains story flow with varied effects
                        filter_complex.append(all_effects[effect_index](i))
                        random.seed()  # Reset seed for other random selections

                    # Apply transitions with storytelling intent - keep this part of the story-driven approach
                    for i in range(len(resized_images)):
                        # Transition selection based on story position
                        story_position = i / len(resized_images)

                        if i == 0:
                            # First image just needs fade in
                            filter_complex.append(f"[v{i}e]fade=t=in:st=0:d=0.5[f{i}];") 
                        else:
                            # Select transition based on story position
                            if story_position < 0.3:
                                transition_index = 0  # Fade for beginning
                            elif story_position < 0.7:
                                transition_index = 1  # Slide for middle
                            elif story_position < 0.9:
                                transition_index = 2  # Blur for climax
                            else:
                                transition_index = 3  # Glitch for resolution/finale

                            # Apply the selected transition
                            filter_complex.append(transition_effects[transition_index % len(transition_effects)](i, image_duration))

                    # Create concatenation string
                    concat_str = ""
                    for i in range(len(resized_images)):
                        concat_str += f"[f{i}]"
                    concat_str += f"concat=n={len(resized_images)}:v=1:a=0[outv]"
                    filter_complex.append(concat_str)

                    # Join all filters
                    filter_complex_str = ''.join(filter_complex)

                    # Build input files list
                    input_files = []
                    for img in resized_images:
                        input_files.extend(['-loop', '1', '-t', str(image_duration), '-i', img])

                    # Create complete FFmpeg command with Frei0r
                    cmd = [
                        'ffmpeg', '-y',
                    ] + input_files + [
                        '-i', audio_path,
                        '-filter_complex', filter_complex_str,
                        '-map', '[outv]',
                        '-map', '1:a',
                        '-c:v', 'libx264',
                        '-preset', 'slow',  # Better quality encoding
                        '-crf', '18',       # High quality (lower is better, 18-23 is good range)
                        '-c:a', 'aac',
                        '-b:a', '192k',     # Higher audio bitrate
                        '-pix_fmt', 'yuv420p',
                        '-shortest',
                        '-r', '30',         # Increased framerate for smoother motion
                        output_path
                    ]
