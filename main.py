import kivy
from kivy.uix.button import Button
kivy.require('2.2.1')
import pyttsx3
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivymd.uix.button import MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import TwoLineListItem
import requests

# loading screen
class IconListItem(TwoLineListItem):
    icon = StringProperty()


class WinVid(Screen):
    def __init__(self, **kwa):
        super(WinVid, self).__init__(**kwa)

        # Background gradient
        bgimg = MDBoxLayout(size_hint=(1, 1))
        bgimg.add_widget(Image(source='data/background.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1)))

        # Loading screen video
        box = MDBoxLayout(size_hint=(1, 0.7), pos_hint={'y': 0.13})
        vid = Video(source="data/vid.mp4", size_hint=(1, 1))
        vid.bind(eos=self.done)
        vid.state = 'play'
        box.add_widget(vid)

        # Adding all the widgets
        self.add_widget(bgimg)
        self.add_widget(box)

    # system for the app to know when the loading video has completed
    def done(self, dt, instance):
        self.manager.current = "homeScreen"

# first screen of the app
class HomeScreen(Screen):
    def __init__(self, **kwa):
        super().__init__(**kwa)

        # Background gradient
        bgbox = MDBoxLayout(size_hint=(1, 1))
        bgbox.add_widget(Image(source='data/background.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1)))
        self.add_widget(bgbox)

        # Page title
        topic = MDLabel(text="Personal Information", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        topic_info = MDLabel(text="Please input the following information. This will be used to generate your report", font_style="H6", pos_hint={'x': 0.06, 'y': 0.37})

        # Name input
        name_prompt = MDLabel(text="Name:", pos_hint={'x': 0.1, 'y': 0.3}, _text_color_str="white")
        self.name_input = TextInput(size_hint=(0.3, 0.05), pos_hint={'x': 0.1, 'y': 0.73}, multiline=False)

        # Age input
        age_prompt = MDLabel(text="Age:", pos_hint={'x': 0.1, 'y': 0.2})
        self.age_input = TextInput(size_hint=(0.3, 0.05), pos_hint={'x': 0.1, 'y': 0.63}, multiline=False)

        # Gender input
        gender_prompt = MDLabel(text="Gender:", pos_hint={'x': 0.1, 'y': 0.1})
        self.gender_input = TextInput(size_hint=(0.3, 0.05), pos_hint={'x': 0.1, 'y': 0.53}, multiline=False)

        # Blood type input
        blood_prompt = MDLabel(text="Blood Type:", pos_hint={'x': 0.1, 'y': 0})
        self.blood_input = TextInput(size_hint=(0.3, 0.05), pos_hint={'x': 0.1, 'y': 0.43}, multiline=False)

        # Address input line 1
        addr_prompt_l1 = MDLabel(text="Address Line 1:", pos_hint={'x': 0.1, 'y': -0.1})
        addr_l1_input = TextInput(size_hint=(0.85, 0.05), pos_hint={'x': 0.1, 'y': 0.33}, multiline=False)

        # Address input line 2
        addr_prompt_l2 = MDLabel(text="Address Line 2:", pos_hint={'x': 0.1, 'y': -0.2})
        addr_l2_input = TextInput(size_hint=(0.85, 0.05), pos_hint={'x': 0.1, 'y': 0.23}, multiline=False)

        # Submit button to submit all the information entered
        submitbtn = MDRaisedButton(text="Submit", on_release=self.submit, pos_hint={'x': 0.86, 'y': 0.06}, size_hint=(0.1, 0.1))

        # Adding all input widgets
        self.add_widget(topic)
        self.add_widget(topic_info)
        self.add_widget(name_prompt)
        self.add_widget(self.name_input)
        self.add_widget(self.age_input)
        self.add_widget(age_prompt)
        self.add_widget(blood_prompt)
        self.add_widget(self.blood_input)
        self.add_widget(addr_prompt_l1)
        self.add_widget(addr_l1_input)
        self.add_widget(addr_prompt_l2)
        self.add_widget(addr_l2_input)
        self.add_widget(gender_prompt)
        self.add_widget(self.gender_input)

        self.add_widget(submitbtn)

        # Name related Stuff
        self.name_input_text = ""

        self.display_name_label = MDLabel(halign="center", pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.add_widget(self.display_name_label)

        # Age Related Stuff
        self.entered_age = ""

        self.display_age_label = MDLabel(halign="center", pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.add_widget(self.display_age_label)

        #Gender Related Stuff
        self.entered_gender = ""

        self.display_gender_label = MDLabel(halign="center", pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.add_widget(self.display_gender_label)

        # Updating the text on input
        def on_text(instance, value):
            print('The widget', instance, 'have:', value)

        self.name_input.bind(text=on_text)
        self.age_input.bind(text=on_text) 
        self.gender_input.bind(text=on_text)
        self.blood_input.bind(text=on_text)
        addr_l1_input.bind(text=on_text)
        addr_l2_input.bind(text=on_text)

    # submit button function
    def submit(self, instance):
        self.name_input_text = self.name_input.text
        self.age_input_text = self.age_input.text  # Updated to store the entered age
        self.gender_input_text = self.gender_input.text
        talk_bot_screen = self.manager.get_screen('talkbot')
        self.display_name_label.text = f"[size=50]Hello, {self.name_input_text}![/size]"
        self.display_age_label.text = f"[size=24]Age: {self.entered_age}[/size]"  # Update the displayed age
        self.display_gender_label = f"[size=24]Age: {self.entered_gender}[/size]"
        self.manager.current = "talkbot"

# 2nd screen
class TalkBot(Screen):
    def __init__(self, **kwa):
        super(TalkBot, self).__init__(**kwa)
        # Background Video
        video = Video(source='data/speechvid.mp4', state='play', options={'eos': 'loop'}, allow_stretch=True, keep_ratio=False, size_hint_y=1, volume=0)  # Set the size according to your needs
        video.bind(eos=self.on_eos)
        self.add_widget(video)
        Clock.schedule_once(self.init)

    def init(self, instance):
        # Get the entered name from the homeScreen
        hs = self.manager.get_screen('homeScreen')
        entered_name = hs.name_input.text  # Access the TextInput widget and get its text
        entered_age = hs.age_input.text
        entered_gender = hs.gender_input.text

        hs = self.manager.get_screen('homeScreen')  # need to reference here but the error
        nam = hs.name_input.text

        # Buttons
        checkstat = MDRaisedButton(md_bg_color=(1, 1, 1, 1), text_color=(0, 0, 0, 1), text="Check Your Stats",
                                   pos_hint={'x': 0.35, 'y': 0.02}, on_release=self.change)
        self.add_widget(checkstat)

        talktoai = MDRaisedButton(text="Talk To AI", text_color=(0, 0, 0, 1), md_bg_color=(1, 1, 1, 1),
                                   pos_hint={'x': 0.55, 'y': 0.02}, on_release=self.changeai)
        self.add_widget(talktoai)

        # Display entered name as a label
        self.display_name_label = MDLabel(text=f"[size=50]Hello, {entered_name}![/size]", bold=True, halign="left",
                                          pos_hint={'center_x': 0.55, 'center_y': 0.7}, markup=True)
        self.add_widget(self.display_name_label)

        # Display entered age as a label
        self.display_age_label = MDLabel(text=f"[size=6][b]Age:[/b] {entered_age}[/size]", halign="left",
                                         pos_hint={'center_x': 0.55, 'center_y': 0.64}, markup=True)
        self.add_widget(self.display_age_label)

        # Display entered gender as a Label
        self.display_gender_label = MDLabel(text=f"[size=6][b]Gender:[/b] {entered_gender}[/size]", halign="left",
                                         pos_hint={'center_x': 0.65, 'center_y': 0.64}, markup=True)
        self.add_widget(self.display_gender_label)

        # Display motivational quote
        quote = self.get_motivational_quote()
        quote_label = MDLabel(
            text=quote,
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            theme_text_color="Primary",
            font_size="18sp",
            bold=True,  # Adjust the font size as needed
            markup=True  # Allows you to use markup text
        )
        self.add_widget(quote_label)

    def get_motivational_quote(self):
        try:
            response = requests.get("https://zenquotes.io/api/random")
            quote = response.json()[0]['q']  # Extracting the quote text
            return quote
        except Exception as e:
            print(f"Error fetching motivational quote: {e}")
            return "Stay motivated!"

    def on_enter(self, *args):
        # Get the entered name from the homeScreen
        hs = self.manager.get_screen('homeScreen')
        entered_name = hs.name_input.text
        print(f"Entered Name: {entered_name}")
        self.display_name_label.text = f"[size=50]Hello,{entered_name}![/size]"

        # Age part
        entered_age = hs.age_input.text
        self.display_age_label.text = f"[size=24][b]Age:[/b] {entered_age}[/size]"

        # Gender part
        entered_gender = hs.gender_input.text
        self.display_gender_label.text = f"[size=24], [b]Gender:[/b] {entered_gender}[/size]"

    def change(self, instance):
        self.scren3_screen = self.manager.get_screen('scren3')
        self.manager.current = "scren3"

    def changeai(self, instance):
        self.talkai_screen = self.manager.get_screen('decide')
        self.manager.current = "decide"

    def on_eos(self, instance):
        # Handle end of video playback (if needed)
        pass

# stats screen
class Scren3(Screen):
    def __init__(self, **kwa):
        super(Scren3, self).__init__(**kwa)

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)

        # label for displaying stats report text
        infolabel = MDLabel(text="Here is your real-time Health Report:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(infolabel)

        back_button2 = MDRaisedButton(text="Back", text_color=(0, 0, 0, 1), md_bg_color=(1, 1, 1, 1),
                                      pos_hint={'x': 0.1, 'y': 0.9}, on_release=self.back2)
        self.add_widget(back_button2)

    def back2(self, instance):
        if self.manager.get_screen('talkbot'):
            self.manager.current = 'talkbot'

    
class Decide(Screen):
    def __init__(self, **kwa):
        super(Decide, self).__init__(**kwa)

        bg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint_y=1)
        self.add_widget(bg)

        scrinfo = MDLabel(text="Take a test by answering this question or ask questions to BlissBuddy!", font_style="H4", pos_hint={'x': 0.03, 'y': 0.4}, bold=True, underline=True)
        self.add_widget(scrinfo)

        ques = MDLabel(text="Q: How do you feel about your Life?", font_style="H6", pos_hint={'x':0.06, 'y':0.25})
        self.add_widget(ques)

        self.ans = TextInput(pos_hint={'x':0.09,'y':0.53}, size_hint={0.85,0.2})
        self.add_widget(self.ans)

        def on_text(instance, value):
            print('The widget', instance, 'have:', value)
        self.ans.bind(text=on_text)

        subtn = MDRaisedButton(text="Submit Answer", pos_hint={'x':0.78,'y':0.47}, on_release=self.submit)
        self.add_widget(subtn)

        self.box = MDBoxLayout()
        self.add_widget(self.box)

    def dumb(self):
        dumb = MDLabel(text="BlissBuddy: Sorry, I couldn't quite get that. Could you please elaborate further?", font_style="H6", pos_hint = {'x':0.5, 'y':-0.1})
        self.box.add_widget(dumb)
        engine = pyttsx3.init()
        engine.say("Sorry, I couldn't quite get that. Could you please elaborate further?")
        engine.runAndWait()

    def chtoai(self):
        self.manager.current = "talkai"
    def chtoham(self):
        self.manager.current = "ham1"
    def submit(self, instance):
            ans_text = self.ans.text
            words=["stressed", "tired", "stress", "anxious", "anxiety",
                "exhausted",
                "nervous",
                "on the rack",
                "stressed-out",
                "annoyed",
                "upset",
                "shell-shocked",
                "angry",
                "irritated",
                "troubled",
                "unnerved",
                "aggravated",
                "disturbed",
                "agitated",
                "perturbed",
                "exasperated",
                "knackered",
                "burnt-out",
                "unstrung",
                "tense",
                "unmanned",
                "undone",
                "uneasy",
                "burned-out",
                "worn-out",
                "edgy",
                "worried",
                "feared",
                "fretted",
                'sweated',
                'troubled',
                'bothered',
                'fussed',
                'stewed',
                'sweat',
                "sweated blood",
                'cared a hang',
                'gave a hang',
                'sweat blood',
                'agonized',
                'longed',
                'yearned',
                'despaired',
                'pined',
                'chafed'
                ]
            sad_words=[
                'melancholy',
                'depression',
                'depressed',
                'sorrow',
                'sorrowfulness',
                'grief',
                'mournfulness',
                'anguish',
                'gloom',
                'unhappiness',
                'misery',
                'dejection',
                'despair',
                'oppression',
                'agony',
                'blues',
                'desperation',
                'heartsickness',
                'gloominess',
                'mourning',
                'joylessness',
                'pain',
                'glumness',
                'dreariness',
                'dumps',
                'forlornness',
                'despondence',
                'despondency',
                'boredom',
                'distress',
                'regret',
                'desolation',
                'miserableness',
                'blue devils',
                'mopes',
                'downheartedness',
                'despond',
                'doldrums',
                'melancholia',
                'disconsolateness',
                'self-pity',
                'somberness',
                'dispiritedness',
                'discouragement',
                'dolefulness',
                'hopelessness',
                'woe',
                'wretchedness',
                'dolor',
                'disheartenment',
                'ennui',
                'moodiness',
                'moroseness',
                'tedium',
                'morbidness',
                'woefulness',
                'drear',
                'self-despair',
                'dismalness',
                'rue',
                'morosity',
                'avadhoot',
                'gay'
            ]
            if any(word in ans_text for word in words):
                self.chtoham()
            elif any(sad_word in ans_text for sad_word in sad_words):
                self.chtoai()
            else:
                self.dumb()

            

        


# AI Screen
class TalkAI(Screen):
    def __init__(self, **kwa):
        super(TalkAI, self).__init__(**kwa)
        self.scorefix = False
        self.First_Time = True
        self.aiscore1 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="1) How often do you feel like to cry?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Never',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="2) Do you experience Apathy?", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'Never',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="3) Has your behaviour changed any\n much lately?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'Yes',
                "on_release": self.yes1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'No',
                "on_release": self.no1,
                "viewclass": "IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="4) Do you feel any guilty without any\n specific reason?", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'Yes',
                "on_release": self.yes2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'No',
                "on_release": self.no2,
                "viewclass": "IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=3,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="5) Are these feelings too intense or\n still manageable?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'Mostly Manageable',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes Manageable',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Not Manageable',
                "on_release": self.always5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            position="bottom",
            width_mult=4,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.47, 'y': 0.225}, size_hint=(0.22, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release = self.nxt)
        self.add_widget(nxtbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def yes1(self):
        self.menu3.dismiss()
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.yep1 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.yep1)
        self.add_widget(box)
        self.score3 = 1

    def no1(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope1)
        self.add_widget(box)
        self.score3 = 0

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def yes2(self):
        self.menu4.dismiss()
        if hasattr(self, 'nope2'):
            self.remove_widget(self.nope2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.yep2 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.yep2)
        self.add_widget(box)
        self.score4 = 1

    def no2(self):
        self.menu4.dismiss()
        if hasattr(self, 'yep2'):
            self.remove_widget(self.yep2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope2 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope2)
        self.add_widget(box)
        self.score4 = 0

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.47, 'y': 0.225}, size_hint=(0.22, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='Mostly Manageable', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.47, 'y': 0.225}, size_hint=(0.22, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Sometimes Manageable', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def always5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.47, 'y': 0.225}, size_hint=(0.22, 0.05), md_bg_color="#FFFFFF")
        self.alw5 = MDLabel(text='Not Manageable', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw5)
        self.add_widget(box)
        self.score5 = 2

    def nxt(self, instance):
        self.manager.current = "talkai2"
        self.aiscore1 = self.aiscore1 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        self.scorefix = True	
        print(self.aiscore1)
		    
    def on_enter(self):
        if self.First_Time:
            engine = pyttsx3.init()
            engine.say("Looks like you may have a case of depression! Please answer these questions so that I can determine your severity.")
            engine.runAndWait()
            self.First_Time = False
        if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0


class TalkAIPg2(Screen):
    def __init__(self, **kwa):
        super(TalkAIPg2, self).__init__(**kwa)
        self.scorefix = False
        self.aiscore2 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="6) Do you believe that you live an\n achievable life?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Yes',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Maybe',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'No',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="7) Do you find yourself being any\n disturbed or feeling restless in the\n middle of the night?", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'No',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Yes',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="8) Are you having any Suicidal\n Thoughts lately?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'No',
                "on_release": self.no1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Yes',
                "on_release": self.yes1,
                "viewclass": "IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="9) How often do you experience\n insomnia?", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'Sometimes',
                "on_release": self.sometimes4,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Often',
                "on_release": self.often4,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Always',
                "on_release": self.always4,
                "viewclass": "IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=4,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="10) Do you wake up a little too early\n in the morning and can't sleep again?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'No',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Yes',
                "on_release": self.always5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            width_mult=3,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release = self.nxt)
        self.add_widget(nxtbtn)
        
        prevbtn = MDRaisedButton(text="<- Prev", pos_hint={'x':0,'y':0.03}, size_hint = (0.1, 0.08), on_release = self.prev)
        self.add_widget(prevbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Maybe', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def yes1(self):
        self.menu3.dismiss()
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.yep1 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.yep1)
        self.add_widget(box)
        self.score3 = 1

    def no1(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope1)
        self.add_widget(box)
        self.score3 = 0

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def sometimes4(self):
        self.menu4.dismiss()
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev4 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev4)
        self.add_widget(box)
        self.score4 = 0

    def often4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som4 = MDLabel(text='Often', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som4)
        self.add_widget(box)
        self.score4 = 1

    def always4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw4 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw4)
        self.add_widget(box)
        self.score4 = 2

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def always5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw5 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw5)
        self.add_widget(box)
        self.score5 = 2

    def nxt(self, instance):
        self.manager.current = "talkai3"
        self.aiscore2 = self.aiscore2 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.aiscore2)
        self.scorefix = True
        
    def on_enter(self):
    	if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0
    
    def prev(self, instance):
        self.manager.current="talkai"
    	


