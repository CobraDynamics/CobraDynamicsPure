import cv2
import gc
import detect_gesture as g
import motor_control2 as mc #########--temporär version 2 von motor_control
import detect_object as do 
import audio_ctrl as ac

    

def main():
    ac.play_file("connected/connected.mp3")
    cap = Picamera2()  # Create an instance of Picamera2
    #cap = cv2.VideoCapture(-1) # use for any camera
    ##############################
    # COLOR ###############################################################
    #========= Variablen ##################################################
    colorlist = ["blue","green","red"]
    found_counter = 0 # inkrement nach jedem erfolgreichen Fund -> bestimmt nächste Farbe
    color = colorlist[found_counter]
    gesture = 1 # Gesten 1,2,3 durchnummeriert für spätere if-Abfrage/Vergleich
    #=====


    ##############################
    initialized = False
    is_found = False
    while True:
        # Lesen Sie ein Bild oder Video von der Kamera
        ret, image = cap.read()
        image = cv2.resize(image, (640, 480)) # resize img size
        if not initialized:            
            # Überprüfen Sie, ob die Handgeste erkannt wurde
            #gesture = gesture_recog(landmarks)
            #--------- für test----
            gesture = 1
            #---------------------
            #if g.detect_hand_gesture(image):
            if gesture:
                print("Successful initialization by hand gesture!")
                initialized = True
                g.hands.close()
                del g.hands
        else:
            #image = process_image(image)
            #x, y = do.find_object(image)
            #--------------------------
            if found_counter < gesture:
                #is_found, found_counter = bg.get_ball(img, color, found_counter)  # get_ball (img, color)
                #schleife color_recog + motor_control
                _, cx, cy, image = color_recog(image, color) #1. Parameter "largest_contour" wird hier nicht benötigt
                is_found = mc.motor_control(x, y)
                if is_found == True:
                    found_counter += 1
                    is_found = False
                    
                
                print("Found-Counter: ", found_counter)
                
            elif found_counter == gesture:
                happy = happy_dance()
                print(happy)
                initialized = False # start again
                #break # statt Programm zu beenden, wieder auf Geste warten
    #---nach der Schleife -----------------------

        cv2.imshow('Kamera', image)
        #cv2.waitKey(1)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    #g.hands.close()
    cv2.destroyAllWindows()
    cap.release() 
    gc.collect() # Clean memory
    # del g.hands
    
if __name__ == "__main__":
    main()
