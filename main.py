from copyreg import constructor
from email import header
from mimetypes import init
import random
import re
from selectors import SelectorKey
import sys
import os
import time


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




class Damage():
  def __init__(self, head, body, leg) -> None:
    self.headDamage = head
    self.bodyDamage = body
    self.legDamage = leg

  def randomHit(self):
    rand = random.random()

    if rand < 0.2:
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

class Characters:
  def __init__(self, name, defaultHP):
    self.name = name
    self.maxHP = defaultHP
    self.hp = defaultHP
    self.inventory = Inventory()

  def CharacterDetail(self):
    return [self.name, self.hp, self.inventory]

  def heal(self, index):
    self.hp = self.hp + self.inventory.useConsumable(index)
    if self.hp > self.maxHP:
      self.hp = self.maxHP


  def attack(self, enemy):
    equippedWeapon = self.inventory.seeWeaponDetail(self.inventory.equippedWeapon) #Weapon
    type(equippedWeapon)
    damage = equippedWeapon.getDetails()[1] #Weapon Damage

    dmg = damage.randomHit()
    equippedWeapon.shoot()

    enemyArmor = enemy.inventory.seeArmorDetail(enemy.inventory.equippedArmor) #Enemy Armor
    dmgReduc = enemyArmor.getDetails()[2] #Damage Reduction

    finalDmg = dmg - dmg * dmgReduc/100 #Calc Damage

    enemy.hp = enemy.hp - finalDmg


class Player(Characters):
  def __init__(self, name, feeling, defaultHP):
    super().__init__(name, defaultHP)
    self.feeling = feeling
    weapon = Weapon("P250 Pistol")
    self.inventory.addWeapon(weapon)
    self.inventory.equipWeapon(0)

class Enemy(Characters):
  def __init__(self, name, defaultHP, template):
    super().__init__(name, defaultHP)
    if template == 1:
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

player = Player("John", "Good", 1000)
enemy = Enemy("Idiot Thugs", 100, 1)

print(player.CharacterDetail())
print(enemy.CharacterDetail())
player.attack(enemy)

