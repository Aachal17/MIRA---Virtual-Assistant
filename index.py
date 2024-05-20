import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import tkinter as tk
import time
import geocoder  

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Create the main application window
app = tk.Tk()
app.title("Virtual Assistant: MIRA")
app.geometry("700x700")  # Set the window size

# Create and configure styles
style = tk.ttk.Style(app)  # Using ttk.Style for themed widgets
style.configure("TButton", font=("Helvetica", 10), foreground="black", background="blue", padding=5)

# Create and pack widgets
conversation_text = tk.Text(
    app,
    font=("Helvetica", 12),
    wrap=tk.WORD,
    height=20,
    width=50
)
conversation_text.pack(pady=20)

input_entry = tk.Entry(app, font=("Helvetica", 12), width=50)
input_entry.pack(pady=10)

# Function to process user commands
def process_command():
    user_input = input_entry.get()
    update_conversation(f"You: {user_input}")
    run_mira(user_input)
    input_entry.delete(0, tk.END)

# Create a button to trigger command processing
process_button = tk.ttk.Button(app, text="Send", style="TButton", command=process_command)
process_button.pack(pady=10)

# Function to update the conversation history
def update_conversation(message):
    conversation_text.insert(tk.END, message + "\n")
    conversation_text.yview(tk.END)  # Scroll to the bottom

# Function to update the response label
def update_response_label(response):
    update_conversation(f"MIRA: {response}")

# Function to process user commands and generate responses
def run_mira(command):
    update_conversation(f"User: {command}")

    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        response = 'Current time is ' + current_time
        talk(response)
    elif 'who is' in command:
        person = command.replace('who is', '').strip()  # Remove extra spaces
        try:
            info = wikipedia.summary(person, sentences=1, auto_suggest=False)
            talk(info)
        except wikipedia.exceptions.WikipediaException as e:
            response = f"Sorry, an error occurred: {e}"
            talk(response)
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        response = 'Current date is: ' + current_date
        talk(response)
    elif 'name' in command:
        response = "My name is MIRA. I am a virtual assistant and developed by the students of Shri M. D. Shah Mahila College. Advanced Arduino code is used for voice communication. I can play any song you want, tell you the current time, current date, share information about any famous personality and tell a joke related to programming."
        talk(response)
    elif 'what can you do' in command:
        response = "I can play any song you want, tell you the current time, current date, share information about any famous personality and tell a joke related to programming."
        talk(response)
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
    elif 'my location' in command:
        # Get the user's location using the geocoder library
        location_data = get_user_location()
        response = f"Your current location is {location_data}."
        talk(response)
        # if location_data:
        #     city = location_data.get('city', 'Unknown City')
        #     state = location_data.get('state', 'Unknown State')
        #     country = location_data.get('country', 'Unknown Country')
        #     response = f"Your current location is in {city}, {state}, {country}."
        #     talk(response)
        # else:
        #     response = 'Unable to determine your location.'
        #     talk(response)
    else:
        response = 'Please say the command again.'
        talk(response)

# Function to perform text-to-speech
def talk(text):
    update_response_label(text)
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print('User Speech:', command)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the speech.")
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e}")
    return command
# Function to get the user's location using the geocoder library
def get_user_location():
    try:
        # Use the geocoder library to get the user's detailed location based on IP address
        g = geocoder.ip('me')

        # Check if the response is successful
        if g.ok:
            return g.geojson['features'][0]['properties']['address']
        else:
            return None
    except Exception as e:
        print(f"Error getting location: {e}")
        return None




def listen_and_run():
    while True:
        run_mira(take_command())
        time.sleep(1)  # Add a small delay to give the main thread some time
thread = Thread(target=listen_and_run)
thread.start()

app.mainloop()
