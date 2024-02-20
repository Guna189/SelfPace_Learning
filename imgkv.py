from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

Builder.load_string("""
<ZoomableImage@ScrollView>:
    do_scroll_x: True
    do_scroll_y: True
    bar_width: 20
    bar_color: 0, 0, 0, 1

<ImageViewer>:
    orientation: 'vertical'
    size_hint: (1.0, 1.0)

    ZoomableImage:
        Image:
            id: img
            source: 'hunting_image_4.jpg'
            allow_stretch: True
            size_hint: (None, None)
            size: self.parent.width, self.parent.height

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1

        Button:
            text: 'Zoom In'
            on_press: root.zoom_in()

        Button:
            text: 'Zoom Out'
            on_press: root.zoom_out()
""")

from kivy.base import runTouchApp

class ImageViewer(BoxLayout):
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

runTouchApp(ImageViewer())
