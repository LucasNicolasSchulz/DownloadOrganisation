import os
import shutil
from tkinter import *
from tkinter import filedialog, scrolledtext

class Organizer:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.extensions = {
            'PowerPoint': ['.pptx'],
            'Bilder': ['.jfif', '.png', '.jpg'],
            'Text': ['.txt', '.rtf'],
            'Code': ['.ipynb', '.js', '.json', '.xml'],
            'Video': ['.wmv', '.mp4'],
            'Audio': ['.mp3', '.wav', '.aac'],
            '3D Modelle': ['.fbx', '.blend'],
            'Installer/Executable': ['.exe', '.msi'],
            'Komprimierte Dateien': ['.zip', '.rar', '.7z', '.xz']
        }

    def organize_files(self, extension_types, output_text):
        for extension_type in extension_types:
            # Für 'Code'-Dateien in einem speziellen 'Code'-Ordner
            if extension_type == 'Code':
                target_folder = os.path.join('C:\\Users\\space\\OneDrive\\Dokumente\\download_organistation', 'Code', extension_type)
            else:
                target_folder = os.path.join('C:\\Users\\space\\OneDrive\\Dokumente\\download_organistation', extension_type)
            
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            for file in os.listdir(self.source_folder):
                filename, file_extension = os.path.splitext(file)

                if file_extension.lower() in self.extensions[extension_type]:
                    source = os.path.join(self.source_folder, file)
                    destination = os.path.join(target_folder, file)

                    shutil.move(source, destination)
                    output_text.insert(END, f"Moved {file} to {extension_type}\n")

class OrganizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Download Organizer")
        self.master.geometry("600x400")
        self.check_vars = {}
        self.folder_var = StringVar(self.master)  # Für die Dropdown-Auswahl
        self.create_dropdown()
        self.create_checkboxes()
        self.start_button()
        self.output_text = scrolledtext.ScrolledText(self.master, wrap=WORD, width=70, height=10)
        self.output_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_dropdown(self):
        folders = {
            "Downloads": "C:\\Users\\space\\Downloads",
            "Desktop": "C:\\Users\\space\\OneDrive\\Desktop",
        }
        self.folder_var.set("Downloads")  # Setzen Sie den Standardwert
        Label(self.master, text="Wählen Sie einen Ordner:").grid(row=0, column=0, sticky=W, padx=10)
        OptionMenu(self.master, self.folder_var, *folders.keys()).grid(row=0, column=1, sticky=W, padx=10)

    def create_checkboxes(self):
        row_counter = 1  # Weil die Dropdown-Liste bereits in Zeile 0 ist
        for ext_type in Organizer("C:\\Users\\space\\Downloads").extensions.keys():
            self.check_vars[ext_type] = BooleanVar()
            Checkbutton(self.master, text=ext_type, variable=self.check_vars[ext_type]).grid(row=row_counter, column=0, sticky=W, padx=10)
            row_counter += 1

    def start_button(self):
        Button(self.master, text="Start", command=self.organisieren).grid(row=5, column=0, padx=10, pady=10)

    def organisieren(self):
        folder_mapping = {
            "Downloads": "C:\\Users\\space\\Downloads",
            "Desktop": "C:\\Users\\space\\OneDrive\\Desktop",
        }
        
        folder_path = folder_mapping[self.folder_var.get()]
        selected_types = [k for k, v in self.check_vars.items() if v.get()]
        org = Organizer(folder_path)
        org.organize_files(selected_types, self.output_text)
