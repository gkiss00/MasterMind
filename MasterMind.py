from kivy.app import App
from kivy.base import runTouchApp

import random
import json

from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

#Liste des couleurs pour le MasterMind
class ColorList():
    def __init__(self):
        self.colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "white", "black"]
        self.colors_dic = {0:"red", 1:"green", 2:"blue", 3:"yellow", 4:"magenta", 5:"cyan", 6:"white", 7:"black"}
        self.rgb = [(255, 0, 0, 1), (0, 255, 0, 1), (0, 0, 255, 1), (255, 255, 0, 1), (255, 0, 255, 1), (0, 255, 255, 1), (255, 255, 255, 1), (0, 0, 0, 1)]

class MasterMind(App):
    def build(self):
        #Used with json
        self.best_score = 0
        self.pseudo = ""
        self.your_score = 0
        
        #List of colors
        self.color_list = ColorList()
        #Var of the gameplay
        self.size = 0
        self.nb_turns = 0
        self.nb_colors = 0
        self.actual_turn = 0
        #Array
        self.goal = []
        self.guess = []
        self.buttons = []
        self.indices = []
        #Screen for the screen manager
        self.menu_screen = self.configuerMenu()
        self.game_screen = self.configureGameScreen("Easy")
        self.end_screen = self.configureEndScreen("End", "wp")
        #Screen manager
        self.screen_manager = self.configureScreenManager()
        #Uncomment to se some scores
        #self.register_scores()
        self.get_best_score()
        return (self.screen_manager)

    #Create a random goal to reach
    def initGoal(self):
        goal = []
        for i in range(self.size):
            goal.append(self.color_list.colors[random.randint(1, self.nb_colors) - 1])
        return (goal)

    def configureScreenManager(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(self.menu_screen)
        screen_manager.add_widget(self.game_screen)
        screen_manager.add_widget(self.end_screen)
        screen_manager.current = "Menu"
        return (screen_manager)

    def configuerMenu(self):
        menu_screen = Screen(name="Menu")
        menu = BoxLayout(orientation="vertical")
        button_easy = Button(text="Easy")
        button_easy.bind(on_press=self.play_easy)
        button_hard = Button(text="Hard")
        button_hard.bind(on_press=self.play_hard)
        menu.add_widget(button_easy)
        menu.add_widget(button_hard)
        menu_screen.add_widget(menu)
        return (menu_screen)
    
    def configureGameScreen(self, _name):
        self.get_best_score()
        game_screen = Screen(name=_name)
        #Config the input and indice grids
        button_grid_layout = GridLayout(cols=self.size, rows=self.nb_turns)
        indices_grid_layout = GridLayout(cols=2, rows=self.nb_turns)
        for i in range(self.nb_turns):
            for j in range(self.size):
                b_id = ""
                b_id += str(j)
                b = Button(id=b_id,disabled=True, size=(10, 10), background_color=self.color_list.rgb[0], on_press=self.change_color)
                self.buttons.append(b)
                button_grid_layout.add_widget(b)
                if(j < 2):
                    label = Label(text="correct\n") if j == 0 else Label(text="wrong place\n")
                    self.indices.append(label)
                    indices_grid_layout.add_widget(label)
        #Button to validate your choise
        b = Button(text="Valider", on_press=self.validate)
        #Layout out to display with style
        horizontal_laout = BoxLayout(orientation="horizontal")
        horizontal_laout.add_widget(button_grid_layout)
        horizontal_laout.add_widget(indices_grid_layout)
        horizontal_laout.add_widget(b)
        #Best score
        label_text = "Best score : "
        label_text += str(self.best_score)
        label = Label(text=label_text, size_hint=(1, .1))
        #Layout out to display with style
        vertical_layout = BoxLayout(orientation="vertical")
        vertical_layout.add_widget(label)
        vertical_layout.add_widget(horizontal_laout)
        game_screen.add_widget(vertical_layout)
        return (game_screen)

    def configureEndScreen(self, _name, _message):
        end_screen = Screen(name=_name)
        box_layout = BoxLayout(orientation="vertical")

        submit = Button(text="register", on_press=self.register_my_score)
        text_input = TextInput(size_hint=(1, .3))
        text_input.bind(text = self.setPseudo)
        label_text = _message
        label_text += "\n"
        label_text += "Your score : "
        label_text += str(self.your_score)
        label = Label(text=label_text)
        b = Button(text="Come back to the menu", on_press=self.go_to_menu)
        box_layout.add_widget(label)
        box_layout.add_widget(text_input)
        box_layout.add_widget(submit)
        box_layout.add_widget(b)
        end_screen.add_widget(box_layout)
        return (end_screen)

    def setPseudo(self, instance, text):
        self.pseudo = text


    def go_to_menu(self, instance):
        self.screen_manager.current = "Menu"
    
    #Set parameters for the easy mode and lauch the game
    def play_easy(self, instance):
        self.size = 4
        self.nb_turns = 10
        self.nb_colors = 6
        for i in range(self.size):
            self.guess.append(0)
        self.goal = self.initGoal()
        self.screen_manager.remove_widget(self.game_screen)
        self.game_screen = self.configureGameScreen("Easy")
        self.screen_manager.add_widget(self.game_screen)
        self.screen_manager.current = "Easy"
        self.play()

    #Set parameters for the hard mode and lauch the game
    def play_hard(self, instance):
        self.size = 5
        self.nb_turns = 12
        self.nb_colors = 8
        for i in range(self.size):
            self.guess.append(0)
        self.goal = self.initGoal()
        self.screen_manager.remove_widget(self.game_screen)
        self.game_screen = self.configureGameScreen("Hard")
        self.screen_manager.add_widget(self.game_screen)
        self.screen_manager.current = "Hard"
        self.play()

    def play(self):
        self.actual_turn = 0
        print(self.goal)
        self.enableButton()
    
    #Check if the conbination is correct
    def validate(self, istance):
        self.your_score = self.nb_turns - self.actual_turn - 1
        #If everything is correct, reset all the data and go to the end screen
        if self.nb_right() == self.size:
            self.reset()
            self.screen_manager.remove_widget(self.end_screen)
            self.end_screen = self.configureEndScreen("End", "Winner")
            self.screen_manager.add_widget(self.end_screen)
            self.screen_manager.current = "End"
        #If u reach the last turn, reset all the data and go to the end screen
        elif self.actual_turn == self.nb_turns - 1:
            self.reset()
            self.screen_manager.remove_widget(self.end_screen)
            self.end_screen = self.configureEndScreen("End", "You lose")
            self.screen_manager.add_widget(self.end_screen)
            self.screen_manager.current = "End"
        #Else, give u the indices and run the next turn   
        else:
            self.indices[self.actual_turn * 2].text += str(self.nb_right())
            self.indices[(self.actual_turn * 2) + 1].text += str(self.nb_semi_right())
            self.actual_turn += 1
            self.enableButton()
            self.refresh_guess()
    
    #refresh the table of guess
    def refresh_guess(self):
        for i in range(self.size):
            self.guess[i] = 0

    #rest all the data
    def reset(self):
        self.color_list = ColorList()
        self.guess = []
        self.size = 0
        self.nb_turns = 0
        self.nb_colors = 0
        self.actual_turn = 0
        self.goal = []
        self.buttons = []
        self.indices = []
        self.enableButton()

    #Return the number of right guess at the right place
    def nb_right(self):
        right = 0
        for i in range(self.size):
            if (self.color_list.colors_dic[self.guess[i]] == self.goal[i]):
                right += 1
        return right

    #Return the number of right guess at the wrong place
    def nb_semi_right(self):
        semiRight = 0
        trueTabGuess = self.initTrueTab()
        trueTabGoal = self.initTrueTab()
        for i in range(self.size):
            if trueTabGuess[i] == False:
                stop = 0
                for j in range(self.size):
                    if trueTabGoal[j] == False and stop == 0:
                        if self.color_list.colors_dic[self.guess[i]] == self.goal[j]:
                            semiRight += 1
                            trueTabGuess[i] = True
                            trueTabGoal[j] = True
                            stop = 1
        return(semiRight)

    #Used in nb_semi_right
    def initTrueTab(self):
        trueTab = []
        for i in range(self.size):
            trueTab.append(False)
        for i in range(self.size):
            if self.color_list.colors_dic[self.guess[i]] == self.goal[i]:
                trueTab[i] = True
        return (trueTab)
    
    #Set the buttons u can use for the current turn
    def enableButton(self):
        count = 0
        for i in range(self.nb_turns):
            for j in range(self.size):
                if i == self.actual_turn:
                    self.buttons[count].disabled=False
                if i != self.actual_turn:
                    self.buttons[count].disabled=True
                count += 1
    
    #Change the color of the button with the next one on the list
    def change_color(self, instance):
        self.guess[int(instance.id)] += 1
        self.guess[int(instance.id)] %= self.nb_colors
        instance.background_color=self.color_list.rgb[self.guess[int(instance.id)]]

    def get_best_score(self):
        self.best_score = 0
        with open('score.json') as json_file:
            data = json.load(json_file)
            for score in data['score']:
                if (score['score'] > self.best_score):
                    self.best_score = score['score']

    def register_my_score(self, instance):
        if self.check_pseudo(self.pseudo) == False:
            return
        found = False
        with open('score.json') as json_file:
            data = json.load(json_file)
            for score in data['score']:
                if score['pseudo'] == self.pseudo:
                    found = True
                    if score['score'] < self.your_score:
                        score['score'] = self.your_score
        if found == False:
            data['score'].append({
                'pseudo': self.pseudo,
                'score': self.your_score
            })
        with open('score.json', 'w') as outfile:
            json.dump(data, outfile)
        self.screen_manager.current = "Menu"

    def check_pseudo(self, _pseudo):
        for i in range(len(_pseudo)):
            if (_pseudo[i] != " "):
                return (True)
        return (False)

    def register_scores(self):
        data = {}
        data['score'] = []
        data['score'].append({
            'pseudo': "the_best",
            'score': 9,
        })
        data['score'].append({
            'pseudo': "betrouze",
            'score': 0,
        })
        data['score'].append({
            'pseudo': "gneeee",
            'score': 4,
        })

        with open('score.json', 'w') as outfile:
            json.dump(data, outfile)

MasterMind().run()