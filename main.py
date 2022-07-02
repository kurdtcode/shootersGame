from copyreg import constructor
from email import header
from mimetypes import init
import random
import re
from selectors import SelectorKey
import sys
import os
import time
screen_width = 100

class damage():
  def __init__(self, headDamage, bodyDamage, legDamage):
    self.headDamage = headDamage
    self.bodyDamage = bodyDamage
    self.legDamage = legDamage

class Items:
  def __init__(self, name, durability: int):
    self.name = name
    self.durability = durability

  def getDetails(self) -> list:
    return [self.name, self.durability]

  def reduceDurability(self, durabilityLost: int):
    self.durability -= durabilityLost


class Armor(Items):
  def __init__(self, name, type):
    super().__init__(name, 0)
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
      self.damageReduction = 0

  def getDetails(self) -> list:
    return [self.name, self.durability, self.damageReduction]


class Consumables(Items):
  def __init__(self, name):
    super().__init__(name, 0)
    self.healamount = 0
    if name == "Bandage":
      self.healamount = 25
    elif name == "Medkit":
      self.healamount = 50

  def getDetails(self) -> list:
    return [self.name, self.healamount]

################
# Weapon Setup #
################

class Weapon(Items):
  def __init__(self, name):
    super().__init__(name, 0)
    self.bullet = 0
    self.maxBullet = 0
    self.damage = Damage(0, 0, 0)
    #self.reloadTime = 0
    self.bulletPerAttack = 0
    if name == "P250 Pistol":
      self.maxBullet = 12
      self.damage = Damage(20, 15, 10)
      #self.reloadTime = 2
      self.durability = 50
      self.bulletPerAttack = 3

    elif name == "Deagle Pistol":
      self.maxBullet = 8
      self.damage = Damage(40, 30, 20)
      #self.reloadTime = 2
      self.durability = 50
      self.bulletPerAttack = 2

    elif name == "M4A1 Riffle":
      self.maxBullet = 50
      self.damage = Damage(75, 50, 40)
      #self.reloadTime = 3
      self.durability = 75
      self.bulletPerAttack = 5

    elif name == "AWM Sniper Riffle":
      self.maxBullet = 5
      self.damage = Damage(150, 100, 80)
      #self.reloadTime = 5
      self.durability = 100
      self.bulletPerAttack = 1

    self.reload()
    
  def getDetails(self) -> list:
    return [self.name, self.damage, self.maxBullet, self.bullet]

  def shoot(self):
    self.bullet = self.bullet - self.bulletPerAttack
    self.durability = self.durability - 5

  def reload(self):
    self.bullet = self.maxBullet

################
# Damage Setup #
################
class Damage():
  def __init__(self, head, body, leg) -> None:
    self.headDamage = head
    self.bodyDamage = body
    self.legDamage = leg

  def randomHit(self):
    rand = random.random()
    if rand < 0.1:
      return self.headDamage
    elif rand < 0.8:
      return self.bodyDamage
    else:
      return self.legDamage

class Inventory():
  def __init__(self):
      self.armor = list()
      self.weapon = list()
      self.consumable = list()
      self.equippedArmor = -1
      self.equippedWeapon = -1

  def addArmor(self, armor:Armor):
    self.armor.append(armor)
  def addWeapon(self, weapon:Weapon):
    self.weapon.append(weapon)
  def addConsumable(self, consumable:Consumables):
    self.consumable.append(consumable)
  def getAllArmor(self):
    return self.armor
  def getAllWeapon(self):
    return self.weapon
  def getAllConsumable(self):
    return self.consumable

  def equipArmor(self, index):
    if index >= len(self.armor):
      return
    if index < 0:
      return
    self.equippedArmor = index

  def seeEquippedArmor(self) -> Armor:
    if self.equippedArmor >= len(self.armor):
      return
    if self.equippedArmor < 0:
      return
    
    return self.armor[self.equippedArmor]

  def seeArmorDetail(self, index) -> Armor:
    if index >= len(self.armor):
      return
    if index < 0:
      return
    return self.armor[index]

  def equipWeapon(self, index):
    if index >= len(self.weapon):
      return
    if index < 0:
      return
    self.equippedWeapon = index

  def seeEquippedWeapon(self) -> Weapon:
    if self.equippedWeapon >= len(self.weapon):
      return
    if self.equippedWeapon < 0:
      return
    
    return self.weapon[self.equippedWeapon]


  def seeWeaponDetail(self, index) -> Weapon:
    if index >= len(self.weapon):
      return
    if index < 0:
      return

    return self.weapon[index]

  def useConsumable(self, index):
    if index >= len(self.consumable):
      return
    if index < 0:
      return

    return self.consumable.pop(index)

