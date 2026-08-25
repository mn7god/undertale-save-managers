import re
import os
import base64
import shutil
from pick import pick
from time import sleep
from pathlib import Path
from subprocess import run, Popen
from InquirerPy import inquirer
from colorama import just_fix_windows_console
from InquirerPy.validator import PathValidator, EmptyInputValidator

## Variables and console settings
just_fix_windows_console()

file_last_bytes = b'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/Pg0KPGFzc2VtYmx5IHhtbG5zPSJ1cm46c2NoZW1hcy1taWNyb3NvZnQtY29tOmFzbS52MSIgbWFuaWZlc3RWZXJzaW9uPSIxLjAiIHhtbG5zOmFzbXYzPSJ1cm46c2NoZW1hcy1taWNyb3NvZnQtY29tOmFzbS52MyI+PGFzc2VtYmx5SWRlbnRpdHkgdmVyc2lvbj0iMS4wLjAuMCIgcHJvY2Vzc29yQXJjaGl0ZWN0dXJlPSIqIiBuYW1lPSJZb1lvR2FtZXMuR2FtZU1ha2VyLlJ1bm5lciIgdHlwZT0id2luMzIiPjwvYXNzZW1ibHlJZGVudGl0eT48ZGVzY3JpcHRpb24+R2FtZU1ha2VyIEMrKyBDb3JlIFJ1bm5lci48L2Rlc2NyaXB0aW9uPjxkZXBlbmRlbmN5PjxkZXBlbmRlbnRBc3NlbWJseT48YXNzZW1ibHlJZGVudGl0eSB0eXBlPSJ3aW4zMiIgbmFtZT0iTWljcm9zb2Z0LldpbmRvd3MuQ29tbW9uLUNvbnRyb2xzIiB2ZXJzaW9uPSI2LjAuMC4wIiBwcm9jZXNzb3JBcmNoaXRlY3R1cmU9IioiIHB1YmxpY0tleVRva2VuPSI2NTk1YjY0MTQ0Y2NmMWRmIiBsYW5ndWFnZT0iKiI+PC9hc3NlbWJseUlkZW50aXR5PjwvZGVwZW5kZW50QXNzZW1ibHk+PC9kZXBlbmRlbmN5Pjx0cnVzdEluZm8geG1sbnM9InVybjpzY2hlbWFzLW1pY3Jvc29mdC1jb206YXNtLnYzIj48c2VjdXJpdHk+PHJlcXVlc3RlZFByaXZpbGVnZXM+PHJlcXVlc3RlZEV4ZWN1dGlvbkxldmVsIGxldmVsPSJhc0ludm9rZXIiIHVpQWNjZXNzPSJmYWxzZSI+PC9yZXF1ZXN0ZWRFeGVjdXRpb25MZXZlbD48L3JlcXVlc3RlZFByaXZpbGVnZXM+PC9zZWN1cml0eT48L3RydXN0SW5mbz48YXNtdjM6YXBwbGljYXRpb24+PGFzbXYzOndpbmRvd3NTZXR0aW5ncyB4bWxucz0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS9TTUkvMjAwNS9XaW5kb3dzU2V0dGluZ3MiPjxkcGlBd2FyZT50cnVlPC9kcGlBd2FyZT48L2FzbXYzOndpbmRvd3NTZXR0aW5ncz48L2FzbXYzOmFwcGxpY2F0aW9uPjwvYXNzZW1ibHk+'
game_exec_path = None
user_uty_save_path = None

user_game_exe_path_info1 = Path(os.getenv("USERPROFILE"),"UTY_Save_Manager_Files","Main_Data.dat").resolve()
user_game_save_path_info1 = Path(os.getenv("USERPROFILE"),"UTY_Save_Manager_Files","Main1_Data.dat").resolve()
user_game_save_backup = Path(os.getenv("USERPROFILE"),"UTY_Save_Manager_Files","Backup").resolve()
user_game_save_backup_file = Path(os.getenv("USERPROFILE"),"UTY_Save_Manager_Files","Backup","Save.sav").resolve()
user_game_exe_path = Path(os.getenv("USERPROFILE"),"UTY_Save_Manager_Files").resolve()
user_base_path = str(Path(os.getenv("USERPROFILE")).resolve())

