"""
    Cobra Dynamics / Oct 2024
    
    Linda Hahn-Tukker (https://github.com/lihatu)
    Martin Schottler (https://github.com/mbient)
    Jan Hildebrandt (https://github.com/abracodedabra)

    This Programm is the Main-Function for the RaspRover Control, based on a Raspberry Pi 4B
"""

import cv2
import gc # garbage collector
import gesture_recognition as gr #detect_gesture
import motor_control2 as mc #########--temporär version 2 von motor_control
import clr_recog as cr #detect_object
from picamera2 import Picamera2  # Library for accessing Raspberry Pi Camera
from flask import Flask, Response # Library für Videostreaming über Websever
import mediapipe as mp

# Flask-Anwendung erstellen
app = Flask(__name__)    

def main():     
    # Initalisierung von MediaPipe für die Handerkennung und die Zeichenwerkzeuge
    mpDraw = mp.solutions.drawing_utils
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    
    cap = Picamera2()  # Create an instance of Picamera2    
    cap.configure(cap.create_video_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))  # Configure camera parameters
    cap.start()  # Start the camera
    #cap = cv2.VideoCapture(-1) # use for any camera
    
    
    ##############################
    # COLOR ###############################################################
    #========= Variablen ##################################################
    colorlist = ["blue","green","red"]
    found_counter = 0 # inkrement nach jedem erfolgreichen Fund -> bestimmt nächste Farbe
    color = colorlist[found_counter]
    # gesture = 1 # Ist nur zum grundlegenden Test ohne gesture_recognition()
    #=====


    ##############################
    is_gesture_initialized = False
    is_found = False

    while True:
        # Lesen Sie ein Bild oder Video von der Kamera
        

        #ret, image = cap.read()
        
        image = cap.capture_array("main") # Capture a frame from the camera
        # image = cv2.resize(image, (640, 480)) # resize img size / wird eigentlich oben in cap.configure schon festgelegt
        if not is_gesture_initialized:            
            frame_flipped = cv2.flip(image, 1)
            img_rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
            frame_flipped_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            # Erkennung der Hand und Landmarks
            results = hands.process(img_rgb)

            # Wenn Handlandmarks erkannt wurden
            if results.multi_hand_landmarks:

                for handLms in results.multi_hand_landmarks:
                    # Zeichne Handlandmarks und Verbindungen auf das BGR-Frame
                    mpDraw.draw_landmarks(frame_flipped_bgr, handLms, mpHands.HAND_CONNECTIONS)
                    # Führe die Gestenerkennung durch und schreibe das Ergebnis auf das Frame
                    gesture = gr.gesture_trigger(handLms.landmark, mpHands)

                    if gesture:
                        cv2.putText(frame_flipped_bgr, str(gesture), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.75, (0, 255, 0), 2, cv2.LINE_AA)
                        print("Successful initialization by hand gesture: ", str(gesture))
                        is_gesture_initialized = True
                        #gr.hands.close() # kein Attribut hands
                        #del gr.hands     # "
                        gr.gesture = None
                        
        else:
            #image = process_image(image)
            #x, y = do.find_object(image)
            #--------------------------
            if found_counter < gesture:
                #is_found, found_counter = bg.get_ball(img, color, found_counter)  # get_ball (img, color)
                #schleife color_recog + motor_control
                _, cx, cy, image, käfer = cr.color_recog(image, color) #1. Parameter "largest_contour" wird hier nicht benötigt
                print("Käfer: ", käfer)
                
                is_found = mc.motor_control(cx, cy)
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

        # Kodierung des Frames im JPEG-Format für MJPEG-Streaming
        ret, buffer = cv2.imencode('.jpg', frame_flipped_bgr)
        frame = buffer.tobytes()
        
        # Erzeuge einen HTTP-Response mit dem Frame-Datenstrom im MJPEG-Format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
        #cv2.imshow('Kamera', image)
        #cv2.waitKey(1)
        #if cv2.waitKey(5) & 0xFF == 27:
         #   break

    #gr.hands.close()
    cv2.destroyAllWindows()
    cap.release() 
    gc.collect() # Clean memory
    # del gr.hands

@app.route('/video_feed')
def video_feed():
    # Route für den Videostream
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Startseite mit eingebettetem Video und JavaScript für den Vollbildmodus
    return '''
    <html>
        <head>
            <title>RaspRover-VideoStream</title>
            <style>
                /* Stil für zentriertes und angepasstes Video */
                body, html { height: 100%; margin: 0; display: flex; justify-content: center; align-items: center; background-color: #333; }
                #videoContainer { max-width: 100%; max-height: 100%; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1 style="color: white;">Cobra Dynamics Videostream (zum Vergrößern klicken)</h1>
            <img src="/video_feed" id="videoContainer" onclick="toggleFullScreen()" width="640" height="480">
            
            <script>
                // Funktion für den Vollbildmodus
                function toggleFullScreen() {
                    var videoElement = document.getElementById("videoContainer");
                    if (!document.fullscreenElement) {
                        if (videoElement.requestFullscreen) {
                            videoElement.requestFullscreen();
                        } else if (videoElement.mozRequestFullScreen) { /* Firefox */
                            videoElement.mozRequestFullScreen();
                        } else if (videoElement.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                            videoElement.webkitRequestFullscreen();
                        } else if (videoElement.msRequestFullscreen) { /* IE/Edge */
                            videoElement.msRequestFullscreen();
                        }
                    } else {
                        if (document.exitFullscreen) {
                            document.exitFullscreen();
                        }
                    }
                }
            </script>
        </body>
    </html>
    '''

if __name__ == "__main__":
    main()
    app.run(host='0.0.0.0', port=8000)