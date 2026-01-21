import customtkinter
from tkinter import PhotoImage, Label, messagebox
from PIL import Image
import minecraft_launcher_lib
import subprocess
import pickle
import uuid
import os
import shutil


if not os.path.exists("instances"):
    os.mkdir("instances")




class Profile:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.profile_directory = "instances/" + self.name
        self.username = app.username
        self.options = {"username": self.username,
                        "uuid": str(uuid.uuid4()),
                        "token": ""}
        
    def launch_sequence(self):
        self.found = False
        for element in minecraft_launcher_lib.utils.get_installed_versions(self.profile_directory):
            if element["id"] == self.version:
                self.found = True
                self.launch()
        if self.found == False:
            minecraft_launcher_lib.install.install_minecraft_version(self.version, self.profile_directory)
            self.launch()

    def launch(self):
        command = minecraft_launcher_lib.command.get_minecraft_command(self.version, self.profile_directory, self.options)
        subprocess.run(command)


class Launcher:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("1000x550")
        self.root.title("Astro Launcher 2")
        self.root.resizable(False, False)
        self.root.iconbitmap("assets/icon.ico")
        self.root.configure(fg_color="#1C1C1C")
        self.bg_img = PhotoImage(file="assets/background.png")
        self.bg = Label(self.root, image=self.bg_img)
        self.gear = Image.open("assets/settings.png")
        self.play = Image.open("assets/play.png")
        
        self.profile_list = self.load_profiles_list()
        self.profile_list_by_name = []
        self.get_profile_list_by_name()
        self.username = "Steve"
        
        self.setup_widgets()
        
    def setup_widgets(self):
        self.play_button = customtkinter.CTkButton(self.root, command=self.start_game,
                                                    fg_color="#47316F",
                                                    bg_color="#1C1C1C",
                                                    hover_color="#342451",
                                                    text="PLAY ",
                                                    width=200,
                                                    height=50,
                                                    corner_radius=20,
                                                    image=customtkinter.CTkImage(self.play, size=(30, 30)),
                                                    compound="right",
                                                    font=("Arial", 25, "bold"))

        self.settings_button = customtkinter.CTkButton(self.root,
                                                        command=self.settings_page,
                                                        image=customtkinter.CTkImage(self.gear, size=(30, 30)),
                                                        fg_color="#363636",
                                                        bg_color="#1C1C1C",
                                                        hover_color="#342451",
                                                        text="",
                                                        width=50,
                                                        height=50,
                                                        corner_radius=20)

        self.add_profile_button = customtkinter.CTkButton(self.root,
                                                            command=self.create_profile_page,
                                                            fg_color="#47316F",
                                                            bg_color="#1C1C1C",
                                                            hover_color="#342451",
                                                            text="+",
                                                            width=46,
                                                            height=28,
                                                            corner_radius=100)

        self.profiles_combobox_variable = customtkinter.StringVar()
        self.profiles_combobox = customtkinter.CTkComboBox(self.root,
                                                            variable=self.profiles_combobox_variable,
                                                            values=self.profile_list_by_name,
                                                            bg_color="#1C1C1C", 
                                                            fg_color="#47316F", 
                                                            button_color="#47316F", 
                                                            border_color="#47316F", 
                                                            text_color="white", 
                                                            state="readonly", 
                                                            corner_radius=15, 
                                                            width=150)

        self.edit_profile_button = customtkinter.CTkButton(self.root,
                                                                text="EDIT PROFILE",
                                                                height=26,
                                                                command=self.edit_profile_page,
                                                                fg_color="#47316F",
                                                                bg_color="#1C1C1C",
                                                                hover_color="#342451",
                                                                corner_radius=15,
                                                                width=200)

        self.loading_bar = customtkinter.CTkProgressBar(self.root,
                                                            mode="indeterminate",
                                                            width=660,
                                                            height=20,
                                                            corner_radius=100,
                                                            fg_color="#474747",
                                                            bg_color="#1C1C1C",
                                                            progress_color="#47316F")

        self.back_button = customtkinter.CTkButton(self.root,
                                                        command=self.main_page,
                                                        fg_color="#972626",
                                                        bg_color="#1C1C1C",
                                                        hover_color="#751F1F",
                                                        text="CANCEL",
                                                        width=200,
                                                        height=50,
                                                        corner_radius=20,
                                                        font=("Arial", 25, "bold"))
        
        self.create_profile_button = customtkinter.CTkButton(self.root,
                                                                command=self.create_profile,
                                                                fg_color="#348D5C",
                                                                bg_color="#1C1C1C",
                                                                hover_color="#24512F",
                                                                text="CREATE",
                                                                width=200,
                                                                height=50,
                                                                corner_radius=20,
                                                                font=("Arial", 25, "bold"))
        
        self.save_edited_profile_button = customtkinter.CTkButton(self.root,
                                                                command=self.edit_profile,
                                                                fg_color="#348D5C",
                                                                bg_color="#1C1C1C",
                                                                hover_color="#24512F",
                                                                text="SAVE",
                                                                width=200,
                                                                height=50,
                                                                corner_radius=20,
                                                                font=("Arial", 25, "bold"))
        
        self.delete_profile_button = customtkinter.CTkButton(self.root,
                                                            fg_color="#47316F",
                                                            bg_color="#1C1C1C",
                                                            hover_color="#342451",
                                                            command=self.delete_profile,
                                                            text="DELETE PROFILE",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)
        
        self.profile_dir_button = customtkinter.CTkButton(self.root,
                                                            fg_color="#47316F",
                                                            bg_color="#1C1C1C",
                                                            hover_color="#342451",
                                                            command=self.open_directory,
                                                            text="OPEN DICTORY",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)
        
        self.profile_name_entry = customtkinter.CTkEntry(self.root,
                                                                height=50,
                                                                placeholder_text="*profile name",
                                                                placeholder_text_color="gray",
                                                                bg_color="#1C1C1C",
                                                                fg_color="white",
                                                                border_color="white",
                                                                text_color="black",
                                                                corner_radius=15,
                                                                width=500)
        
        self.profile_edition_label = customtkinter.CTkLabel(self.root, 
                                                           text="Profile Edition",
                                                           font=("Arial", 50, "bold"))
        
        self.profile_creation_label = customtkinter.CTkLabel(self.root, 
                                                           text="Profile Creation",
                                                           font=("Arial", 50, "bold"))
        self.username_label = customtkinter.CTkLabel(self.root, 
                                                           text="Hello There !",
                                                           font=("Arial", 50, "bold"))
        self.username_entry = customtkinter.CTkEntry(self.root,
                                                                height=50,
                                                                placeholder_text="*username",
                                                                placeholder_text_color="gray",
                                                                bg_color="#1C1C1C",
                                                                fg_color="white",
                                                                border_color="white",
                                                                text_color="black",
                                                                corner_radius=15,
                                                                width=500)
        
        self.login_button = customtkinter.CTkButton(self.root,
                                                            fg_color="#47316F",
                                                            bg_color="#1C1C1C",
                                                            hover_color="#342451",
                                                            command=self.login,
                                                            text="LOGIN",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)
        
        self.versions_combobox_variable = customtkinter.StringVar()
        self.versions_combobox = customtkinter.CTkComboBox(self.root,
                                                            variable=self.versions_combobox_variable,
                                                            bg_color="#1C1C1C", 
                                                            fg_color="#47316F", 
                                                            button_color="#47316F", 
                                                            border_color="#47316F", 
                                                            text_color="white", 
                                                            state="readonly", 
                                                            height=50,
                                                            corner_radius=15,
                                                            width=500)
                        
    def clear_ui(self):
        self.play_button.place_forget()
        self.settings_button.place_forget()
        self.add_profile_button.place_forget()
        self.profiles_combobox.place_forget()
        self.edit_profile_button.place_forget()
        self.loading_bar.place_forget()
        self.back_button.place_forget()
        self.create_profile_button.place_forget()
        self.save_edited_profile_button.place_forget()
        self.delete_profile_button.place_forget()
        self.profile_dir_button.place_forget()
        self.profile_name_entry.place_forget()
        self.profile_edition_label.place_forget()
        self.versions_combobox.place_forget()
        self.profile_creation_label.place_forget()
        self.username_entry.place_forget()
        self.username_label.place_forget()
        self.login_button.place_forget()
        print("SCREEN CLEARED")

    def loading_page(self):
        self.clear_ui()
        self.bg.pack()
        self.loading_bar.place(relx=0.05, rely=0.882)
        self.loading_bar.start()
        print("LOADING PAGE DISPLAYED")
        
    def login_page(self):
        self.clear_ui()
        self.bg.pack_forget()
        self.username_label.place(relx=0.5, rely=0.1, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.68, anchor="center")
        self.login_button.place(relx=0.5, rely=0.80, anchor="center")
        
    def main_page(self):
        self.clear_ui()
        self.bg.pack()
        self.profiles_combobox_variable.set("latest")
        self.profiles_combobox.place(relx=0.05, rely=0.836)
        self.add_profile_button.place(relx=0.204, rely=0.836)
        self.edit_profile_button.place(relx=0.05, rely=0.91)
        self.settings_button.place(relx=0.67, rely=0.855)
        self.settings_button.configure(state = "disabled")
        self.play_button.place(relx=0.75, rely=0.855)
        print("MAIN PAGE DISPLAYED")
        
    def settings_page(self):
        print("SETTINGS PAGE DISPLAYED")
        
    def edit_profile_page(self):
        if self.profiles_combobox_variable.get() == "latest" :
            messagebox.showwarning("Invalid Action", "You can't edit an integrated profile.")
            return
        self.clear_ui()
        self.bg.pack_forget()
        self.back_button.place(relx=0.75, rely=0.855)
        self.save_edited_profile_button.place(relx=0.525, rely=0.855)
        self.delete_profile_button.place(relx=0.5, rely=0.72, anchor="center")
        self.profile_dir_button.place(relx=0.5, rely=0.60, anchor="center")
        self.profile_name_entry.place(relx=0.5, rely=0.36, anchor="center")
        self.profile_edition_label.place(relx=0.5, rely=0.1, anchor="center")
        self.versions_combobox.place(relx=0.5, rely=0.48, anchor="center")
        
        self.profile = self.get_profile_from_name(self.profiles_combobox.get())
        self.available_versions = self.get_available_versions(self.profile)
        self.versions_combobox.configure(values=self.available_versions)
        self.versions_combobox.set(self.profile.version)
        self.profile_name_entry.insert(0, self.profile.name)
        
    def create_profile_page(self):
        self.clear_ui()
        self.bg.pack_forget()
        self.profile_name_entry.place(relx=0.5, rely=0.36, anchor="center")
        self.back_button.place(relx=0.75, rely=0.855)
        self.create_profile_button.place(relx=0.525, rely=0.855)
        self.profile_creation_label.place(relx=0.5, rely=0.1, anchor="center") 
        self.versions_combobox.place(relx=0.5, rely=0.48, anchor="center")       

        self.installable_versions = self.get_versions()
        self.versions_combobox.configure(values=self.installable_versions)
        self.latest_released_version = self.installable_versions[0]
        self.versions_combobox.set(self.latest_released_version)
        
    def gui_update(self):
        self.profiles_combobox.configure(values=self.get_profile_list_by_name())
        self.profile_name_entry.delete(0, customtkinter.END)
        
    def display(self):
        self.login_page()
        self.root.mainloop()
        
    def get_versions(self):
        self.versions_list = []
        for version in minecraft_launcher_lib.utils.get_version_list():
            if version["type"] == "release": self.versions_list.append(version["id"])
        return self.versions_list
            
    def get_available_versions(self, profile):
        self.available_versions_list = []
        for version in minecraft_launcher_lib.utils.get_available_versions(profile.profile_directory):
            if version["type"] == "release": self.available_versions_list.append(version["id"])
        return self.available_versions_list
    
    def create_profile(self):
        if self.profile_name_entry.get() == "" or " " in self.profile_name_entry.get():
            messagebox.showerror("Error", "Invalid Name.")
            return 1
        os.mkdir(f"instances/{self.profile_name_entry.get()}")
        self.profile_list.append(Profile(self.profile_name_entry.get(), self.versions_combobox.get()))
        self.save_profiles()
        self.gui_update()
        self.main_page()

    def edit_profile(self):
        old_name = self.profiles_combobox.get()
        new_name = self.profile_name_entry.get()
        new_version = self.versions_combobox.get()

        if not new_name:
            messagebox.showerror("Error", "Invalid Name.")
            return 1

        target_index = -1
        for i, p in enumerate(self.profile_list):
            if p.name == old_name:
                target_index = i
                break

        if target_index != -1:
            old_profile = self.profile_list[target_index]
            old_dir = old_profile.profile_directory
            new_dir = os.path.join("instances", new_name)
            os.rename(old_dir, new_dir)
            self.profile_list[target_index] = Profile(new_name, new_version)
            
            self.save_profiles()
            self.gui_update()
            self.main_page()

    def delete_profile(self):
        profile_name = self.profiles_combobox.get()
        if not messagebox.askyesno("Profile Removal", f"Are you sure you want to delete '{profile_name}' and all its data?"):
            return 1

        target_index = -1
        for i, p in enumerate(self.profile_list):
            if p.name == profile_name:
                target_index = i
                break

        if target_index != -1:
            profile_to_delete = self.profile_list[target_index]
            shutil.rmtree(profile_to_delete.profile_directory)
            self.profile_list.pop(target_index)

        self.save_profiles()
        self.gui_update()
        self.main_page()
        messagebox.showinfo("Profile Removal", f"Profile '{profile_name}' has been deleted.")
        
    def open_directory(self):
        profile_name = self.profiles_combobox.get()
        profile = self.get_profile_from_name(profile_name)
        path = os.path.abspath(profile.profile_directory)
        os.startfile(path)
        
    def save_profiles(self):
        with open("profiles.dat", "wb") as f:
            pickle.dump(self.profile_list, f)
        self.profile_list = self.load_profiles_list()
        
    def login(self):
        self.username = self.username_entry.get()
        if len(self.username) < 1 or " " in self.username:
            messagebox.showerror("Error", "Invalid Username.")
        else:
            self.main_page()
            
    
    def load_profiles_list(self):
        filename = "profiles.dat"
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return []
        with open(filename, "rb") as f:
            return pickle.load(f)
        
    def get_profile_list_by_name(self):
        self.profile_list_by_name = []
        if len(self.profile_list) == 0: 
            return self.profile_list_by_name
        else:
            for element in self.profile_list:
                self.profile_list_by_name.append(element.name)
            return self.profile_list_by_name
        
    def get_profile_from_name(self, name):
        for i in range(len(self.profile_list_by_name)):
            if name == self.profile_list[i].name:
                return self.profile_list[i]
    
    def start_game(self):
        self.loading_page()
        self.selected_profile_name = self.profiles_combobox_variable.get()
        self.selected_profile = self.get_profile_from_name(self.selected_profile_name)
        if self.profiles_combobox.get() == "latest":
            last_version = self.get_versions()
            self.selected_profile = Profile("latest", last_version[0])
            
        self.selected_profile.launch_sequence()
        

app = Launcher()
app.display()