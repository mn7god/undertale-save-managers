import re
import os
import string
import base64
import shutil
from time import sleep
from pathlib import Path
from subprocess import run, Popen
from InquirerPy import inquirer
from colorama import just_fix_windows_console
from InquirerPy.validator import PathValidator, EmptyInputValidator

## Variables and console settings
just_fix_windows_console()

game_exec_path = None
user_ut_save_path = None

user_game_exe_path_info1 = Path(os.getenv("USERPROFILE"),"UT_Save_Manager_Files","Main_Data.dat").resolve()
user_game_save_path_info1 = Path(os.getenv("USERPROFILE"),"UT_Save_Manager_Files","Main1_Data.dat").resolve()
user_game_save_backup = Path(os.getenv("USERPROFILE"),"UT_Save_Manager_Files","Backup").resolve()
user_game_save_backup_file = Path(os.getenv("USERPROFILE"),"UT_Save_Manager_Files","Backup","file0").resolve()
user_game_exe_path = Path(os.getenv("USERPROFILE"),"UT_Save_Manager_Files").resolve()
user_base_path = str(Path(os.getenv("USERPROFILE")).resolve())

default_path = Path(os.getenv("LOCALAPPDATA"), "UNDERTALE").expanduser().resolve()
default_save_file = str(Path(os.getenv("LOCALAPPDATA"), "UNDERTALE", "file0").expanduser().resolve())

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

symbols = string.punctuation
letters = string.ascii_letters
numbers = string.digits
spaces = string.whitespace

items_ids = {
    "0": "Nothing",
    "1": "Monster Candy",
    "2": "Croquet Roll",
    "5": "Rock Candy",
    "6": "Pumpkin Rings",
    "7": "Spider Donut",
    "8": "Stoic Onion",
    "9": "Ghost Fruit",
    "10": "Spider Cider",
    "11": "Butterscotch Pie",
    "16": "Snowman Piece",
    "17": "Nice Cream",
    "18": "Puppydough Icecream",
    "19": "Bisicle",
    "20": "Unisicle",
    "21": "Cinnamon Bun",
    "22": "Temmie Flakes",
    "23": "Abandoned Quiche",
    "26": "Punch Card",
    "27": "Annoying Dog",
    "28": "Dog Salad",
    "29": "Dog Residue",
    "30": "Dog Residue",
    "31": "Dog Residue",
    "32": "Dog Residue",
    "33": "Dog Residue",
    "34": "Dog Residue",
    "35": "Astronaut Food",
    "36": "Instant Noodles",
    "37": "Crab Apple",
    "38": "Hot Dog...?",
    "39": "Hot Cat",
    "40": "Glamburger",
    "41": "Sea Tea",
    "42": "Starfait",
    "43": "Legendary Hero",
    "54": "Bad Memory",
    "55": "Dream",
    "56": "Undyne's Letter",
    "57": "Undyne Letter EX",
    "58": "Popato Chisps",
    "59": "Junk Food",
    "60": "Mystery Key",
    "61": "Face Steak",
    "62": "Hush Puppy",
    "63": "Snail Pie",
    "3": "Stick",
    "4": "Bandage",
    "12": "Faded Ribbon",
    "13": "Toy Knife",
    "14": "Tough Glove",
    "15": "Manly Bandanna",
    "24": "Old Tutu",
    "25": "Ballet Shoes",
    "44": "Butty Glasses",
    "45": "Torn Notebook",
    "46": "Stained Apron",
    "47": "Burnt Pan",
    "48": "Cowboy Hat",
    "49": "Empty Gun",
    "50": "Heart Locket",
    "51": "Worn Dagger",
    "52": "Real Knife",
    "53": "The Locket",
    "64": "temy armor"
}

w_ids = {
    '3': 'Stick',
    '13': 'Toy Knife',
    '14': 'Tough Glove',
    '25': 'Ballet Shoes',
    '45': 'Torn Notebook',
    '47': 'Burnt Pan',
    '49': 'Empty Gun',
    '51': 'Worn Dagger',
    '52': 'Real Knife'
}

