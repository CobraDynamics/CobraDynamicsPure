import numpy as np
# Berechne die Abstände der Punkte zur Mitte
def confirm_ballshape(largest_contour, cx, cy):
    distances = []
    kreis = False
    radius = 0
    for point in largest_contour:
        distance = np.sqrt((point[0][0] - cx) ** 2 + (point[0][1] - cy) ** 2)
        distances.append(distance)
        if distance > radius:
            radius = distance
    # Berechne die Standardabweichung der Abstände
    std_dev = np.std(distances)
    # Überprüfe, ob die Standardabweichung klein ist
    if std_dev < 5:
        kreis = True                
        #cv2.putText(img, "Ball entdeckt!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
        #1, (0, 255, 0), 2, cv2.LINE_AA)  # Display the message

    else:
        kreis = False
    #cv2.circle(img, (int(cX), int(cY)), int(radius), (128, 255, 255), 5)
    
    return kreis, radius