print(player.CharacterDetail())
print(enemy.CharacterDetail())



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
  print("boss", realChanceBoss)
  print("enemy", realChanceEnemy)
  print("armor", realChanceArmor)
  print("weapon", realChanceWeapon)
  print("Healing", realChanceHealing)
  print("------------")
  print(angkaRandom)


  if angkaRandom <= realChanceBoss :
      print("dapet boss")
      ##get.boss
  elif angkaRandom <= realChanceBoss +  realChanceEnemy :
      print("dapet musuh")
      lastEnemyTurn += 1
      ## get.enemy
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon :
      print("dapet weapon")
      ## get.weapon
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon +realChanceArmor :
      print("dapet armor")
      ## get.armor
  else :
      print("dapet heal")
      ## get.heal


    

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
  a= '''
  ⡿⣽⣳⡽⢮⣟⣿⣿⠃⠀⢬⣻⣽⢣⡄⡀⠀⠀⠀⠀⠀⠀⠀⠼⣯⢿⡽⣯⢿⡽⢯⡶⣥⢆⡦⣄⡀⠀⠀⢢⢑⢮⡹⢯⢿⡽⣯⢿⡽⣯⢿⢯⡿⢯⡿⣽⢯⡿⣽⢯⡿⣽⠿⣽⢿
  ⣟⡷⣯⣟⡿⣽⣿⡃⠁⢈⢶⣻⣞⣯⢷⣹⣆⠤⡀⠄⠀⠀⠀⢻⣞⡿⣽⣻⢯⣿⣻⡽⣯⣻⢷⣛⣾⣏⣷⢢⣎⣳⣻⢯⣻⣻⡽⣯⣟⣯⣟⡿⣽⣟⡿⣽⣻⡽⣯⣟⣻⣽⣻⣯⢿
  ⣽⣛⣷⢯⣟⣿⡷⠀⢠⣙⣾⣳⣟⡾⣯⢷⣾⣻⡵⣊⣶⣠⢆⡱⡏⣟⣷⣿⣻⢾⣷⣻⣷⣻⢯⣟⣾⣳⢯⣷⣻⣖⣯⣟⣷⣻⣽⣳⣟⣾⣽⣻⢷⣯⣟⡷⣏⣿⣳⣟⣻⣾⣳⣯⢿
  ⢷⣯⣟⡿⣾⡿⠁⠀⢦⣻⣞⡷⣯⣻⣽⣻⣞⣷⣻⡟⣗⣫⢹⣾⠡⡠⠄⡤⢀⠎⣁⠙⠚⠫⠿⣾⣳⣟⡿⣞⣷⣻⢾⡽⣞⣷⣳⣟⣾⣳⣯⣟⡿⣞⣷⣻⣛⣾⣳⣟⡷⣯⣷⣻⢿
  ⣟⣾⡽⣿⣿⠁⢀⡙⣾⣳⣯⣟⣷⣻⣞⡷⣟⡞⢙⣮⡯⡂⣿⡟⠑⠁⢊⠔⡌⢢⠡⠋⡜⠠⠄⡀⠙⢽⣻⣽⣾⣻⢯⣟⡿⣞⣷⣻⣞⣷⣻⣾⣻⣽⣞⣷⣻⣞⡷⣯⣟⣷⣯⣟⣿
  ⣻⣞⣿⣿⠇⠈⢤⣻⣽⣳⣟⣾⣳⣟⡾⠟⡡⢔⠫⠤⣾⣇⣿⡇⠀⣵⠪⣴⠡⢆⡉⡔⠠⠃⡠⠐⢃⠂⠌⢻⣾⣽⡿⣽⣻⣽⣞⡷⣟⣾⣯⣷⢿⣳⢿⣞⡷⣯⢿⣳⣯⢿⡾⣽⣾
  ⣷⣿⣿⡏⠀⢸⡜⣷⣯⣟⣾⣳⡿⣞⣣⠔⡐⢎⠡⢊⢹⡿⣿⠇⠘⣡⠞⠍⢔⣷⣨⠂⢬⡑⢤⢋⡄⢪⠄⠃⠹⣷⣿⢿⣽⢷⣯⡿⣿⡽⣷⢿⣻⣯⢿⣯⢿⣿⣻⣽⢿⣿⢿⣿⣽
  ⣿⣿⠏⠀⢌⢶⡿⣽⡾⣽⣾⣿⣹⡙⠁⠐⡈⣂⠘⠤⢸⡇⣿⠀⠁⢀⠈⠌⠋⡐⠓⠐⡃⣧⠘⡛⠖⠊⠰⠠⢁⠸⣿⣿⣯⣿⣯⣿⢿⣿⢿⣿⣯⣿⣿⣽⣿⣽⣿⣽⣿⡿⣿⣯⣿
  ⣿⠏⠀⠐⣮⣿⢿⣿⣽⣿⣿⢒⡏⢀⣱⣰⡾⣽⡮⠐⣸⢹⡓⠀⠀⠂⠀⡐⠠⠐⠠⢁⠂⠠⠈⠄⢃⠀⡁⠁⠂⠀⢹⣿⣿⣽⣿⣻⣿⣿⣿⣿⣽⣿⣾⣿⣟⣯⣿⣿⣻⣿⣿⣟⣿
  ⠛⡀⠠⣝⣯⣿⣿⣿⣻⣽⡞⢌⠂⠸⣿⡜⣾⡫⢚⣽⠇⡿⠁⠀⠀⠀⠐⠀⠀⠐⠁⠀⠌⠀⠐⡈⠀⠄⠀⠀⠀⠀⠘⣿⣿⣿⢿⣿⣿⣽⣾⣿⣿⣟⣿⣽⣿⣿⣿⣿⣿⣿⣽⣿⣿
  ⠀⢀⣳⣿⣿⣿⣯⣿⣿⣿⡇⢌⠀⠠⣪⡬⠊⣗⢾⡀⡾⡃⢀⠀⠀⡄⠀⠀⠀⣧⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿
  ⠀⣮⣿⣿⣿⣿⣿⣿⣿⣿⣧⠐⡐⢗⡗⠪⡹⠎⠃⠁⠻⠿⠟⠀⣸⠁⢰⡄⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠂⠱⠗⠨⠵⠀⠄⠀⠠⠀⠀⣸⡟⠀⣚⢃⢸⣛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⣸⡇⠀⢈⠌⡙⠀⠀⠀⡟⠃⠈⠋⠉⠈⠹⠃⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⡟⠇⠃⣹⣿⣿⣿⠇⡐⠀⠀⣿⡇⠀⢸⡞⠀⠀⢦⠀⣧⠀⠀⠀⢀⠀⠀⣄⡀⡿⣷⣾⣿⡏⠀⠀⡤⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣛⠟⡠⠘⢆⠣⡸⢿⡿⣿⠠⠐⠠⠀⣿⣷⠀⠘⡧⠂⠀⢼⣄⣻⢸⠘⣦⣤⣧⣼⣿⣿⣷⣿⣿⣿⣇⣔⣼⠳⠀⠀⠀⠀⠀⠀⠀⠀⠸⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⢬⡳⣔⠈⠠⠁⠄⠃⠜⠡⢀⠡⢀⢹⢹⡯⠀⠀⠈⠸⠼⠚⣿⣿⣞⡔⣿⣯⣿⣿⣿⣿⣿⣿⣿⣟⡯⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⠀⠡⡙⢦⡡⢉⠔⡈⣠⠀⠂⠀⠄⢸⢸⡇⠀⠀⠀⠀⠀⠀⢘⢿⣷⣽⣮⣛⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡿⠀⠀⠘⠀⠀⠀⠀⠀⠠⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⠀⣁⠚⠣⠁⠌⢢⡵⡇⠀⢸⠀⠈⠸⢘⠆⠀⠀⠠⠀⠀⠀⢰⢷⡽⡿⣾⣿⣾⣿⣿⣿⣿⣿⣉⣽⣿⠟⠁⠀⡀⠀⠃⠀⠀⠀⠀⠀⢦⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⠀⠀⢄⠂⠄⠀⠱⡘⠇⠀⢸⠀⠀⠀⠘⠒⠀⠀⠀⠀⠀⠀⠸⣎⣿⣽⣷⣯⣛⡿⣿⣿⣿⣿⣿⡟⠅⠀⠀⠀⠰⡄⠀⠀⠀⠀⠀⠀⠘⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⠀⣩⣾⡁⠂⠈⡐⠡⠈⠀⠈⠆⠠⠀⠀⠈⡄⠀⠀⠀⢄⠀⢨⢽⣿⣽⣞⣿⣿⣿⣟⠈⠉⠛⠋⠀⠈⠀⢀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⢠⡾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣰⣿⣿⢆⡁⠂⢀⢷⡀⠐⣀⠈⠱⣄⠀⠀⠘⠄⠀⠀⢈⣽⡌⣿⣿⣿⣼⣿⢿⣿⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⡟⢣⡄⠁⣀⢻⡄⠠⣼⣷⣄⣀⠁⠀⠀⠀⢀⢴⣿⣿⣧⠘⣿⣿⣿⣿⣯⣿⣿⣸⠁⣀⢀⠠⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠿⢛⣉⣉⡙⠛⣿⣿⣿⣿⣿⣿
  ⣿⠧⡑⠬⣙⠤⢸⣿⣿⣇⣾⣿⣿⣿⣿⣶⣢⣾⣿⣧⡩⠻⣿⠠⠹⣿⣿⣿⣿⢷⡻⡇⢧⣳⡿⣅⢠⠐⣆⡀⢀⣀⠀⠀⠀⠀⠀⠀⠠⣀⠰⡄⠀⠘⠉⠁⠠⡓⠈⠀⣻⣿⣿⣿⣿
  ⠋⢅⡰⣧⣝⡆⡌⢙⡉⢘⠿⢻⣿⢟⣿⣿⣿⣿⣿⣿⣷⢢⣿⣶⡄⢿⣿⣿⣿⣷⣽⣮⣞⡿⣼⢝⡜⠀⢢⡙⠷⣖⡀⠀⠀⡀⣀⠀⢡⠂⠼⢣⢀⠃⠜⡆⠀⣀⣤⣾⣿⢿⣿⣿⣿
  ⠀⠀⠀⠙⠎⢿⡘⠄⠐⠈⠂⠁⣴⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⡗⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⢠⡠⠙⠦⡍⠢⡀⠱⠘⢦⣡⣀⢉⠲⢛⠀⡈⠠⠁⠾⠟⣛⣭⣾⢏⡿⣿⣿
  ⠀⠀⠀⠀⠈⢠⢺⣴⣦⣧⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣪⣌⡂⢌⠳⣄⠲⢄⠀⠈⠈⠃⠀⠫⠀⡅⢀⣴⣶⠿⡛⣫⣽⣿⣳⢿⢿
  ⠀⠀⠠⢄⣻⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⣿⢸⣤⠈⢻⡀⠈⠳⢶⠆⠀⠀⠄⠀⣻⣽⡶⡿⣟⣋⡱⡯⢺⣟⣽
  ⣤⣐⣐⢢⡈⢽⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠈⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⡿⣾⡯⡷⠀⡆⣇⠀⠀⠀⠂⠀⠀⠀⣀⣩⣷⣿⣿⡿⡟⢁⡾⣯⢽⢻
  ⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⡆⠘⠻⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣷⣚⣵⣿⠀⠀⠀⠀⢡⣤⣶⣿⣿⣿⣷⣵⡿⡿⢸⣧⡙⣌⠣
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣿⠁⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣏⢻⣿⣿⣿⣿⣿⣿⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣵⢾⡷⢣⠵⣈⢧
  ⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⠿⣛⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢺⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣧⢭⣻⣿⣿⣿⣿⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣯⣴⣿⣧⡿⣟⡾
  ⠉⠡⠉⠌⢡⡐⣤⣲⣴⣧⣞⣴⣥⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡔⡽⣿⣿⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣇⢞⣝⢿⣿⡏⠀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠗⣵⣪⣔
  ⢠⡁⡌⡘⢳⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡹⣽⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⢘⣎⢯⠛⣠⣾⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠀⠀⠀⢀⣽⣟⣷⣿
  ⣾⣿⣿⣷⡅⠊⠍⠛⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢫⣎⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠘⣿⣿⠏⡼⢪⣤⣾⣿⣿⣿⣿⣿⢟⣽⣶⡇⠀⠀⠀⠀⠀⠀⠈⢹⣿⣾⣻
  ⢿⡛⣏⣱⣌⣖⣌⣰⣠⢌⠛⡹⢻⢟⡋⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡻⢏⡴⣎⣏⣿⣿⣿⣿⣿⠟⣱⣿⣿⣿⣷⡤⠀⠈⠄⠀⡀⡄⠀⣻⣷⣿
  ⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣞⣯⢷⡽⢿⣿⣿⣿⢟⢑⣿⣿⣿⣿⣿⡟⠀⠀⠄⠂⠰⠀⡇⠀⣽⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⡀⠀⠀⠀⠀⣀⣴⣾⢻⡾⣽⢞⡯⣞⣾⣿⣿⡱⣻⣿⣿⣿⣿⣿⣿⡇⠘⠀⢀⠠⠈⣰⠁⢠⣿⣟⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡝⢇⣫⡶⣟⣯⢷⢯⡿⣹⠽⣎⢷⣹⡿⡫⣢⣾⣿⣿⣿⣿⣿⣿⣿⣇⠀⠋⡄⠀⡜⠀⢠⣿⣿⣿⣽
  ⢋⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣴⣻⣿⣿⣿⣿⣿⣿⣿⡿⣹⣿⣿⣿⣷⣽⡿⣫⠷⣭⣛⡼⢯⢩⣼⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠀⠁⠀⠀⠀⠄⢼⣿⣿⣿
  ⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⡾⣧⠟⣡⢷⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢀⠁⠀⠠⡈⠄⠂⢸⣿⣿⣿
  ⠐⠈⡙⠛⠿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⡱⣎⣵⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⠀⠠⡱⠀⠀⠐⣼⣿⣿⣿
  ⢀⢡⣰⣬⣤⣱⣤⡛⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣏⣾⣟⡞⡶⣽⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡀⠘⡀⡜⠁⠀⠀⣾⣿⣿⣿⣿
  ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠻⣿⣿⣿⣿⣿⢿⢫⢯⠓⢱⣿⣯⡟⡼⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠆⠀⠀⠀⢹⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⡟⢻⢹⢻⣦⣿⣾⠀⣿⣿⣿⡼⣱⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠐⠀⢸⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⣧⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣌⣿⣿⣿⣿⣿⣿⣏⣧⣿⣿⣏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⡀⠀⠀⢠⠁⠀⣼⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⢿⣾⣿⣿⣿⣮⣾⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⢿⡽⣺⣿⡯⣺⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠡⢀⠃⠀⠸⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⡏⣛⣛⠛⠋⠛⠻⠿⣿⣾⣽⣻⢟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢫⣞⣿⣿⡾⠏⣠⢝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣾⡟⠡⠂⡄⠳⠘⣶⣦⣬⣉⠛⠿⣾⣧⣟⣽⣻⢿⣿⣿⣿⣿⣿⣿⣿⡿⢏⡳⣺⠿⠋⣡⣾⢿⣇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠐⡀⠀⠀⠠⠀⢸⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣟⣾⣿⣿⣷⢸⡇⣷⣿⣿⣿⣿⣿⣿⠶⠤⠉⠙⠛⠢⠻⠿⠿⠿⠿⠿⠿⠿⠟⠑⠙⢁⡤⣚⣭⣶⣾⣿⡆⢹⣿⣿⣿⣿⣿⣿⣿⣿⣀⠀⡀⠀⠠⠁⢀⣾⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⠸⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣦⣤⣤⣀⣀⠀⠀⠀⠀⣀⡵⣞⡿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠀⠀⡁⠀⠈⢿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣧⣿⣿⣿⣿⡿⢠⣿⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣥⣿⣜⣻⡽⢿⣷⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⢸⣞⣿⡿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣯⣟⣓⢯⢟⣿⢿⣿⢟⣿⣷⠀⠀⠀⠀⠀⠀⣿⢯⣾⢍⣿
  ⣿⣿⣿⣻⡟⣿⣿⣿⣿⡇⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣞⢯⢎⡭⢞⣟⢂⠀⠀⢀⠀⠐⢿⣑⡿⣻⣯
  ⣿⣿⢾⣽⣗⢿⣿⣿⣿⣇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢚⣯⢌⣥⠀⠀⠀⠀⠀⢸⣾⣷⣾⣟
  ⣿⣿⣿⣾⣯⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⠶⢢⡶⣃⡀⠀⠀⠀⣸⡿⣻⣷⣿
  ⣿⡯⣯⣾⡷⠦⠞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣟⡵⣟⣍⠀⠀⠀⠀⠰⣾⣿⣿⣿
  ⣿⣿⣷⣿⣻⢷⣋⣛⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⢚⢫⢂⠀⠀⠀⠀⢰⣿⣿⣿⣿
  ⣿⣿⣷⣯⣟⡿⣶⣯⣍⡭⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣵⣾⣧⡀⠀⠀⣾⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣷⣿⣽⣛⡮⢌⢫⢛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠟⢍⡦⠈⠀⠁⢩⣻⣿⣿⣿
  ⣿⣿⣟⣻⣛⣻⣿⣿⣿⣿⣿⣿⣷⣾⣮⣴⣭⣙⣛⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢀⣈⠈⠀⠀⠀⠈⠃⣸⣿⣿
  '''
  print(a)
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