import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.clock import Clock
from kivy.core.window import Window 
import os
import socket_client
import sys
kivy.require("1.11.1")
class connectpage(GridLayout):
    def __init__(self,**kwargs):
        super(connectpage,self).__init__(**kwargs)
        self.cols=1
        
        self.inside=GridLayout()
        self.inside.cols=2
        self.inside.row_default_height=10
        
        self.inside.add_widget(Label(text="IP:"))
        self.ip=TextInput(multiline=False)
        self.ip.bind(on_text_validation=self.On_enter)
        self.inside.add_widget(self.ip)
        
        self.inside.add_widget(Label(text="Port:"))
        self.port=TextInput(multiline=False)
        self.inside.add_widget(self.port)
        
        self.inside.add_widget(Label(text="Username:"))
        self.username=TextInput(multiline=False)
        self.inside.add_widget(self.username)
        
        self.add_widget(self.inside)
        
        self.join=Button(text="join")
        self.join.bind(on_press=self.join_button)
        self.add_widget(self.join)
    def On_enter(self,instance):
        ip=self.ip
        if "\n" in ip:
            self.next.focus=True
    def join_button(self, instance):
         port= self.port.text
         ip=self.ip.text
         username= self.username.text
         info=(f"attemting to join {ip}:{port} as {username}")
         chatapp.info_page.update_info(info)
         chatapp.screen_manager.current="Info"
         Clock.schedule_once(self.connect,1)
    def connect(self, _):
        port = int(self.port.text)
        ip= self.ip.text
        username= self.username.text
        
        if not socket_client.connect(ip,port,username,show_error):
            return
        chatapp.create_chat_page()
        chatapp.screen_manager.current="Chat"
class infopage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=1
        self.message=Label(halign="center", valign="middle", font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
    def update_info(self,message):
        self.message.text=message
    def update_text_width(self,*_):
        self.message.text_size=(self.message.width*0.9,None)
        
class ChatPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=1
        self.history=Label(height=Window.size[1]*0.9,size_hint_y=None)
        self.add_widget(self.history)
        
        self.new_message= TextInput(width=Window.size[0]*0.8,size_hint_x=None,multiline=False)
        self.send=Button(text="send")
        self.send.bind(on_press=self.send_message)
        
        bottom_line=GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        
        self.add_widget(bottom_line)
    def send_message(self, _):
        print("send a message")

class epicapp(App):
    def build(self):
        self.screen_manager=ScreenManager()
        
        self.connect_page=connectpage()
        screen=Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)
        
        self.info_page=infopage()
        screen=Screen(name="Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager
    def create_chat_page(self):
        self.chat_page=ChatPage()
        screen=Screen(name="Chat")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)
def show_error(message):
    chatapp.info_page.update_info(message)
    chatapp.screen_manager.current="Info"
    Clock.schedule_once(os.exit,5)
    
if __name__=="__main__":
    chatapp= epicapp()
    chatapp.run()