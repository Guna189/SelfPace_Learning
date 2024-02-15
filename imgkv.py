from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

class ImageChatbotApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical')

        # Image display widget
        self.image_widget = Image(source='', size_hint=(1, 0.8))
        layout.add_widget(self.image_widget)

        # Button to change the displayed image
        button = Button(text='Show Next Image', size_hint=(1, 0.2))
        button.bind(on_press=self.show_next_image)
        layout.add_widget(button)

        return layout

    def show_next_image(self, instance):
        # Change the image source here (replace this logic with your chatbot's image selection logic)
        next_image_path = self.get_next_image_path()

        # Update the image source in the Image widget
        self.image_widget.source = next_image_path

    def get_next_image_path(self):
        # Replace this logic with your chatbot's image selection logic
        # For demonstration purposes, it rotates through three sample images
        image_paths = ["hunting_image_2.jpg", "hunting_image_3.jpg", "hunting_image_4.jpg"]

        # Get the next image path in the sequence
        current_index = image_paths.index(self.image_widget.source) if self.image_widget.source in image_paths else 0
        next_index = (current_index + 1) % len(image_paths)

        return image_paths[next_index]

if __name__ == '__main__':
    ImageChatbotApp().run()
