from conversion import (
    detecter_type,
    convertir_discord,
    convertir_whatsapp,
    convertir_instagram,
    convertir_sms,
    get_nom_conv
)
import os

def fusionner_conversations(fichiers, log_func):
    contenu_fusionne = ["[Multi]\n"]
    nb_convs = 0
    for fichier in fichiers:
        type_conv = detecter_type(fichier)
        nom_sans_ext = os.path.splitext(os.path.basename(fichier))[0]
        log_func(f"[{type_conv}] Processing {os.path.basename(fichier)}...")
        try:
            if type_conv == "Discord":
                conv = convertir_discord(fichier)
                plateforme = "Discord"
                nom_conv = get_nom_conv(fichier, plateforme, nom_sans_ext)
            elif type_conv == "WhatsApp":
                conv = convertir_whatsapp(fichier)
                plateforme = "WhatsApp"
                nom_conv = get_nom_conv(fichier, plateforme, nom_sans_ext)
            elif type_conv == "Instagram":
                conv, titre = convertir_instagram(fichier)
                plateforme = "Insta"
                nom_conv = get_nom_conv(fichier, plateforme, nom_sans_ext, titre)
            elif type_conv == "SMS":
                conv = convertir_sms(fichier)
                plateforme = "SMS"
                nom_conv = get_nom_conv(fichier, plateforme, nom_sans_ext)
            else:
                log_func(f"[{type_conv}] File ignored: {os.path.basename(fichier)}")
                continue
            contenu_fusionne.append(f"[{plateforme}]({nom_conv})\n")
            contenu_fusionne.extend(conv.splitlines()[2:])
            contenu_fusionne.append("")
            nb_convs += 1
        except Exception as e:
            log_func(f"[{type_conv}] Error processing {os.path.basename(fichier)}: {e}")
    if nb_convs > 0:
        with open("data.lov", "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(contenu_fusionne))
        log_func("✅ Merged file created: data.lov")
    else:
        log_func("No valid conversation file found. No data.lov created.")