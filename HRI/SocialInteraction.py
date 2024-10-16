import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI as api
from spherov2.types import Color
from spherov2 import sphero_edu as se
from spherov2.toy.bolt import BOLT 
from playsound import playsound

bolt = scanner.find_toy() ##Change this to the name of my robot for use in class
with api(bolt) as droid:
    # droid.set_back_led(255)
    # Define a color for the matrix (white)
    yellow = Color(255, 255, 0)  # Yellow for the face
    black = Color(0, 0, 0)        # Black for the background

    # Define a smiley face in an 8x8 matrix
    smiley_face = [
        [0, 0, 1, 0, 0, 1, 0, 0],  # Row 0
        [0, 0, 1, 0, 0, 1, 0, 0],  # Row 1
        [0, 0, 0, 0, 0, 0, 0, 0],  # Row 2
        [1, 0, 0, 0, 0, 0, 0, 1],  # Row 3
        [0, 1, 0, 0, 0, 0, 1, 0],  # Row 4
        [0, 0, 1, 0, 0, 1, 0, 0],  # Row 5 (smiling mouth)
        [0, 0, 0, 1, 1, 0, 0, 0],  # Row 6
        [0, 0, 0, 0, 0, 0, 0, 0],  # Row 7 (blank)
        ]
    
    frowny_face = [
    [0, 0, 1, 0, 0, 1, 0, 0],  # Row 0 (eyes)
    [0, 0, 1, 0, 0, 1, 0, 0],  # Row 1 (eyes)
    [0, 0, 0, 0, 0, 0, 0, 0],  # Row 2 (blank)
    [0, 0, 0, 1, 1, 0, 0, 0],  # Row 3 (top of frown)
    [0, 0, 1, 0, 0, 1, 0, 0],  # Row 4 (base of frown)
    [0, 1, 0, 0, 0, 0, 1, 0],  # Row 5 (frown curve)
    [1, 0, 0, 0, 0, 0, 0, 1],  # Row 6 (frown curve)
    [0, 0, 0, 0, 0, 0, 0, 0],  # Row 7 (blank)
]

    # Function to set the smiley face on the matrix
    def display_smiley_face(bolt, face):
        for y in range(8):
            for x in range(8):
                color = yellow if face[y][x] == 1 else black
                droid.set_matrix_pixel(x, y, color)  # Set the pixel

    # Display the smiley face on the matrix
    try:
        display_smiley_face(bolt, frowny_face)
        print("Smiley face displayed successfully.")
    except Exception as e:
        print(f"Failed to display smiley face: {e}")

    def on_collision(api):
        api.stop_roll()  # Stop the Sphero's movement
        api.set_main_led(Color(255, 0, 0))  # Change LED color to red
        print('Collision detected!')  # Print message to console

        # Optional: Change the LED color back after a brief moment
        time.sleep(0.5)
        api.set_main_led(Color(255, 255, 255))  # Reset LED to white

# Register the collision event
    api.register_event(se.EventType.on_collision, on_collision)

    # Initial setup
    api.set_main_led(Color(255, 255, 255))  # Set main LED to white
    api.set_speed(100)  # Set initial speed

    # Main loop to keep the program running
    try:
        while True:
            time.sleep(0.1)  # Small delay to prevent busy waiting
    except KeyboardInterrupt:
        print("Program terminated.")

