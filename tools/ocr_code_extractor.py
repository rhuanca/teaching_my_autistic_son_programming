#!/usr/bin/env python3
"""
OCR Code Extractor
Extracts FMSLogo code from screenshots using OCR (Optical Character Recognition)
"""

import cv2
import pytesseract
import numpy as np
from PIL import Image
import re
import sys
import os
import argparse

class CodeOCR:
    def __init__(self):
        # Common FMSLogo commands to help with OCR accuracy
        self.known_commands = [
            'CS', 'CLEARSCREEN',
            'FD', 'FORWARD', 'BK', 'BACKWARD', 'BACK',
            'RT', 'RIGHT', 'LT', 'LEFT',
            'PU', 'PENUP', 'PD', 'PENDOWN',
            'HOME', 'PENCOLOR'
        ]
        
        # Common colors
        self.known_colors = [
            'RED', 'BLUE', 'GREEN', 'YELLOW', 'BLACK', 'WHITE',
            'ORANGE', 'PURPLE', 'PINK', 'BROWN', 'GRAY'
        ]
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR accuracy"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get better contrast
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Remove noise with morphological operations
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Scale image for better OCR (make it larger)
            height, width = processed.shape
            scale_factor = 3
            processed = cv2.resize(processed, (width * scale_factor, height * scale_factor), 
                                 interpolation=cv2.INTER_CUBIC)
            
            return processed
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def extract_text(self, image_path):
        """Extract text from image using OCR"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            if processed_img is None:
                return None
            
            # OCR configuration for better code recognition
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
            
            # Extract text
            text = pytesseract.image_to_string(processed_img, config=custom_config)
            
            return text
            
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
    
    def clean_code(self, raw_text):
        """Clean and format extracted text into proper FMSLogo commands (more permissive, multiple per line)"""
        if not raw_text:
            return ""
        lines = raw_text.split('\n')
        cleaned_commands = []
        for line in lines:
            line = line.strip().upper()
            if not line:
                continue
            words = line.split()
            i = 0
            while i < len(words):
                word = self.fix_common_ocr_errors(words[i])
                if word in self.known_commands:
                    command = word
                    # Look for a number after the command
                    if i + 1 < len(words):
                        next_word = words[i + 1]
                        numbers = re.findall(r'\d+', next_word)
                        if numbers:
                            command += f" {numbers[0]}"
                            i += 1  # Skip the number
                    cleaned_commands.append(command)
                elif word == 'PENCOLOR' and i + 1 < len(words):
                    color = self.fix_color_ocr_errors(words[i + 1].upper())
                    if color in self.known_colors:
                        cleaned_commands.append(f"PENCOLOR {color}")
                        i += 1  # Skip the color
                i += 1
        return '\n'.join(cleaned_commands)
    
    def fix_common_ocr_errors(self, word):
        """Fix common OCR recognition errors"""
        # Common OCR mistakes for programming commands
        fixes = {
            'FO': 'FD',     # F0 -> FD
            'F0': 'FD',     # F0 -> FD
            'FT': 'FD',     # FT -> FD
            'RD': 'FD',     # RD -> FD
            'FID': 'FD',    # FID -> FD
            'LD': 'FD',     # LD -> FD
            'FR': 'FD',     # FR -> FD
            'PTU': 'RT',    # Common RT mistakes
            'RI': 'RT',     # RI -> RT
            'HT': 'RT',     # HT -> RT
            'LI': 'LT',     # LI -> LT
            'IT': 'LT',     # IT -> LT
            'CI': 'CS',     # CI -> CS
            'GS': 'CS',     # GS -> CS
            'C5': 'CS',     # C5 -> CS
            'PU1': 'PU',    # PU1 -> PU
            'P0': 'PD',     # P0 -> PD
            'PO': 'PD',     # PO -> PD
        }
        
        return fixes.get(word, word)
    
    def fix_color_ocr_errors(self, color):
        """Fix common OCR errors for color names"""
        fixes = {
            'REO': 'RED',
            'RLUE': 'BLUE',
            'BLUF': 'BLUE',
            'GRFEN': 'GREEN',
            'GREIN': 'GREEN',
            'YELLQW': 'YELLOW',
            'YELLUW': 'YELLOW',
            'BLACX': 'BLACK',
            'WHITT': 'WHITE',
            'QRANGE': 'ORANGE',
            'PURPIE': 'PURPLE',
        }
        
        return fixes.get(color, color)
    
    def process_screenshot(self, image_path, output_file=None):
        """Main function to process screenshot and extract FMSLogo code"""
        print(f"🔍 Processing screenshot: {image_path}")
        
        # Extract raw text
        raw_text = self.extract_text(image_path)
        if not raw_text:
            print("❌ Failed to extract text from image")
            return None
        
        print("📝 Raw OCR text:")
        print("-" * 40)
        print(raw_text)
        print("-" * 40)
        
        # Clean and format code
        cleaned_code = self.clean_code(raw_text)
        
        print("\n✨ Cleaned FMSLogo code:")
        print("-" * 40)
        print(cleaned_code)
        print("-" * 40)
        
        # Save to file if requested
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(cleaned_code)
                print(f"\n💾 Code saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving file: {e}")
        
        return cleaned_code

def main():
    parser = argparse.ArgumentParser(description='Extract FMSLogo code from screenshots')
    parser.add_argument('image', help='Path to screenshot image file')
    parser.add_argument('-o', '--output', help='Output file to save extracted code')
    parser.add_argument('--copy', action='store_true', help='Copy result to clipboard (requires pyperclip)')
    
    args = parser.parse_args()
    
    # Check if image file exists
    if not os.path.exists(args.image):
        print(f"❌ Error: Image file not found: {args.image}")
        sys.exit(1)
    
    # Initialize OCR
    ocr = CodeOCR()
    
    # Process screenshot
    code = ocr.process_screenshot(args.image, args.output)
    
    if code:
        # Copy to clipboard if requested
        if args.copy:
            try:
                import pyperclip
                pyperclip.copy(code)
                print("\n📋 Code copied to clipboard!")
            except ImportError:
                print("\n💡 Install pyperclip to enable clipboard copying: pip install pyperclip")
        
        print(f"\n🎉 Success! Extracted {len(code.split())} lines of code")
        print("\n💡 You can now paste this code into the evaluator:")
        print("   python tools/fmslogo_evaluator.py")
    else:
        print("\n❌ Failed to extract any valid FMSLogo code")
        print("\n💡 Tips for better results:")
        print("   - Ensure screenshot is clear and high resolution")
        print("   - Commands should be clearly visible")
        print("   - Try taking screenshot with better contrast")

if __name__ == "__main__":
    main()
