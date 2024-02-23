import pyttsx

def generate_speech(text):
    engine = pyttsx.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text_to_speak = input("Enter the text you want to convert to speech: ")
    generate_speech(text_to_speak)