a_ids = {
    '4': 'Bandage',
    '12': 'Faded Ribbon',
    '15': 'Manly Bandana',
    '24': 'Old Tutu',
    '44': 'Cloudy Glasses',  
    '46': 'Stained Apron',
    '48': 'Cowboy Hat',
    '50': 'Heart Locket',
    '64': "temy armor" 
}

ritems_id = {
    "Nothing": "0",
    "Monster Candy": "1",
    "Croquet Roll": "2",
    "Rock Candy": "5",
    "Pumpkin Rings": "6",
    "Spider Donut": "7",
    "Stoic Onion": "8",
    "Ghost Fruit": "9",
    "Spider Cider": "10",
    "Butterscotch Pie": "11",
    "Snowman Piece": "16",
    "Nice Cream": "17",
    "Puppydough Icecream": "18",
    "Bisicle": "19",
    "Unisicle": "20",
    "Cinnamon Bun": "21",
    "Temmie Flakes": "22",
    "Abandoned Quiche": "23",
    "Punch Card": "26",
    "Annoying Dog": "27",
    "Dog Salad": "28",
    "Dog Residue": "30", 
    "Astronaut Food": "35",
    "Instant Noodles": "36",
    "Crab Apple": "37",
    "Hot Dog...?": "38",
    "Hot Cat": "39",
    "Glamburger": "40",
    "Sea Tea": "41",
    "Starfait": "42",
    "Legendary Hero": "43",
    "Bad Memory": "54",
    "Dream": "55",
    "Undyne's Letter": "56",
    "Undyne Letter EX": "57",
    "Popato Chisps": "58",
    "Junk Food": "59",
    "Mystery Key": "60",
    "Face Steak": "61",
    "Hush Puppy": "62",
    "Snail Pie": "63",
    "Stick": "3",
    "Bandage": "4",
    "Faded Ribbon": "12",
    "Toy Knife": "13",
    "Tough Glove": "14",
    "Manly Bandanna": "15",
    "Old Tutu": "24",
    "Ballet Shoes": "25",
    "Butty Glasses": "44",
    "Torn Notebook": "45",
    "Stained Apron": "46",
    "Burnt Pan": "47",
    "Cowboy Hat": "48",
    "Empty Gun": "49",
    "Heart Locket": "50",
    "Worn Dagger": "51",
    "Real Knife": "52",
    "The Locket": "53",
    "temy armor": "64"
}

rw_ids = {
    "Stick": "3",
    "Toy Knife": "13",
    "Tough Glove": "14",
    "Ballet Shoes": "25",
    "Torn Notebook": "45",
    "Burnt Pan": "47",
    "Empty Gun": "49",
    "Worn Dagger": "51",
    "Real Knife": "52"
}

ra_ids = {
    "Bandage": "4",
    "Faded Ribbon": "12",
    "Manly Bandana": "15",
    "Old Tutu": "24",
    "Butty Glasses": "44",  
    "Stained Apron": "46",
    "Cowboy Hat": "48",
    "Heart Locket": "50",
    "temy armor": "64"
}

all_in_one = {
  "Nothing": "0",
  "Monster Candy": "1",
  "Croquet Roll": "2",
  "Stick": "3",
  "Bandage": "4",
  "Rock Candy": "5",
  "Pumpkin Rings": "6",
  "Spider Donut": "7",
  "Stoic Onion": "8",
  "Ghost Fruit": "9",
  "Spider Cider": "10",
  "Butterscotch Pie": "11",
  "Faded Ribbon": "12",
  "Toy Knife": "13",
  "Tough Glove": "14",
  "Manly Bandanna": "15",
  "Snowman Piece": "16",
  "Nice Cream": "17",
  "Puppydough Icecream": "18",
  "Bisicle": "19",
  "Unisicle": "20",
  "Cinnamon Bun": "21",
  "Temmie Flakes": "22",
  "Abandoned Quiche": "23",
  "Old Tutu": "24",
  "Ballet Shoes": "25",
  "Punch Card": "26",
  "Annoying Dog": "27",
  "Dog Salad": "28",
  "Astronaut Food": "35",
  "Instant Noodles": "36",
  "Crab Apple": "37",
  "Hot Dog...?": "38",
  "Hot Cat": "39",
  "Glamburger": "40",
  "Sea Tea": "41",
  "Starfait": "42",
  "Legendary Hero": "43",
  "Butty Glasses": "44",
  "Torn Notebook": "45",
  "Stained Apron": "46",
  "Burnt Pan": "47",
  "Cowboy Hat": "48",
  "Empty Gun": "49",
  "Heart Locket": "50",  
  "Worn Dagger": "51",
  "Real Knife": "52",
  "The Locket": "53", 
  "Bad Memory": "54",
  "Dream": "55",
  "Undyne's Letter": "56",
  "Undyne Letter EX": "57",
  "Popato Chisps": "58",
  "Junk Food": "59",
  "Mystery Key": "60",
  "Face Steak": "61",
  "Hush Puppy": "62",
  "Snail Pie": "63",
  "temy armor": "64"
}

