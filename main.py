import customtkinter as ctk
from tkinter import filedialog
from fusion import fusionner_conversations
from conversion import detecter_type
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Merge to Lov")
        self.geometry("500x400")
        self.resizable(False, False)
        self.fichiers = []

        self.label_intro = ctk.CTkLabel(
            self,
            text="Convert convs. to data.lov",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_intro.pack(pady=10)

        frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        frame_buttons.pack(pady=10)

        self.button_add_files = ctk.CTkButton(
            frame_buttons, text="Add files", command=self.ajouter_fichiers
        )
        self.button_add_files.pack(side="left", padx=10)

        self.button_convert = ctk.CTkButton(
            frame_buttons, text="Merge to data.lov", command=self.lancer_conversion, state="disabled"
        )
        self.button_convert.pack(side="left", padx=10)

        self.button_clear = ctk.CTkButton(
            frame_buttons, text="Clear", command=self.clear_all
        )
        self.button_clear.pack(side="left", padx=10)

        self.label_fichiers = ctk.CTkLabel(self, text="No file selected")
        self.label_fichiers.pack(pady=10)

        self.text_fichiers = ctk.CTkTextbox(self, height=100, state="disabled")
        self.text_fichiers.pack(fill="x", padx=20, pady=5)

        self.text_log = ctk.CTkTextbox(self, height=100)
        self.text_log.pack(fill="both", expand=True, padx=20, pady=20)

    def ajouter_fichiers(self):
        fichiers = filedialog.askopenfilenames(
            title="Select files to merge",
            filetypes=[("Text, HTML, XML files", "*.txt *.html *.xml")]
        )
        if fichiers:
            self.fichiers = list(fichiers)
            self.afficher_fichiers()
            self.button_convert.configure(state="normal")
            self.log(f"{len(self.fichiers)} file(s) added.")

    def afficher_fichiers(self):
        self.text_fichiers.configure(state="normal")
        self.text_fichiers.delete("1.0", "end")
        if not self.fichiers:
            self.label_fichiers.configure(text="No file selected")
            self.text_fichiers.configure(state="disabled")
            return
        self.label_fichiers.configure(text="Selected files:")
        for fichier in self.fichiers:
            type_conv = detecter_type(fichier)
            self.text_fichiers.insert("end", f"[{type_conv}] {os.path.basename(fichier)}\n")
        self.text_fichiers.configure(state="disabled")

    def log(self, message):
        self.text_log.insert("end", message + "\n")
        self.text_log.see("end")

    def lancer_conversion(self):
        if not self.fichiers:
            self.log("Error: no file selected.")
            return
        self.log("Processing...")
        self.button_convert.configure(state="disabled")
        self.after(100, self.traiter_fichiers_selectionnes)

    def traiter_fichiers_selectionnes(self):
        fusionner_conversations(self.fichiers, self.log)
        self.button_convert.configure(state="normal")

    def clear_all(self):
        self.fichiers = []
        self.text_fichiers.configure(state="normal")
        self.text_fichiers.delete("1.0", "end")
        self.text_fichiers.configure(state="disabled")
        self.text_log.delete("1.0", "end")
        self.label_fichiers.configure(text="No file selected")
        self.button_convert.configure(state="disabled")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = App()
    app.mainloop()