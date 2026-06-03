import minecraft_launcher_lib
import subprocess
import threading

class Profile:
    def __init__(self, name, version): #Initialize a profile with default launch settings
        self.name = name
        self.version = version
        self.options = None
        self.profile_directory = "instances/" + self.name

    def set_options(self, options):
        self.options = options

    def launch(self): #Build launch command and start Minecraft process
            command = minecraft_launcher_lib.command.get_minecraft_command(self.version, self.profile_directory, self.options)
            
            process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)
            
            wait_thread = threading.Thread(target=self.wait_minecraft_close, args=(process,), daemon=True)
            wait_thread.start()