import customtkinter
from tkinter import PhotoImage, Label, messagebox
from PIL import Image
import minecraft_launcher_lib
import subprocess
import pickle
import psutil
import os

def dummyFunc():
    print("Hello World")
    
    
def get_total_ram_gb():
    mem = psutil.virtual_memory()
    ram_gb = mem.total / (1024**3)
    return round(ram_gb)


class Profile:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.profile_directory = "instances/"+self.name
 
    def launch(self):
        self.found = False
        for element in minecraft_launcher_lib.utils.get_installed_versions(self.profile_directory):
            if element["id"] == self.version:
                self.found = True
                options = minecraft_launcher_lib.utils.generate_test_options()
                command = minecraft_launcher_lib.command.get_minecraft_command(self.version, self.profile_directory, options)
                subprocess.run(command)
                self.found = False
        if self.found == False:
            minecraft_launcher_lib.install.install_minecraft_version(self.version, self.profile_directory)
            self.launch()



class Launcher:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("1000x550")
        self.root.title("Astro Launcher 2")
        self.root.resizable(False, False)
        self.root.iconbitmap("assets/icon.ico")
        self.root.configure(fg_color="#1C1C1C")
        self.bg_img= PhotoImage(file = "assets/background.png")
        self.bg= Label(self.root, image = self.bg_img)
        self.gear = Image.open("assets/settings.png")
        
        self.profile_list = self.loadProfilesList()
        self.profileListByName = []
        self.getProfileListByName()
        
        self.setupWidgets()
        
        
        
        
    def setupWidgets(self):
        self.play_button = customtkinter.CTkButton(self.root, command=self.startGame,
                                            fg_color="#47316F",
                                            bg_color="#1C1C1C",
                                            hover_color="#342451",
                                            text="PLAY",
                                            width=200,
                                            height=50,
                                            corner_radius=20,
                                            font=("Arial", 25, "bold"))

        self.settings_button = customtkinter.CTkButton(self.root,
                                                command=self.settingsPage,
                                                image=customtkinter.CTkImage(self.gear, size=(30, 30)),
                                                fg_color="#47316F",
                                                bg_color="#1C1C1C",
                                                hover_color="#342451",
                                                text="",
                                                width=50,
                                                height=50,
                                                corner_radius=20)

        self.addProfileButton = customtkinter.CTkButton(self.root,
                                                    command=self.createProfilePage,
                                                    fg_color="#47316F",
                                                    bg_color="#1C1C1C",
                                                    hover_color="#342451",
                                                    text="+",
                                                    width=46,
                                                    height=28,
                                                    corner_radius=100)

        self.profilesComboboxVariable = customtkinter.StringVar()
        self.profilesCombobox = customtkinter.CTkComboBox(self.root,
                                            variable=self.profilesComboboxVariable,
                                            values=self.profileListByName,
                                            bg_color="#1C1C1C", 
                                            fg_color="#47316F", 
                                            button_color="#47316F", 
                                            border_color="#47316F", 
                                            text_color="white", 
                                            state="readonly", 
                                            corner_radius=15, 
                                            width=150)

        self.editProfile = customtkinter.CTkButton(self.root,
                                                text="EDIT PROFILE",
                                                height=26,
                                                command=lambda: self.editProfilePage(self.profilesComboboxVariable.get()),
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

        self.backButton = customtkinter.CTkButton(self.root,
                                                command=self.mainPage,
                                                fg_color="#972626",
                                                bg_color="#1C1C1C",
                                                hover_color="#751F1F",
                                                text="CANCEL",
                                                width=200,
                                                height=50,
                                                corner_radius=20,
                                                font=("Arial", 25, "bold"))
        self.createProfileButton = customtkinter.CTkButton(self.root,
                                                command=self.createProfile,
                                                fg_color="#348D5C",
                                                bg_color="#1C1C1C",
                                                hover_color="#24512F",
                                                text="SAVE",
                                                width=200,
                                                height=50,
                                                corner_radius=20,
                                                font=("Arial", 25, "bold"))
        
        self.deleteProfileButton = customtkinter.CTkButton(self.root, 
                                            text="DELETE PROFILE",
                                            width=500,
                                            height=50,
                                            corner_radius=20)
        self.profileDirButton = customtkinter.CTkButton(self.root, 
                                            text="OPEN DICTORY",
                                            width=500,
                                            height=50,
                                            corner_radius=20)
        self.profileNameEntry = customtkinter.CTkEntry(self.root,
                                                height=50,
                                                placeholder_text="*profile name",
                                                placeholder_text_color="gray",
                                                bg_color="#1C1C1C",
                                                fg_color="white",
                                                border_color="white",
                                                text_color="black",
                                                corner_radius=15,
                                                width=500)
        self.profileEditionLabel = customtkinter.CTkLabel(self.root, 
                                       text="Profile Edition",
                                       font=("Arial", 50, "bold"))
        self.profileCreationLabel = customtkinter.CTkLabel(self.root, 
                                       text="Profile Creation",
                                       font=("Arial", 50, "bold"))
        self.versionsComboboxVariable = customtkinter.StringVar()
        self.versionsCombobox = customtkinter.CTkComboBox(self.root,
                                            variable=self.versionsComboboxVariable,
                                            bg_color="#1C1C1C", 
                                            fg_color="#47316F", 
                                            button_color="#47316F", 
                                            border_color="#47316F", 
                                            text_color="white", 
                                            state="readonly", 
                                            height=50,
                                            corner_radius=15,
                                            width=500)
                
                
    def clearUi(self):
        self.play_button.place_forget()
        self.settings_button.place_forget()
        self.addProfileButton.place_forget()
        self.profilesCombobox.place_forget()
        self.editProfile.place_forget()
        self.loading_bar.place_forget()
        self.backButton.place_forget()
        self.createProfileButton.place_forget()
        self.deleteProfileButton.place_forget()
        self.profileDirButton.place_forget()
        self.profileNameEntry.place_forget()
        self.profileEditionLabel.place_forget()
        self.versionsCombobox.place_forget()
        self.profileCreationLabel.place_forget()
        print("SCREEN CLEARED")

    def loadingPage(self):
        self.clearUi()
        self.bg.pack()
        self.loading_bar.place(x=50, y=485)
        self.loading_bar.start()
        self.backButton.place(x=750, y=470)
        print("LOADING PAGE DISPLAYED")

    def mainPage(self):
        self.clearUi()
        self.bg.pack()
        self.profilesComboboxVariable.set("latest")
        self.profilesCombobox.place(x=50, y=460)
        self.addProfileButton.place(x=204, y=460)
        self.editProfile.place(x=50, y=500)
        self.settings_button.place(x=670, y=470)
        self.play_button.place(x=750, y=470)
        print("MAIN PAGE DISPLAYED")
        
    def settingsPage(self):
        self.clearUi()
        self.bg.pack_forget()
        print("SETTINGS PAGE DISPLAYED")
        
    def editProfilePage(self, profile):
        self.clearUi()
        self.bg.pack_forget()
        self.backButton.place(x=750, y=470)
        self.createProfileButton.place(x=525, y=470)
        self.deleteProfileButton.place(relx=0.5, rely=0.72, anchor="center")
        self.profileDirButton.place(relx=0.5, rely=0.60, anchor="center")
        self.profileNameEntry.place(relx=0.5, rely=0.36, anchor="center")
        self.profileEditionLabel.place(relx=0.5, rely=0.1, anchor="center")
        self.versionsCombobox.place(relx=0.5, rely=0.48, anchor="center")
        self.availableVersions = self.getAvailableVersions(profile)
        self.versionsCombobox.configure(values=self.availableVersions)
        print("EDIT PROFILE PAGE DISPLAYED")
        
    def createProfilePage(self):
        self.clearUi()
        self.bg.pack_forget()
        self.profileNameEntry.place(relx=0.5, rely=0.36, anchor="center")
        self.backButton.place(x=750, y=470)
        self.createProfileButton.place(x=525, y=470)
        self.profileCreationLabel.place(relx=0.5, rely=0.1, anchor="center") 
        self.versionsCombobox.place(relx=0.5, rely=0.48, anchor="center")       
        print("EDIT PROFILE PAGE DISPLAYED")
        self.installableversions = self.getVersions()
        self.versionsCombobox.configure(values=self.installableversions)
#/!\WILL SOON BE SEPARED FROM THE GUI CLASS/!\
    def getVersions(self):
        self.versionsList = []
        for version in minecraft_launcher_lib.utils.get_version_list():
            if version["type"] == "release": self.versionsList.append(version["id"])
        return self.versionsList
            
    def getAvailableVersions(self, profile):
        self.availableVersionsList = []
        for version in minecraft_launcher_lib.utils.get_available_versions(profile.profile_directory):
            if version["type"] == "release": self.availableVersionsList.append(version["id"])
        return self.availableVersionsList
    
    def display(self):
        self.mainPage()
        self.root.mainloop()
        
    def createProfile(self):
        self.profile_list.append(Profile(self.profileNameEntry.get(), self.versionsCombobox.get()))
        self.saveProfiles()
        self.profile_list = self.loadProfilesList()
        self.profilesCombobox.configure(values=self.getProfileListByName())
        self.mainPage()
        
    def saveProfiles(self):
        with open("profiles.dat", "wb") as f:
                pickle.dump(self.profile_list, f)
    
    def loadProfilesList(self):
        filename = "profiles.dat"
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            return []
        with open(filename, "rb") as f:
            return pickle.load(f)
        
    def getProfileListByName(self):
        self.profileListByName = []
        if len(self.profile_list) == 0: 
            return self.profileListByName
        else:
            for element in self.profile_list:
                self.profileListByName.append(element.name)
            return self.profileListByName
        
    def getProfileFromName(self, name):
        for i in range(len(self.profileListByName)):
            if name == self.profile_list[i].name:
                return self.profile_list[i]
    
    def startGame(self):
        self.loadingPage()
        self.selectedProfileName = self.profilesComboboxVariable.get()
        self.selectedProfile = self.getProfileFromName(self.selectedProfileName)
        self.selectedProfile.launch()
        
        

app = Launcher()
app.display()