## FUNCTIONS

def nick_filter(text: str, pattern: str):
    """Erases any pattern of an specific string."""
    string = str.maketrans('', '', pattern)
    return text.translate(string)

def adjust_cmd_prompt():
    """Adjusts cmd prompt for better experience."""
    os.system("mode con: cols=101 lines=28")
    os.system("title Undertale Save Manager")
    
def check_user_game_exe_path():
    """Checks ut save manager important files/directories."""
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

def check_game_exe_path():
    """Checks ut default .exe path."""
    global game_exec_path
    if game_exec_path == None:
        try:
            with open(str(user_game_exe_path_info1), 'r') as f:
                data = f.read().splitlines()[0].strip()
            
            if data.endswith('.exe'):
                game_exec_path = Path(data)
                
        except Exception as e:
            print(str(e)) 
            
def check_game_save_path():
    """Check default custom game saves path."""
    global user_ut_save_path
    if user_ut_save_path == None:
        try:
            with open(str(user_game_save_path_info1), 'r') as f:
                data = f.read().splitlines()[0].strip()
                
            if Path(data).is_dir() and Path(data).exists(): 
                user_ut_save_path = Path(data)
                
        except Exception as e:
            print(str(e))      
            
def write_on_file(file_path: Path, data: str):
    """Write(or overwrites) an file content for a new stuff."""
    with open(file_path, 'w') as file:
        file.write(data)      
            
def check_files(path: Path):
    """Check if important ut files exists."""
    path_files = [Path(f) for f in path.glob("*")]
    path_files_names = [f.name for f in path_files]
    conditions = [
        len(path_files) >= 3,
        "file0" in path_files_names,
        "config.ini" in path_files_names,
        "undertale.ini" in path_files_names
    ]
    if all(conditions):
        return True
        
    return False         

def path_test():
    """Tests if default ut path exists, if dont, just allow user put his own and test it."""
    global default_path
    if check_files(default_path):
        print(f"[{GREEN}*{RESET}] UT Path found!")
        return True
    
    else:
        ut_path = Path(inquirer.filepath(
            message="Please select UT saves path to continue:",
            default="C:\\",
            validate=PathValidator(is_dir=True, message="This isnt a valid path."),
            only_directories=True
        ).execute())
        
        if check_files(ut_path):
            default_path = ut_path
            print(f"[{GREEN}*{RESET}] UTY Valid path selected!")
            return True
        
        elif not ut_path:
            print(f"[{RED}!{RESET}] Empty input error!")
            return False
            
        else:
            print(f"[{RED}!{RESET}] UT Path is missing several files!")
            return False