############################################################################################################################
# Character Setup  
# Character can heal and attack

class Characters:
  def __init__(self, maxHp):
    self.name = ""
    self.maxHP = maxHp
    self.hp = maxHp
    self.game_over = False
    self.inventory = Inventory()

  def CharacterDetail(self):
    return [self.name, self.hp, self.inventory]

  def heal(self, index):
    self.hp = self.hp + self.inventory.useConsumable(index)
    if self.hp > self.maxHP:
      self.hp = self.maxHP

  def attack(self, enemy):
    equippedWeapon = self.inventory.seeWeaponDetail(self.inventory.equippedWeapon) #Weapon
    # type(equippedWeapon)
    damage = equippedWeapon.getDetails()[1] #Weapon Damage

    dmg = damage.randomHit()
    equippedWeapon.shoot()

    enemyArmor = enemy.inventory.seeEquippedArmor() #Enemy Armor
    dmgReduc = enemyArmor.getDetails()[2] #Damage Reduction

    finalDmg = dmg - dmg * dmgReduc/100 #Calc Damage

    enemy.hp = enemy.hp - finalDmg


################
# Player Setup #
################
class Player(Characters):
  def __init__(self):
    super().__init__(200)
    weapon = Weapon("P250 Pistol")
    self.inventory.addWeapon(weapon)
    self.inventory.equipWeapon(0)
#declare object player
player1 = Player()

