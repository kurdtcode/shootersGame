from copyreg import constructor
from email import header
from mimetypes import init
import random
import re
from selectors import SelectorKey
import sys
import os
from this import s
import time
screen_width = 100

class Items():
  def __init__(self, name, durability: int):
    self.name = name
    self.durability = durability

  def getDetails(self) -> list:
    return [self.name, self.durability]

  def reduceDurability(self, durabilityLost: int):
    self.durability -= durabilityLost

class Armor(Items):
  def __init__(self, name = '', type = ''):
    super().__init__(name, 0)

    #Select type
    x = random.randint(0,100)
    if name == '' and type == '':
      if x < 10:
        type = "Heavy"
        name = "Heavy Armor"
      elif x < 30:
        type = "Medium"
        name = "Medium Armor"
      elif x < 60:
        type = "Basic"
        name = "Basic Armor"
      else:
        type = "Light"
        name = "Light Armor"

    self.type = type
    self.name = name
    if type == "No Armor":
      self.durability = 10000
      self.damageReduction = 0
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
  def __init__(self, name = ""):

    x = random.randint(0,100)
    if name == "":
      if x < 75:
        name = "Bandage"
      else:
        name = "Medkit"

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
  def __init__(self, name = ""):

    x = random.randint(0,100)
    if name == "":
      if x < 10:
        name = "AWM Sniper Rifle"
      elif x < 20:
        name = "M4A1 Rifle"
      elif x < 60:
        name = "Deagle Pistol"
      else:
        name = "P250 Pistol"

    super().__init__(name, 0)
    self.bullet = 0
    self.maxBullet = 0
    self.damage = Damage(0, 0, 0)
    #self.reloadTime = 0
    self.bulletPerAttack = 0
    if name == "Punch":
      self.maxBullet = 1
      self.damage = Damage(10, 8, 5)
      #self.reloadTime = 2
      self.durability = 10000
      self.bulletPerAttack = 0
    elif name == "P250 Pistol":
      self.maxBullet = 12
      self.image = '''
      ⣿⣿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⢿⣿⣿⣿⣿
      ⠟⠛⢛⠚⡛⢛⠛⡓⡛⡛⢛⢷⢿⢿⠻⡓⡛⡛⡛⡓⢛⡛⡛⢓⠛⡉⡙⣷⣿⣿
      ⠨⢈⢐⠐⡈⡐⡈⠄⡂⡈⡂⡂⡂⠅⠪⡐⠡⢊⢐⠌⠔⡐⡐⡡⢈⠰⠠⢹⣿⣿
      ⣦⠁⢂⠃⡒⢂⢊⠒⠢⢑⠐⠨⠠⡁⠅⠨⠈⡐⠠⠨⠠⠁⡀⢂⢐⢈⠨⠐⢿⣿
      ⣿⡀⠄⢀⠄⠄⡀⠠⠈⠄⡈⠠⠑⠠⢐⠄⠅⡂⠅⡡⠡⠄⠄⠠⠐⡀⢂⠁⠈⣹
      ⣿⣷⣶⣶⣶⣶⣷⣾⣶⣶⠄⣴⣾⣶⣶⠐⣠⣶⡄⢀⠠⠄⠂⡁⠌⡐⢀⣾⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡔⢹⣿⣟⢋⣢⣿⡿⠃⠄⠄⠌⠠⡀⠢⢊⠸⣿⣿⣿
      ⣿⣿⣿⣯⣿⣷⣿⣿⣿⣿⣧⣴⣤⣦⣦⣦⣤⣶⣶⡁⠈⡀⠡⠄⠌⢀⠂⢿⣿⣿
      ⣿⣿⣯⣿⣿⣻⣿⣽⣿⣾⣿⣿⣿⣿⢿⣿⣿⣿⣿⣧⠄⠐⡀⠡⠐⢀⠊⠌⣿⣿
      ⣿⣿⣿⣟⣿⣿⡿⣿⣟⣿⣯⣷⣿⣿⣿⣿⣯⣿⣟⣿⠄⠠⠐⠄⠌⠄⠄⠡⢹⣿
      ⣿⣿⣟⣿⣿⣻⣿⣿⣿⣿⢿⣿⣿⣯⣷⣿⣿⢿⣿⣿⡇⠄⠂⢁⠠⠁⠄⠁⢜⣿
      ⣿⣿⣿⡿⣿⣿⢿⣿⣾⣿⣿⣿⣷⣿⣿⣿⢿⣿⣿⣻⣧⠄⠨⠠⠠⠂⠨⠐⢀⣿
      ⣿⣿⡿⣿⣿⣿⣿⣿⣻⣽⣿⣾⣿⣟⣿⣾⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
      self.damage = Damage(20, 15, 10)
      #self.reloadTime = 2
      self.durability = 50
      self.bulletPerAttack = 3

    elif name == "Deagle Pistol":
      self.maxBullet = 8
      self.image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⠇⡍⡿⢻⠿⠿⠿⡿⠿⢿⠿⠿⡿⢿⠿⡿⢟⠿⣟⠿⡟⡿⢿⡻⡿⠿⡿⡿⣿⡩⢸⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⡝⡝⡄⡇⣫⡩⣕⡱⡩⡊⡎⠕⢅⠣⡑⠏⠎⠎⠦⠣⢕⢽⠸⡜⢼⢩⢎⡂⡅⢊⠨⢫⢏⠩⣸⣿⣿⣿
      ⣿⣿⡮⣪⢪⢪⡣⡣⡣⡪⡪⡪⡪⢝⢜⢜⢬⢣⢫⢪⢪⢪⢪⢪⢪⢭⢣⢏⢮⢪⢎⢖⢆⢗⢵⢲⣿⣿⣿⣿
      ⣿⣿⣿⣮⡮⡳⢵⢹⢜⠵⢝⢝⠮⡳⢝⠵⢝⢮⡺⡸⣘⢎⢮⢪⠪⠊⠎⢊⠊⢪⠪⡓⢭⢳⡹⣪⢯⢟⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⣼⣿⣿⣿⢨⡏⡏⢀⠉⡁⢔⢂⢫⢎⣾⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣿⣧⣾⠫⣢⠂⡁⡂⡂⠅⠘⢺⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡺⡀⠄⠐⠠⠈⠢⠈⣻⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠣⢈⠄⡁⠌⢈⢂⠈⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢯⠂⠔⡀⡊⡐⠄⡃⠸⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢕⠇⠁⠂⠐⠄⠅⠂⡈⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣍⣋⣋⣋⣋⣋⣋⣯⣾⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
      self.damage = Damage(40, 30, 20)
      #self.reloadTime = 2
      self.durability = 50
      self.bulletPerAttack = 2

    elif name == "M4A1 Rifle":
      self.maxBullet = 50
      self.image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⡿⣿⣿⣿⣿⣿⣿⣿⢿⠿⢿⣿⣿
      ⣿⣿⣿⡿⡿⢿⠿⣿⣿⢿⠿⠿⠿⣿⠿⡿⠿⠛⡛⠛⠋⡍⠍⡍⢍⢌⢔⢀⠑⠍⠩⢑⠨⢐⠐⢄⢑⡐⢼⣿
      ⣿⣿⢿⠓⠐⢁⠒⡐⠄⢅⠡⡁⠔⠠⡨⠐⢐⢐⢈⠰⡉⠌⢌⢐⠔⡐⡐⡐⡡⣥⣄⢢⠡⠅⢍⠢⢁⠈⢼⣿
      ⣿⣤⣤⣥⣈⣂⣅⣴⣤⣥⣴⣤⣤⣵⣶⣷⣶⣿⣿⣇⠢⢑⠡⢢⣵⢌⢂⢔⠸⣿⣿⣿⣾⣷⣥⣮⣔⠄⣹⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⡅⠕⢈⣾⣿⣶⣧⠂⢅⠻⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢗⠐⠅⡂⣿⣿⣿⣿⡌⢔⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣊⠰⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
      self.damage = Damage(75, 50, 40)
      #self.reloadTime = 3
      self.durability = 75
      self.bulletPerAttack = 5

    elif name == "AWM Sniper Rifle":
      self.maxBullet = 5
      self.image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡿⠿⠛⠋⠙⣿⣿⣿⡿⠿⠿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠿⠛⠛⠉⠄⠄⠄⠠⠤⣶⣾⠏⠉⠄⠄⠄⠄⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠄⣀⠄⠐⠄⠄⠄⠄⠄⠄⠁⡀⠄⠄⠄⠄⠄⢠⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢛⠩⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⠁⢀⣴⣿⣶⣾⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⢋⠉⠐⠄⠁⠄⠄⣀⣤⣤⣤⢀⣀⣠⣼⣶⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡛⠫⣁⣠⣴⣶⣿⣿⣄⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢟⠛⢍⣑⣤⣼⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⡿⠟⠛⠋⠩⣀⣢⣬⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣯⣰⣤⣦⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
      self.damage = Damage(150, 100, 80)
      #self.reloadTime = 5
      self.durability = 100
      self.bulletPerAttack = 1

    self.reload()

  def getDetails(self) -> list:
    return [self.name, self.damage, self.maxBullet, self.bullet, self.image]

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
    self.hp = self.hp + self.inventory.useConsumable(index).getDetails()[1]
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
    enemyArmor.reduceDurability(dmg * dmgReduc/100)

################
# Player Setup #
################
class Player(Characters):
  def __init__(self):
    super().__init__(200)
    self.feeling = ""
    weapon = Weapon("P250 Pistol")
    self.inventory.addWeapon(weapon)
    self.inventory.equipWeapon(0)
    armor = Armor("No Armor", "No Armor")
    self.inventory.addArmor(armor)
    self.inventory.equipArmor(0)
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

  def currentEnemyAuto(self, player):
    #Initial Value/Known Value
    #self.hp
    #self.inventory.seeEquippedWeapon()
    #self.inventory.seeEquippedArmor()
    selfDmg = self.inventory.seeEquippedWeapon().getDetails()[1].bodyDamage
    selfDmgReduc = self.inventory.seeEquippedArmor().getDetails()[2]

    playerHP = player.hp
    self.inventory.seeEquippedWeapon()
    playerWeapon = player.inventory.seeEquippedWeapon()
    playerArmor = player.inventory.seeEquippedArmor()

    playerDmg = playerWeapon.getDetails()[1].bodyDamage
    playerDmgReduc = playerArmor.getDetails()[2]

    #Condition Value Init 2
    selfFinalDamage = selfDmg - selfDmg * playerDmgReduc/100
    playerFinalDamage = playerDmg - playerDmg * selfDmgReduc/100


    #Condition Value Init 3
    selfOneHit = False
    playerOneHit = False

    #Condition Value Init 4
    selfConsumableExist = False
    # playerConsumableExist = False

    #Condition Value Init 5
    medkitCount = 0
    medkitIndex = -1
    bandageCount = 0
    bandageIndex = -1
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
    selfHealMedkit = False
    selfHealBandage = False
    
    #Condition 1
    if self.hp - playerFinalDamage <= 0:
      selfOneHit = True
    if player.hp - selfFinalDamage <= 0:
      playerOneHit = True

    #Condition 2
    if len(self.inventory.getAllConsumable()) != 0:
      selfConsumableExist = True
    # if len(player.inventory.getAllConsumable()) != 0:
    #   playerConsumableExist = Trueh
    
    
    #Condition 3
    temp = self.inventory.getAllConsumable()
    for i in range(len(self.inventory.getAllConsumable())):
      if temp[i].getDetails()[1] == 50:
        medkitCount += 1
        medkitIndex = i
      else:
        bandageCount += 1
        bandageIndex = i

    if medkitCount > 0:
      medkitExist = True
    if bandageCount > 0:
      bandageExist = True
    if self.hp + 50 > self.maxHP:
      medkitHealExceedMax = True

    #Condition 4
    if self.hp > 70:
      selfHighHealth = True
    elif self.hp > 30:
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
    if selfConsumableExist:
      if playerOneHit:
        selfAttack = True
      elif selfOneHit:
        selfHeal = True
      else:
        if selfHighHealth:
          selfAttack = True
        elif selfMediumHealth and playerHighHealth:
          rands = random.random()
          if rands > 0.25:
            selfHeal = True
          else:
            selfAttack = True
        elif selfMediumHealth and playerMediumHealth:
          rands = random.random()
          if rands > 0.5:
            selfHeal = True
          else:
            selfAttack = True
        elif selfMediumHealth and playerLowHealth:
          rands = random.random()
          if rands > 0.8:
            selfHeal = True
          else:
            selfAttack = True
        
        elif selfLowHealth and playerHighHealth:
          rands = random.random()
          if rands > 0.2:
            selfHeal = True
          else:
            selfAttack = True

        elif selfLowHealth and playerMediumHealth:
          rands = random.random()
          if rands > 0.7:
            selfHeal = True
          else:
            selfAttack = True

        elif selfLowHealth and playerLowHealth:
          rands = random.random()
          if rands > 0.5:
            selfHeal = True
          else:
            selfAttack = True
    else:
      selfAttack = True

    if selfAttack == True:
      pass

    if selfHeal == True:
      if medkitHealExceedMax:
        if bandageExist:
          selfHealBandage = True
        else:
          selfHealMedkit = True
      else:
        if medkitExist:
          selfHealMedkit = True
        else:
          selfHealBandage = True
    
    if selfHealBandage:
      self.heal(bandageIndex)
      return "healBandage"
      
    
    if selfHealMedkit:
      self.heal(medkitIndex)
      return "healMedkit"
    
    if selfAttack:
      self.attack(player)
      return "attack"

#declare object enemy
enemy = Enemy(1)
turn = 0
def Search():
  global turn
  print('turn, ', turn)
  playerHealth=player1.hp
  ##rumus masih agak ngaco soalnya semakin banyak turn nya chance dapet enemy nya semakin turun, weapon sm armor nya naik
  chanceFindBoss  = max(((turn - 10) * 0.2) + (100 * 0.005),0)
  chanceFindEnemy = (turn * 0.7) + (100 * 0.05)
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
  turn+=1
  if angkaRandom <= realChanceBoss :
      return "get enemy Special Force Soldier"
  elif angkaRandom <= realChanceBoss +  realChanceEnemy :
      if turn >= 0 and turn <= 3:
          randomGear = random.randint(1,2)
          if randomGear == 1 :
              return "get weapon"
          else:
              return "get armor"
      elif turn > 3 and turn <= 6 :
          return "get enemy Militia"
      elif turn > 6 and turn <= 9 :
          return "get enemy Normal Soldier"
      elif turn > 9 and turn <=12 :
          return "get enemy Veteran Soldier"
      else :
          return "get enemy Special Force Soldier"
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon :
      return "get weapon"
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon +realChanceArmor :
      return "get armor"
  else :
      return "get heal"

##################################### kd ##################################

##################
# look inventory #
# (use invetory) #
##################
def lookInventory():
  changeSomething = False
  while(True):
    print("The following is a list from your inventory\n(View Weapon/View Armor/View Consumables/Back)")
    intp = input("> ").lower()
    while intp not in ['view weapon', 'view armor', 'view consumables', 'back']:
      print("Unknown action command, please try again.\n")
      intp = input("> ").lower()

    if intp == 'view weapon':
      weapon = player1.inventory.getAllWeapon()
      for i in range (len(weapon)):
        print("Weapon ",i,":", weapon[i].getDetails()[0])
        print("Head Damage : ", weapon[i].getDetails()[1].headDamage)
        print("Body Damage : ", weapon[i].getDetails()[1].bodyDamage)
        print("Leg Damage : ", weapon[i].getDetails()[1].legDamage)
        print("Bullet : ", weapon[i].getDetails()[2])
      
      print("What do you want to do? ")
      intp2 = input("> ")
      if intp2 in ['equip weapon', 'back']:
        if intp2 == 'equip weapon':
          print("Which weapon do you want to equip? (numbers)")
          intp2 = int(input("> "))
          player1.inventory.equipWeapon(intp2)
          changeSomething = True
        elif intp2 == 'back':
          continue
        

    elif intp == 'view armor':
      armors = player1.inventory.getAllArmor()
      for i in range (len(armors)):
        print("Armor : ", armors[i].getDetails()[0])
        print("Durability : ", armors[i].getDetails()[1])
        print("Damage Reduction : ", armors[i].getDetails()[2])
        print("What do you want to do? ")
      intp2 = input("> ")
      if intp2 in ['equip armor', 'back']:
        if intp2 == 'equip armor':
          print("Which armor do you want to equip? (numbers)")
          intp2 = int(input("> "))
          player1.inventory.equipArmor(intp2)
          changeSomething = True
        elif intp2 == 'back':
          continue

    elif intp == 'view consumables':
      consumable = player1.inventory.getAllConsumable()
      for i in range (len(consumable)):
        print("Item : ", consumable[i].getDetails()[0])
        print("Heal Amount : ", consumable[i].getDetails()[1])
      print("What do you want to do? ")
      intp2 = input("> ")
      if intp2 in ['use consumables', 'back']:
        if intp2 == 'use consumables':
          print("Which consumables do you want to use? (numbers)")
          intp2 = int(input("> "))
          player1.heal(intp2)
          changeSomething = True
        elif intp2 == 'back':
          continue
    
    elif intp == 'back':
      break
  if changeSomething == True:
    return True
  else:
    return False

################
# Battle Phase #
################
def battleLoop(currentEnemy:Enemy):
  print("Oh no! There is ", currentEnemy.name ,"(",currentEnemy.hp," HP) in front of you!")
  while currentEnemy.hp > 0:
    print(player1.name, "'s Health: " , player1.hp)
    print(currentEnemy.name, "'s Health: " , currentEnemy.hp)

    print("What do you want to do?\n(attack/heal/view inventory)")
    battleInput = input("> ")
    acceptable_actions = ['attack', 'shoot', 'inventory', 'view inventory']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
    while battleInput.lower() not in acceptable_actions:
      print("Unknown action command, please try again.\n")
      battleInput = input("> ")
    print("What do you want to do?\n(attack/heal/view inventory)")
    change = True
    if battleInput.lower() == quitgame:
        sys.exit()
    elif battleInput.lower() in ['attack', 'shoot']:
        player1.attack(currentEnemy)
    elif battleInput.lower() in ['heal']:
        consumable = player1.inventory.getAllConsumable()
        for i in range (len(consumable)):
          print("Item : ", consumable[i].getDetails()[0])
          print("Heal Amount : ", consumable[i].getDetails()[1])
        print("What do you want to do? ")
        intp2 = input("> ")
        if intp2 in ['use consumables', 'heal', 'back']:
          if intp2 in ['use consumables', 'heal']:
            print("Which consumables do you want to use? (numbers)")
            intp2 = int(input("> "))
            player1.heal(intp2)
            changeSomething = True
          elif intp2 == 'back':
            change = False
    elif battleInput.lower() in ['inventory', 'view inventory']:
        change = lookInventory()
    os.system('cls||clear')

    if change:
      move = currentEnemy.currentEnemyAuto(player1)
      if move == "attack":
        print("Enemy Is Attacking")
      elif move == "healMedkit":
        print("Enemy used a medkit")
      elif move == "healBandage":
        print("Enemy used a bandage")

# Check if either or both Players is below zero health
def check_win():
    if player1.hp < 1:
        player1.game_over = True
        print("You Dead")
    elif enemy.hp < 1 and player1.hp > 0:
        player1.game_over = True
        print("You Win")
    elif player1.hp < 1 and enemy.hp < 1:
        player1.game_over = True
        print("*** Draw ***")

################
# main looping #
################
def main_game_loop():
    global enemy
    os.system('cls||clear')
    print("################################")
    print("# Here begins the adventure... #")
    print("################################\n")
    print("You find yourself in the center of a strange place.\nSeems like you are trapped in a forest.\n")
    time.sleep(1)
    while player1.game_over is False:
      os.system('cls||clear')
      print(f"{player1.name}'s health = {player1.hp}")
      print("\n=========================")
      print("What would you like to do?\n1. Search\n2. View Inventory\n3. Quit game")
      action = input("> ")
      acceptable_actions = ['search', 'look', 'view', 'inventory', 'view inventory', 'inspect', 'quit']
      #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
      while action.lower() not in acceptable_actions:
        print("Unknown action command, please try again.\n")
        action = input("> ")
      if action.lower() == quitgame:
          sys.exit()
      elif action.lower() in ['search', 'look', 'view', 'inspect']:
          value = Search()
          print('value = ', value)
          #Make new enemy object based on return on function Search()
          # currentEnemy = Enemy(1)

          if value == "get enemy Militia":
            militia = Enemy(1)
            enemy = militia
            battleLoop(enemy)
          elif value == "get enemy Normal Soldier":
            nSoldier = Enemy(2)
            enemy = nSoldier
            battleLoop(enemy)
          elif value == "get enemy Veteran Soldier":
            vSoldier = Enemy(3)
            enemy = vSoldier
            battleLoop(enemy)
          elif value == "get enemy Special Force Soldier":
            boss = Enemy(4)
            enemy = boss
            battleLoop(enemy)
          elif value == "get armor":
            print("Congratulation! You found an armor!")
            armor = Armor()
            player1.inventory.addArmor(armor)
            print("Armor : ", armor.getDetails()[0])
            print("Durability : ", armor.getDetails()[1])
            print("Damage Reduction : ", armor.getDetails()[2])
            tanya = input("Equip Armor? (yes/no)")
            if tanya.lower() == 'yes':
              player1.inventory.equipArmor(len(player1.inventory.armor)-1)
            else:
              continue
          elif value == "get weapon":
            print("Congratulation! You found a weapon!")
            weapon = Weapon()
            player1.inventory.addWeapon(weapon)
            print("Weapon : ", weapon.getDetails()[0])
            print("Head Damage : ", weapon.getDetails()[1].headDamage)
            print("Body Damage : ", weapon.getDetails()[1].bodyDamage)
            print("Leg Damage : ", weapon.getDetails()[1].legDamage)
            print("Bullet : ", weapon.getDetails()[2])
          elif value == "get heal":
            print("Congratulation! You found a consumable item!")
            consumable = Consumables()
            player1.inventory.addConsumable(consumable)
            print("Item : ", consumable.getDetails()[0])
            print("Heal Amount : ", consumable.getDetails()[1])
      elif action.lower() in ['inventory', 'view inventory']:
          lookInventory()
      input("Press enter to continue ....")
      check_win()

################
# Title Screen #
################
def opening():
  os.system('cls||clear')
  a='''

 ██▓███   ██▀███   ▒█████ ▓██   ██▓▓█████  ██ ▄█▀    ██ ▄█▀ ▄▄▄▄      
▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒██  ██▒▓█   ▀  ██▄█▒     ██▄█▒ ▓█████▄    
▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒ ▒██ ██░▒███   ▓███▄░    ▓███▄░ ▒██▒ ▄██   
▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░ ░ ▐██▓░▒▓█  ▄ ▓██ █▄    ▓██ █▄ ▒██░█▀     
▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░ ░ ██▒▓░░▒████▒▒██▒ █▄   ▒██▒ █▄░▓█  ▀█▓   
▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░   ██▒▒▒ ░░ ▒░ ░▒ ▒▒ ▓▒   ▒ ▒▒ ▓▒░▒▓███▀▒   
░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ▓██ ░▒░  ░ ░  ░░ ░▒ ▒░   ░ ░▒ ▒░▒░▒   ░    
░░         ░░   ░ ░ ░ ░ ▒  ▒ ▒ ░░     ░   ░ ░░ ░    ░ ░░ ░  ░    ░    
            ░         ░ ░  ░ ░        ░  ░░  ░      ░  ░    ░         
                           ░ ░                                   ░    

  '''
  b='''
  KELOMPOK 14
- Michael Christian - C14200013
- Joshua Yordana - C14200020
- Steven Kusuma - C14200079
- Kevin Daniel - C14200140
- Alan Satria - C14200196
'''
  print(a)
  # for character in b:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.0001)
  # time.sleep(0.1)
  
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
  opening() 
  os.system('cls||clear')
  a= '''

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡀⠀⠀⣠⡄⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⣞⠋⡇⠀⡿⢦⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣷⣷⣴⣧⣾⡿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢽⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠋⠙⢿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⣤⣀⣼⣿⣿⡿⠋⠀⠀⠀⠀⠙⢿⣿⣿⣷⣴⣯⣙⢆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢢⣾⣿⣿⣿⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⣽⣿⣿⣿⣿⣇⡙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⢋⣴⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⣿⣿⣿⣿⣿⣦⣙⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣷⣿⣿⡇⣶⣶⠈⢃⣶⡆⣆⣶⡶⠀⢀⣴⣶⣶⣌⠻⢟⣡⣶⣶⣶⡖⢸⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⣿⣿⢀⣾⣿⡇⣸⡿⠁⢰⣿⡏⡝⣹⣿⠁⣾⣿⠉⢩⣿⠃⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⣿⣿⣾⠏⣿⣧⣿⠁⠀⣿⣿⣷⣶⣿⡇⢰⣿⣿⣶⣾⡿⢸⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠋⠙⠁⠈⣿⡇⣿⣿⡟⠀⣿⣿⡇⠀⢰⣿⡟⠉⢹⣿⠁⣼⣿⠃⢿⣿⣰⠇⠀⠈⠀⠙⢿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⠏⠀⠀⠀⠀⠀⣿⠇⠿⠿⠀⠀⠿⠿⠁⠀⠼⠿⠇⠀⠾⠟⠀⠿⠿⠀⠸⠿⠿⠀⠀⠀⠀⠀⠀⢻⣿⣿⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡁⠀⠀⠀⠀⠀⠀⠛⠸⠿⢿⣿⣿⠇⢸⣿⠿⢿⣿⡟⢀⣿⡇⠀⣼⣿⠃⣼⣿⠿⠿⠏⠀⠀⠀⠀⠀⣹⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣀⣤⣾⣿⣿⣿⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⡿⠋⠀⣿⡇⠀⣸⣿⠇⣸⣿⣿⢀⣿⡟⢀⣿⣿⣀⣀⠀⠀⠀⠀⠀⠀⠹⢿⣿⣿⣿⣿⣷⣶⡦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢹⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠟⠁⠀⢸⣿⡇⢀⣿⣿⠀⣿⡿⢻⣾⣿⠇⢸⣿⡟⠛⠋⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠉⢻⣿⠏⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣭⣤⡄⠀⣾⣿⣥⣼⣿⠇⢸⣿⠇⢸⣿⡿⢀⣿⣿⣥⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠁⠙⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠉⠉⠉⠉⠉⠀⠉⠉⠀⠈⠉⠁⠈⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  
  '''
  print(a)
  # print('#' * 45)
  print("           Welcome to text-based shooting game       ")
  print("                   Final Project KB 2022!             ")
  print("                         WarZone                      ")
  print()
  print("                       .: Play :.                 ")
  print("                       .: Help :.                 ")
  print("                       .: Quit :.                 ")
  title_screen_options()

#############
# Help Menu #
#############
def help_menu():
  print("")
  print("~" * 45)
  print("WarZone is a shooting game with a text-based program.")
  print("You can type a command such as 'search' or 'view inventory'")
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

  # question1 = "Hello there, what is your name?\n"
  # for character in question1:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)
  # player_name = input("> ")
  # player1.name = player_name

  # question2 = "My dear friend " + player1.name + ", how are you feeling?\n"
  # for character in question2:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)
  # feeling = input("> ")
  # player1.feeling = feeling.lower()

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
  # for character in question3:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)

  #Leads the player into the warzone now!
  speech2 = "Too bad, i have bad news for you. It seems this is where we must part, " + player1.name + ".\n"
  speech3 = "I bet you don't know where you are now.\n"  
  speech4 = "Well... look around you!\n"
  art = '''
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣻⣿⣿⡟⠛⢿⡿⠟⢛⣿⣿⣿⡛⢻⣿⣿⣿⣿⠟⣿
⣿⡿⠟⠉⠁⠀⣀⣀⣈⣉⣻⣿⣿⣿⣶⣤⣤⣶⣿⣿⣿⣿⣷⣄⠙⠿⠛⢁⣴⣿
⣿⠀⠀⠀⠴⣿⣿⣯⣀⣹⣿⣿⣿⠟⠋⠉⠁⠈⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠀⢀⡀⠀⠀⠈⠉⠻⣿⣿⣿⣿⣿⣷⣶⣤⡀⠀⠀⠙⢿⠟⠉⠀⢀⣠⣤⣿
⣿⠀⠀⠀⢹⣿⡿⠷⢶⣤⣈⣿⣿⣿⡿⠛⠛⠉⠉⠀⠀⠀⠀⠀⠀⠰⠿⢿⣿⣿
⣿⣧⡀⠀⠀⣿⡇⠀⣸⣿⣿⣿⣿⡏⣀⣤⣤⣤⣤⡄⠀⠀⠀⢀⠀⠀⠀⠀⠈⣿
⣿⣿⣷⣄⡀⣿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⢀⣾⠛⠶⣦⣤⣄⣿
⣿⠿⠿⠿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⣤⣾⣿⣆⠀⠘⣿⣿⣿
⣿⣶⣶⣦⣤⣿⠀⠀⣿⠻⠿⠛⠋⣠⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣆⠀⠘⣿⣿
⣿⣿⣿⣿⣿⣿⠀⢀⣿⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡛⠛⠛⠉⠉⢻⡄⠀⠸⣿
⣿⣿⠿⠿⠟⠻⠿⠾⣿⣿⣿⠿⠛⠉⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣧⠀⠀⣿
⣿⣶⣶⣶⣤⣄⠀⠀⠀⠉⠁⠀⢀⣠⣤⣴⣶⣶⣿⣿⣿⣿⣿⡟⠉⠀⣿⡀⠀⣿
⣿⣿⣿⡿⠛⠉⠉⠀⠀⠀⠀⠀⠙⠛⠛⠻⠿⣿⣿⣿⣿⣿⣟⣀⣴⣾⣿⡇⠀⣿
⣿⣿⠋⠀⣀⣤⣶⣶⡄⠀⠀⠀⢰⣦⣤⣤⣀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿
⣿⣿⣴⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣿
  '''
  speech5 = "Yes! You are now in the middle of the forest and it seems you are lost.\n"
  speech6 = "Heh. Heh.. Heh...\n"
  # for character in speech2:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)
  # for character in speech3:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.1)
  # for character in speech4:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)
  # os.system('cls||clear')
  # print(art)
  # time.sleep(0.05)
  # for character in speech5:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.05)
  # for character in speech6:
  #   sys.stdout.write(character)
  #   sys.stdout.flush()
  #   time.sleep(0.1)
  # time.sleep(1)

  main_game_loop()

title_screen()