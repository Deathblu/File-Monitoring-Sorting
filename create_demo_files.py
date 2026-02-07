#!/usr/bin/env python3
"""
Demo Script for Smart File Sorter
Creates sample files for testing the application
"""

import os
import random
from pathlib import Path

def create_demo_files(output_dir="demo_files"):
    """Create sample files for testing"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Creating demo files in: {output_dir}/")
    print("=" * 50)
    
    # Sample file types
    files_to_create = {
        "Images": [
            "vacation_photo.jpg",
            "screenshot.png",
            "diagram.svg",
            "icon.ico"
        ],
        "Documents": [
            "report.pdf",
            "letter.docx",
            "budget.xlsx",
            "presentation.pptx",
            "notes.txt"
        ],
        "Videos": [
            "tutorial.mp4",
            "movie.mkv",
            "clip.avi"
        ],
        "Audio": [
            "song.mp3",
            "podcast.wav",
            "recording.m4a"
        ],
        "Archives": [
            "backup.zip",
            "archive.rar",
            "compressed.7z"
        ],
        "Code": [
            "script.py",
            "webpage.html",
            "styles.css",
            "app.js",
            "data.json"
        ]
    }
    
    # Create sample content
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00"  # PNG header
    text_content = "This is a sample file created by the demo script.\n"
    
    total_files = 0
    
    for category, filenames in files_to_create.items():
        print(f"\n{category}:")
        for filename in filenames:
            filepath = os.path.join(output_dir, filename)
            
            # Determine content based on file type
            ext = Path(filename).suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp']:
                content = image_content
                mode = 'wb'
            else:
                content = f"Sample {category} file: {filename}\n" + text_content
                mode = 'w'
            
            # Write file
            with open(filepath, mode) as f:
                f.write(content)
            
            print(f"  ✓ Created: {filename}")
            total_files += 1
    
    # Create some duplicate files for testing duplicate detection
    print(f"\nDuplicates (for testing):")
    duplicates = [
        ("duplicate_photo.jpg", image_content, 'wb'),
        ("duplicate_doc.txt", text_content, 'w'),
    ]
    
    for filename, content, mode in duplicates:
        # Create original
        original_path = os.path.join(output_dir, filename)
        with open(original_path, mode) as f:
            f.write(content)
        
        # Create duplicate with different name
        dup_name = f"copy_of_{filename}"
        dup_path = os.path.join(output_dir, dup_name)
        with open(dup_path, mode) as f:
            f.write(content)
        
        print(f"  ✓ Created: {filename} and {dup_name}")
        total_files += 2
    
    print("\n" + "=" * 50)
    print(f"✅ Created {total_files} demo files!")
    print(f"\nNext steps:")
    print(f"1. Run the File Sorter: python file_sorter.py")
    print(f"2. Browse to the '{output_dir}' folder")
    print(f"3. Click 'Organize Now' to see it in action!")
    print(f"4. Try 'Start Monitoring' and add new files to the folder")

if __name__ == "__main__":
    create_demo_files()
