import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import sys
from datetime import datetime
import pyttsx3
import google.generativeai as palm

palm.configure(api_key="AIzaSyB80qiuLLEnQuEZkgpDWjlE-dm6VqzM6IQ")

# Only load the KV file once
Builder.load_file("interface.kv")

def get_response(prompt):
    response = palm.generate_text(
        prompt=prompt)
    result = response.result
    result = result.replace("**","")
    return str(result)

def mock_interview(topic):
    return "Interviewed on "+topic

def quick_revison(topic):
    return "Revision on topic: "+topic+"\n\n"+get_response("Write about "+topic+" in 15 points for revision.")

class InterfaceLayout(BoxLayout):

    def pressed(self):
        query = self.ids.input_query.text

        doubt_solver_button_state = self.ids.doubt_solver_button.state
        mock_interview_button_state = self.ids.mock_interview_button.state
        quick_revision_button_state = self.ids.quick_revision_button.state
        if len(query)==0:
            self.ids.output_textbox.text = "Please enter query"
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
            elif mock_interview_button_state == "down":
                response = mock_interview(query)
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
                self.ids.output_textbox.text = "Choose Doubt Solver / Mock Interview / Quick Revision ?"

    def get_history(self):
        query = self.ids.input_query.text
        doubt_solver_button_state = self.ids.doubt_solver_button.state
        mock_interview_button_state = self.ids.mock_interview_button.state
        quick_revision_button_state = self.ids.quick_revision_button.state

        if doubt_solver_button_state == "down":
            with open("doubt_history.txt","r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist
        elif mock_interview_button_state == "down":
            with open("mock_history.txt", "r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist
        elif quick_revision_button_state == "down":
            with open("revision_history.txt", "r") as file:
                hist = file.read()
                self.ids.output_textbox.text = hist

    def get_cleared(self):
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

    def exit(self):
        sys.exit(0)


class MentorApp(App):
    def build(self):
        self.title = "Self-Pace Learning"
        return InterfaceLayout()



if __name__ == '__main__':
    MentorApp().run()