class Enemy(Characters):
  def __init__(self, template):
    super().__init__(100)
    if template == 1:
      self.name = "Militia"
      armor = Armor("Light Armor", "Light")
      self.inventory.addArmor(armor)
      weapon = Weapon("P250 Pistol")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(0)
      self.inventory.equipWeapon(0)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      
    if template == 2:
      self.name = "Normal Soldier"
      armor = Armor("Basic Armor", "Basic")
      self.inventory.addArmor(armor)
      weapon = Weapon("Deagle Pistol")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(0)
      self.inventory.equipWeapon(0)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      consumables2 = Consumables("Bandage")

      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      self.inventory.addConsumable(consumables2)

    if template == 3:
      self.name = "Veteran Soldier"
      armor = Armor("Medium Armor", "Medium")
      self.inventory.addArmor(armor)
      weapon = Weapon("M4A1 Rifle")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(0)
      self.inventory.equipWeapon(0)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      consumables2 = Consumables("Bandage")

      consumables3 = Consumables("Medkit")

      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      self.inventory.addConsumable(consumables2)
      self.inventory.addConsumable(consumables3)

    if template == 4:
      self.name = "Special Force Soldier"
      armor = Armor("Heavy Armor", "Heavy")
      self.inventory.addArmor(armor)
      weapon = Weapon("AWM Sniper Rifle")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(0)
      self.inventory.equipWeapon(0)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      consumables2 = Consumables("Bandage")
      consumables3 = Consumables("Bandage")
      consumables4 = Consumables("Bandage")

      consumables5 = Consumables("Medkit")
      consumables6 = Consumables("Medkit")
      consumables7 = Consumables("Medkit")

      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      self.inventory.addConsumable(consumables2)
      self.inventory.addConsumable(consumables3)
      self.inventory.addConsumable(consumables4)
      self.inventory.addConsumable(consumables5)
      self.inventory.addConsumable(consumables6)
      self.inventory.addConsumable(consumables7)

  def auto(self, player):
    #Initial Value/Known Value
    #self.hp
    #self.inventory.seeEquippedWeapon()
    #self.inventory.seeEquippedArmor()
    selfDmg = self.inventory.seeEquippedWeapon().getDetails()[1].body
    selfDmgReduc = self.inventory.seeEquippedArmor().getDetails()[2]

    playerHP = player.hp
    self.inventory.seeEquippedWeapon(self.inventory.equippedWeapon)
    playerWeapon = player.inventory.seeEquippedWeapon()
    playerArmor = player.inventory.seeEquippedArmor()

    playerDmg = playerWeapon.getDetails()[1].body
    playerDmgReduc = playerArmor.getDetails()[2]

    #Condition Value Init 2
    selfFinalDamage = selfDmg - selfDmg * playerDmgReduc/100
    playerFinalDamage = playerDmg - playerDmg * selfDmgReduc/100


    #Condition Value Init 3
    selfOneHit = False
    playerOneHit = False

    #Condition Value Init 4
    selfConsumableExist = False
    playerConsumableExist = False

    #Condition Value Init 5
    medkitCount = 0
    bandageCount = 0
    medkitExist = False
    bandageExist = False
    medkitHealExceedMax = False
    
    #Condition Value Init 6
    selfHighHealth = False
    selfMediumHealth = False
    selfLowHealth = False
    playerHighHealth = False
    playerMediumHealth = False
    playerLowHealth = False

    #Action
    selfAttack = False
    selfHeal = False
    
    #Condition 1
    if self.hp - playerFinalDamage <= 0:
      selfOneHit = True
    if player.hp - selfFinalDamage <= 0:
      playerOneHit = True

    #Condition 2
    if len(self.inventory.getAllConsumable()) != 0:
      selfConsumableExist = True
    if len(player.inventory.getAllConsumable()) != 0:
      playerConsumableExist = True
    
    
    #Condition 3
    for consumable in self.inventory.getAllConsumable():
      temp = consumable.getDetails()
      if temp[1] == 50:
        pass

    if self.hp + 50 > self.maxHP:
      medkitHealExceedMax = True


    #Condition 4
    if self.hp > 80:
      selfHighHealth = True
    elif self.hp > 40:
      selfMediumHealth = True
    else:
      selfLowHealth = True
    
    if player.hp > 80:
      playerHighHealth = True
    elif player.hp > 40:
      playerMediumHealth = True
    else:
      playerLowHealth = True
    
    #Condition 5
    if playerOneHit:
      selfAttack = True
    else:
      if selfOneHit:
        if selfConsumableExist:
          if medkitHealExceedMax:
            pass





#declare object enemy
enemy1 = Enemy(1)

print(player1.CharacterDetail())
print(enemy1.CharacterDetail())
player1.attack(enemy1)

print(player1.CharacterDetail())
print(enemy1.CharacterDetail())

