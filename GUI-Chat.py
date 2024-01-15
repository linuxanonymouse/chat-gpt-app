import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
import openai
import threading

openai.api_key = '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'

class Message(BoxLayout):
    def __init__(self, text='', role='user', **kwargs):
        super(Message, self).__init__(**kwargs)
        self.orientation = 'vertical'
        color = '0066CC' if role == 'user' else 'FF4500'
        label = Label(text=f"[color={color}]{role.capitalize()}:[/color] {text}", halign='left', markup=True, size_hint_y=None)
        label.bind(size=label.setter('text_size'))
        self.add_widget(label)

class ChatBox(ScrollView):
    def __init__(self, **kwargs):
        super(ChatBox, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(10, 10))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, text, role):
        message_widget = Message(text=text, role=role, size_hint_y=None)
        self.layout.add_widget(message_widget)

       
        self.layout.height = sum(child.height + 10 for child in self.layout.children)

       
        self.scroll_to(message_widget)

class GPTChatApp(App):
    def build(self):
        try:
            print("Building the app...")
            self.chat_box = ChatBox()

            self.text_input = TextInput(multiline=False, size_hint_y=None, height=40)
            send_button = Button(text="Send", on_press=self.on_button_press, size_hint_y=None, height=40)

            input_layout = BoxLayout(orientation='horizontal', spacing=10)
            input_layout.add_widget(self.text_input)
            input_layout.add_widget(send_button)

            layout = BoxLayout(orientation='vertical')
            layout.add_widget(self.chat_box)
            layout.add_widget(input_layout)

           
            with layout.canvas.before:
                Color(0, 0, 0, 1) 
                self.rect = Rectangle(size=Window.size, pos=layout.pos)

            layout.bind(size=self._update_rect, pos=self._update_rect)

            self.is_responding = False
            print("App built successfully.")
            return layout
        except Exception as e:
            print(f"An exception occurred during the app initialization: {e}")
            raise

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_button_press(self, instance):
        try:
            print("massage sended to the chat gpt...")
            if not self.is_responding:
                user_input = self.text_input.text
                user_message = f"{user_input}\n"
                self.chat_box.add_message(user_message, role='user')

                self.is_responding = True

                threading.Thread(target=self.process_response, args=(user_input,)).start()

                self.text_input.text = ""  
        except Exception as e:
            print(f"An exception occurred during button press: {e}")

    def process_response(self, user_input):
        try:
            response = self.chat_with_gpt(user_input)

            
            Clock.schedule_once(lambda dt: self.update_response(response))
            
        except Exception as e:
            print(f"An exception occurred during process_response: {e}")

    def update_response(self, response):
        try:
            ai_message = f"{response}\n"
            self.chat_box.add_message(ai_message, role='ai')

        finally:
           
            self.is_responding = False

    def chat_with_gpt(self, prompt):
        try:
            print("Chatting with GPT...")
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=100,
                temperature=0.7,
                n=1,
                stop=None,
            )
            print("Chatting with GPT successful.")
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"An exception occurred during chat_with_gpt: {e}")
            return "Error in response"

if __name__ == '__main__':
    try:
        print("Running the app...")
        GPTChatApp().run()
        print("App execution completed.")
    except KeyboardInterrupt:
        print("Quitting..... bye. {e}")