def banner():
    """Program ascii art banner."""
    adjust_cmd_prompt()
    os.system("cls")
    print(f"""{RED} ▄• ▄▌▄▄▄▄▄{RESET}    .▄▄ ·  ▄▄▄·  ▌ ▐·▄▄▄ .    • ▌ ▄ ·.  ▄▄▄·  ▐ ▄  ▄▄▄·  ▄▄ • ▄▄▄ .▄▄▄  
{RED} █▪██▌•██{RESET}      ▐█ ▀. ▐█ ▀█ ▪█·█▌▀▄.▀·    ·██ ▐███▪▐█ ▀█ •█▌▐█▐█ ▀█ ▐█ ▀ ▪▀▄.▀·▀▄ █·
{RED} █▌▐█▌ ▐█.▪{RESET}    ▄▀▀▀█▄▄█▀▀█ ▐█▐█•▐▀▀▪▄    ▐█ ▌▐▌▐█·▄█▀▀█ ▐█▐▐▌▄█▀▀█ ▄█ ▀█▄▐▀▀▪▄▐▀▀▄ 
{RED} ▐█▄█▌ ▐█▌·{RESET}    ▐█▄▪▐█▐█ ▪▐▌ ███ ▐█▄▄▌    ██ ██▌▐█▌▐█ ▪▐▌██▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▄▄▌▐█•█▌
{RED}  ▀▀▀  ▀▀▀{RESET}      ▀▀▀▀  ▀  ▀ . ▀   ▀▀▀     ▀▀  █▪▀▀▀ ▀  ▀ ▀▀ █▪ ▀  ▀ ·▀▀▀▀  ▀▀▀ .▀  ▀""")
        
def extract_specs(save_path: Path):
    """Extracts specifications from a valid file(file0)."""
    s_data = save_path.read_text().splitlines()
    user = s_data[0]
    love = s_data[1]
    hp = s_data[2]
    maxhp = s_data[3]
    atk_p = s_data[4]
    atk_s = s_data[5]
    def_p = s_data[6]
    def_s = s_data[7]
    soul_s = s_data[8]
    exp = s_data[9]
    gold = s_data[10]
    eqp_w = s_data[28]
    eqp_a = s_data[29]
    full_tags = {
        'Player Name': user.strip(),
        'ATK (Native)': atk_p.strip(),
        'ATK (Weapon)': atk_s.strip(),
        'DEF (Native)': def_p.strip(),
        'DEF (Armor)': def_s.strip(),
        'Current HP': hp.strip(),
        'Max HP': maxhp.strip(),
        'LV (LOVE)': love.strip(),
        'Souls Speed': soul_s.strip(),
        'EXP (Experience)': exp.strip(),
        'Gold': gold.strip(),
        'Equiped Weapon': w_ids[eqp_w.strip()],
        'Equiped Armor': a_ids[eqp_a.strip()]
        
    }
    return full_tags
        
        
def show_specs():
    """Shows specifications from a valid file(file0)."""
    banner()
    save_file_path = Path(inquirer.filepath(
        message="Select 'file0' file you want to view:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file path."),
        only_files=True
    ).execute())
    result = extract_specs(save_file_path)
    if result != {}:
        print(f"[{GREEN}*{RESET}] UT File Readed Succefully!")
        print("[-] Save Specs:")
        for name, value in result.items():
            print(f"{WHITE_LINE}{name}{RESET}: {GREEN}{value}{RESET}")
        input("<-Back")
    
    else:
        print(f"[{RED}!{RESET}]: Error while attributes reading: {str(e)}")
        input('<-Back')