class TalkAIPg3(Screen):
    def __init__(self, **kwa):
        super(TalkAIPg3, self).__init__(**kwa)
        self.scorefix = False
        self.aiscore3 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="11) Do you Like working in your\n current workplace?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Yes',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'No',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="12) Will you consider yourself Social?", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'Yes',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'No',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="13) Do you still practice hobbies\n during your leisure?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'Yes',
                "on_release": self.yes1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.no1,
                "viewclass": "IconListItem"
            },
            {
                "text" : 'No',
                "on_release": self.no3,
                "viewclass": "IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="14) How will you rate your working\n productivity?", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'Good',
                "on_release": self.sometimes4,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Average',
                "on_release": self.often4,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Bad',
                "on_release": self.always4,
                "viewclass": "IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=4,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="15) How would you rate your speaking\n skills?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'Good',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Average',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Bad',
                "on_release": self.always5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            width_mult=3,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08),on_release=self.nxt)
        self.add_widget(nxtbtn)
        
        prevbtn = MDRaisedButton(text="<- Prev", pos_hint={'x':0, 'y':0.03}, size_hint = (0.1,0.08), on_release = self.prev)
        self.add_widget(prevbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def yes1(self):
        self.menu3.dismiss()
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        if hasattr(self, 'nope3'):
            self.remove_widget(self.nope3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.yep1 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.yep1)
        self.add_widget(box)
        self.score3 = 0

    def no1(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        if hasattr(self, 'nope3'):
            self.remove_widget(self.nope3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope1)
        self.add_widget(box)
        self.score3 = 1
    def no3(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope3 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope3)
        self.add_widget(box)
        self.score3 = 2
        

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def sometimes4(self):
        self.menu4.dismiss()
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev4 = MDLabel(text='Good', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev4)
        self.add_widget(box)
        self.score4 = 0

    def often4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som4 = MDLabel(text='Average', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som4)
        self.add_widget(box)
        self.score4 = 1

    def always4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw4 = MDLabel(text='Bad', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw4)
        self.add_widget(box)
        self.score4 = 2

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='Good', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Average', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def always5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw5 = MDLabel(text='Bad', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw5)
        self.add_widget(box)
        self.score5 = 2

    def nxt(self,instance):
        self.manager.current = "talkai4"
        self.aiscore3 = self.aiscore3 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.aiscore3)
        self.scorefix = True
        
    def on_enter(self):
    	if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0
    
    def prev(self,instance):
        self.manager.current="talkai2"


class TalkAiPg4(Screen):
    def __init__(self, **kwa):
        super(TalkAiPg4, self).__init__(**kwa)
        self.scorefix = False
        self.aiscore4 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="16) Do you feel agitated easily?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'No',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Mild',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Severe',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #2ND QUESTION
        q2 = MDLabel(text="17) Do you feel that you understand\nslower than an average person?", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'No',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Partial or Doubtful Loss',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Loss of Insight',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=5,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.07), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="18) Do you keep thinking about small\n imperfections in any general ", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'No',
                "on_release": self.yes1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.no1,
                "viewclass": "IconListItem"
            },
            {
                "text" : 'Always',
                "on_release": self.no3,
                "viewclass": "IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="19) Is it hard for you to start on new\n projects because it is ", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'No',
                "on_release": self.sometimes4,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Yes',
                "on_release": self.often4,
                "viewclass": "IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=4,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="20) Do you feel any stomach related\n issues, when you feel anxious?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'No',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Mild',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            width_mult=3,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release=self.nxt)
        self.add_widget(nxtbtn)
        
        prevbtn = MDRaisedButton(text="<- Prev", pos_hint={'x':0,'y':0.03}, size_hint = (0.1, 0.08), on_release=self.prev)
        self.add_widget(prevbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Mild', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='Severe', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2
        
    #FUNCTIONS OF 2ND QUESTION
    #FUNCTIONS OF 1ST MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.07), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.07), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Partial or\nDoubtful Loss', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.07), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Loss of Insight', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def yes1(self):
        self.menu3.dismiss()
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        if hasattr(self, 'nope3'):
            self.remove_widget(self.nope3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.yep1 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.yep1)
        self.add_widget(box)
        self.score3 = 0

    def no1(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        if hasattr(self, 'nope3'):
            self.remove_widget(self.nope3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope1)
        self.add_widget(box)
        self.score3 = 1
    def no3(self):
        self.menu3.dismiss()
        if hasattr(self, 'yep1'):
            self.remove_widget(self.yep1)
        if hasattr(self, 'nope1'):
            self.remove_widget(self.nope1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nope3 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nope3)
        self.add_widget(box)
        self.score3 = 2
        

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def sometimes4(self):
        self.menu4.dismiss()
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev4 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev4)
        self.add_widget(box)
        self.score4 = 0

    def often4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som4 = MDLabel(text='Yes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som4)
        self.add_widget(box)
        self.score4 = 1

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='No', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Mild', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def nxt(self,instance):
        self.manager.current = "airesult"
        self.aiscore4 = self.aiscore4 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.aiscore4)
        self.scorefix = True
        
    def on_enter(self):
    	if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0
    
    def prev(self, instance):
        self.manager.current="talkai3"


class HamApg1(Screen):
    def __init__(self, **kwa):
        super(HamApg1, self).__init__(**kwa)
        self.scorefix = False
        self.First_Time = True
        self.hamscore1 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="1) Do you frequently feel anxious,\nfearful or feel that only the worst will\nhappen?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Never',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="2) Do you have feeling of tension,\nmove to tears easily, tremble or feel\nrestless?", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'Never',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="3) Do you fear being left alone or\n being with strangers, animals,\ntraffic or in a crowd, or in dark?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'Never',
                "on_release": self.never3,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes3,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always3,
                "viewclass":"IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="4) Do you have difficulty sleeping,\nbroken sleep or nightmares?", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'Never',
                "on_release": self.never4,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes4,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always4,
                "viewclass":"IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=3,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="5) Do you feel distracted or face\nmemory loss?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'Never',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Always',
                "on_release": self.always5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            position="bottom",
            width_mult=4,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release = self.nxt)
        self.add_widget(nxtbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def never3(self):
        self.menu3.dismiss()
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev3 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev3)
        self.add_widget(box)
        self.score3 = 0

    def sometimes3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som3 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som3)
        self.add_widget(box)
        self.score3 = 1

    def always3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw3 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw3)
        self.add_widget(box)
        self.score3 = 2

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def never4(self):
        self.menu4.dismiss()
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev4 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev4)
        self.add_widget(box)
        self.score4 = 0

    def sometimes4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som4 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som4)
        self.add_widget(box)
        self.score4 = 1

    def always4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw4 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw4)
        self.add_widget(box)
        self.score4 = 2

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def always5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw5 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw5)
        self.add_widget(box)
        self.score5 = 2

    def nxt(self, instance):
        self.manager.current = "ham2"
        self.hamscore1 = self.hamscore1 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.hamscore1)
        self.scorefix = True
    
    def on_enter(self):
        if self.First_Time:
            engine = pyttsx3.init()
            engine.say("Looks like you may have a case of Anxiety! Please answer these questions so that I can determine your severity.")
            engine.runAndWait()
            self.First_Time = False
        if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0


