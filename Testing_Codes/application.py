import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from creator import createqr

class MyApp(App):
    def build(self):
        # Create a vertical layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a TextInput widget
        self.text_input = TextInput(hint_text="Type something here", font_size=24, size_hint=(1, 0.2))

        # Create a Button widget
        self.button = Button(text="Submit", size_hint=(1, 0.2), font_size=24)
        self.button.bind(on_press=self.on_button_press)

        # Create a Label widget to display the result
        self.result_label = Label(text="", font_size=24)

        # Add widgets to the layout
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.result_label)

        return self.layout

    def on_button_press(self, instance):

        createqr()
        
        # Get the text from the TextInput widget
        typed_text = self.text_input.text
        
        # Update the Label with the typed text
        self.result_label.text = f"You typed: {typed_text}"

# Run the app
if __name__ == '__main__':
    MyApp().run()


'''
to do:
create a streamlit to finalize a place where everything will be:
then import the code from append so that you have a tracker on what's happening
then import the qr code scanner
then merge them all together
you are done

'''