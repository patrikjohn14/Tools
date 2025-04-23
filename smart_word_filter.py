#!/usr/bin/env python3
import os
import math
import chardet
from tqdm import tqdm

def detect_encoding(file_path):
    """Detect file encoding automatically"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Read sample for faster detection
    result = chardet.detect(raw_data)
    return result['encoding']

def filter_words(input_file, min_length=8):
    """Filter words by minimum length"""
    encoding = detect_encoding(input_file)
    print(f"[+] Detected encoding: {encoding}")
    
    with open(input_file, 'r', encoding=encoding, errors='ignore') as f:
        words = [word.strip() for word in f if len(word.strip()) >= min_length]
    
    return words

def split_and_save(words, output_dir, num_parts):
    """Split list into multiple files"""
    os.makedirs(output_dir, exist_ok=True)
    total_words = len(words)
    words_per_file = math.ceil(total_words / num_parts)
    
    for part in tqdm(range(num_parts), desc="Splitting files"):
        start_idx = part * words_per_file
        end_idx = start_idx + words_per_file
        part_words = words[start_idx:end_idx]
        
        output_file = os.path.join(output_dir, f"part_{part+1}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(part_words))
    
    print(f"[+] Successfully split into {num_parts} files in '{output_dir}'")

def main():
    print("""
    ███████╗██╗  ██╗██████╗ ██╗████████╗███████╗██████╗ 
    ██╔════╝╚██╗██╔╝██╔══██╗██║╚══██╔══╝██╔════╝██╔══██╗
    █████╗   ╚███╔╝ ██████╔╝██║   ██║   █████╗  ██████╔╝
    ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║   ██╔══╝  ██╔══██╗
    ███████╗██╔╝ ██╗██║     ██║   ██║   ███████╗██║  ██║
    ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    """)

    # User input
    input_file = input("[?] Path to wordlist file: ").strip()
    output_dir = input("[?] Output directory (will be created): ").strip()
    num_parts = int(input("[?] Number of parts to split into: "))
    min_length = int(input("[?] Minimum word length (default 8): ") or "8")

    # File validation
    if not os.path.isfile(input_file):
        print(f"[!] Error: File '{input_file}' not found!")
        return

    # Processing
    try:
        print("\n[+] Filtering words...")
        filtered_words = filter_words(input_file, min_length)
        
        print(f"[+] Found {len(filtered_words)} words (length >= {min_length})")
        
        if not filtered_words:
            print("[!] No words remaining after filtering!")
            return
            
        print("[+] Splitting files...")
        split_and_save(filtered_words, output_dir, num_parts)
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    main()