default_path = Path(os.getenv("LOCALAPPDATA"), "Undertale_Yellow").expanduser().resolve()
default_save_file = str(Path(os.getenv("LOCALAPPDATA"), "Undertale_Yellow", "Save.sav").expanduser().resolve())

RED = "\033[91m"        
GREEN = "\033[92m"   
DARK_GREEN = "\033[2;49;32m" 
WHITE = "\033[4;49;97m"      
WHITE_4 = "\033[1;49;39m"
YELLOW = "\033[93m"
BLUE = "\033[0;94m"     
PURPLE = "\033[0;95m"   
CYAN = "\033[0;96m"
NEGATIVE = "\033[7m"
RESET = "\033[0m"
GRAY = "\033[2;49;37m"
GRAY_2 = "\033[2;49;39m"
WHITE_LINE = "\033[4;49;97m"
DARK_GREEN_LINE = "\033[4;49;32m"

tags = { 
    'Save.sav': 
        [
            '[NPCs]', 
            '[Talks]', 
            '[GenoComplete]', 
            'Accessory=', 
            'MAXSP=', 
            'room=', 
            '[DBox]'
        ],
        
    'Controls.sav':
        [
            '[Controls]',
            'X=',
            'Y=',
            'Z='
        ],
        
    'Save02.sav':
        [
            '[Deaths]',
            '[00]',
        ]
}

## FUNCTIONS

def adjust_cmd_prompt():
    """Adjusts cmd prompt for better experience."""
    os.system("mode con: cols=101 lines=28")
    os.system("title Undertale Yellow Save Manager")
    
def check_tags(paths: list[Path], tag_dict: dict):
    """Search in 3 uty files specific tags to validate save authenticity."""
    results = {}
    for p in paths:
        if p.name in ('Save02.sav','Save.sav','Controls.sav'):
            rep = [p.name, 0]
            data = p.read_text()
            for item in tag_dict[p.name]:
                if item in data:
                    rep[1] += 1
                    
            if rep[1] not in (7,2,3):
                results[p.name] = False
            
            else:
                results[p.name] = True
            
    return results
    
def check_tags_single(path: Path, tag_dict: dict):
    """Validate only 'Save.sav' authenticity."""
    if path.name == 'Save.sav':
        rep = [path.name, 0]
        data = path.read_text()
        for item in tag_dict[path.name]:
            if item in data:
                rep[1] += 1
                
        if rep[1] == 7:
            return True
        
        return False

def uty_exe_verify(path: Path):
    """Verifies if last 1120 bytes of uty executable are valid and compare in runtime with specific string."""
    with open(path, 'rb') as f:
        data = f.read()[-1121::]
        
    if base64.b64decode(file_last_bytes) in data:
        return True
        
    return False
    
def check_user_game_exe_path():
    """Checks all uty save manager important files/directories."""
    if not user_game_exe_path.exists():
        user_game_exe_path.mkdir(parents=True, exist_ok=True)
        
    if not user_game_save_backup.exists():
        user_game_save_backup.mkdir(parents=True, exist_ok=True)
        
    if not user_game_exe_path_info1.exists():
        with open(str(user_game_exe_path_info1), 'w') as f:
            f.write("")
        
    if not user_game_save_path_info1.exists():
        with open(str(user_game_save_path_info1), 'w') as f2:
            f2.write("")
            
def write_on_file(file_path: Path, data: str):
    """Writes(or overwrites) specific path with a new content."""
    with open(file_path, 'w') as file:
        file.write(data)

def check_game_exe_path():
    """Check game executable path and if it is valid."""
    global game_exec_path
    check_user_game_exe_path()
    if game_exec_path == None:
        try:
            with open(str(user_game_exe_path_info1), 'r') as f:
                data = f.read().splitlines()[0].strip()
            
            if uty_exe_verify(Path(data)):
                game_exec_path = Path(data)
                
        except Exception as e:
            return             

