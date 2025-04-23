import random
import string
from colorama import Fore, Back, Style, init
import time
import os
from tqdm import tqdm
import math

# Initialize colorama
init(autoreset=True)

def display_banner():
    print(Fore.CYAN + r"""
   ___                      _     _____                           _             
  / _ \ _ __ __ _ _ __ __ _| |   /__   \___  __ _ _ __ ___  ___| |_ ___ _ __ 
 / /_)/| '__/ _` | '__/ _` | |     / /\/ _ \/ _` | '__/ __|/ _ \ __/ _ \ '__|
/ ___/ | | | (_| | | | (_| | |    / / |  __/ (_| | |  \__ \  __/ ||  __/ |   
\/     |_|  \__,_|_|  \__,_|_|    \/   \___|\__,_|_|  |___/\___|\__\___|_|   
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + "="*60 + Style.RESET_ALL)
    print(Fore.GREEN + "Advanced Password Generator v2.0 (2025)" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*60 + Style.RESET_ALL + "\n")

def generate_random_words(prefix, min_length, max_length, count, custom_chars, complexity):
    words = []
    char_sets = {
        '1': string.ascii_lowercase,
        '2': string.ascii_letters,
        '3': string.ascii_letters + string.digits,
        '4': string.ascii_letters + string.digits + "!@#$%^&*",
        '5': string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?~"
    }
    
    charset = custom_chars if custom_chars else char_sets.get(complexity, char_sets['4'])
    
    with tqdm(total=count, desc=Fore.BLUE + "Generating Passwords" + Style.RESET_ALL, 
              bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Style.RESET_ALL)) as pbar:
        for _ in range(count):
            random_length = random.randint(min_length - len(prefix), max_length - len(prefix))
            random_part = ''.join(random.choice(charset) for _ in range(random_length))
            word = prefix + random_part
            words.append(word)
            pbar.update(1)
            time.sleep(0.01)  # Small delay for visual effect
    
    return words, charset

def save_to_file(words, filename):
    try:
        with open(filename, 'w') as file:
            for word in words:
                file.write(word + '\n')
        return True
    except Exception as e:
        print(Fore.RED + f"\nError saving file: {e}" + Style.RESET_ALL)
        return False

def show_stats(words, charset):
    avg_length = sum(len(word) for word in words) / len(words)
    char_count = len(charset)
    possible_combinations = sum(char_count**i for i in range(min(len(word) for word in words), max(len(word) for word in words) + 1))
    
    print(Fore.MAGENTA + "\n=== Generation Statistics ===" + Style.RESET_ALL)
    print(Fore.CYAN + f"Total passwords generated: {len(words)}")
    print(f"Average length: {avg_length:.2f} characters")
    print(f"Shortest password: {min(len(word) for word in words)} chars")
    print(f"Longest password: {max(len(word) for word in words)} chars")
    print(f"Character set size: {char_count} unique characters")
    print(f"Possible combinations: ~{possible_combinations:.2e}" + Style.RESET_ALL)
    print(Fore.MAGENTA + "="*30 + Style.RESET_ALL)

def preview_passwords(words, sample_size=5):
    print(Fore.YELLOW + "\n=== Password Samples ===" + Style.RESET_ALL)
    for i, word in enumerate(words[:sample_size]):
        colored_pwd = ''
        for char in word:
            if char in string.ascii_uppercase:
                colored_pwd += Fore.GREEN + char
            elif char in string.ascii_lowercase:
                colored_pwd += Fore.BLUE + char
            elif char in string.digits:
                colored_pwd += Fore.YELLOW + char
            else:
                colored_pwd += Fore.RED + char
        print(f"{i+1}. {colored_pwd}{Style.RESET_ALL}")
    
    if len(words) > sample_size:
        print(Fore.CYAN + f"\n... and {len(words)-sample_size} more" + Style.RESET_ALL)

def get_complexity_level():
    print(Fore.CYAN + "\nSelect complexity level:" + Style.RESET_ALL)
    print(Fore.GREEN + "1. Lowercase letters only")
    print("2. Upper and lowercase letters")
    print("3. Letters + numbers")
    print("4. Letters + numbers + basic symbols (!@#$%^&*)")
    print("5. Letters + numbers + extended symbols" + Style.RESET_ALL)
    
    while True:
        choice = input(Fore.YELLOW + "Enter choice (1-5, default 4): " + Style.RESET_ALL) or '4'
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print(Fore.RED + "Invalid choice. Please enter 1-5." + Style.RESET_ALL)

def main():
    display_banner()
    
    try:
        prefix = input(Fore.YELLOW + "Enter the fixed prefix (or leave blank for fully random passwords): " + Style.RESET_ALL)
        min_length = int(input(Fore.YELLOW + "Enter the minimum length of the password: " + Style.RESET_ALL))
        max_length = int(input(Fore.YELLOW + "Enter the maximum length of the password: " + Style.RESET_ALL))
        count = int(input(Fore.YELLOW + "Enter the number of passwords to generate: " + Style.RESET_ALL))
        filename = input(Fore.YELLOW + "Enter the filename to save the passwords: " + Style.RESET_ALL)
        
        complexity = get_complexity_level()
        
        custom_chars = input(Fore.YELLOW + "Enter specific characters to use (or leave blank to use selected complexity): " + Style.RESET_ALL)
        
        if min_length > max_length:
            print(Fore.RED + "Error: Minimum length cannot be greater than maximum length." + Style.RESET_ALL)
            return
        if min_length < len(prefix):
            print(Fore.RED + f"Error: Minimum length ({min_length}) cannot be less than prefix length ({len(prefix)})." + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + "\nStarting password generation..." + Style.RESET_ALL)
        words, charset = generate_random_words(prefix, min_length, max_length, count, custom_chars, complexity)
        
        if save_to_file(words, filename):
            print(Fore.GREEN + f"\nSuccessfully saved {count} passwords to '{filename}'" + Style.RESET_ALL)
            show_stats(words, charset)
            
            preview = input(Fore.YELLOW + "\nWould you like to preview some passwords? (y/n): " + Style.RESET_ALL).lower()
            if preview == 'y':
                preview_passwords(words)
            
            print(Fore.GREEN + "\nPassword generation complete!" + Style.RESET_ALL)
    
    except ValueError:
        print(Fore.RED + "Error: Please enter valid numbers for length and count." + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.RED + "\nOperation cancelled by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
