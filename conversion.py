import os
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def detecter_type(fichier):
    nom = os.path.basename(fichier)
    if nom.startswith("Direct Messages") or "Salons textuels" in nom:
        return "Discord"
    elif nom.startswith("Discussion WhatsApp avec "):
        return "WhatsApp"
    elif nom.endswith(".html"):
        return "Instagram"
    elif nom.endswith(".xml"):
        return "SMS"
    else:
        return "Inconnu"

def convertir_discord(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    start_index = 0
    for i, ligne in enumerate(lignes):
        if ligne.strip() == "":
            start_index = i + 1
            break
    lignes = lignes[start_index:]
    conversations = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i].strip()
        match = re.match(r"\[(\d{2}/\d{2}/\d{4} \d{2}:\d{2})\] (.+)", ligne)
        if match:
            timestamp = match.group(1).replace(" ", ", ")
            pseudo = match.group(2)
            i += 1
        message_lignes = []
        while i < len(lignes) and lignes[i].strip() != "":
            message_lignes.append(lignes[i].strip())
            i += 1
        if match:
            message = " ".join(message_lignes)
            conversations.append(f"[{timestamp}] {pseudo} : {message}")
        else:
            i += 1
    return "[Discord]\n\n" + "\n".join(conversations) + "\n"

def convertir_whatsapp(fichier):
    def reformater_ligne(ligne):
        match = re.match(r"(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.*)", ligne)
        if match:
            date, auteur, message = match.groups()
            return f"[{date}] {auteur} : {message}"
        return None
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()
    messages = [reformater_ligne(l) for l in lignes]
    messages = [m for m in messages if m]
    return "[WhatsApp]\n\n" + "\n".join(messages) + "\n"

def convertir_instagram(fichier):
    def convertir_date_insta(date_str):
        from datetime import datetime
        mois_fr = {
            "janv": "01", "févr": "02", "mars": "03", "avr": "04", "mai": "05", "juin": "06",
            "juil": "07", "août": "08", "sept": "09", "oct": "10", "nov": "11", "déc": "12"
        }
        for mois in mois_fr:
            if date_str.lower().startswith(mois):
                num_mois = mois_fr[mois]
                reste = date_str[len(mois):].strip()
                date_modif = reste.replace(',', '')
                date_str_mod = f"{date_modif[:2]}-{num_mois}-{date_modif[3:]}"
                try:
                    dt = datetime.strptime(date_str_mod, "%d-%m-%Y %I:%M %p")
                    return dt.strftime("%d/%m/%Y, %H:%M")
                except:
                    return date_str
        return date_str
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.read()
    match_title = re.search(r"<title>(.*?)</title>", contenu, re.IGNORECASE | re.DOTALL)
    titre = match_title.group(1).strip() if match_title else os.path.splitext(os.path.basename(fichier))[0]
    soup = BeautifulSoup(contenu, "html.parser")
    messages = soup.find_all("div", class_="pam _3-95 _2ph- _a6-g uiBoxWhite noborder")
    lignes = []
    for msg in messages:
        nom = msg.find("h2")
        contenu = msg.select_one("._3-95._a6-p > div > div:nth-of-type(2)")
        date = msg.select_one("._3-94._a6-o")
        if nom and contenu and date:
            pseudo = nom.text.strip()
            message = " ".join(contenu.text.strip().splitlines())
            date_str = convertir_date_insta(date.text.strip())
            lignes.append(f"[{date_str}] {pseudo} : {message}")
    return "[Insta]\n\n" + "\n".join(lignes) + "\n", titre

def convertir_sms(fichier):
    def convertir_date_sms(date_str):
        try:
            mois_fr = {
                "janv.": "01", "févr.": "02", "mars": "03", "avr.": "04", "mai": "05", "juin": "06",
                "juil.": "07", "août": "08", "sept.": "09", "oct.": "10", "nov.": "11", "déc.": "12"
            }
            parties = date_str.split()
            jour = f"{int(parties[0]):02d}"
            mois = mois_fr[parties[1].lower()]
            annee = parties[2]
            heure, minute = parties[3].split(":")[:2]
            return f"{jour}/{mois}/{annee}, {heure}:{minute}"
        except:
            return date_str
    tree = ET.parse(fichier)
    root = tree.getroot()
    lignes = []
    for sms in root.findall("sms"):
        date_str = sms.get("readable_date")
        message = sms.get("body")
        type_sms = sms.get("type")
        if type_sms == "1":
            auteur = "Doliprane"
        elif type_sms == "2":
            auteur = "Mehdi"
        else:
            auteur = "Inconnu"
        if date_str and message:
            date_formatee = convertir_date_sms(date_str)
            lignes.append(f"[{date_formatee}] {auteur} : {message}")
    return "[SMS]\n\n" + "\n".join(lignes) + "\n"

def get_nom_conv(fichier, plateforme, nom_sans_ext, titre_insta=None):
    if plateforme == "Discord":
        base = os.path.splitext(os.path.basename(fichier))[0]
        match_dm = re.match(r"Direct Messages - (.+?) \[\d+\]", base)
        match_salon = re.match(r"(.+?) - Salons textuels - (.+?) \[\d+\]", base)
        if match_dm:
            return match_dm.group(1).strip()
        elif match_salon:
            return f"{match_salon.group(2).strip()} ({match_salon.group(1).strip()})"
        else:
            return nom_sans_ext
    elif plateforme == "WhatsApp":
        return os.path.basename(fichier).replace("Discussion WhatsApp avec ", "").replace(".txt", "")
    elif plateforme == "Insta":
        return titre_insta or nom_sans_ext
    else:
        return nom_sans_ext