def check_game_save_path():
    """Check if uty custom saves path exists."""
    global user_uty_save_path
    check_user_game_exe_path()
    if user_uty_save_path == None:
        try:
            with open(str(user_game_save_path_info1), 'r') as f:
                data = f.read().splitlines()[0].strip()
                
            if Path(data).is_dir() and Path(data).exists(): 
                user_uty_save_path = Path(data)
                
        except Exception as e:
            return             

def banner():
    """Banner just for UI."""
    adjust_cmd_prompt()
    os.system("cls")
    print(f"""{YELLOW} ▄• ▄▌▄▄▄▄▄ ▄· ▄▌{RESET}    .▄▄ ·  ▄▄▄·  ▌ ▐·▄▄▄ .    • ▌ ▄ ·.  ▄▄▄·  ▐ ▄  ▄▄▄·  ▄▄ • ▄▄▄ .▄▄▄  
{YELLOW} █▪██▌•██  ▐█▪██▌{RESET}    ▐█ ▀. ▐█ ▀█ ▪█·█▌▀▄.▀·    ·██ ▐███▪▐█ ▀█ •█▌▐█▐█ ▀█ ▐█ ▀ ▪▀▄.▀·▀▄ █·
{YELLOW} █▌▐█▌ ▐█.▪▐█▌▐█▪{RESET}    ▄▀▀▀█▄▄█▀▀█ ▐█▐█•▐▀▀▪▄    ▐█ ▌▐▌▐█·▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄▐▀▀▄ 
{YELLOW} ▐█▄█▌ ▐█▌· ▐█▀·.{RESET}    ▐█▄▪▐█▐█ ▪▐▌ ███ ▐█▄▄▌    ██ ██▌▐█▌▐█ ▪▐▌██▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
{YELLOW}  ▀▀▀  ▀▀▀   ▀ •{RESET}      ▀▀▀▀  ▀  ▀ . ▀   ▀▀▀     ▀▀  █▪▀▀▀ ▀  ▀ ▀▀ █▪ ▀  ▀ ·▀▀▀▀  ▀▀▀ .▀  ▀{RESET}""")
        
def extract_tags(save_path: Path):
    """Extracts every useful tag in specific 'Save.sav' file type."""
    s_data = save_path.read_text()
    save_data = s_data.splitlines()
    data_tags = [
        'AT - Primary="',
        'AT - Secondary="',
        'DFP="',
        'DFS="',
        'HP="',
        'MAXHP="',
        'PP="',
        'MAXPP="',
        'SP="',
        'MAXSP="',
        'RP="',
        'MAXRP="',
        'LV="',
        'EXP="',
        'Gold="',
        'Armor="',
        'Accessory="',
        'Weapon="',
        'Ammo="',
        'rmName="'
    ]
    tags_name= [
        'AT (Primary)',
        'AT (Ammo)',
        'DF (Primary)',
        'DF (Accessory)',
        'Current HP',
        'Max HP',
        'Current PP(Protection Points)',
        'Max PP(Protection Points)',
        'Current SP(Speed Points)',
        'Max SP(Speed Points)',
        'Current RP(Recuperation Points)',
        'Max RP(Recuperation Points)',
        'LV(LOVE)',
        'EXP(Experience)',
        'Gold',
        'Armor',
        'Acessory',
        'Weapon',
        'Ammo',
        'Current Location',
    ]
    full_tags = {}
    for param, name in zip(data_tags, tags_name):
        for item in save_data:
            if item.startswith(param):
                r = re.search(param, item).span()
                strip_1 = item[r[1]:]
                if '.' in strip_1:
                    line_strip = strip_1.find('.')
                    value = strip_1[:line_strip]
                    
                elif strip_1.endswith('"'):
                    line_strip = strip_1.find('"')
                    value = strip_1[:line_strip]
                    
                full_tags[name] = value
        
    return full_tags
                
def check_files(path: Path):
    """Check if important files exists in some specific path."""
    path_files = [Path(f) for f in path.glob("*")]
    path_files_names = [f.name for f in path_files]
    conditions = [
        len(path_files) >= 3,
        "Save.sav" in path_files_names,
        "Controls.sav" in path_files_names,
        "Save02.sav" in path_files_names
    ]
    if all(conditions):
        if all(check_tags(path_files, tags).values()):
            return True
        
    return False
                                                                    
