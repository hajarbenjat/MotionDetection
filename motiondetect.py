from tkinter import *
import cv2
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime

# Initialisation de l'application Tkinter
app = Tk()
app.bind('<Escape>', lambda e: app.quit())  # Associer la touche Echap pour quitter l'application

# Initialisation de la caméra et du DataFrame
video = cv2.VideoCapture(0)
largeur, hauteur = 800, 600
video.set(cv2.CAP_PROP_FRAME_WIDTH, largeur)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, hauteur)

# Création des labels pour le flux de la caméra et le compteur de mouvements
label_flux_camera = Label(app)
label_flux_camera.pack()
label_compteur_mouvements = Label(app, text="Mouvements: 0")
label_compteur_mouvements.pack()

# Initialisation des variables de détection de mouvement
arriere_plan_statique, liste_mouvements, temps, df = None, [None, None], [], pd.DataFrame(columns=["Début", "Fin"])

# Fonction pour détecter et dessiner les bordures du mouvement
def detecter_mouvement(cadre):
    global arriere_plan_statique, liste_mouvements, temps, df
    
    mouvement = 0  # Initialisation du mouvement = 0 (pas de mouvement)
    gris = cv2.cvtColor(cadre, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (21, 21), 0)

    if arriere_plan_statique is None:
        arriere_plan_statique = gris
    else:
        cadre_difference = cv2.absdiff(arriere_plan_statique, gris)
        seuil_cadre = cv2.threshold(cadre_difference, 30, 255, cv2.THRESH_BINARY)[1]
        seuil_cadre = cv2.dilate(seuil_cadre, None, iterations=2)
        contours, _ = cv2.findContours(seuil_cadre.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue
            mouvement = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(cadre, (x, y), (x + w, y + h), (0, 255, 0), 3)

        liste_mouvements.append(mouvement)
        liste_mouvements = liste_mouvements[-2:]

        if liste_mouvements[-1] == 1 and liste_mouvements[-2] == 0:
            temps.append(datetime.now())
            app.nouveau_mouvement_detecte = True

        if liste_mouvements[-1] == 0 and liste_mouvements[-2] == 1:
            temps.append(datetime.now())
            app.nouveau_mouvement_detecte = True

        if len(temps) >= 2:
            nouvelle_donnee = {"Début": temps[-2], "Fin": temps[-1]}
            df = pd.concat([df, pd.DataFrame([nouvelle_donnee])], ignore_index=True)

            if app.nouveau_mouvement_detecte:
                label_compteur_mouvements.config(text="Mouvements: {}".format(len(df)))
                app.nouveau_mouvement_detecte = False

    return cadre

# Fonction pour ouvrir la caméra et afficher le flux sur l'application
def ouvrir_camera():
    _, cadre = video.read()
    cadre_avec_mouvement = detecter_mouvement(cadre)
    image_opencv = cv2.cvtColor(cadre_avec_mouvement, cv2.COLOR_BGR2RGBA)
    image_capturee = Image.fromarray(image_opencv)
    photo_image = ImageTk.PhotoImage(image=image_capturee)
    label_flux_camera.photo_image = photo_image
    label_flux_camera.configure(image=photo_image)
    label_flux_camera.after(10, ouvrir_camera)

app.nouveau_mouvement_detecte = False
ouvrir_camera()
app.mainloop()
video.release()
cv2.destroyAllWindows()
