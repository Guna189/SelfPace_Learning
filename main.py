import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import Builder
import sys
from datetime import datetime
import google.generativeai as palm
import requests
import os


palm.configure(api_key="AIzaSyB_c4r0sHLy_MYSWI4FpA8h3Ug-T2nFX7s")
API_KEY = "AIzaSyA7Yv-Vhg-lpwmxzTchong9rZnmGw8r3EY"
CX = "3614c3861b0c648e7"


# Only load the KV file once
Builder.load_file("interface.kv")
Window.fullscreen = 'auto'


def get_response(prompt):
    response = palm.generate_text(
        prompt=prompt)
    result = response.result
    result = result.replace("**","")
    return str(result)


def get_images(query, api_key, cx, output_folder="cache", num_images=10):
    """
    Fetch images using Google Custom Search API and download them.

    Args:
        query (str): The search query.
        api_key (str): Your Google API key.
        cx (str): Your Custom Search Engine ID (cx).
        output_folder (str): Folder to save the images.
        num_images (int): Number of images to download.

    Returns:
        None
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Google Custom Search API endpoint
    api_url = "https://www.googleapis.com/customsearch/v1"

    # Set parameters for the API request
    params = {
        "q": query,
        "cx": cx,
        "searchType": "image",
        "key": api_key,
        "num": num_images
    }

    # Make the API request
    response = requests.get(api_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Download and save images
        for i, item in enumerate(data.get("items", [])):
            image_url = item.get("link")
            filename = os.path.join(output_folder, f"image_{i + 1}.jpg")

            # Download the image
            try:
                image_response = requests.get(image_url, stream=True)
                image_response.raise_for_status()

                with open(filename, 'wb') as file:
                    for chunk in image_response.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"Image {i + 1} downloaded to {filename}.")
            except Exception as e:
                print(f"Error downloading image {i + 1}: {e}")
    else:
        print(f"Failed to fetch images. Status code: {response.status_code}")

def mock_assesment(topic):
    questions = get_response("Generate 10 MCQ questions on topic "+topic+"with 4 options and list out answers in the end")
    ques = questions.split("\n")
    summary=""
    return questions

def quick_revison(topic):
    return "Revision on topic: "+topic+"\n\n"+get_response("Write about "+topic+" in 15 points for revision.")

class InterfaceLayout(BoxLayout):
    current_image_index = 0
    image_folder = "cache"
    image_files = []

    def pressed(self):
        query = self.ids.input_query.text
        self.ids.title_bar.text = query
        doubt_solver_button_state = self.ids.doubt_solver_button.state
        mock_assessment_button_state = self.ids.mock_assessment_button.state
        quick_revision_button_state = self.ids.quick_revision_button.state
        if len(query) == 0:
            self.ids.output_textbox.text = "Please, ask your doubt or provide topic for assessment/ revision."
        else:
            if doubt_solver_button_state == "down":
                response = query + "\n" + get_response(query)
                try:
                    hist = ""
                    with open("doubt_history.txt", "r") as file:
                        hist = file.read()

                    with open("doubt_history.txt", "w") as file:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        file.write("\n\n=========="+timestamp+"==========\n\n"+response + "\n"+hist+"\n\n")


                except Exception as e:
                    print(e)
                    print("Error Occured")
                    self.ids.output_textbox.text = "Error!! Please Try Again Later..."
                self.ids.output_textbox.text = response
            elif mock_assessment_button_state == "down":
                self.ids.output_textbox.text = 'Assessment on topic "' + str(self.ids.input_query.text)+'"'

                response = mock_assesment(query)
                try:
                    hist = ""
                    with open("mock_history.txt", "r") as file:
                        hist = file.read()

                    with open("mock_history.txt", "w") as file:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        file.write("\n\n=========="+timestamp+"==========\n\n"+response + "\n"+hist+"\n\n")


                except Exception as e:
                    print(e)
                    print("Error Occured")

                self.ids.output_textbox.text = response
            elif quick_revision_button_state == "down":
                response = quick_revison(query)
                try:
                    hist = ""
                    with open("revision_history.txt", "r") as file:
                        hist = file.read()

                    with open("revision_history.txt", "w") as file:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        file.write("\n\n=========="+timestamp+"==========\n\n"+response + "\n"+hist+"\n\n")


                except Exception as e:
                    print(e)
                    print("Error Occured")
                self.ids.output_textbox.text = response

            else:
                self.ids.output_textbox.text = "Choose Doubt Solver / Assessment / Quick Revision ?"

    def get_history(self):
        query = self.ids.input_query.text
        doubt_solver_button_state = self.ids.doubt_solver_button.state
        mock_assessment_button_state = self.ids.mock_assessment_button.state
        quick_revision_button_state = self.ids.quick_revision_button.state

        if doubt_solver_button_state == "down":
            with open("doubt_history.txt", "r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist
                self.ids.title_bar.text = "Doubts History"
        elif mock_assessment_button_state == "down":
            with open("mock_history.txt", "r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist
                self.ids.title_bar.text = "Performance History"
        elif quick_revision_button_state == "down":
            with open("revision_history.txt", "r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist
                self.ids.title_bar.text = "Revision History"

    def get_cleared(self):
        for i in os.listdir("cache"):
            os.remove("cache/" + i)
        self.ids.query_image.source = "wallpaper.png"
        self.ids.title_bar.text = "Self-Pace Learning Tool"
        self.ids.output_textbox.text = "Welcome to the Self-Pace Learning Tool!\n\n        Explore a world of knowledge and personalized learning experiences. Uncover the power of advanced Natural Language Processing and the seamless Python Kivy interface designed to enhance your educational journey. \n\n        Engage in a transformative learning experience that goes beyond traditional methods. Our virtual assistant is here to empower your academic endeavors, providing personalized support for your inquiries. \n\n        Discover an innovative platform that not only answers your questions but also encourages a collaborative and approachable learning environment. \n\n        Embark on enriched learning journeys as AI and education converge to redefine the landscape of your educational experience. Type your queries below and let our AI guide you toward academic success!"

    def zoom_in(self):
        scroll = self.ids.img.parent
        scroll.scroll_x = max(0, min(1, scroll.scroll_x + 0.1))
        scroll.scroll_y = max(0, min(1, scroll.scroll_y + 0.1))
        self.ids.img.width = self.parent.width * (1 / (1 - scroll.scroll_x))

    def zoom_out(self):
        scroll = self.ids.img.parent
        scroll.scroll_x = max(0, min(1, scroll.scroll_x - 0.1))
        scroll.scroll_y = max(0, min(1, scroll.scroll_y - 0.1))
        self.ids.img.width = self.parent.width * (1 / (1 - scroll.scroll_x))

    def get_current_image(self):
        if self.image_files:
            return os.path.join(self.image_folder, self.image_files[self.current_image_index])
        else:
            return ""

    def get_query_images(self):
        query = self.ids.input_query.text
        if query == "":
            self.ids.query_image.source="wallpaper.png"
            return
        get_images(query, API_KEY, CX)
        self.image_files = [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        self.image_files.sort()
        self.current_image_index = 0  # Reset current_image_index to 0
        self.ids.query_image.source = self.get_current_image()

    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.ids.query_image.source = self.get_current_image()

    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.ids.query_image.source = self.get_current_image()

    def exit(self):
        sys.exit(0)



class MentorApp(App):
    def build(self):
        self.title = "Self-Pace Learning"
        return InterfaceLayout()



if __name__ == '__main__':
    MentorApp().run()
