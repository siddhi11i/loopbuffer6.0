import tkinter as tk
from tkinter import messagebox
import threading
import speech_recognition as sr
from twilio.rest import Client
from geopy.geocoders import Nominatim
import geopy.exc

# Twilio credentials
TWILIO_SID = "AC65825afdb0ced54b7b95923e1239b644"
TWILIO_AUTH_TOKEN = "1bfb8ac4136fd98aa953e965b20c037f"
TWILIO_PHONE_NUMBER = "+1 715 908 9623"
EMERGENCY_CONTACT = "+919021484187"

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Function to get the current location
def get_location():
    try:
        geolocator = Nominatim(user_agent="sos_alert_app")
        location = geolocator.geocode("Pune, India")  # You can make this dynamic too
        return f"{location.address}, Latitude: {location.latitude}, Longitude: {location.longitude}"
    except Exception as e:
        return f"Location could not be determined: {e}"

# Function to send an SOS alert
def send_sos_alert():
    location = get_location()
    message_body = f"🚨 EMERGENCY ALERT! 🚨\nI need help! My location: {location}"

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_PHONE_NUMBER,
        to=EMERGENCY_CONTACT
    )
    return message.sid

# Function to listen for voice command
def listen_for_sos(status_label):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎤 Listening for 'help me'...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio).lower()
            status_label.config(text=f"🗣 You said: {text}")
            if "help me" in text:
                status_label.config(text="🚨 Distress word detected! Sending SOS...")
                sid = send_sos_alert()
                status_label.config(text=f"✅ SOS Sent! Message ID: {sid}")
                messagebox.showinfo("SOS Sent", "Emergency message sent successfully!")
            else:
                status_label.config(text="❌ 'Help me' not detected.")
        except sr.UnknownValueError:
            status_label.config(text="🤷 Could not understand the audio.")
        except sr.RequestError:
            status_label.config(text="⚠ Speech recognition service error.")

# Function to run voice recognition in a new thread (so GUI doesn't freeze)
def start_listening_thread(status_label):
    thread = threading.Thread(target=listen_for_sos, args=(status_label,))
    thread.start()

# GUI setup
def main():
    root = tk.Tk()
    root.title("SOS Voice Alert System")
    root.geometry("400x250")

    title_label = tk.Label(root, text="🔊 SOS Voice Listener", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=20)

    status_label = tk.Label(root, text="Press Start to begin", font=("Helvetica", 12))
    status_label.pack(pady=10)

    start_button = tk.Button(root, text="▶ Start Listening", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                             command=lambda: start_listening_thread(status_label))
    start_button.pack(pady=10)

    exit_button = tk.Button(root, text="❌ Exit", font=("Helvetica", 12), bg="#f44336", fg="white", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
