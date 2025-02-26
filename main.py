import cv2
import tkinter as tk
from tkinter import messagebox


# Load the video file
video_path = "DoraEdit.mp4"  # Change this to your video file path
cap = cv2.VideoCapture(video_path)
pause_timer = [2,5,7]
last_pause_time = -1
# Check if the video file opened successfully
# Function to show the dialog box
# Function to show the multiple-choice question

# Function to check if current time matches any pause time
def if_pause_timer(current_time):
    return current_time in pause_timer  # Check directly in list
def show_question():
    def on_option_selected(option):
        print(f"User selected: {option}")
        messagebox.showinfo("Answer", f"You selected: {option}")
        root.destroy()  # Close the dialog after selection

    root = tk.Tk()
    root.title("Question")
    root.geometry("300x200")

    # Question label
    question_label = tk.Label(root, text="What should Dora go first?",
                              font=("Arial", 12))
    question_label.pack(pady=10)

    # Buttons for choices
    options = ["Jump for Bridge", "Squat for school", "Raise Hand for surprise hill"]
    for option in options:
        btn = tk.Button(root, text=option, font=("Arial", 10),width=30,bg="lightblue")
                        #command=lambda opt=option: on_option_selected(opt))
        btn.pack(pady=5)

    root.mainloop()
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()  # Read a frame
    if not ret:
        break  # Stop if video ends

    # Get current time in milliseconds and convert to seconds
    current_time = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # Convert ms to sec

    # Display the elapsed time on the video frame
    text = f"Time: {current_time} sec"
    cv2.putText(frame, text, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Pause exactly at those times
    if if_pause_timer(current_time) and last_pause_time!=current_time:
        show_question()  # Show the question dialog
        last_pause_time = current_time
        current_time = current_time+1
    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Exergame Video", frame)  # Display the frame

    # Press 'q' to exit the video early
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