def Search():
  turn=0
  playerHealth=100 ## 100 diganti darah karakter
  lastEnemyTurn=0
  ##rumus masih agak ngaco soalnya semakin banyak turn nya chanche dapet enemy nya semakin turun, weapon sm armomr nya naik
  chanceFindBoss  = max(((turn - 10) * 0.2) + (100 * 0.005),0)
  chanceFindEnemy = (turn * 0.7) + (100 * 0.05) - ( lastEnemyTurn * 0.08)
  chanceGetArmor = (turn * 0.3) + (100 * 0.01)
  chanceGetWeapon = (turn * 0.5) + (100 * 0.01)
  chanceGetHealing = (turn * 0.6) + (playerHealth * 0.01)

  pembagi = (chanceFindBoss + chanceFindEnemy + chanceGetWeapon + chanceGetWeapon + chanceGetHealing)

  realChanceBoss = round(chanceFindBoss / pembagi,2)
  realChanceEnemy = round(chanceFindEnemy / pembagi,3)
  realChanceArmor = round(chanceGetArmor / pembagi,3)
  realChanceWeapon = round(chanceGetWeapon / pembagi,3)
  realChanceHealing = round(chanceGetHealing / pembagi,3)

  angkaRandom = random.randint(0,10)/10
  ## cuman buat ngelihat nilai chance (buat ngepasin udah bener sama if if an nya belom)
  # print("boss", realChanceBoss)
  # print("enemy", realChanceEnemy)
  # print("armor", realChanceArmor)
  # print("weapon", realChanceWeapon)
  # print("Healing", realChanceHealing)
  # print("------------")
  # print(angkaRandom)

  if angkaRandom <= realChanceBoss :
      print("get boss")
  elif angkaRandom <= realChanceBoss +  realChanceEnemy :
      if turn >= 0 and turn <= 3:
          randomGear = random.randint(1,2)
          if randomGear == 1 :
              print("get weapon")
          else:
              print("get armor")
      elif turn > 3 and turn <= 6 :
          print("get enemy Militia")
      elif turn > 6 and turn <= 9 :
          print("get enemy Normal Soldier")
      elif turn > 9 and turn <=12 :
          print("get enemy Veteran Soldier")
      else :
          print("get boss")
      lastEnemyTurn += 1
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon :
      print("get weapon")
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon +realChanceArmor :
      print("get armor")
  else :
      print("get heal")




##################################### kd ##################################

##################
# look inventory #
# (use invetory) #
##################
def lookInventory():
    print("The following is a list from your inventory\n")
    player1.inventory.getAllArmor()
    player1.inventory.getAllWeapon()
    player1.inventory.getAllConsumable()
    print("What do you want to do? ")
    battleInput2 = input("> ")
    if battleInput2 in ['use consumable', 'equip weapon', 'equip armor']:
        print("It will take your turn and the enemy can attack you!\nAre you sure you want to use this turn to replace inventory?")
        sure = input(">")
        if sure.lower() in ['ok', 'yes']:
            battleInput3 = input("> ")
            if battleInput3.lower() in ['equip weapon', 'weapon']:
              player1.inventory.equipWeapon()
            elif battleInput3.lower() in ['equip armor', 'armor']:
              player1.inventory.equipArmor()
            elif battleInput3.lower() in ['use consumable', 'consumable', 'heal']:
              player1.inventory.useConsumable()

def doHeal():
    print

################
# Battle Phase #
################
def battleLoop(currentEnemy):
  while currentEnemy.hp > 0:
    print("Enemy HP:", currentEnemy.hp)
    print(player1.name, "HP: ", player1.hp)
    print("")
    print("how unlucky you are!", currentEnemy.name, " with ", currentEnemy.hp, " is in front of you!\nWhat do you want to do?")
    battleInput = input("> ")
    acceptable_actions = ['attack', 'shoot', 'inventory', 'view inventory']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
    while battleInput.lower() not in acceptable_actions:
      print("Unknown action command, please try again.\n")
      battleInput = input("> ")
    print("What do you want to do?\n(attack/heal/view inventory)")
    if battleInput.lower() == quitgame:
        sys.exit()
    elif battleInput.lower() in ['attack', 'shoot']:
        pass
    elif battleInput.lower() in ['heal']:
        doHeal()
    elif battleInput.lower() in ['inventory', 'view inventory']:
        lookInventory()
    # currentEnemy.Enemy.auto()

# Check if either or both Players is below zero health
def check_win():
    if player1.hp < 1:
        player1.game_over = True
        print("You Dead")
    elif enemy1.hp < 1 and player1.hp > 0:
        player1.game_over = True
        print("You Win")
    elif player1.hp < 1 and enemy1.hp < 1:
        player1.game_over = True
        print("*** Draw ***")

