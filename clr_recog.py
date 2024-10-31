import cv2
import numpy as np
from ball_shape import confirm_ballshape


def color_recog(img, color):
    #debugging
    bug = "nix"
    # Standardwerte für den Fall, dass keine Konturen gefunden werden
    largest_contour = None
    cx = -1
    cy = -1
    # leere Masken, weil "red" eine andere Maske benötigt
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Leere Maske für die allgemeine Farberkennung
    maskRed = np.zeros(img.shape[:2], dtype=np.uint8)  # Leere Maske für die rote Farberkennung

    # Frame in den HSV-Farbraum konvertieren
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Farbgrenzen für die Erkennung des blauen Balls definieren
    #lower_blue = np.array([120, 255, 220])  # Untere Grenze für blau
    #upper_blue = np.array([90, 120, 90])  # Obere Grenze für blau
    lower_blue = np.array([100, 150, 50])  # Niedrigere Schwellenwerte für Blau
    upper_blue = np.array([140, 255, 255]) # Obere Schwellenwerte für Blau

    # Farbgrenzen für die Erkennung des grünen Balls definieren
    #lower_green = np.array([35, 100, 100])  # Untere Grenze für grün
    #upper_green = np.array([80, 255, 255])  # Obere Grenze für grün
    lower_green = np.array([35, 100, 100])  # Untere Grenze für grün
    upper_green = np.array([80, 255, 255])  # Obere Grenze für grün


    # Farbgrenzen für die Erkennung des roten Balls definieren
    lower_red = np.array([157, 144, 49])
    upper_red = np.array([179, 255, 255])

    # gesuchte Farbe bestimmen
    if color == "blue":
        color_upper = upper_blue
        color_lower = lower_blue
    elif color == "green":
        color_upper = upper_green
        color_lower = lower_green
    else:
        color_upper = upper_red
        color_lower = lower_red

    # Maske erstellen, die nur die gewünschten farbigen Bereiche zeigt
    mask = cv2.inRange(hsv, color_lower, color_upper)        

    # Konturen finden
    if color == "red":
        _, maskRed = cv2.threshold(mask, 245, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(maskRed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bug = str(np.mean(mask))

    # Wenn Konturen gefunden werden, zeichne sie auf das Bild
    if contours:
        # Größte Kontur auswählen
        bug = "contours ja"
        largest_contour = max(contours, key=cv2.contourArea)
        # Berechne den Mittelpunkt der Kontur
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            kreis, radius = confirm_ballshape(largest_contour, cx, cy)

            if kreis:
                cv2.putText(img, "Ball entdeckt!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)  # Display the message
                cv2.circle(img, (cx, cy), int(radius), (128, 255, 255), 3)
            else:
                cv2.putText(img, "Kein Ball", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(img, "Kein Ball", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(img, "Keine Konturen gefunden", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        cx = -1
        cy = -1

    # Rückgabe der Werte
    return largest_contour, cx, cy, img, bug, mask