def path_test():
    """Tests if default uty path exists, if dont, it get and verify the path you send it."""
    global default_path
    if check_files(default_path):
        print(f"[{GREEN}*{RESET}] UTY Path found!")
        return True
    
    else:
        uty_path = Path(inquirer.filepath(
            message="Please select UTY saves path to continue:",
            default="C:\\",
            validate=PathValidator(is_dir=True, message="This isnt a valid path."),
            only_directories=True
        ).execute())
        
        if check_files(uty_path):
            default_path = uty_path
            print(f"[{GREEN}*{RESET}] UTY Valid path selected!")
            return True
        
        elif not uty_path:
            print(f"[{RED}!{RESET}] Empty input error!")
            return False
            
        else:
            print(f"[{RED}!{RESET}] UTY Path is missing several files!")
            return False
            
def show_specs():
    """Shows 'Save.sav' specifications."""
    banner()
    save_file_path = Path(inquirer.filepath(
        message="Select .sav file you want to view:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file path."),
        only_files=True
    ).execute())
    if check_tags_single(save_file_path, tags):
        result = extract_tags(save_file_path)
        if result != {}:
            print(f"[{GREEN}*{RESET}] UTY File Readed Succefully!")
            print("[-] Save Specs:")
            for name, value in result.items():
                print(f"{WHITE_LINE}{name}{RESET}: {GREEN}{value}{RESET}")
            input("<-Back")
    
    else:
        print("[!] Several tags not found in this save file.")
        
