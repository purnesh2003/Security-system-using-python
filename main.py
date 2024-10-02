import face_recognition
import threading
import cv2
import numpy as np
import csv
from datetime import datetime
import os
import pywhatkit


import glob

folder_path = "C:/p/attendence/"

# Get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Delete each file
for file_path in csv_files:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted")
    else:
        print(f"{file_path} does not exist")



# Function to create a new CSV file with headers
def create_new_csv():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'security.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time"])
    return csv_filename

# Load and encode multiple reference images
known_face_encodings = []
known_face_names = []

# image directory
reference_dir = "C:/p/attendence/image/"

for filename in os.listdir(reference_dir):
    if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
        image_path = os.path.join(reference_dir, filename)
        reference_image = face_recognition.load_image_file(image_path)
        print(f"Loading reference image: {filename}")

        face_locations = face_recognition.face_locations(reference_image)
        if len(face_locations) == 0:
            print(f"No face detected in {filename}. Skipping this image.")
            continue

        reference_encoding = face_recognition.face_encodings(reference_image, face_locations)[0]
        known_face_encodings.append(reference_encoding)
        known_face_names.append(os.path.splitext(filename)[0])  # Use filename (without extension) as the person's name

print(f"Loaded {len(known_face_names)} reference images")


# Create a new CSV file for this run
csv_filename = create_new_csv()
attendance_marked = set()  # To keep track of marked attendances

recognition_history = {name: 0 for name in known_face_names}
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
current_time = now.strftime("%H:%M:%S")

# MY FACE RECO FUNC
def my_func():
    global stop_flag
    stop_flag = False
    video_capture = cv2.VideoCapture(0)

    count = 0
    while not stop_flag:
        ret, frame = video_capture.read()
        count +=1
        if not ret:
            print("Failed to capture frame")
            break

    # Resize frame for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        print(f"Faces detected in frame: {len(face_locations)}")

        recognized_names = []  # To keep track of names recognized in this frame

        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
            # Increase tolerance for more lenient matching
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    recognized_names.append(name)
                    recognition_history[name] += 1
                    print(f"Recognized: {name}")
                
                # Check attendance for the recognized person
                    if recognition_history[name] >= 3:
                        if name not in attendance_marked:
                            print(f"Marking attendance for {name}")
                        
                       
                        
                        # Write to CSV file
                            with open(csv_filename, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([name, current_date, current_time])
                        
                            attendance_marked.add(name)
                            print(f"Attendance marked for {name} at {current_time}")
                else:
                    with open(csv_filename, mode='a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["unknown", current_date, current_time])
            
            

    # Reset recognition history for names not detected in this frame
        for name in known_face_names:
            if name not in recognized_names:
                recognition_history[name] = 0

    # Display the resulting frame
        for (top, right, bottom, left) in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

        # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow("Attendance System", frame)

    # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


timer = threading.Timer(0, my_func)
timer.start()

# Stop the function after 5 seconds
timer.join(10)
stop_flag = True


current_hour = now.hour
current_minute = now.minute + 1

with open(csv_filename, mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        condition,x,y=row
       
        if len(condition)!=0:
            
             
            print(condition)
            break
        break
        


# Extract hour and minute as integers
if condition == "unknown":
    reader ="Unknown person detected "

    print(current_hour)
    print(current_minute)
    pywhatkit.sendwhatmsg('+919019864152',reader,current_hour,current_minute)
    # After main execution of file2.py completes, launch file1.py
else:
    print("no unknown person detected")
