# Merge to Lov

**Merge to Lov** est une application Windows qui fusionne des conversations exportées de Discord, WhatsApp, Instagram et SMS Android en un seul fichier `data.lov` lisible et structuré.

> Ce projet est distribué sous licence [MIT](#-license).


## 📦 Fonctionnalités

- Sélectionnez plusieurs fichiers de conversations exportés (Discord, WhatsApp, Instagram, SMS)
- Affiche le type de chaque fichier sélectionné
- Fusionne toutes les conversations dans un seul fichier `data.lov`
- Interface graphique simple et rapide
- Aucun fichier source n’est modifié


## 📥 Tutoriel : Exporter vos conversations

### Discord

1. Ouvrez Discord sur PC.
2. Utilisez un outil comme [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) pour exporter vos conversations :
   - Téléchargez l’outil.
   - Suivez les instructions pour exporter vos salons ou messages privés au format `.txt`.
3. Placez les fichiers `.txt` exportés dans un dossier de votre choix.

### WhatsApp

1. Ouvrez WhatsApp sur votre téléphone.
2. Ouvrez la conversation à exporter.
3. Appuyez sur les trois points > **Plus** > **Exporter discussion**.
4. Choisissez **Sans médias** et transférez le fichier `.txt` sur votre PC.

### Instagram

1. Rendez-vous sur [Instagram Data Download](https://www.instagram.com/download/request/) (Paramètres > Confidentialité et sécurité > Télécharger les données).
2. Demandez une archive de vos données.
3. Une fois reçue par mail, téléchargez et extrayez l’archive.
4. Dans le dossier, ouvrez `your_instagram_activity`, ensuite `messages` puis sélectionnez le fichier `.html` de la conversation souhaitée.

### SMS Android

1. Utilisez une application comme [SMS Backup & Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore).
2. Sauvegardez vos SMS au format `.xml`.
3. Transférez le fichier `.xml` sur votre PC.


## 🚀 Utilisation de l’application

### 1. Lancer l’application

- Téléchargez le fichier `.exe` depuis la section [Releases](https://github.com/Maoeuf/MergeToLov/releases) de ce dépôt.
- Double-cliquez sur `MergeToLov.exe`.

### 2. Fusionner vos conversations

1. Cliquez sur **Add files** et sélectionnez vos fichiers `.txt`, `.html` ou `.xml` exportés.
2. Vérifiez la liste et le type détecté pour chaque fichier.
3. Cliquez sur **Merge to data.lov**.
4. Le fichier `data.lov` sera créé dans le même dossier que l’application.
5. Cliquez sur **Clear** pour réinitialiser la sélection si besoin.
## 🛠️ Compilation manuelle (optionnel)

Si vous souhaitez générer l’exécutable vous-même :

1. Installez Python 3.10+ et pip.
2. Installez les dépendances :
    ```
    pip install customtkinter bs4
    ```
3. Installez PyInstaller :
    ```
    pip install pyinstaller
    ```
4. Compilez :
    ```
    pyinstaller --onefile --noconsole main.py
    ```
5. L’exécutable sera dans le dossier `dist`.


## ❓ Support

Pour toute question, ouvrez une issue sur GitHub ou contactez-moi.


## 📝 License

This project is licensed under the [MIT License](LICENSE).