def load_file():
    """Load any 'Save.sav' into original uty save."""
    resp = Path(inquirer.filepath(
        message="Please select the UTY original save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute()).absolute()
    if check_tags_single(resp, tags):
        print(f"[{GREEN}*{RESET}]: Original UTY save file accepted.")
        copy = Path(inquirer.filepath(
            message="Please select your custom 'Save.sav' to replace the original.",
            default=str(user_uty_save_path),
            validate=PathValidator(is_file=True, message="This isnt a valid file.")
        ).execute()).absolute()
        
        if check_tags_single(copy, tags):
            print(f"[{GREEN}*{RESET}]: Custom UTY save file accepted.")
            sleep(0.1)
            print(f"[{YELLOW}-{RESET}]: Replacing original save file...")
            sleep(0.4)
            try:
                shutil.copy2(str(copy), str(resp))
            except Exception as e:
                 print(f"[{RED}!{RESET}]: Error while file replacement: {str(e)}")
                 
            print(f"[{GREEN}*{RESET}]: Custom UTY save file replaced on target!") 
           
    else:
        print(f"[{RED}!{RESET}]: Invalid UTY save file selected.")
    
    input("<-Back")
            
def modify_save_file():
    """Manual modifier for uty original(or not) file."""
    save = Path(inquirer.filepath(
        message="Please select the UTY original save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute())
    if check_tags_single(save, tags):
        print(f"[{YELLOW}-{RESET}]: Opening default editor...")
        sleep(1)
        try:
            Popen(["notepad", f"{str(save)}"])
        except Exception as e:
            print(f"[{RED}!{RESET}]: Error while file replacement: {str(e)}")
            
    else:
        print(f"[{RED}!{RESET}]: Invalid UTY save file selected.")

    input("<-Back")

def modify_save_file2():
    """Modify interactively original(or not) uty file."""
    save = Path(inquirer.filepath(
        message="Please select the UTY original save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute())

    if not check_tags_single(save, tags):
        print(f"[{RED}!{RESET}]: Invalid UTY save file selected.")
        input("<-Back")
        return

    print(f"[{GREEN}*{RESET}]: UTY Save file loaded!")
    print(f"[{YELLOW}-{RESET}]: Starting interactive injection...")
    sleep(2)

    with open(save, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    modified = False

    def get_val(tag):
        """Checks if specific tag match in content."""
        match = re.search(rf'{tag}="([^"]*)"', content)
        return match.group(1) if match else ""

    def set_val(tag, new_value):
        """Set specific new value for the tag."""
        nonlocal content, modified
        
        lines = content.splitlines(keepends=True)
        found = False
        old = None
    
        for i, line in enumerate(lines):
            if re.match(rf'^{re.escape(tag)}\s*=\s*".*"', line.strip()):
                match = re.search(rf'{re.escape(tag)}\s*=\s*"([^"]*)"', line)
                if match:
                    old = match.group(1)
                    if old == new_value:
                        return False  # já está igual
                    new_line = re.sub(rf'({re.escape(tag)}\s*=\s*")[^"]*(")',
                                      rf'\g<1>{new_value}\g<2>', line)
                    lines[i] = new_line
                    found = True
                    break
    
        if not found:
            return False
    
        content = ''.join(lines)
        modified = True
        return old

    def get_item(slot):
        """Tries to find out [Items] section in 'Save.sav'."""
        pattern = rf'\[Items\](.*?)(?=\n\[|\Z)'
        sec_match = re.search(pattern, content, re.DOTALL)
        if sec_match:
            sec = sec_match.group(1)
            match = re.search(rf'{slot}="([^"]*)"', sec)
            if match:
                return match.group(1)
        return ""

    def set_item(slot, new_value):
        """Sets items for the [Items] section in 'Save.sav'."""
        nonlocal content, modified
        old = get_item(slot)
        if old == new_value:
            return False
        pattern = rf'(\[Items\]\s*)(.*?)(?=\n\[|\Z)'
        def repl(match):
            sec = match.group(2)
            line_pattern = rf'({slot}=")[^"]*(")'
            new_sec = re.sub(line_pattern, rf'\g<1>{new_value}\g<2>', sec, count=1)
            return match.group(1) + new_sec
        content = re.sub(pattern, repl, content, flags=re.DOTALL)
        modified = True
        return old

    while True:
        menu_options = [
            "ATK (Primary)",
            "ATK (Ammo)",
            "DEF (Primary)",
            "DEF (Accessory)",
            "HP",
            "Max HP",
            "PP (Protections Points)",
            "Max PP (Protections Points)",
            "SP (Speed Points)",
            "Max SP (Speed Points)",
            "RP (Recuperation Points)",
            "Max RP (Recuperation Points)",
            "LV(LOVE)",
            "EXP(Experience)",
            "Gold",
            "Armor",
            "Accessory",
            "Weapon",
            "Ammo",
            "Items",
            "<-Back",
        ]
        resp, _ = pick(menu_options, "Please select the attribute to modify:", indicator='=>')

        if resp == "<-Back":
            if modified:
                with open(save, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[{GREEN}*{RESET}]: Save file updated successfully!")
            else:
                print(f"[{YELLOW}-{RESET}]: No changes made.")
            break

        elif resp == "ATK (Primary)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('AT - Primary', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: ATK (Primary) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "ATK (Ammo)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('AT - Secondary', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: ATK (Ammo) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "DEF (Primary)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('DFP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: DEF (Primary) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "DEF (Accessory)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('DFS', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: DEF (Accessory) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "HP":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('HP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: HP changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Max HP":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('MAXHP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: Max HP changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "PP (Protections Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('PP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: PP (Protection Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Max PP (Protections Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('MAXPP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: Max PP (Protection Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "SP (Speed Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('SP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: SP (Speed Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Max SP (Speed Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('MAXSP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: Max SP (Speed Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "RP (Recuperation Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('RP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: RP (Recuperation Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Max RP (Recuperation Points)":
            while True:
                try:
                    value = int(input("Digit an value (1-9999): "))
                    if 1 <= value <= 9999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 9999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('MAXRP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: Max RP (Recuperation Points) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "LV (LOVE)":
            while True:
                try:
                    value = int(input("Digit an value (1-21): "))
                    if 1 <= value <= 21:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 21.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('LV', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: LV (LOVE) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "EXP (Experience)":
            while True:
                try:
                    value = int(input("Digit an value (1-99999): "))
                    if 1 <= value <= 99999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 99999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('EXP', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: EXP (Experience) changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Gold":
            while True:
                try:
                    value = int(input("Digit an value (1-99999): "))
                    if 1 <= value <= 99999:
                        break
                    print(f"[{RED}!{RESET}] Value must be between 1 and 99999.")
                except ValueError:
                    print(f"[{RED}!{RESET}] Please enter a valid number.")
            new_val = f'{value}.000000'
            old_val = set_val('Gold', new_val)
            if old_val is not False:
                print(f"[{GREEN}*{RESET}]: Gold changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
            else:
                print(f"[{YELLOW}!{RESET}]: Value unchanged.")
            input("+Save")

        elif resp == "Armor":
            choices = ["Worn Hat", "Nice Hat", "<-Back"]
            value, _ = pick(choices, "Choose a value for armor:", indicator='=>')
            if value != "<-Back":
                old_val = set_val('Armor', value)
                if old_val is not False:
                    print(f"[{GREEN}*{RESET}]: Armor changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
                else:
                    print(f"[{YELLOW}!{RESET}]: Value unchanged.")
                input("+Save")

        elif resp == "Accessory":
            choices = [
                "Patch", "Feather", "Honeydew Pin", "Band Merch Pin",
                "Safety Jacket", "Steel Buckle", "Fancy Holster",
                "Safety Goggles", "Silver Scarf", "Golden Bandana",
                "Delta Rune Patch", "Golden Scarf", "<-Back"
            ]
            value, _ = pick(choices, "Choose a value for accessory:", indicator='=>')
            if value != "<-Back":
                old_val = set_val('Accessory', value)
                if old_val is not False:
                    print(f"[{GREEN}*{RESET}]: Accessory changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
                else:
                    print(f"[{YELLOW}!{RESET}]: Value unchanged.")
                input("+Save")

        elif resp == "Weapon":
            choices = ["Toy Gun", "Wild Revolver", "Toy Knife", "<-Back"]
            value, _ = pick(choices, "Choose a value for weapon:", indicator='=>')
            if value != "<-Back":
                old_val = set_val('Weapon', value)
                if old_val is not False:
                    print(f"[{GREEN}*{RESET}]: Weapon changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
                else:
                    print(f"[{YELLOW}!{RESET}]: Value unchanged.")
                input("+Save")

        elif resp == "Ammo":
            choices = [
                "Rubber Ammo", "Pebble Ammo", "Ice Pellets",
                "Coffee Bean Ammo", "Glass Ammo", "Flint",
                "Silver Ammo", "Nails", "Friendliness Pellets",
                "Super Ammo", "<-Back"
            ]
            value, _ = pick(choices, "Choose a value for ammo:", indicator='=>')
            if value != "<-Back":
                old_val = set_val('Ammo', value)
                if old_val is not False:
                    print(f"[{GREEN}*{RESET}]: Ammo changed from {RED}{old_val}{RESET} to {GREEN}{value}{RESET}.")
                else:
                    print(f"[{YELLOW}!{RESET}]: Value unchanged.")
                input("+Save")

        elif resp == "Items":
            while True:
                slot_choices = ["00", "01", "02", "03", "04", "05", "06", "07", "Exit"]
                slot, _ = pick(slot_choices, "Choose the slot:", indicator='=>')
                if slot == "Exit":
                    break

                type_choices = [
                    "Ammo",
                    "Armors",
                    "Accessories",
                    "Weapons",
                    "Miscellaneous Items",
                    "Consumable Items",
                    "<-Back"
                ]
                value_type, _ = pick(type_choices, f"Choose the item type for slot {slot}:", indicator='=>')
                if value_type == "<-Back":
                    continue

                if value_type == "Ammo":
                    item_list = [
                        "Rubber Ammo", "Pebble Ammo", "Ice Pellets",
                        "Coffee Bean Ammo", "Glass Ammo", "Flint",
                        "Silver Ammo", "Nails", "Friendliness Pellets",
                        "Super Ammo", "<-Back"
                    ]
                elif value_type == "Armors":
                    item_list = ["Worn Hat", "Nice Hat", "<-Back"]
                elif value_type == "Accessories":
                    item_list = [
                        "Patch", "Feather", "Honeydew Pin", "Band Merch Pin",
                        "Safety Jacket", "Steel Buckle", "Fancy Holster",
                        "Safety Goggles", "Silver Scarf", "Golden Bandana",
                        "Delta Rune Patch", "Golden Scarf", "<-Back"
                    ]
                elif value_type == "Weapons":
                    item_list = ["Toy Gun", "Wild Revolver", "Toy Knife", "<-Back"]
                elif value_type == "Miscellaneous Items":
                    item_list = [
                        "Missing Poster", "Snowdin Map", "Matches",
                        "Lukewarm Coffee", "Soggy Mitten", "Pickaxe",
                        "Necklace", "Hydrochloric Acid", "Videotape", "<-Back"
                    ]
                elif value_type == "Consumable Items":
                    item_list = [
                        "Feisty Slider", "Gunpowder", "Adult Soda",
                        "Moss Salad", "Grassy Fries", "Flower Stew",
                        "Gravity Granola", "Dihydrogen Monoxide",
                        "Popato Chisps", "Beef Jerky", "Cake",
                        "Monster Candy", "Monster Candy+", "Corn Chowder",
                        "Hot Dog", "C-B Strudel", "Floral Cupcake",
                        "Cinnamon Cookie", "Oasis Latte", "Golden Pear",
                        "Golden Coffee", "Golden Cactus", "Lemonade",
                        "Candy Corn", "Corn Dog", "Sponge Cake",
                        "Homemade Cookie", "Hot Pop", "Lukewarm Pop",
                        "Cold Pop", "Honeydew Coffee", "Honeydew Pancake",
                        "Gingerbread Bear", "Packing Peanuts", "Trail Mix",
                        "Ice Tea", "Green Tea", "Sea Tea", "Fruitcake",
                        "Spider Donut", "Icewater", "Root Beer", "<-Back"
                    ]
                else:
                    continue

                chosen, _ = pick(item_list, f"Choose the item for slot {slot}:", indicator='=>')
                if chosen == "<-Back":
                    continue

                old_val = set_item(slot, chosen)
                if old_val is not False:
                    print(f"[{GREEN}*{RESET}]: Item slot {slot} changed from {RED}{old_val}{RESET} to {GREEN}{chosen}{RESET}.")
                else:
                    print(f"[{YELLOW}!{RESET}]: Value unchanged.")
                input("+Save")

    input("<-Back")    
    
def run_game():
    """Run the game."""
    global game_exec_path
    
    if not game_exec_path:
        resp = Path(inquirer.filepath(
            message="Please select game path",
            default=user_base_path,
            validate=PathValidator(is_file=True, message="This isnt a valid game executable path.")
        ).execute())
        if resp.suffix == ".exe" and uty_exe_verify(resp):
            print(f"[{GREEN}*{RESET}]: UTY Valid exe found!")
            sleep(0.5)
            print(f"[{YELLOW}-{RESET}]: Starting game...")
            game_exec_path = str(resp)
            sleep(3)
            Popen([f"{str(resp)}"])
            
        else:
            print(f"[{RED}-{RESET}]: Invalid exe file, please choose a valid game executable.")
            
    elif game_exec_path:
        if str(game_exec_path).endswith('.exe') and uty_exe_verify(game_exec_path):
            print(f"[{YELLOW}-{RESET}]: Starting game...")
            sleep(3)
            Popen([f"{str(game_exec_path)}"])
            
        else:
            print(f"[{RED}-{RESET}]: Invalid exe file, please choose a valid game executable.")
        
    input("<-Back")
    
def change_settings():
    """Settings section."""
    def sett_exe_path():
        """Modifies and visualize the default .exe game path."""
        global game_exec_path
        _pp = "-" if game_exec_path == None else game_exec_path
        sel = inquirer.select(
            message=f"[*] Current executable path: {_pp}",
            choices=[
                "Set new game exe path",
                "Open game path in default file manager",
                "<-Back"
            ],
        ).execute()
        if sel == "Set new game exe path":
            new_path = Path(inquirer.filepath(
                message="New game path:",
                default="C:\\",
                validate=PathValidator(is_file=True, message="Invalid file path.")
            ).execute())
            if uty_exe_verify(new_path):
                print(f"[{GREEN}*{RESET}]: New exe file path: '{new_path}'")
                write_on_file(user_game_exe_path_info1, str(new_path))
                game_exec_path = new_path
                input("<-Back")
                
        elif sel == "Open game path in default file manager":
            if game_exec_path == None:
                print(f"[{RED}-{RESET}]: You dont have a valid path to open.")
                input("<-Back")
            else:
                Popen(["explorer.exe",str(game_exec_path.parent)])
                
    def sett_save_path():
        """Modifies and visualize the default custom saves path."""
        global user_uty_save_path
        _pp = "-" if user_uty_save_path == None else user_uty_save_path
        sel = inquirer.select(
            message=f"[*] Current game saves path: {_pp}",
            choices=[
                "Set new game saves path",
                "Open game path in default file manager",
                "<-Back"
            ],
        ).execute()
        if sel == "Set new game saves path":
            new_path = Path(inquirer.filepath(
                message="New game saves path:",
                default="C:\\",
                validate=PathValidator(is_dir=True, message="Invalid file path."),
                only_directories=True
            ).execute())
            if new_path.exists():
                print(f"[{GREEN}*{RESET}]: New game saves path: '{new_path}'")
                write_on_file(user_game_save_path_info1, str(new_path))
                user_uty_save_path = new_path
                input("<-Back")
                
        elif sel == "Open game path in default file manager":
            if user_uty_save_path == None:
                print(f"[{RED}-{RESET}]: You dont have a valid path to open.")
                input("<-Back")
            else:
                Popen(["explorer.exe",str(user_uty_save_path)])
    
    def sett_save_backup():
        """Save and load original 'Save.sav' backups."""
        result = "[*] Backup file found." if 'Save.sav' in [f.name for f in user_game_save_backup.iterdir() if f.is_file()] else "[!] No backup file found."
        select = inquirer.select(
            message=result,
            choices=[
                "Backup uty save file",
                "Load uty save file backup",
                "<-Back"
            ]
        ).execute()
        if select == "Backup uty save file":
            shutil.copy2(str(default_save_file), str(user_game_save_backup))
            print(f"[{GREEN}*{RESET}]: Backup uty save file copied to: '{user_game_save_backup}'")
            input("<-Back")
            
        elif select == "Load uty save file backup":
            shutil.copy2(str(user_game_save_backup_file), str(default_save_file))
            print(f"[{GREEN}*{RESET}]: Backup from '{user_game_save_backup}' loaded!")
            input("<-Back")

    while True:
        banner()
        option = inquirer.select(
            message="Settings",
            choices=[
                "Game executable path",
                "Game custom saves path",
                "Backup game save",
                "<-Back"
            ],
            validate=EmptyInputValidator
        ).execute()
        options = {
                "Game executable path": sett_exe_path,
                "Game custom saves path": sett_save_path,
                "Backup game save": sett_save_backup
        }
        if option == "<-Back":
            break
            
        options[option]()

#This look like properly a __main__ funcion, nothing more about it.
def main():
    check_game_exe_path()
    check_game_save_path()
    while True:
        banner()
        exec_tree = {
            "Run game": run_game,
            "Load save file": load_file,
            "Modify save file manually": modify_save_file,
            "Modify save file easily": modify_save_file2,
            "View save file specifications": show_specs,
            "Settings": change_settings
        }
        resp = inquirer.select(
            message = "Please select your action:",
            choices = [
                "Run game",
                "Load save file",
                "View save file specifications",
                "Modify save file manually",
                "Modify save file easily",
                "Settings",
                "Exit"
            ]
        ).execute()
        if resp == 'Exit':
            break
            
        exec_tree[resp]()

if path_test():
    try:
        main()
    except KeyboardInterrupt:
        print(f"[{RED}!{RESET}]: KeyboardInterrupt Detected.")
    except Exception as e:
        print(f"[{RED}!{RESET}]: Error: {str(e)}")
