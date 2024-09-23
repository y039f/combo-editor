import os
import random
import platform
import re
from datetime import datetime
from collections import Counter
import csv
import json
import colorama
from colorama import Fore, Style, init
from pystyle import Center, Colors, Colorate
import logging
import pickle

class ComboEditor:
    def __init__(self):
        self.check_dependencies()
        init(autoreset=True)
        self.page = 1
        self.history = []
        self.modules = [
            ("Remove Duplicates", self.remove_duplicates, "Removes duplicate lines."),
            ("Remove Empty Lines", self.remove_empty, "Removes empty lines."),
            ("Split (Email Split)", lambda x: self.split_lines(x, split_by='@'), "Splits lines at '@' and keeps the first part."),
            ("Split (Pass Split)", lambda x: self.split_lines(x, split_by=':'), "Splits lines at ':' and keeps the first part."),
            ("Randomize Lines", self.randomize_lines, "Randomly shuffles the lines."),
            ("Reverse Lines", self.reverse_lines, "Reverses the order of the lines."),
            ("Extract Emails", self.extract_emails, "Extracts valid email addresses from the lines."),
            ("Extract Passwords", self.extract_passwords, "Extracts passwords from lines in 'email:password' format."),
            ("Mask Passwords", self.mask_passwords, "Replaces passwords with asterisks."),
            ("Check Valid Emails", self.check_valid_emails, "Keeps only lines with valid email addresses."),
            ("Extract LOGIN:PASS", self.extract_login_pass, "Extracts 'login:password' pairs from lines."),
            ("Extract URL Logs", self.extract_url_logs, "Extracts login and password from URL logs."),
            ("Preview Lines", self.preview_lines, "Shows a preview of the first few lines."),
            ("Export As", self.export_as, "Exports the lines to a file."),
            ("Filter by Domain", self.filter_by_domain, "Keeps only lines with a specific email domain."),
            ("Find and Replace", self.find_and_replace, "Finds and replaces text in the lines."),
            ("Show Statistics", self.show_statistics, "Displays statistics about the lines."),
            ("Remove Specific Lines", self.remove_specific_lines, "Removes lines matching a specific pattern.")
        ]
        self.clear_console()
        self.print_ascii()
        self.setup_logging()
        self.filename = self.choose_file()
        if self.filename:
            self.load_file()
            self.update_console_title()
            self.run()

    def check_dependencies(self):
        try:
            import pystyle
            import colorama
        except ImportError:
            print("Missing dependencies. Please install required packages using: pip install pystyle colorama")
            exit()

    def setup_logging(self):
        logging.basicConfig(filename='combo_editor.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def clear_console(self):
        os.system('cls' if platform.system() == "Windows" else 'clear')

    def print_ascii(self):
        ascii_art = '''
        
 ██░ ██▓██   ██▓ ██▓███  ▓█████ 
▓██░ ██▒▒██  ██▒▓██░  ██▒▓█   ▀ 
▒██▀▀██░ ▒██ ██░▓██░ ██▓▒▒███   
░▓█ ░██  ░ ▐██▓░▒██▄█▓▒ ▒▒▓█  ▄ 
░▓█▒░██▓ ░ ██▒▓░▒██▒ ░  ░░▒████▒
 ▒ ░░▒░▒  ██▒▒▒ ▒▓▒░ ░  ░░░ ▒░ ░
 ▒ ░▒░ ░▓██ ░▒░ ░▒ ░      ░ ░  ░
 ░  ░░ ░▒ ▒ ░░  ░░          ░   
 ░  ░  ░░ ░                 ░  ░  0.2
        ░ ░                     

[/] Combo Editor - github.com/y039f

[/] Discord      | discord.gg/DBMBPdeqZm
[/] Telegram     | @pasjonatyk
[/] Cracked      | cracked.io/hypedfs
        '''
        colored_ascii = Colorate.Horizontal(Colors.blue_to_purple,(ascii_art))
        print(colored_ascii)

    def choose_file(self):
        files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.txt')]
        if not files:
            print(f"{Fore.RED}No text files found in the current directory.")
            return None

        print(f"{Fore.MAGENTA}[?] {Fore.WHITE}Available text files:\n")
        for i, file in enumerate(files, start=1):
            print(f"{Fore.MAGENTA}{i} > {Fore.WHITE}{file}")
        try:
            choice = int(input(f"\n{Fore.MAGENTA}[?] {Fore.WHITE}Select a file by number: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                print(f"{Fore.RED}Invalid choice. Please select a valid file number.")
                return None
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number.")
            return None

    def load_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8", errors="ignore") as file:
                self.lines = [line.rstrip() for line in file if line.strip()]
            self.history.append(self.lines.copy())
            logging.info(f"Loaded file {self.filename} with {len(self.lines)} lines.")
        except Exception as e:
            print(f"{Fore.RED}Error loading file: {e}")
            logging.error(f"Error loading file: {e}")
            self.lines = []

    def update_console_title(self):
        lines_count = len(self.lines)
        title = f"Hype / Loaded {lines_count} lines"
        if platform.system() == "Windows":
            os.system(f"title {title}")
        else:
            print(f"\33]0;{title}\a", end='', flush=True)

    def save_session(self):
        try:
            with open('session.pkl', 'wb') as f:
                pickle.dump(self.lines, f)
            print(f"{Fore.GREEN}Session saved successfully.")
            logging.info("Session saved.")
        except Exception as e:
            print(f"{Fore.RED}Error saving session: {e}")
            logging.error(f"Error saving session: {e}")

    def load_session(self):
        try:
            with open('session.pkl', 'rb') as f:
                self.lines = pickle.load(f)
            self.history.append(self.lines.copy())
            print(f"{Fore.GREEN}Session loaded successfully.")
            logging.info("Session loaded.")
        except Exception as e:
            print(f"{Fore.RED}Error loading session: {e}")
            logging.error(f"Error loading session: {e}")

    def undo_last_action(self):
        if len(self.history) > 1:
            self.history.pop()
            self.lines = self.history[-1].copy()
            print(f"{Fore.GREEN}Undid the last action.")
            logging.info("Undid the last action.")
        else:
            print(f"{Fore.YELLOW}No actions to undo.")
            logging.info("No actions to undo.")

    def remove_duplicates(self, lines):
        original_count = len(lines)
        lines = list(dict.fromkeys(lines))
        removed = original_count - len(lines)
        print(f"{Fore.GREEN}Removed {removed} duplicates.")
        logging.info(f"Removed {removed} duplicates.")
        return lines

    def remove_empty(self, lines):
        original_count = len(lines)
        lines = [line for line in lines if line.strip()]
        removed = original_count - len(lines)
        print(f"{Fore.GREEN}Removed {removed} empty lines.")
        logging.info(f"Removed {removed} empty lines.")
        return lines

    def split_lines(self, lines, split_by=':'):
        try:
            lines = [line.split(split_by)[0] for line in lines if split_by in line]
            print(f"{Fore.GREEN}Lines split by '{split_by}'.")
            logging.info(f"Lines split by '{split_by}'.")
            return lines
        except Exception as e:
            print(f"{Fore.RED}Error splitting lines: {e}")
            logging.error(f"Error splitting lines: {e}")
            return lines

    def randomize_lines(self, lines):
        random.shuffle(lines)
        print(f"{Fore.GREEN}Lines randomized.")
        logging.info("Lines randomized.")
        return lines

    def reverse_lines(self, lines):
        lines = lines[::-1]
        print(f"{Fore.GREEN}Lines reversed.")
        logging.info("Lines reversed.")
        return lines

    def extract_emails(self, lines):
        try:
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = [line for line in lines if re.search(email_pattern, line)]
            print(f"{Fore.GREEN}Extracted {len(emails)} emails.")
            logging.info(f"Extracted {len(emails)} emails.")
            return emails
        except Exception as e:
            print(f"{Fore.RED}Error extracting emails: {e}")
            logging.error(f"Error extracting emails: {e}")
            return lines

    def extract_passwords(self, lines):
        try:
            passwords = []
            for line in lines:
                if ':' in line:
                    passwords.append(line.split(':', 1)[1])
                elif '@' in line:
                    passwords.append(line.split('@', 1)[1])
            print(f"{Fore.GREEN}Extracted {len(passwords)} passwords.")
            logging.info(f"Extracted {len(passwords)} passwords.")
            return passwords
        except Exception as e:
            print(f"{Fore.RED}Error extracting passwords: {e}")
            logging.error(f"Error extracting passwords: {e}")
            return lines

    def mask_passwords(self, lines):
        masked = []
        for line in lines:
            try:
                if ':' in line:
                    email, password = line.split(':', 1)
                    masked.append(f"{email}:{'*' * len(password.strip())}")
                else:
                    masked.append(line)
            except Exception as e:
                print(f"{Fore.RED}Error masking passwords: {e}")
                logging.error(f"Error masking passwords: {e}")
                masked.append(line)
        print(f"{Fore.GREEN}Passwords masked.")
        logging.info("Passwords masked.")
        return masked

    def check_valid_emails(self, lines):
        try:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            valid_emails = [line for line in lines if re.match(email_pattern, line.split(':')[0])]
            removed = len(lines) - len(valid_emails)
            print(f"{Fore.GREEN}Removed {removed} invalid emails.")
            logging.info(f"Removed {removed} invalid emails.")
            return valid_emails
        except Exception as e:
            print(f"{Fore.RED}Error checking valid emails: {e}")
            logging.error(f"Error checking valid emails: {e}")
            return lines

    def extract_login_pass(self, lines):
        result = []
        for line in lines:
            try:
                parts = line.split(':')
                if len(parts) >= 3:
                    result.append(f"{parts[1]}:{parts[2]}")
            except Exception as e:
                print(f"{Fore.RED}Error extracting LOGIN:PASS: {e}")
                logging.error(f"Error extracting LOGIN:PASS: {e}")
        print(f"{Fore.GREEN}Extracted {len(result)} LOGIN:PASS pairs.")
        logging.info(f"Extracted {len(result)} LOGIN:PASS pairs.")
        return result



    def extract_url_logs(self, lines):
        """Extracts login and passwords from logs containing URLs and/or email:password."""
        result = []
        
        # Definiujemy ogólny regex do dopasowania email i password oddzielonych | ; : lub spacją
        pattern = re.compile(
            r'([A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+)\s*[|;:]\s*([^|;:\s]+)'
        )
        
        # Dodatkowy regex do dopasowania email i password oddzielonych spacją bez | ; :
        pattern_space = re.compile(
            r'([A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+)\s+([^|;:\s]+)'
        )
        
        for line in lines:
            line = line.strip()
            email = None
            password = None
            
            # Próba dopasowania wzorca z separatorami | ; :
            match = pattern.search(line)
            if match:
                email = match.group(1)
                password = match.group(2)
                result.append(f"{email}:{password}")
                continue  # Przejdź do następnej linii
            
            # Próba dopasowania wzorca ze spacją jako separatorem
            match = pattern_space.search(line)
            if match:
                email = match.group(1)
                password = match.group(2)
                result.append(f"{email}:{password}")
                continue  # Przejdź do następnej linii
            
            # Jeśli linia nie pasuje do powyższych wzorców, sprawdź, czy jest w formacie email:password
            if ':' in line:
                parts = line.split(':', 2)  # Maksymalnie podziel na 3 części
                if len(parts) == 2:
                    email_candidate, password_candidate = parts
                    # Walidacja formatu email
                    if re.match(r'^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$', email_candidate):
                        email = email_candidate
                        password = password_candidate
                        result.append(f"{email}:{password}")
                        continue
            
            # Jeśli linia nie pasuje do żadnego wzorca, zaloguj ostrzeżenie
            logging.warning(f"Unknown format: {line}")
        
        print(f"{Fore.GREEN}Extracted {len(result)} login:password pairs from logs.")
        logging.info(f"Extracted {len(result)} login:password pairs from logs.")
        return result



    def export_as(self, lines):
        print(f"{Fore.MAGENTA}[Export As] {Fore.WHITE}Choose export format:")
        print(f"{Fore.MAGENTA}1 > {Fore.WHITE}TXT")
        print(f"{Fore.MAGENTA}2 > {Fore.WHITE}CSV")
        print(f"{Fore.MAGENTA}3 > {Fore.WHITE}JSON")
        choice = input(f"\n{Fore.MAGENTA}[?] {Fore.WHITE}Select format (1-3): ")

        if choice == '1':
            self.export_txt(lines)
        elif choice == '2':
            self.export_csv(lines)
        elif choice == '3':
            self.export_json(lines)
        else:
            print(f"{Fore.RED}Invalid choice. Export cancelled.")
            self.display_message("")

    def export_txt(self, lines):
        try:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            folder_path = os.path.join("result", timestamp)
            os.makedirs(folder_path, exist_ok=True)
            filename = os.path.join(folder_path, "output.txt")
            with open(filename, "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            print(f"{Fore.GREEN}TXT export successful: {filename}")
            logging.info(f"TXT export successful: {filename}")
        except Exception as e:
            print(f"{Fore.RED}Error exporting TXT: {e}")
            logging.error(f"Error exporting TXT: {e}")

    def export_csv(self, lines):
        try:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            folder_path = os.path.join("result", timestamp)
            os.makedirs(folder_path, exist_ok=True)
            filename = os.path.join(folder_path, "output.csv")
            with open(filename, "w", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Email", "Password"])
                for line in lines:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        writer.writerow([parts[0], parts[1]])
            print(f"{Fore.GREEN}CSV export successful: {filename}")
            logging.info(f"CSV export successful: {filename}")
        except Exception as e:
            print(f"{Fore.RED}Error exporting CSV: {e}")
            logging.error(f"Error exporting CSV: {e}")

    def export_json(self, lines):
        try:
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            folder_path = os.path.join("result", timestamp)
            os.makedirs(folder_path, exist_ok=True)
            filename = os.path.join(folder_path, "output.json")
            data = []
            for line in lines:
                parts = line.split(':')
                if len(parts) >= 2:
                    data.append({"email": parts[0], "password": parts[1]})
            with open(filename, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=4)
            print(f"{Fore.GREEN}JSON export successful: {filename}")
            logging.info(f"JSON export successful: {filename}")
        except Exception as e:
            print(f"{Fore.RED}Error exporting JSON: {e}")
            logging.error(f"Error exporting JSON: {e}")

    def filter_by_domain(self, lines):
        domain = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Enter the domain to filter by (e.g., gmail.com): ").strip().lower()
        if not domain:
            print(f"{Fore.RED}No domain entered. Operation cancelled.")
            self.display_message("")
            return lines
        filtered = [line for line in lines if line.lower().endswith(f"@{domain}")]
        removed = len(lines) - len(filtered)
        print(f"{Fore.GREEN}Filtered out {removed} lines not matching the domain '{domain}'.")
        logging.info(f"Filtered out {removed} lines not matching the domain '{domain}'.")
        return filtered

    def find_and_replace(self, lines):
        find_str = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Enter the string to find: ").strip()
        replace_str = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Enter the string to replace with: ").strip()
        if not find_str:
            print(f"{Fore.RED}Find string is empty. Operation cancelled.")
            self.display_message("")
            return lines
        replaced = [line.replace(find_str, replace_str) for line in lines]
        print(f"{Fore.GREEN}Replaced all occurrences of '{find_str}' with '{replace_str}'.")
        logging.info(f"Replaced all occurrences of '{find_str}' with '{replace_str}'.")
        return replaced

    def show_statistics(self, lines):
        total = len(lines)
        unique = len(set(lines))
        emails = [line.split(':')[0] for line in lines if ':' in line]
        domains = [email.split('@')[-1] for email in emails]
        domain_counts = Counter(domains)

        stats = f'''
--- Statistics ---
Total lines      : {total}
Unique lines     : {unique}
Total emails     : {len(emails)}
Unique emails    : {len(set(emails))}

Domains distribution:
'''
        for domain, count in domain_counts.most_common(20):
            stats += f"  {domain} [{count}]\n"
        if len(domain_counts) > 20:
            remaining = len(domain_counts) - 20
            stats += f"  + and {remaining} more\n"
        print(f"{Fore.GREEN}{stats}")
        logging.info("Displayed statistics.")
        self.display_message("")
        return lines

    def remove_specific_lines(self, lines):
        criteria = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Enter the substring or regex pattern to remove lines: ").strip()
        if not criteria:
            print(f"{Fore.RED}No criteria entered. Operation cancelled.")
            self.display_message("")
            return lines
        try:
            pattern = re.compile(criteria)
            filtered = [line for line in lines if not pattern.search(line)]
            removed = len(lines) - len(filtered)
            print(f"{Fore.GREEN}Removed {removed} lines matching the criteria.")
            logging.info(f"Removed {removed} lines matching the criteria '{criteria}'.")
            return filtered
        except re.error as e:
            print(f"{Fore.RED}Invalid regex pattern: {e}. Operation cancelled.")
            logging.error(f"Invalid regex pattern: {e}.")
            self.display_message("")
            return lines

    def help_menu(self):
        print(f"{Fore.GREEN}--- Help Menu ---\n")
        for i, (name, _, description) in enumerate(self.modules, start=1):
            print(f"{Fore.MAGENTA}[{i}] {Fore.WHITE}{name}: {Fore.LIGHTBLACK_EX}{description}")
        print(f"{Fore.MAGENTA}[@] {Fore.WHITE}Undo Last Action")
        print(f"{Fore.MAGENTA}[M] {Fore.WHITE}Manage Session")
        print(f"{Fore.MAGENTA}[?] {Fore.WHITE}Help")
        print(f"{Fore.RED}[!] {Fore.WHITE}Exit")
        self.display_message("")

    def manage_session(self):
        while True:
            print(f"{Fore.MAGENTA}--- Manage Session ---")
            print(f"{Fore.MAGENTA}[1] {Fore.WHITE}Save Session")
            print(f"{Fore.MAGENTA}[2] {Fore.WHITE}Load Session")
            print(f"{Fore.MAGENTA}[0] {Fore.WHITE}Back to Main Menu")
            choice = input(f"\n{Fore.MAGENTA}[?] {Fore.WHITE}Choose an option: ")

            if choice == '1':
                self.save_session()
                self.display_message("")
            elif choice == '2':
                self.load_session()
                self.display_message("")
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")
                self.display_message("")

    def display_message(self, message="", delay=2):
        if message:
            print(f"{Fore.GREEN}{message}")
        input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Press Enter to continue...")

    def display_menu(self):
        total_pages = (len(self.modules) + 4) // 6
        start_index = (self.page - 1) * 6
        end_index = start_index + 6
        current_modules = self.modules[start_index:end_index]

        # Additional options
        additional_options = [
            (Fore.YELLOW + "[*]", Fore.WHITE + "Export As"),
            (Fore.BLUE + "[#]", Fore.WHITE + "Load New File"),
            (Fore.CYAN + "[@]", Fore.WHITE + "Undo Last Action"),
            (Fore.MAGENTA + "[M]", Fore.WHITE + "Manage Session"),
            (Fore.CYAN + "[?]", Fore.WHITE + "Help"),
            (Fore.RED + "[!]", Fore.WHITE + "Exit")
        ]

        # Prepare module and option strings
        module_strings = []
        for i, (name, _, _) in enumerate(current_modules, start=1):
            module_strings.append(f"{Fore.MAGENTA}[{i}] {Fore.WHITE}{name}")

        option_strings = [f"{symbol} {description}" for symbol, description in additional_options]

        max_lines = max(len(module_strings), len(option_strings))
        print(f"{Fore.WHITE}[<] {Fore.MAGENTA} Previous Page {Fore.WHITE}[{self.page}/{total_pages}] {Fore.MAGENTA}Next Page {Fore.WHITE} [>]\n")

        for i in range(max_lines):
            module_str = module_strings[i] if i < len(module_strings) else ""
            option_str = option_strings[i] if i < len(option_strings) else ""
            print(f"{module_str:<40}{option_str}")

        print("\n")

    def preview_lines(self, lines):
        preview_count = min(10, len(lines))
        print(f"{Fore.GREEN}Previewing first {preview_count} lines:")
        print(f"{Fore.CYAN}" + "-"*50)
        for i in range(preview_count):
            print(f"{Fore.WHITE}{lines[i]}")
        print(f"{Fore.CYAN}" + "-"*50)
        self.display_message("")

    def run(self):
        while True:
            self.clear_console()
            self.print_ascii()
            self.update_console_title()
            self.display_menu()
            choice = input(f"{Fore.MAGENTA}[?] {Fore.WHITE}Choose an option: ")

            if choice == "<" and self.page > 1:
                self.page -= 1
            elif choice == ">" and self.page < (len(self.modules) + 4) // 5:
                self.page += 1
            elif choice == "*" :
                self.export_as(self.lines)
            elif choice == "#":
                self.filename = self.choose_file()
                if self.filename:
                    self.load_file()
                    self.update_console_title()
                    self.display_message("New file loaded.")
            elif choice == "@":
                self.undo_last_action()
                self.display_message("")
            elif choice.upper() == "M":
                self.manage_session()
            elif choice == "?":
                self.help_menu()
            elif choice == "!":
                self.display_message("Exiting...", delay=1)
                logging.info("Exiting application.")
                break
            elif choice.isdigit():
                choice = int(choice)
                current_modules = self.modules[(self.page - 1) * 6: self.page * 6]

                if 1 <= choice <= len(current_modules):
                    name, func, _ = current_modules[choice - 1]
                    original_count = len(self.lines)
                    try:
                        self.lines = func(self.lines)
                        self.history.append(self.lines.copy())
                        self.update_console_title()
                        if len(self.lines) != original_count:
                            print(f"{Fore.GREEN}{name} executed. Lines changed from {original_count} to {len(self.lines)}.")
                        else:
                            print(f"{Fore.GREEN}{name} executed.")
                        logging.info(f"Executed {name}.")
                        self.display_message("Operation completed.")
                    except Exception as e:
                        print(f"{Fore.RED}An error occurred during '{name}': {e}")
                        logging.error(f"Error during '{name}': {e}")
                        self.display_message("")
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.")
                    self.display_message("")
            else:
                print(f"{Fore.RED}Invalid input. Please try again.")
                self.display_message("")

if __name__ == "__main__":
    ComboEditor()
