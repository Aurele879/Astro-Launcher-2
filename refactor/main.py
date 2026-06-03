import configparser
from gui import Gui
from profile import Profile
import pickle
import os
from tkinter import messagebox
import minecraft_launcher_lib
import json
import threading
import uuid
import hashlib

"""
Global Variables
"""
ui = Gui()
username = None
config = configparser.ConfigParser()
profile_list = []
ram = "2"

"""
Backend
"""
def get_options():
    options = {
    "username": username,
    "uuid": str(uuid.UUID(bytes=hashlib.md5(bytes(f"OfflinePlayer:{username}", "utf-8")).digest()[:16])),
    "token": "",
    "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"]}
    return options

def get_profiles_list(): #Load the stored profiles list
    filename = "profiles.dat"
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []
    with open(filename, "rb") as f:
        return pickle.load(f)

def get_profile_list_by_name(): #Returns a list with all the profiles's names
    profile_list_by_name = []
    for element in get_profiles_list():
        profile_list_by_name.append(element.name)
    return profile_list_by_name

def get_profile_from_name(name): #Returns a profile from its name
    for profile in get_profiles_list():
        if profile.name == name:
            return profile

def save_last_used_profile(): #Save the last used profile in the config file
    config.set('GUI', 'last_used_profile', ui.profiles_combobox_variable.get())
    with open("config.ini", 'w') as configfile:
        config.write(configfile)

def save_profiles(): #Save a profile
    with open("profiles.dat", "wb") as f:
            pickle.dump(profile_list, f)

def create_profile(): #Create a profile
    os.mkdir(f"instances/{ui.profile_name_entry.get()}")
    create_dummy_launcher_config(f"instances/{ui.profile_name_entry.get()}", ui.versions_combobox.get())
    profile_list.append(Profile(ui.profile_name_entry.get(), ui.versions_combobox.get()))
    save_profiles()
    ui.profiles_combobox_variable.set(ui.profile_name_entry.get())
    save_last_used_profile()
    go_to_main()

def get_available_versions(): #Returns all the official versions of the game
    versions_list = []
    for version in minecraft_launcher_lib.utils.get_version_list():
        if version["type"] == "release": versions_list.append(version["id"])
    return versions_list
        
def get_installed_and_available_versions(selected_profile): #Returns all the official versions of the game and the ones installed
    versions_list = []
    for version in minecraft_launcher_lib.utils.get_available_versions(selected_profile.profile_directory):
        if version["type"] in ["release", "forge", "neoforge", "fabric"]:
            versions_list.append(version["id"])
    return versions_list

def create_dummy_launcher_config(profile_directory, version): #Create a dummy launcher_profiles.json to avoid errors when launching the game for the first time
        data = {
            "profiles": {
                "Default": {
                    "name": "Default",
                    "type": "custom",
                    "created": "2026-01-01T00:00:00.000Z",
                    "lastUsed": "2026-01-01T00:00:00.000Z",
                    "icon": "Grass",
                    "lastVersionId": version
                }
            },
            "settings": {
                "crashAssistance": True,
                "enableAdvanced": True
            },
            "launcherVersion": {
                "format": 21,
                "name": "2.x",
                "profilesFormat": 3
            }
        }
        if os.path.exists(os.path.join(profile_directory, "launcher_profiles.json")):
            os.remove(os.path.join(profile_directory, "launcher_profiles.json"))
        os.makedirs(profile_directory, exist_ok=True)
        path = os.path.join(profile_directory, "launcher_profiles.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def download_game_files(profile): #Install missing version if needed, then launch
    found = False
    for element in minecraft_launcher_lib.utils.get_installed_versions(profile.profile_directory):
        if element["id"] == profile.version:
            found = True
            start_game()
    if found == False:
        minecraft_launcher_lib.install.install_minecraft_version(profile.version, profile.profile_directory)
        profile.launch()

def start_game(): #Start the game files download and launch
    selected_profile_name = ui.profiles_combobox_variable.get()
    if selected_profile_name == "none":
        messagebox.showerror("Error", "Create a profile first !")
        return
    ui.loading_page(text='Downloading game files ...')
    selected_profile = get_profile_from_name(selected_profile_name)
    save_last_used_profile()
    selected_profile.set_options = get_options()
    thread = threading.Thread(target=lambda: download_game_files(selected_profile), daemon=True)
    thread.start()

        


"""
Frontend interactions
"""
def connect():
    username = ui.username_entry.get()
    if len(username) == 0:
        messagebox.showerror("Error", "Username cannot be empty.")
        return
    for element in username:
        if element not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_":
            messagebox.showerror("Error", "Username can only contain letters, numbers and underscores.")
            return
    go_to_main()


def go_to_settings():
    ui.settings_page()

def go_to_main():
    ui.fill_profiles_combobox(get_profile_list_by_name()) #Filling the profiles combobox with the profiles names
    ui.main_page()

def go_to_new_profile():
    ui.create_profile_page()

def go_to_edit_profile():
    ui.edit_profile_page()
    ui.versions_combobox.set(get_installed_and_available_versions(get_profile_from_name(ui.profile_name_entry.get()))) #Setting the default version to the first one in the list)

def run():
    ui.create_profile_button.configure(command=lambda: create_profile())
    ui.off_login_button.configure(command=lambda: connect())
    ui.settings_button.configure(command=lambda: go_to_settings())
    ui.add_loader_button.configure(command=lambda: go_to_new_profile())
    ui.edit_profile_button.configure(command=lambda: go_to_edit_profile())
    ui.play_button.configure(command=lambda: start_game())
    ui.create_profile_button.configure(command=lambda: create_profile())
    ui.add_profile_button.configure(command=lambda: ui.create_profile_page())
    #ui.save_edited_profile_button.configure(command=lambda: save_profiles())
    ui.back_button.configure(command=lambda: go_to_main())
    ui.display()

if __name__ == "__main__":
    profile_list = get_profiles_list()
    if not os.path.exists("config.ini"):
        config['GUI'] = {
            'last_used_profile': 'none',
            'last_used_nickname': 'Steve',
            'ram_allocation': '2'
        }
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')

    if not os.path.exists("instances"):
        os.mkdir("instances")
    run()