################
# main looping #
################
def main_game_loop():
    while player1.game_over is False:
      os.system('cls||clear')
      print(f"{player1.name}'s health = {player1.hp}")
      print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
      print("What would you like to do?\n1. Search\n2. View Inventory\n3. Quit game")
      action = input("> ")
      acceptable_actions = ['search', 'look', 'view', 'inventory', 'view inventory', 'inspect', 'quit']
      #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
      while action.lower() not in acceptable_actions:
        print("Unknown action command, please try again.\n")
        action = input("> ")
      print("What do you want to do?\n1. Search\n2. View inventory\n3. Quit")
      if action.lower() == quitgame:
          sys.exit()
      elif action.lower() in ['search', 'look', 'view', 'inspect']:
          value = Search()

          #Make new enemy object based on return on function Search()
          currentEnemy = Enemy(1)

          if value == "get enemy Militia":
            militia = Enemy(1)
            currentEnemy = militia
          elif value == "get enemy Normal Soldier":
            nSoldier = Enemy(2)
            currentEnemy = nSoldier
          elif value == "get enemy Veteran Soldier":
            vSoldier = Enemy(3)
            currentEnemy = vSoldier
          elif value == "get boss":
            boss = Enemy(4)
            currentEnemy = boss
          print("test", currentEnemy.hp)
          battleLoop(player1,currentEnemy)
      
      elif action.lower() in ['inventory', 'view inventory']:
          lookInventory()
      check_win()

################
# Title Screen #
################
def title_screen_options():
  option = input("> ")
  if option.lower() == ("play"):
    menu()
  elif option.lower() == ("quit"):
    sys.exit()
  elif option.lower() == ("help"):
    help_menu()
  while option.lower() not in ['play', 'help', 'quit']:
    print("Invalid command, please try again.")
    option = input("> ")
    if option.lower() == ("play"):
      menu()
    elif option.lower() == ("quit"):
      sys.exit()
    elif option.lower() == ("help"):
      help_menu()

def title_screen():
  os.system('cls||clear')
  a= '''
        |\_______________ (_____\\______________
HH======#H###############H#######################
        ' ~""""""""""""""`##(_))#H\"""""Y########
                          ))    \#H\       `"Y###
                          "      }#H)
  '''
  print(a)
  print('#' * 45)
  print('# Welcome to this text-based shooting game  #')
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
  print("Type a command such as 'search' or 'view inventory'")
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
def menu():
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

  good_adj = ['good', 'great', 'happy', 'aight', 'understanding', 'great', 'alright', 'calm', 'confident', 'not bad', 'courageous', 'peaceful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'easy', 'lucky', 'k', 'comfortable', 'amazed', 'fortunate', 'optimistic', 'pleased', 'free', 'delighted', 'swag', 'encouraged', 'ok', 'overjoyed', 'impulsive', 'clever', 'interested', 'gleeful', 'free', 'surprised', 'satisfied', 'thankful', 'frisky', 'content', 'receptive', 'important', 'animated', 'quiet', 'okay', 'festive', 'spirited', 'certain', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'satisfied', 'wonderful', 'serene', 'glad', 'free', 'and', 'easy', 'cheerful', 'bright', 'sunny', 'blessed', 'merry', 'reassured', 'elated', '1738', 'love', 'interested', 'positive', 'strong', 'loving']
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

  #Leads the player into the warzone now!
  speech2 = "Ok, It seems this is where we must part, " + player1.name + ".\n"
  speech3 = "How unfortunate.\n"  
  speech4 = "Oh, you don't know where you are?  Well...\n"
  speech5 = "How unlucky you are. You are now in the middle of the forest and it seems you are lost.\n"
  speech6 = "Heh. Heh.. Heh...\n"
  for character in speech2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speech3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)
  for character in speech4:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speech5:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speech6:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.2)
  time.sleep(1)
  
  os.system('cls||clear')
  print("################################")
  print("# Here begins the adventure... #")
  print("################################\n")
  print("You find yourself in the center of a strange place.\nSeems like you are trapped in a forest.\n")
  main_game_loop()

title_screen()