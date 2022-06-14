import sys
import os
import time

class damage():
  def __init__(self, headDamage, bodyDamage, legDamage):
    self.headDamage = headDamage
    self.bodyDamage = bodyDamage
    self.legDamage = legDamage

class Items:
<<<<<<< HEAD
  def __init__(self, name):
    self.firstname = name
    
=======
  def __init__(self, name, durability: int):
    self.name = name
    self.durability = durability

  def getDetails(self) -> list:
    return [self.name, self.durability]

  def reduceDurability(self, durabilityLost: int):
    self.durability -= durabilityLost
>>>>>>> 6aa0680c01805817618f881a122b087b5c689300


class Armor(Items):
  def __init__(self, name, type):
    super().__init__(name, 0)
    self.damageReduction = 0
    self.type = type
    if type == "Light":
      self.durability = 25
      self.damageReduction = 5
    elif type == "Basic":
      self.durability = 50
      self.damageReduction = 10
    elif type == "Medium":
      self.durability = 75
      self.damageReduction = 15
    elif type == "Heavy":
      self.durability = 100
      self.damageReduction = 20
    else:
      self.durability = 0

  def getDetails(self) -> list:
    return [self.name, self.durability, self.damageReduction]


y = Armor("Armor 1", "Medium")
print(y.getDetails())
y.reduceDurability(20)
print(y.getDetails())


class Consumables(Items):
  def __init__(self, name,types):
    super().__init__(name)
    self.types = types
 
  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)


class Weapon(Items):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

  def reload():
    pass

class damage():
  pass

class Characters:
  def __init__(self):
    self.name = ''
    self.feeling = ''

  def printname(self):
    print(self.firstname, self.lastname)

class Player(Characters):
  def __init__(self):
    pass
    # super().__init__(self)
    # self.graduationyear = year

player1 = Player()

class Enemy(Characters):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    print("Welcome", self.firstname, self.lastname, "to the class of", self.graduationyear)

def Search():
    pass

def Inventory():
    pass

##################################### kd ##################################

################
# Title Screen #
################
def title_screen_options():
  option = input("> ")
  if option.lower() == ("play"):
    main()
  elif option.lower() == ("quit"):
    sys.exit()
  elif option.lower() == ("help"):
    help_menu()
  while option.lower() not in ['play', 'help', 'quit']:
    print("Invalid command, please try again.")
    option = input("> ")
    if option.lower() == ("play"):
      main()
    elif option.lower() == ("quit"):
      sys.exit()
    elif option.lower() == ("help"):
      help_menu()

def title_screen():
  os.system('cls||clear')
  print('#' * 45)
  print('# Welcome to this text-based shooting game. #')
  print("#      Brum Brum Final Project KB 2022!     #")
  print('#' * 45)
  print("               .: Play :.               ")
  print("               .: Help :.               ")
  print("               .: Quit :.               ")
  title_screen_options()


#############
# Help Menu #
#############
def help_menu():
  print("")
  print("~" * 45)
  print("Type a command such as 'search' or 'check inventory'")
  print("to move on to the next stage.\n")
  print("After you do a search, you can inputs such as 'attack' or 'reload' or 'fallback' or 'heal'")
  print("the game will let you interact with the next move.\n")
  print("Please ensure to type in lowercase for ease.\n")
  print('#' * 45)
  print("    Please select an option to continue.     ")
  print('#' * 45)
  print("               .: Play :.               ")
  print("               .: Help :.               ")
  print("               .: Quit :.               ")
  title_screen_options()

#################
# Game Handling #
#################
quitgame = 'quit'