def load_file():
    """Load any custom 'file0' overwriting the original save."""
    resp = Path(inquirer.filepath(
        message="Please select the UT original save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute()).absolute()
    try:
        extract_specs(resp)
        print(f"[{GREEN}*{RESET}]: Original UT save file accepted.")
        copy = Path(inquirer.filepath(
            message="Please select your custom 'file0' to replace the original.",
            default=user_ut_save_path,
            validate=PathValidator(is_file=True, message="This isnt a valid file.")
        ).execute()).absolute()
        
        if extract_specs(copy) != {}:
            print(f"[{GREEN}*{RESET}]: Custom UT save file accepted.")
            sleep(0.1)
            print(f"[{YELLOW}-{RESET}]: Replacing original save file...")
            sleep(0.4)
            try:
                shutil.copy2(str(copy), str(resp))
                print(f"[{GREEN}*{RESET}]: Custom UT save file replaced on target!") 
            except Exception as e:
                 print(f"[{RED}!{RESET}]: Error while file replacement: {str(e)}")
                 
    except Exception:
        print(f"[{RED}!{RESET}]: Invalid UT save file selected.")
    
    input("<-Back")
    
def run_game():
    """Runs game executable."""
    global game_exec_path
    if not game_exec_path:
        resp = Path(inquirer.filepath(
            message="Please select game path:",
            default=user_base_path,
            validate=PathValidator(is_file=True, message="This isnt a valid game executable path.")
        ).execute())
        if resp.suffix == ".exe":
            print(f"[{GREEN}*{RESET}]: UT Valid exe found!")
            sleep(0.5)
            print(f"[{YELLOW}-{RESET}]: Starting game...")
            game_exec_path = str(resp)
            Popen([f"{str(resp)}"])
            
        else:
            print(f"[{RED}-{RESET}]: Invalid exe file, please choose a valid game executable.")
    
    else:
        print(f"[{GREEN}*{RESET}]: UT Valid exe found!")
        sleep(0.5)
        print(f"[{YELLOW}-{RESET}]: Starting game...")
        Popen([f"{str(game_exec_path)}"])
            
def modify_save_file():
    """Modify manually file0 save."""
    save_path = Path(inquirer.filepath(
        message="Please select the UT save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute())
    if extract_specs(save_path) != {}:
        print(f"[{YELLOW}-{RESET}]: Opening default editor...")
        sleep(1)
        try:
            Popen(["notepad", f"{str(save_path)}"])
        except Exception as e:
            print(f"[{RED}!{RESET}]: Error while file replacement: {str(e)}")
            
    else:
        print(f"[{RED}!{RESET}]: Invalid UT save file selected.")

    input("<-Back")

def modify_save_file2():
    """Modify interactively original(or not) uty file."""
    global a_ids, w_ids, items_ids
    def write_file0_save(path: Path, index: int, new_content: str):
        lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
        
        if lines[index].endswith("\n"):
            new_content += "\n"
            
        lines[index] = new_content
            
        path.write_text(''.join(lines))
    
    save_path = Path(inquirer.filepath(
        message="Please select the UT original save file path:",
        default=default_save_file,
        validate=PathValidator(is_file=True, message="This isnt a valid file.")
    ).execute())

    if extract_specs(save_path) == {}:
        print(f"[{RED}!{RESET}]: Invalid UT save file selected.")
        input("<-Back")
        return

    print(f"[{GREEN}*{RESET}]: UT Save file loaded!")
    print(f"[{YELLOW}-{RESET}]: Starting interactive injection...")
    sleep(2)

    while True:
        s_data = save_path.read_text().splitlines()
        user = s_data[0]
        love = s_data[1]
        hp = s_data[2]
        maxhp = s_data[3]
        atk_p = s_data[4]
        atk_s = s_data[5]
        def_p = s_data[6]
        def_s = s_data[7]
        soul_s = s_data[8]
        exp = s_data[9]
        gold = s_data[10]
        kills = s_data[11]
        item_1 = s_data[12]
        item_2 = s_data[14]
        item_3 = s_data[16]
        item_4 = s_data[18]
        item_5 = s_data[20]
        item_6 = s_data[22]
        item_7 = s_data[24]
        item_8 = s_data[26]
        eqp_w = s_data[28]
        eqp_a = s_data[29]
        g_time = s_data[548]
        slot_tags = {
            'Item Slot 1': items_ids[item_1.strip()],
            'Item Slot 2': items_ids[item_2.strip()],
            'Item Slot 3': items_ids[item_3.strip()],
            'Item Slot 4': items_ids[item_4.strip()],
            'Item Slot 5': items_ids[item_5.strip()],
            'Item Slot 6': items_ids[item_6.strip()],
            'Item Slot 7': items_ids[item_7.strip()],
            'Item Slot 8': items_ids[item_8.strip()]
        }
        slot_numbers={
            'Item Slot 1': 12,
            'Item Slot 2': 14,
            'Item Slot 3': 16,
            'Item Slot 4': 18,
            'Item Slot 5': 20,
            'Item Slot 6': 22,
            'Item Slot 7': 24,
            'Item Slot 8': 26
        }
        resp = inquirer.select(
            message="Please select the attribute to modify:",
            choices=[
                f'Player Name',
                f'ATK (Native)',
                f'ATK (Weapon)',
                f'DEF (Native)',
                f'DEF (Armor)',
                f'HP',
                f'Max HP',
                f'LV (LOVE)',
                f'Soul Speed',
                f'EXP (Experience)',
                f'Gold',
                f'Equiped Weapon',
                f'Equiped Armor',
                f'Kills',
                f'Playing Time (Seconds)',
                f'Items',
                "<-Back"
            ]
        ).execute()

        if resp == "<-Back":
            break
            
        elif resp == "Player Name":
            print(f"[*] Current Player Name: {user}")
            new_name = input("Your new game nick: ")
            _filter = nick_filter(new_name, symbols+spaces)
            if new_name and _filter:
                try:
                    write_file0_save(save_path, 0, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_name}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_name}' in UT file0.")
            
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                    
            input('<-Back')
            
        elif resp == "ATK (Native)":
            print(f"[*] Current ATK (Native): {atk_p}")
            new_atkp = input("Your new value for ATK: ")
            _filter = nick_filter(new_atkp, symbols+letters+spaces)
            if new_atkp and _filter:
                try:
                    write_file0_save(save_path, 4, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_atkp}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_atkp}' in UT file0.")
            
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "ATK (Weapon)":
            print(f"[*] Current ATK (Weapon): {atk_s}")
            new_atks = input("Your new value for ATK: ")
            _filter = nick_filter(new_atks, symbols+letters+spaces)
            if new_atks and _filter:
                try:
                    write_file0_save(save_path, 5, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_atks}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_atks}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "DEF (Native)":
            print(f"[*] Current DEF (Native): {def_p}")
            new_defp = input("Your new value for DEF: ")
            _filter = nick_filter(new_defp, symbols+letters+spaces)
            if new_defp and _filter:
                try:
                    write_file0_save(save_path, 6, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_defp}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_defp}' in UT file0.")
                    
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "DEF (Armor)":
            print(f"[*] Current DEF (Armor): {def_p}")
            new_defs = input("Your new value for DEF: ")
            _filter = nick_filter(new_defs, symbols+letters+spaces)
            if new_defs and _filter:
                try:
                    write_file0_save(save_path, 7, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_defs}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_defs}' in UT file0.")
            
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
            
            input('<-Back')
            
        elif resp == "HP":
            print(f"[*] Current HP: {hp}")
            new_hp = input("Your new value for HP: ")
            _filter = nick_filter(new_hp, symbols+letters+spaces)
            if new_hp and _filter:
                try:
                    write_file0_save(save_path, 2, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_hp}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_hp}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
            
            input('<-Back')
            
        elif resp == "Max HP":
            print(f"[*] Current Max HP: {maxhp}")
            new_mhp = input("Your new value for Max HP: ")
            _filter = nick_filter(new_mhp, symbols+letters+spaces)
            if new_mhp and _filter:
                try:
                    write_file0_save(save_path, 3, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_mhp}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_mhp}' in UT file0.")
                    
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "LV (LOVE)":
            print(f"[*] Current LV (LOVE): {maxhp}")
            new_lv = input("Your new value for LV (LOVE): ")
            _filter = nick_filter(new_lv, symbols+letters+spaces)
            if new_lv and _filter:
                try:
                    write_file0_save(save_path, 1, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_lv}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_lv}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "Soul Speed":
            print(f"[*] Current Soul Speed: {soul_s}")
            new_soul_s = input("Your new value for soul speed: ")
            _filter = nick_filter(new_soul_s, symbols+letters+spaces)
            if new_soul_s and _filter:
                try:
                    write_file0_save(save_path, 8, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_soul_s}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_soul_s}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "EXP (Experience)":
            print(f"[*] Current EXP (Experience): {exp}")
            new_exp = input("Your new value for EXP: ")
            _filter = nick_filter(new_exp, symbols+letters+spaces)
            if new_exp and _filter:
                try:
                    write_file0_save(save_path, 9, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_exp}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_exp}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "Gold":
            print(f"[*] Current Gold: {exp}")
            new_gold = input("Your new value for gold: ")
            _filter = nick_filter(new_gold, symbols+letters+spaces)
            if new_gold and _filter:
                try:
                    write_file0_save(save_path, 10, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_gold}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_gold}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "Equiped Weapon":
            print(f"[*] Current Equipped Weapon: {w_ids[eqp_w.strip()]}")
            new_eqpw = inquirer.select(
                message="Your new value for EQP Weapon:",
                choices=w_ids.values()
            ).execute()
            try:
                write_file0_save(save_path, 28, rw_ids[new_eqpw])
                print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_eqpw}' in UT file0!")

            except Exception:
                print(f"[{RED}!{RESET}]: Couldnt injected value '{new_eqpw}' in UT file0.")
                
            input('<-Back')
            
        elif resp == "Equiped Armor":
            print(f"[*] Current Equipped Armor: {a_ids[eqp_a.strip()]}")
            new_eqpa = inquirer.select(
                message="Your new value for EQP Armor:",
                choices=a_ids.values()
            ).execute()
            try:
                write_file0_save(save_path, 29, ra_ids[new_eqpa])
                print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_eqpa}' in UT file0!")

            except Exception:
                print(f"[{RED}!{RESET}]: Couldnt injected value '{new_eqpa}' in UT file0.")
                
            input('<-Back')
            
        elif resp == "Kills":
            print(f"[*] Current Kills: {exp}")
            new_k = input("Your new value for kills: ")
            _filter = nick_filter(new_k, symbols+letters+spaces)
            if new_k and _filter:
                try:
                    write_file0_save(save_path, 11, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_k}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_k}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "Playing Time":
            print(f"[*] Current PT: {exp}")
            new_pt = input("Your new value for PT: ")
            _filter = nick_filter(new_pt, symbols+letters+spaces)
            if new_pt and _filter:
                try:
                    write_file0_save(save_path, 548, _filter)
                    print(f"[{GREEN}*{RESET}]: Succefully injected value '{new_pt}' in UT file0!")
    
                except Exception:
                    print(f"[{RED}!{RESET}]: Couldnt injected value '{new_pt}' in UT file0.")
                
            else:
                print(f"[{RED}!{RESET}]: Empty value will not be acepted.")
                
            input('<-Back')
            
        elif resp == "Items":
            slot = inquirer.select(
                message="Please select the slot:",
                choices=slot_tags.keys()
            ).execute()
            item = inquirer.select(
                message=f"Please select the item for slot {slot}:",
                choices=all_in_one.keys()
            ).execute()
            try:
                write_file0_save(save_path, slot_numbers[slot], all_in_one[item])
                print(f"[{GREEN}*{RESET}]: Succefully injected value '{item}' in slot '{slot}' on UT file0!")
            
            except Exception as e:
                print(f"[{RED}!{RESET}]: Injection failed: {str(e)}")
            
            input('<-Back')
    
def change_settings():
    def sett_exe_path():
        """Modifies and show the default game executable path."""
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
            if new_path.exists() and str(new_path).endswith(".exe"):
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
        """Manage and show the default custom saves path."""
        global user_ut_save_path
        _pp = "-" if user_ut_save_path == None else user_ut_save_path
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
                user_ut_save_path = new_path
                input("<-Back")
                
        elif sel == "Open game path in default file manager":
            if user_ut_save_path == None:
                print(f"[{RED}-{RESET}]: You dont have a valid path to open.")
                input("<-Back")
            else:
                Popen(["explorer.exe",str(user_ut_save_path)])
    
    def sett_save_backup():
        """Save and load backup files."""
        result = "[*] Backup file found." if 'file0' in [f.name for f in user_game_save_backup.iterdir() if f.is_file()] else "[!] No backup file found."
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

# Looks like a functional __main__, thats awesome!
def main():
    check_user_game_exe_path()
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
    main()

