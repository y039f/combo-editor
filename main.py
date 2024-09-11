import os
import random
import time
import platform
import re
from datetime import datetime
from colorama import Fore, Style, init

class ComboEditor:
    def __init__(self):
        self.check_dependencies()
        init(autoreset=True)
        self.page = 1
        self.modules = [
            ("Remove Duplicates", self.remove_duplicates),
            ("Remove Empty Lines", self.remove_empty),
            ("Split (Email Split)", lambda x: self.split_lines(x, split_by='@')),
            ("Split (Pass Split)", lambda x: self.split_lines(x, split_by=':')),
            ("Randomize Lines", self.randomize_lines),
            ("Reverse Lines", self.reverse_lines),
            ("Extract Emails", self.extract_emails),
            ("Extract Passwords", self.extract_passwords),
            ("Mask Passwords", self.mask_passwords),
            ("Check Valid Emails", self.check_valid_emails),
            ("Extract LOGIN:PASS", self.extract_login_pass)
        ]
        self.clear_console()
        self.print_ascii()
        self.filename = self.choose_file()
        if self.filename:
            with open(self.filename, "r", encoding="utf-8", errors="ignore") as file:
                self.lines = [line.rstrip() for line in file if line.strip()]
            self.update_console_title()
            self.run()

    def check_dependencies(self):
        try:
            import colorama
        except ImportError:
            print("Missing dependencies. Please install required packages using: pip install -r requirements.txt")
            exit()

    def clear_console(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def print_ascii(self):
        print(f'''{Style.BRIGHT}{Fore.MAGENTA}
                                                          
 ____   ____  _____      _____      _____        ______   
|    | |    ||\    \    /    /| ___|\    \   ___|\     \  
|    | |    || \    \  /    / ||    |\    \ |     \     \ 
|    |_|    ||  \____\/    /  /|    | |    ||     ,_____/|
|    .-.    | \ |    /    /  / |    |/____/||     \--'\_|/
|    | |    |  \|___/    /  /  |    ||    |||     /___/|  
|    | |    |      /    /  /   |    ||____|/|     \____|\ 
|____| |____|     /____/  /    |____|       |____ '     /|
|    | |    |    |`    | /     |    |       |    /_____/ |
|____| |____|    |_____|/      |____|       |____|     | /
  \(     )/         )/           \(           \( |_____|/ 
   '     '          '             '            '    )/        0.1
                                                    '    
            {Fore.YELLOW} Combo Editor - github.com/y039f           
                                                      
            {Fore.MAGENTA}Discord      {Fore.LIGHTBLACK_EX}|{Fore.WHITE} discord.gg/DBMBPdeqZm
            {Fore.MAGENTA}Telegram     {Fore.LIGHTBLACK_EX}|{Fore.WHITE} @pasjonatyk
        ''')

    def choose_file(self):
        files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.txt')]
        if not files:
            print(f"{Fore.RED}No text files found in the current directory.")
            return None

        print(f"{Fore.MAGENTA}[?] {Fore.WHITE}Available text files: \n")

        for i, file in enumerate(files, start=1):
            print(f"{Fore.MAGENTA}{i} > {Fore.WHITE}{file}")
        try:
            choice = int(input(f"\n{Fore.MAGENTA}[?] {Fore.WHITE}File: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                print(f"{Fore.RED}Invalid choice. Please select a valid file number.")
                return None
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")
            return None

    def update_console_title(self):
        lines_count = len(self.lines)
        title = f"Loaded {lines_count} lines (email:password)"
        if platform.system() == "Windows":
            os.system(f"title {title}")
        else:
            print(f"\33]0;{title}\a", end='', flush=True)

    def remove_duplicates(self, lines):
        return list(dict.fromkeys(lines))

    def remove_empty(self, lines):
        return [line for line in lines if line.strip()]

    def split_lines(self, lines, split_by=':'):
        try:
            return [line.split(split_by)[0] for line in lines]
        except Exception as e:
            print(f"{Fore.RED}Error splitting lines: {e}")
            return lines

    def randomize_lines(self, lines):
        random.shuffle(lines)
        return lines

    def reverse_lines(self, lines):
        return lines[::-1]

    def extract_emails(self, lines):
        try:
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            return [line for line in lines if re.search(email_pattern, line)]
        except Exception as e:
            print(f"{Fore.RED}Error extracting emails: {e}")
            return lines

    def extract_passwords(self, lines):
        try:
            return [line.split(':')[1] if ':' in line else line.split('@')[1] if '@' in line else line for line in lines]
        except Exception as e:
            print(f"{Fore.RED}Error extracting passwords: {e}")
            return lines

    def mask_passwords(self, lines):
        masked = []
        for line in lines:
            try:
                if ':' in line:
                    email, password = line.split(':', 1)
                    masked.append(f"{email}: {'*' * len(password.strip())}")
                else:
                    masked.append(line)
            except Exception as e:
                print(f"{Fore.RED}Error masking passwords: {e}")
                masked.append(line)
        return masked

    def check_valid_emails(self, lines):
        try:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return [line for line in lines if re.match(email_pattern, line.split(':')[0])]
        except Exception as e:
            print(f"{Fore.RED}Error checking valid emails: {e}")
            return lines

    def extract_login_pass(self, lines):
        result = []
        for line in lines:
            try:
                parts = line.split(':')
                if len(parts) == 3:
                    result.append(f"{parts[1]}:{parts[2]}")
            except Exception as e:
                print(f"{Fore.RED}Error extracting LOGIN:PASS: {e}")
        return result

    def download_output(self, lines):
        try:
            timestamp = datetime.now().strftime("%d-%H-%M")
            folder_path = os.path.join("result", timestamp)
            os.makedirs(folder_path, exist_ok=True)
            filename = os.path.join(folder_path, "output.txt")
            with open(filename, "w") as file:
                file.write("\n".join(lines))
            print(f"{Fore.GREEN}Output saved to {filename}")
        except Exception as e:
            print(f"{Fore.RED}Error saving output: {e}")

    def display_message(self, message, delay=2):
        print(f"{Fore.GREEN}{message}")
        time.sleep(delay)
        self.clear_console()

    def display_menu(self):
        self.clear_console()
        self.print_ascii()
        total_pages = (len(self.modules) + 4) // 5
        start_index = (self.page - 1) * 5
        end_index = start_index + 5
        current_modules = self.modules[start_index:end_index]

        print(f"{Fore.MAGENTA}< Previous Page [{self.page}/{total_pages}] Next Page >\n")
        for i, (name, _) in enumerate(current_modules, start=1):
            print(f"{Fore.MAGENTA}[{i}] {Fore.WHITE}{name}")
        print("\n")
        print(f"{Fore.YELLOW}[*] {Fore.LIGHTBLACK_EX}Download Output")
        print(f"{Fore.RED}[!] {Fore.LIGHTBLACK_EX}Exit\n")

    def run(self):
        while True:
            self.display_menu()
            choice = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Choose an option: ")

            if choice == "<" and self.page > 1:
                self.page -= 1
            elif choice == ">" and self.page < (len(self.modules) + 4) // 5:
                self.page += 1
            elif choice == "*":
                self.download_output(self.lines)
                self.display_message("Output downloaded.")
            elif choice == "!":
                self.display_message("Exiting...", delay=1)
                break
            elif choice.isdigit():
                choice = int(choice)
                current_modules = self.modules[(self.page - 1) * 5: self.page * 5]

                if 1 <= choice <= len(current_modules):
                    name, func = current_modules[choice - 1]
                    self.lines = func(self.lines)
                    self.update_console_title()
                    self.display_message(f"{name} executed.")
                else:
                    self.display_message("Invalid choice. Please try again.", delay=1)
            else:
                self.display_message("Invalid input. Please try again.", delay=1)

if __name__ == "__main__":
    ComboEditor()
