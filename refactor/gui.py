import random
from tkinter import Label, PhotoImage
import customtkinter
from PIL import Image


customtkinter.set_default_color_theme("assets/theme.json")

class Gui:
    def __init__(self): #Initialize launcher window, assets, state, and widgets
            self.root = customtkinter.CTk()
            self.root.geometry("1000x550")
            self.root.title("Astro Launcher 2")
            self.root.resizable(False, False)
            self.root.iconbitmap("assets/icon.ico")
            self.root.configure(fg_color="#1C1C1C")
            
            self.bg_number = random.randint(0, 2)
            if self.bg_number == 0: self.bg_img = PhotoImage(file="assets/background1.png")
            elif self.bg_number == 1: self.bg_img = PhotoImage(file="assets/background2.png")
            elif self.bg_number == 2: self.bg_img = PhotoImage(file="assets/background3.png")  
            self.bg = Label(self.root, image=self.bg_img)      

            self.play_img = Image.open("assets/play.png")
            self.settings_img = Image.open("assets/settings.png")
            self.creeper_img = Image.open("assets/off_login_logo.png")
            self.block_img = Image.open("assets/block_logo.png")
            
            self.setup_widgets()
            
    def setup_widgets(self): #Filling widgets proprieties
        self.play_button = customtkinter.CTkButton(self.root,
                                                    text="PLAY ",
                                                    width=200,
                                                    height=50,
                                                    corner_radius=20,
                                                    image=customtkinter.CTkImage(self.play_img, size=(30, 30)),
                                                    compound="right",
                                                    font=("Arial", 25, "bold"))
                                                    
        self.settings_button = customtkinter.CTkButton(self.root,
                                                    text="",
                                                    width=50,
                                                    height=50,
                                                    corner_radius=20,
                                                    image=customtkinter.CTkImage(self.settings_img, size=(30, 30)))

        self.add_profile_button = customtkinter.CTkButton(self.root,
                                                            text="+",
                                                            width=46,
                                                            height=28,
                                                            corner_radius=100)

        self.profiles_combobox_variable = customtkinter.StringVar()
        self.profiles_combobox = customtkinter.CTkComboBox(self.root,
                                                            variable=self.profiles_combobox_variable,
                                                            state="readonly", 
                                                            corner_radius=15, 
                                                            width=150)

        self.edit_profile_button = customtkinter.CTkButton(self.root,
                                                                text="EDIT PROFILE",
                                                                height=26,
                                                                corner_radius=15,
                                                                width=200)

        self.loading_bar = customtkinter.CTkProgressBar(self.root,
                                                            mode="indeterminate",
                                                            width=900,
                                                            height=20,
                                                            corner_radius=100)
        
        self.loading_label = customtkinter.CTkLabel(self.root, 
                                                        text="Downloading files ...",
                                                        font=("Arial", 15, "bold"))

        self.back_button = customtkinter.CTkButton(self.root,
                                                        fg_color="#972626",
                                                        hover_color="#751F1F",
                                                        text="CANCEL",
                                                        width=200,
                                                        height=50,
                                                        corner_radius=20,
                                                        font=("Arial", 25, "bold"))
        
        self.create_profile_button = customtkinter.CTkButton(self.root,
                                                                fg_color="#28A33C",
                                                                hover_color="#1B6D28",
                                                                text="CREATE",
                                                                width=200,
                                                                height=50,
                                                                corner_radius=20,
                                                                font=("Arial", 25, "bold"))
        
        self.save_edited_profile_button = customtkinter.CTkButton(self.root,
                                                                fg_color="#28A33C",
                                                                hover_color="#1B6D28",
                                                                text="SAVE",
                                                                width=200,
                                                                height=50,
                                                                corner_radius=20,
                                                                font=("Arial", 25, "bold"))
        
        self.delete_profile_button = customtkinter.CTkButton(self.root,
                                                            text="DELETE PROFILE",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)
        
        self.profile_name_entry = customtkinter.CTkEntry(self.root,
                                                                height=50,
                                                                placeholder_text="*profile name",
                                                                corner_radius=15,
                                                                width=500)
        
        self.profile_edition_label = customtkinter.CTkLabel(self.root, 
                                                        text="Profile Editor",
                                                        font=("Arial", 50, "bold"))
        
        self.profile_creation_label = customtkinter.CTkLabel(self.root, 
                                                        text="New Profile",
                                                        font=("Arial", 50, "bold"))
        
        self.block = customtkinter.CTkImage(light_image=self.block_img,
                                        dark_image=self.block_img,
                                        size=(200, 200))
        self.block = customtkinter.CTkLabel(self.root, image=self.block, text="")
        
        self.versions_combobox_variable = customtkinter.StringVar()
        self.versions_combobox = customtkinter.CTkComboBox(self.root,
                                                            variable=self.versions_combobox_variable,
                                                            state="readonly", 
                                                            height=50,
                                                            corner_radius=15,
                                                            width=500)

        self.add_loader_button = customtkinter.CTkButton(self.root,
                                bg_color="#1C1C1C",
                                text="+",
                                width=50,
                                height=50,
                                corner_radius=15,
                                font=("Arial", 30, "bold"))
            
        self.profile_dir_button = customtkinter.CTkButton(self.root,
                                                            text="OPEN DIRECTORY",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)

        self.connection_label = customtkinter.CTkLabel(self.root, 
                                                        text="Welcome !",
                                                        font=("Arial", 50, "bold"))
        
        self.creeper = customtkinter.CTkImage(light_image=self.creeper_img,
                                        dark_image=self.creeper_img,
                                        size=(200, 200))
        self.creeper = customtkinter.CTkLabel(self.root, image=self.creeper, text="")
        
        self.username_entry = customtkinter.CTkEntry(self.root,
                                                                height=50,
                                                                placeholder_text="*username",
                                                                corner_radius=15,
                                                                width=500)
        
        self.off_login_button = customtkinter.CTkButton(self.root,
                                                            text="LOGIN",
                                                            width=500,
                                                            height=50,
                                                            corner_radius=20)
                                                        
        self.settings_label_title = customtkinter.CTkLabel(self.root, 
                                                        text="Settings",
                                                        font=("Arial", 50, "bold"))
        
        self.ram_slider = customtkinter.CTkSlider(self.root,
                                                width=500,
                                                command=self.update_ram_label,
                                                from_=2,
                                                )
                                                
        self.ram_value_label = customtkinter.CTkLabel(self.root, 
                                                    text="Allocated RAM: 2 GB",
                                                    font=("Arial", 25, "bold"))
                                                    
        self.save_settings_button = customtkinter.CTkButton(self.root,
                                                                fg_color="#28A33C",
                                                                hover_color="#1B6D28",
                                                                text="SAVE",
                                                                width=200,
                                                                height=50,
                                                                corner_radius=20,
                                                                font=("Arial", 25, "bold"))

        self.widgets = [
            self.play_button,
            self.settings_button,
            self.add_profile_button,
            self.profiles_combobox,
            self.edit_profile_button,
            self.loading_bar,
            self.back_button,
            self.create_profile_button,
            self.save_edited_profile_button,
            self.delete_profile_button,
            self.profile_dir_button,
            self.profile_name_entry,
            self.profile_edition_label,
            self.versions_combobox,
            self.add_loader_button,
            self.profile_creation_label,
            self.username_entry,
            self.connection_label,
            self.off_login_button,
            self.creeper,
            self.block,
            self.loading_label,
            self.settings_label_title,
            self.ram_slider,
            self.ram_value_label,
            self.save_settings_button,
        ]
              
    def clear_ui(self): #Clearing the widgets in the window
        for widget in self.widgets:
            widget.place_forget()

    def loading_page(self, text): #Displaying loading page widgets in the window
        self.clear_ui()
        self.bg.pack()
        self.loading_bar.place(relx=0.05, rely=0.882)
        self.loading_label.place(relx=0.05, rely=0.92)
        self.loading_label.configure(text=text)
        self.loading_bar.start()
        
    def off_login_page(self): #Displaying offline login page widgets in the window
        self.clear_ui()
        self.bg.pack_forget()
        self.connection_label.place(relx=0.5, rely=0.1, anchor="center")
        self.creeper.place(relx=0.5, rely=0.37, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.68, anchor="center")
        self.off_login_button.place(relx=0.5, rely=0.80, anchor="center")
        
    def main_page(self): #Displaying main page widgets in the window
        self.clear_ui()
        self.bg.pack()
        self.profiles_combobox.place(relx=0.05, rely=0.836)
        self.add_profile_button.place(relx=0.204, rely=0.836)
        self.edit_profile_button.place(relx=0.05, rely=0.91)
        self.settings_button.place(relx=0.66, rely=0.855)
        self.play_button.place(relx=0.75, rely=0.855)
        
    def settings_page(self): #Displaying settings page widgets in the window
        self.clear_ui()
        self.bg.pack_forget()

        self.settings_label_title.place(relx=0.5, rely=0.1, anchor="center")
        
        self.ram_value_label.place(relx=0.5, rely=0.4, anchor="center")
        self.ram_slider.place(relx=0.5, rely=0.5, anchor="center")
        
        self.back_button.place(relx=0.75, rely=0.855)
        self.save_settings_button.place(relx=0.525, rely=0.855)
        
    def edit_profile_page(self): #Displaying profile edition page widgets in the window
        self.clear_ui()
        self.bg.pack_forget()

        self.back_button.place(relx=0.75, rely=0.855)
        self.save_edited_profile_button.place(relx=0.525, rely=0.855)

        self.delete_profile_button.place(relx=0.5, rely=0.72, anchor="center")

        self.profile_dir_button.place(relx=0.5, rely=0.60, anchor="center")
        
        self.profile_name_entry.place(relx=0.5, rely=0.36, anchor="center")
        
        self.profile_edition_label.place(relx=0.5, rely=0.1, anchor="center")
        
        self.versions_combobox.configure(width=442)
        self.versions_combobox.place(relx=0.25, rely=0.48, anchor="w")
        
        self.add_loader_button.place(relx=0.7, rely=0.48, anchor="w")
        
    def create_profile_page(self): #Displaying profile creation page widgets in the window
        self.clear_ui()
        self.bg.pack_forget()

        self.profile_name_entry.place(relx=0.5, rely=0.58, anchor="center")

        self.back_button.place(relx=0.75, rely=0.855)
        self.create_profile_button.place(relx=0.525, rely=0.855)

        self.profile_creation_label.place(relx=0.5, rely=0.1, anchor="center")
        self.block.place(relx=0.5, rely=0.33, anchor="center")

        self.versions_combobox.configure(width=500)
        self.versions_combobox.place(relx=0.5, rely=0.70, anchor="center")
        
    def display(self): #Displaying the window on the offline login page
        self.off_login_page()
        self.root.mainloop()

    def fill_profiles_combobox(self, profiles_list): #Filling the profiles combobox with the profiles names
        self.profiles_combobox.configure(values=profiles_list)

    def fill_versions_combobox(self, versions_list): #Filling the versions combobox with the versions names
        self.versions_combobox.configure(values=versions_list)

    def update_ram_label(self, value): #Updating the allocated ram label with the slider value
        self.ram_value_label.configure(text=f"Allocated RAM: {int(float(value))} GB")