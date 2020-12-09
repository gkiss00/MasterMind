import random

#The class of the game, need to create one to play the game
class MasterMind:
    #The key word "self" is used to call method or variables of the class in the others functions of the class

    #The constructor of the class, is called when u instantiate an object of the class. See line: 79
    #And is used to initialize the vars of the class
    def __init__(self):
        self.size = 6
        self.goal = self.initGoal()
        self.nb_turn = 10
        print(self.goal)

    #Create a random goal to reach
    def initGoal(self):
        goal = []
        for i in range(self.size):
            #Fill your goal at place i with a random number between 1 and 6 included, rise up the second number to make the game more complicated
            goal.append(random.randint(1, 6))
        return goal
    
    #This function contains the whole game
    def play(self):
        #Each turn during 10 turns
        for i in range(self.nb_turn):
            #Enter your input with space between numbers
            guess = [ int(x) for x in input().split()]
            #If everything is correct
            if self.isCorrect(guess) == self.size:
                print("Winner")
                break
            #Else 
            else:
                #if it is the last turn, u lose
                if i == self.nb_turn - 1:
                    print("U lost, u are a f**king loser BOUUUUUUUUU")
                #Else you continue
                else:
                    print(self.isCorrect(guess),
                    " are correct and ",
                    self.isSemiCorrect(guess),
                    " arn't at the right place!!")
                    print("try again")
    
    #Return the number of correct numbers at the right place
    def isCorrect(self, guess):
        right = 0
        for i in range(self.size):
            if (guess[i] == self.goal[i]):
                right += 1
        return right

    #Return the number of correct numbers at the wrong place
    def isSemiCorrect(self, guess):
        semiRight = 0
        trueTabGuess = self.initTrueTab(guess)
        trueTabGoal = self.initTrueTab(guess)
        for i in range(self.size):
            if trueTabGuess[i] == False:
                stop = 0
                for j in range(self.size):
                    if trueTabGoal[j] == False and stop == 0:
                        if guess[i] == self.goal[j]:
                            semiRight += 1
                            trueTabGuess[i] = True
                            trueTabGoal[j] = True
                            stop = 1
        return(semiRight)

    #Used in "isSemiCorrect"
    def initTrueTab(self, guess):
        trueTab = []
        for i in range(self.size):
            trueTab.append(False)
        for i in range(self.size):
            if (guess[i] == self.goal[i]):
                trueTab[i] = True
        return (trueTab)

#Create an object from the class MasterMind
masterMind = MasterMind()
#Call the method play on this object
masterMind.play()