##################
# main task menu #
##################
def main():
  os.system('cls||clear')

  question1 = "Hello there, what is your name?\n"
  for character in question1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  player_name = input("> ")
  player1.name = player_name

  question2 = "My dear friend " + player1.name + ", how are you feeling?\n"
  for character in question2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  feeling = input("> ")
  player1.feeling = feeling.lower()

  good_adj = ['good', 'great', 'rohit', 'happy', 'aight', 'understanding', 'great', 'alright', 'calm', 'confident', 'not bad', 'courageous', 'peaceful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'easy', 'lucky', 'k', 'comfortable', 'amazed', 'fortunate', 'optimistic', 'pleased', 'free', 'delighted', 'swag', 'encouraged', 'ok', 'overjoyed', 'impulsive', 'clever', 'interested', 'gleeful', 'free', 'surprised', 'satisfied', 'thankful', 'frisky', 'content', 'receptive', 'important', 'animated', 'quiet', 'okay', 'festive', 'spirited', 'certain', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'satisfied', 'wonderful', 'serene', 'glad', 'free', 'and', 'easy', 'cheerful', 'bright', 'sunny', 'blessed', 'merry', 'reassured', 'elated', '1738', 'love', 'interested', 'positive', 'strong', 'loving']
  hmm_adj = ['idk', 'concerned', 'lakshya', 'eager', 'impulsive', 'considerate', 'affected', 'keen', 'free', 'affectionate', 'fascinated', 'earnest', 'sure', 'sensitive', 'intrigued', 'intent', 'certain', 'tender', 'absorbed', 'anxious', 'rebellious', 'devoted', 'inquisitive', 'inspired', 'unique', 'attracted', 'nosy', 'determined', 'dynamic', 'passionate', 'snoopy', 'excited', 'tenacious', 'admiration', 'engrossed', 'enthusiastic', 'hardy', 'warm', 'curious', 'bold', 'secure', 'touched', 'brave', 'sympathy', 'daring', 'close', 'challenged', 'loved', 'optimistic', 'comforted', 're', 'enforced', 'drawn', 'toward', 'confident', 'hopeful', 'difficult']
  bad_adj = ['bad', 'meh', 'sad', 'hungry', 'unpleasant', 'qus', 'angry', 'depressed', 'confused', 'helpless', 'irritated', 'lousy', 'upset', 'incapable', 'enraged', 'disappointed', 'doubtful', 'alone', 'hostile', 'discouraged', 'uncertain', 'paralyzed', 'insulting', 'ashamed', 'indecisive', 'fatigued', 'sore', 'powerless', 'perplexed', 'useless', 'annoyed', 'diminished', 'embarrassed', 'inferior', 'upset', 'guilty', 'hesitant', 'vulnerable', 'hateful', 'dissatisfied', 'shy', 'empty', 'unpleasant', 'miserable', 'stupefied', 'forced', 'offensive', 'detestable', 'disillusioned', 'hesitant', 'bitter', 'repugnant', 'unbelieving', 'despair', 'aggressive', 'despicable', 'skeptical', 'frustrated', 'resentful', 'disgusting', 'distrustful', 'distressed', 'inflamed', 'abominable', 'misgiving', 'woeful', 'provoked', 'terrible', 'lost', 'pathetic', 'incensed', 'in', 'despair', 'unsure', 'tragic', 'infuriated', 'sulky', 'uneasy', 'cross', 'bad', 'pessimistic', 'dominated', 'worked', 'up', 'a', 'sense', 'of', 'loss', 'tense', 'boiling', 'fuming', 'indignant', 'indifferent', 'afraid', 'hurt', 'sad', 'insensitive', 'fearful', 'crushed', 'tearful', 'dull', 'terrified', 'tormented', 'sorrowful', 'nonchalant', 'suspicious', 'deprived', 'pained', 'neutral', 'anxious', 'pained', 'grief', 'reserved', 'alarmed', 'tortured', 'anguish', 'weary', 'panic', 'dejected', 'desolate', 'bored', 'nervous', 'rejected', 'desperate', 'preoccupied', 'scared', 'injured', 'pessimistic', 'cold', 'worried', 'offended', 'unhappy', 'disinterested', 'frightened', 'afflicted', 'lonely', 'lifeless', 'timid', 'aching', 'grieved', 'shaky', 'victimized', 'mournful', 'restless', 'heartbroken', 'dismayed', 'doubtful', 'agonized', 'threatened', 'appalled', 'cowardly', 'humiliated', 'quaking', 'wronged', 'menaced', 'alienated', 'wary']

  if player1.feeling in good_adj:
    feeling_string = "I am glad you feel"
  elif player1.feeling in hmm_adj:
    feeling_string = "that is interesting you feel"
  elif player1.feeling in bad_adj:
    feeling_string = "I am sorry to hear you feel"
  else:
    feeling_string = "I do not know what it is like to feel"

  question3 = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
  for character in question3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)

title_screen()