class HamAPg2(Screen):
    def __init__(self, **kwa):
        super(HamAPg2, self).__init__(**kwa)
        self.scorefix = False
        self.hamscore2 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="6) Do you face lack of pleasure in\nhobbies?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Never',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="7) Do you face stomach aches or do\nyou have a habit of often grinding your\nteeth.", font_style="H6", pos_hint={'x': 0.07, "y": 0.2})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.65}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'Never',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="8) Do you feel suddenly weak or\nexperience blurring of vision?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'Never',
                "on_release": self.never3,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes3,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always3,
                "viewclass":"IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #4TH QUESTION
        q4 = MDLabel(text="9) Do you have pain in chest or\nfainting feelings?", font_style="H6", pos_hint={'x': 0.07, "y": -0.1})
        self.add_widget(q4)
        
        self.b4 = MDRaisedButton( text="Select One", on_release=self.op4, pos_hint={'x': 0.7, "y": 0.35}, size_hint = (0.2,0.1))
        self.add_widget(self.b4)

        menu4_items = [
            {
                "text" :'Never',
                "on_release": self.never4,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes4,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always4,
                "viewclass":"IconListItem"
            }
        ]


        self.menu4 = MDDropdownMenu(
            caller = self.b4,
            items=menu4_items,
            position="bottom",
            width_mult=3,
        )

        box4 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box4)

        #5TH QUESTION
        q5 = MDLabel(text="10) Do you have choking sensations?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q5)
        
        self.b5 = MDRaisedButton( text="Select One", on_release=self.op5, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b5)

        menu5_items = [
            {
                "text" :'Never',
                "on_release": self.never5,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes5,
                "viewclass": "IconListItem"
            },
            {
                "text" :'Always',
                "on_release": self.always5,
                "viewclass": "IconListItem"
            }
        ]


        self.menu5 = MDDropdownMenu(
            caller = self.b5,
            items=menu5_items,
            position="bottom",
            width_mult=4,
        )

        box5 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box5)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release = self.nxt)
        self.add_widget(nxtbtn)
        
        prevbtn = MDRaisedButton(text="<- Prev", pos_hint={'x':0,'y': 0.03}, size_hint = (0.1, 0.08), on_release = self.prev)
        self.add_widget(prevbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.675}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def never3(self):
        self.menu3.dismiss()
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev3 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev3)
        self.add_widget(box)
        self.score3 = 0

    def sometimes3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som3 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som3)
        self.add_widget(box)
        self.score3 = 1

    def always3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw3 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw3)
        self.add_widget(box)
        self.score3 = 2

    #FUNCTIONS OF 4TH QUESTION
    def op4(self,instance):
        self.menu4.open()  
    
    def never4(self):
        self.menu4.dismiss()
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev4 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev4)
        self.add_widget(box)
        self.score4 = 0

    def sometimes4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'alw4'):
            self.remove_widget(self.alw4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som4 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som4)
        self.add_widget(box)
        self.score4 = 1

    def always4(self):
        self.menu4.dismiss()
        if hasattr(self, 'nev4'):
            self.remove_widget(self.nev4)
        if hasattr(self, 'som4'):
            self.remove_widget(self.som4)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.375}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw4 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw4)
        self.add_widget(box)
        self.score4 = 2

    #FUNCTIONS OF 5TH MENU
    def op5(self,instance):
        self.menu5.open()  
    
    def never5(self):
        self.menu5.dismiss()
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev5 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev5)
        self.add_widget(box)
        self.score5 = 0

    def sometimes5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'alw5'):
            self.remove_widget(self.alw5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som5 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som5)
        self.add_widget(box)
        self.score5 = 1

    def always5(self):
        self.menu5.dismiss()
        if hasattr(self, 'nev5'):
            self.remove_widget(self.nev5)
        if hasattr(self, 'som5'):
            self.remove_widget(self.som5)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw5 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw5)
        self.add_widget(box)
        self.score5 = 2

    def nxt(self, instance):
        self.manager.current = "ham3"
        self.hamscore2 = self.hamscore2 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.hamscore2)
        self.scorefix = True
    
    def on_enter(self):
    	if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0
    
    def prev(self, instance):
        self.manager.current="ham1"


class HamAPg3(Screen):
    def __init__(self, **kwa):
        super(HamAPg3, self).__init__(**kwa)
        self.scorefix = False
        self.hamscore3 = 0
        self.score1 = 0
        self.score2 = 0
        self.score3 = 0
        self.score4 = 0
        self.score5 = 0

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Answer some questions:", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        q1 = MDLabel(text="11) Do you have abdominal pain,\nburning sensations, nausea, vomiting\n or difficulty in swallowing?", font_style="H6", pos_hint={'x': 0.07, "y": 0.35})
        self.add_widget(q1)
        
        self.b1 = MDRaisedButton( text="Select One", on_release=self.op1, pos_hint={'x': 0.7, "y": 0.8}, size_hint = (0.2,0.1))
        self.add_widget(self.b1)

        menu1_items = [
            {
                "text" :'Never',
                "on_release": self.never1,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes1,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always1,
                "viewclass":"IconListItem"
            }
        ]


        self.menu1 = MDDropdownMenu(
            caller = self.b1,
            items=menu1_items,
            position="bottom",
            width_mult=3,
        )

        box1 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box1)
        
        #SECOND QUESTION
        q2 = MDLabel(text="12) Are you experiencing:\na) Loss of Libido (Males), premature\nejaculation\nb) Menstrual disturbances (Females)?", font_style="H6", pos_hint={'x': 0.07, "y": 0.05})
        self.add_widget(q2)
        
        self.b2 = MDRaisedButton( text="Select One", on_release=self.op2, pos_hint={'x': 0.7, "y": 0.5}, size_hint = (0.2,0.1))
        self.add_widget(self.b2)

        menu2_items = [
            {
                "text" :'Never',
                "on_release": self.never2,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes2,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always2,
                "viewclass":"IconListItem"
            }
        ]


        self.menu2 = MDDropdownMenu(
            caller = self.b2,
            items=menu2_items,
            position="bottom",
            width_mult=3,
        )

        box2 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box2)

        #3RD QUESTION
        q3 = MDLabel(text="13) Do you have sensations of dry\n mouth or tendency to sweat?", font_style="H6", pos_hint={'x': 0.07, "y": -0.25})
        self.add_widget(q3)
        
        self.b3 = MDRaisedButton( text="Select One", on_release=self.op3, pos_hint={'x': 0.7, "y": 0.2}, size_hint = (0.2,0.1))
        self.add_widget(self.b3)

        menu3_items = [
            {
                "text" :'Never',
                "on_release": self.never3,
                "viewclass": "IconListItem"
            },

            {
                "text" :'Sometimes',
                "on_release": self.sometimes3,
                "viewclass": "IconListItem"
            },

            {
                "text": 'Always',
                "on_release":  self.always3,
                "viewclass":"IconListItem"
            }
        ]


        self.menu3 = MDDropdownMenu(
            caller = self.b3,
            items=menu3_items,
            position="bottom",
            width_mult=3,
        )

        box3 = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.add_widget(box3)

        #NEXT SCREEN BUTTON THAT ALSO ACTS AS A SUBMIT BUTTON
        nxtbtn = MDRaisedButton(text="Next ->", pos_hint={'x': 0.9,'y':  0.03}, size_hint = (0.1, 0.08), on_release = self.nxt)
        self.add_widget(nxtbtn)
        
        prevbtn = MDRaisedButton(text="<- Prev", pos_hint={'x':0, 'y':0.03}, size_hint = (0.1, 0.08), on_release = self.prev)
        self.add_widget(prevbtn)

    #FUNCTIONS OF 1ST MENU
    def op1(self,instance):
        self.menu1.open()  
    
    def never1(self):
        self.menu1.dismiss()
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev1 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev1)
        self.add_widget(box)
        self.score1 = 0

    def sometimes1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'alw1'):
            self.remove_widget(self.alw1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som1 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som1)
        self.add_widget(box)
        self.score1 = 1

    def always1(self):
        self.menu1.dismiss()
        if hasattr(self, 'nev1'):
            self.remove_widget(self.nev1)
        if hasattr(self, 'som1'):
            self.remove_widget(self.som1)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.825}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw1 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw1)
        self.add_widget(box)
        self.score1 = 2

    #FUNCTIONS OF 2ND MENU
    def op2(self,instance):
        self.menu2.open()  
    
    def never2(self):
        self.menu2.dismiss()
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev2 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev2)
        self.add_widget(box)
        self.score2 = 0

    def sometimes2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'alw2'):
            self.remove_widget(self.alw2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som2 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som2)
        self.add_widget(box)
        self.score2 = 1

    def always2(self):
        self.menu2.dismiss()
        if hasattr(self, 'nev2'):
            self.remove_widget(self.nev2)
        if hasattr(self, 'som2'):
            self.remove_widget(self.som2)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.525}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw2 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw2)
        self.add_widget(box)
        self.score2 = 2

    #FUNCTIONS OF 3RD QUESTION
    def op3(self,instance):
        self.menu3.open()  
    
    def never3(self):
        self.menu3.dismiss()
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.nev3 = MDLabel(text='Never', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.nev3)
        self.add_widget(box)
        self.score3 = 0

    def sometimes3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'alw3'):
            self.remove_widget(self.alw3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.som3 = MDLabel(text='Sometimes', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.som3)
        self.add_widget(box)
        self.score3 = 1

    def always3(self):
        self.menu3.dismiss()
        if hasattr(self, 'nev3'):
            self.remove_widget(self.nev3)
        if hasattr(self, 'som3'):
            self.remove_widget(self.som3)
        box = MDBoxLayout(pos_hint={'x': 0.5, 'y': 0.225}, size_hint=(0.15, 0.05), md_bg_color="#FFFFFF")
        self.alw3 = MDLabel(text='Always', pos_hint={'x': 0.5, 'y': 0.5},size_hint=(0.8, 0.01), background="#000000")
        box.add_widget(self.alw3)
        self.add_widget(box)
        self.score3 = 2

    def nxt(self, instance):
        self.manager.current = "hamresult"
        self.hamscore3 = self.hamscore3 + self.score1 + self.score2 + self.score3 + self.score4 + self.score5
        print(self.hamscore3)
        self.scorefix = True
        
    def on_enter(self):
    	if self.scorefix:
            self.scorefix = False
            self.score = 0
            self.score1 = 0
            self.score2 = 0
            self.score3 = 0
            self.score4 = 0
            self.score5 = 0
    
    def prev(self):
        self.manager.current="talkai"
        
        
class HamResult(Screen):
    def __init__(self, **kwa):
        super(HamResult, self).__init__(**kwa)

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Here are your results!", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        self.box = MDBoxLayout()
        self.add_widget(self.box)

    def on_enter(self):
        ham1_screen = self.manager.get_screen('ham1')
        ham1_score = ham1_screen.hamscore1

        ham2_screen = self.manager.get_screen('ham2')
        ham2_score = ham2_screen.hamscore2

        ham3_screen = self.manager.get_screen('ham3')
        ham3_score = ham3_screen.hamscore3

        hamA_score = ham1_score + ham2_score + ham3_score

        hs = self.manager.get_screen('homeScreen')
        hs_name = hs.name_input.text
        hs_age = hs.age_input.text
        hs_gender = hs.gender_input.text
        hs_bloodgrp = hs.blood_input.text
        
        self.status = ""
        self.status_img = ""
        if hamA_score < 7:
            self.status = "Normal"
            self.status_img = Image(source="data/four.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch=True)
        elif hamA_score > 6 and hamA_score < 18:
            self.status = "Mild Anxiety"
            self.status_img = Image(source="data/three.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch=True)
        elif hamA_score > 17 and hamA_score < 25:
            self.status = "Moderate Anxiety"
            self.status_img = Image(source="data/two.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)
        elif hamA_score > 24:
            self.status = "Severe Anxiety"
            self.status_img = Image(source="data/one.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)
        elif hamA_score == 0:
            self.status = "Perfectly Healthy!"
            self.status_img = Image(source="data/five.png", size_hint_y = None, height = 200,pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)

        self.name_box = MDLabel(text=f"Name: {hs_name}", font_style="H6", pos_hint={'x': 0.2, 'y': 0.3})
        self.age_box = MDLabel(text=f"Age: {hs_age}", font_style="H6", pos_hint = {'x':0.2,'y':0.15})
        self.gender_box = MDLabel(text=f"Gender: {hs_gender}", font_style="H6", pos_hint={'x':0.2,'y':0})
        self.blood_box = MDLabel(text=f"Blood Group: {hs_bloodgrp}", font_style="H6", pos_hint={'x':0.2,'y':-0.15})
        self.scorebox = MDLabel(text=f"Mental Health Status:\n{self.status}", font_style = "H6", pos_hint={'x':0.6,'y':0.3})
        
        self.add_widget(self.name_box)
        self.add_widget(self.age_box)
        self.add_widget(self.gender_box)
        self.add_widget(self.blood_box)
        self.add_widget(self.scorebox)    
        self.add_widget(self.status_img)    
        	
        home = MDRaisedButton(text="Home", pos_hint={'x':0.5,'y':0.03}, on_release=self.home)
        self.add_widget(home)
        
    def home(self, instance):
        self.manager.current = "talkbot"
        
    def on_leave(self):
        self.status_img = ""
        self.status = ""
    	
        self.remove_widget(self.name_box)
        self.remove_widget(self.age_box)
        self.remove_widget(self.gender_box)
        self.remove_widget(self.scorebox)


class aiResult(Screen):
    def __init__(self, **kwa):
        super(aiResult, self).__init__(**kwa)

        bgimg = Image(source="data/background.png", allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.add_widget(bgimg)
        
        heading = MDLabel(text="Here are your results!", font_style="H4", pos_hint={'x': 0.03, 'y': 0.45})
        self.add_widget(heading)

        self.box = MDBoxLayout()
        self.add_widget(self.box)

    def on_enter(self):
        ai1_screen = self.manager.get_screen('talkai')
        ai1_score = ai1_screen.aiscore1

        ai2_screen = self.manager.get_screen('talkai2')
        ai2_score = ai2_screen.aiscore2

        ai3_screen = self.manager.get_screen('talkai3')
        ai3_score = ai3_screen.aiscore3

        ai4_screen = self.manager.get_screen('talkai4')
        ai4_score = ai4_screen.aiscore4

        ai_score = ai1_score + ai2_score + ai3_score + ai4_score

        hs = self.manager.get_screen('homeScreen')
        hs_name = hs.name_input.text
        hs_age = hs.age_input.text
        hs_gender = hs.gender_input.text
        hs_bloodgrp = hs.blood_input.text
        
        self.status = ""
        self.status_img = ""
        if ai_score < 7:
            self.status = "Normal"
            self.status_img = Image(source="data/four.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch=True)
        elif ai_score > 6 and ai_score < 18:
            self.status = "Mild Depression"
            self.status_img = Image(source="data/three.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch=True)
        elif ai_score > 17 and ai_score < 25:
            self.status = "Moderate Depression"
            self.status_img = Image(source="data/two.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)
        elif ai_score > 24:
            self.status = "Severe Depression"
            self.status_img = Image(source="data/one.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)
        elif ai_score == 0:
            self.status = "Perfectly Healthy!"
            self.status_img = Image(source="data/five.png", size_hint_x=None, height = 200, pos_hint={'x':0.65, 'y':0.1}, allow_stretch = True)

        self.name_box = MDLabel(text=f"Name: {hs_name}", font_style="H6", pos_hint={'x': 0.2, 'y': 0.3})
        self.age_box = MDLabel(text=f"Age: {hs_age}", font_style="H6", pos_hint = {'x':0.2,'y':0.15})
        self.gender_box = MDLabel(text=f"Gender: {hs_gender}", font_style="H6", pos_hint={'x':0.2,'y':0})
        self.blood_box = MDLabel(text=f"Blood Group: {hs_bloodgrp}", font_style="H6", pos_hint={'x':0.2,'y':-0.15})
        self.scorebox = MDLabel(text=f"Mental Health Status:\n{self.status}", font_style = "H6", pos_hint={'x':0.6,'y':0.3})

        self.add_widget(self.name_box)
        self.add_widget(self.age_box)
        self.add_widget(self.gender_box)
        self.add_widget(self.blood_box)
        self.add_widget(self.scorebox)   
        self.add_widget(self.status_img)
        
        home = MDRaisedButton(text="Home", pos_hint={'x':0.5,'y':0.03}, on_release=self.home)
        self.add_widget(home)
        
    def home(self, instance):
        self.manager.current = "talkbot" 

    def on_leave(self):
        self.status_img = ""
        self.status = ""
    	
        self.remove_widget(self.name_box)
        self.remove_widget(self.age_box)
        self.remove_widget(self.gender_box)
        self.remove_widget(self.scorebox)


class MindMagic(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self._app_name = "RakshaKavach!"
        self.icon = "data/logo.png"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(WinVid(name="winvid"))
        sm.add_widget(HomeScreen(name="homeScreen"))
        sm.add_widget(TalkBot(name="talkbot"))
        sm.add_widget(Scren3(name="scren3"))
        sm.add_widget(Decide(name="decide"))
        sm.add_widget(TalkAI(name="talkai"))
        sm.add_widget(TalkAIPg2(name="talkai2"))
        sm.add_widget(TalkAIPg3(name="talkai3"))
        sm.add_widget(TalkAiPg4(name="talkai4"))
        sm.add_widget(aiResult(name="airesult"))
        sm.add_widget(HamApg1(name="ham1"))
        sm.add_widget(HamAPg2(name="ham2"))
        sm.add_widget(HamAPg3(name="ham3"))
        sm.add_widget(HamResult(name="hamresult"))
        return sm

if __name__ == "__main__":
    MindMagic().run()
