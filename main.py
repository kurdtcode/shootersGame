from copyreg import constructor
from email import header
from mimetypes import init
from operator import eq
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
    #Select type
    x = random.randint(0,100)
    self.damageReduction = 0
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

    if type == "No Armor":
      durability = 99999
      damageReduction = 0
      image = '''
      ⣿⣿⡿⠫⣝⢽⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣧⢚⣿⡇⠄⠄⡀⠄⡐⡐⢌⢘⠋⠄⠈⡙⢍⠩⡉⠉⠛⠛⠻⣛⢿⣿⣿⣿
      ⣿⣿⣿⣷⣿⣆⣀⠐⠄⠄⠄⡈⠄⠄⢀⢂⢁⠄⡀⠁⡀⢀⠢⡠⢀⣿⡪⣹⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡆⠄⠄⠂⢌⠢⠡⢢⣶⣶⣶⣶⣷⣮⣴⣧⣵⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢌⠪⡀⢀⠠⠐⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢠⣕⣈⣀⣀⣀⡆⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡹⡽⣯⢿⡽⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣪⣿⣳⣿⢽⣗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣻⣾⢸⡜⡽⣽⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣻⡾⣼⣧⢹⣻⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⢸⢺⢂⣿⣿⡆⣟⡆⡫⣽⡻⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣘⣛⣚⣒⣾⣿⣿⣿⣔⣒⣙⣓⣣⣿⣿⣿⣿⣿⣿⣿⣿
      ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
      '''
    elif type == "Light":
      durability = 200
      damageReduction = 25
      image = '''
      ⣿⣿⣿⣿⣿⣿⢿⣛⣯⣽⣽⠿⡿⢿⢿⠿⡿⢯⣿⣯⣽⣟⣻⢿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣟⣾⣿⡿⣟⢏⣲⣿⡿⣫⡳⡣⣱⢹⣿⣿⣽⣿⣻⣷⣧⣻⣿⣿⣿⣿
      ⣿⣿⣿⣏⣾⣿⣟⢿⠫⣾⣧⡣⡹⡸⡨⣦⣿⡜⣿⣷⣿⣻⣿⣽⣿⢢⢻⣿⣿⣿
      ⣿⣿⣿⢹⠿⡍⣦⣿⣾⣿⣟⣿⡿⣿⢿⣻⣿⣿⡸⢿⣽⣿⣯⣷⣿⢝⢜⣿⣿⣿
      ⣿⣿⣿⣿⣿⣼⣿⣿⣟⣷⣿⣟⣿⡿⣿⣿⣻⣾⣿⣷⣬⣛⡫⢿⢫⢫⢢⣿⣿⣿
      ⣿⣿⣿⣿⡇⣿⣿⣯⣿⢿⣽⡿⣯⣿⣿⣽⣿⣻⣾⣯⣿⢿⡪⡇⢽⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⡇⣯⣟⣛⠿⢿⣿⣻⣿⣿⠾⠿⠽⠿⢯⣿⣟⢿⢕⣏⢪⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣇⣿⣿⢿⣿⣾⣭⣽⣶⣶⡿⣿⣿⣿⣷⣷⣗⢽⣱⡣⣻⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣞⣿⡿⣿⣾⡏⣿⣾⣿⣻⣿⢷⣿⢷⣿⢿⡳⡵⣙⣾⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣯⢻⣿⣷⣯⣿⢿⣾⣿⣻⣿⢿⡿⣫⡳⡝⣼⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⡎⣿⣾⣿⣻⣿⢿⣾⣿⣻⡿⣝⢮⡺⣸⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣷⢺⣯⣿⢟⣿⣿⣻⣾⣿⡫⡮⡣⣣⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣽⣙⣻⣙⣛⣫⣳⣽⣼⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
    elif type == "Basic":
      durability = 300
      damageReduction = 30
      image = '''
      ⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠟⡛⣛⣛⣛⡛⡻⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⠋⣠⡴⣶⣖⣶⡲⣌⣞⣾⣬⠨⢊⠑⠅⡤⢔⢶⡶⣔⠤⡈⢻⣿⣿⣿
      ⣿⣿⣿⠃⣺⣺⣟⣿⣿⣯⢿⣕⢮⢪⢳⢵⣲⢜⣖⡕⡭⡣⣏⢮⢪⢪⠂⢻⣿⣿
      ⣿⣿⠇⣘⢞⢮⢿⢽⣻⣞⡯⡞⡎⡇⡗⡕⣎⣟⣮⡺⣕⡕⡎⡎⡇⡇⢕⠈⣿⣿
      ⣿⣿⠄⡪⡪⡫⡫⡫⡞⠮⠪⢃⢣⣧⣧⣷⡿⣽⣞⢞⢮⢺⢜⢜⢔⠈⢂⣀⣿⣿
      ⣿⣿⣤⣁⣙⡈⠨⡃⡊⠨⠐⡐⣾⣿⣿⣟⣿⣳⢯⡫⣎⢏⡧⡣⡱⡑⢸⣿⣿⣿
      ⣿⣿⣿⣿⣿⣇⠈⡎⠔⡁⠅⣸⡿⣽⣾⣻⢾⣝⢷⡹⡪⡪⣣⠣⡒⢌⢸⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⠄⢪⢪⢔⢯⢗⡿⡽⣺⣺⢳⡳⡳⡹⡸⡱⣱⠱⡘⢔⢸⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⡆⠨⢪⢣⢫⡣⡏⣞⢵⢱⢳⢱⢹⢸⢪⢪⢪⠨⡊⡂⢸⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣷⠈⢜⢜⢜⢜⢜⢜⢜⢜⢜⢎⢇⢇⢗⢕⠕⡅⢕⠄⣾⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⡀⠂⠕⠕⢇⢗⢕⢝⢜⢕⢕⢕⢵⢱⢕⡱⠨⠂⢸⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣯⣿⣷⣄⠁⠅⡑⠌⡊⡪⢑⠱⢑⠅⡹⢉⢡⢰⠁⠂⣸⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿
      '''
    elif type == "Medium":
      durability = 400
      damageReduction = 40
      image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢿⢿⢿⢿⢿⢿⢿⢿⣿⡿⠛⠛⡿⣿⣿⣿⣿⣿
      ⣿⣿⣿⡿⡿⣛⣛⠛⡉⡍⣉⡐⢔⡔⡄⢄⠄⡄⢄⠊⡉⠁⡐⠠⡀⢀⠉⠻⣿⣿
      ⣿⣿⡷⡫⡅⢓⠑⢀⢕⢕⡕⡺⡢⡍⡙⢕⢋⢨⢲⢌⠜⠄⣈⠌⢔⢐⠐⡀⢹⣿
      ⣿⡟⣸⢪⡚⢦⡑⢔⠠⠁⠕⡁⢇⢏⢎⢐⡰⡕⡕⡢⡱⢁⠄⠂⡁⠢⠡⠠⠄⣿
      ⣿⡇⣳⣑⢩⢢⢝⠰⡡⠡⠑⠄⡂⠁⢁⠑⢘⠘⠊⡈⠐⢀⢤⠲⠸⡐⢅⠅⠄⣿
      ⣿⡇⡮⠊⠪⡪⡢⠐⡕⡥⡡⡑⡄⠑⢠⢚⠢⡁⠅⠠⠈⠔⠈⡈⠸⡸⡂⠕⠄⣿
      ⣿⣷⣬⣘⠔⢅⣊⠄⠧⢃⠓⠡⡁⠅⢂⢑⠡⠂⡂⠅⡡⠨⢀⠄⢀⠥⠔⠅⣡⣿
      ⣿⣿⣿⣿⣿⣿⣿⠄⡐⡀⡡⢡⢐⢬⢸⢔⢪⣐⡐⠔⢄⠅⠤⡐⣼⣿⣿⣿⣿⣿
      ⣿⣿⣿⣽⣿⣯⣿⠄⡇⣇⢇⠳⡱⡱⡑⡜⡎⡆⡏⢝⢜⢕⠭⡀⣿⣿⣿⡿⣿⣿
      ⣿⣿⣯⣿⣿⣻⣿⡄⢓⢅⠕⡱⡸⣒⡪⡪⣜⢐⢪⢪⢪⠪⡡⢠⣿⣿⣟⣿⣿⣿
      ⣿⣿⣟⣿⣟⣿⣿⡇⠸⠜⠬⠲⡸⢰⠱⡑⡕⡑⢕⢑⢐⠡⠂⢸⣿⣿⡿⣿⣯⣿
      ⣿⣿⣿⢿⣿⢿⣻⡇⠄⠌⠨⡈⠂⢢⠃⡅⢌⠌⡀⠂⠄⠠⠄⢸⣿⣿⣿⣿⢿⣿
      ⣿⣿⡿⣿⣿⣿⣿⠃⢄⢌⣀⣀⡁⡊⡒⡒⣂⢁⣀⣁⡐⡤⠠⠘⣿⣿⣾⣿⣿⣿
      ⣿⣿⣿⣿⣿⣽⡛⢠⡣⡳⡸⡠⡢⡑⡩⡜⡌⡧⢕⠢⢣⢊⠌⡄⢹⣿⣿⣽⣿⣽
      ⣿⣿⣷⣿⣟⡟⢁⢎⠎⡮⡪⣒⢕⢕⢕⢕⡣⡥⡣⡱⡑⢔⠡⢂⠈⣿⣽⣿⡿⣿
      ⣿⣿⣿⣽⣿⣏⡠⠃⢎⠘⠘⠨⠬⢑⢕⢢⠰⠨⠄⠂⠐⠄⢈⣀⣢⣿⣻⣽⣿⣿
      ⣿⣿⣯⣿⣿⢿⣿⣿⣷⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
    elif type == "Heavy":
      durability = 500
      damageReduction = 50
      image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣻⠉⠉⠉⠋⡋⠍⠉⠉⠉⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣟⠟⢭⠉⣉⣁⡀⢈⡉⡋⠒⠆⠆⣢⠂⢁⡁⡐⠠⣀⣡⠩⠩⠻⣿⣟⣿
      ⣿⣿⡞⠁⠬⠝⣼⡳⣯⣻⢽⣖⣮⢭⡋⢊⡧⣝⣶⣺⢽⢯⢯⡯⡗⠧⢇⠘⣿⣿
      ⣿⠏⠄⠘⡲⢷⣳⢯⣗⡯⣗⣞⡾⡽⡑⠎⣏⣗⣗⣗⡯⡿⣽⡺⣇⠈⢽⠄⠘⣿
      ⡏⠄⠄⢈⠨⢸⣺⣳⡳⣝⣗⣗⢯⢯⠏⢸⡳⣳⣳⣳⡫⣟⢮⡻⠂⠈⢝⠄⠄⣼
      ⣿⣦⣄⠨⡒⣬⣊⠮⠚⡕⡗⢗⣝⢭⠕⢇⡏⣗⢧⡳⣝⡚⠍⣐⢠⠙⡈⣴⣾⣿
      ⣿⣿⣿⣇⠁⠃⣗⢯⣫⡳⡝⢵⡳⣹⢜⢕⣝⣪⡳⣝⢮⡺⣝⠮⠔⠈⣠⣿⣿⣿
      ⣿⣿⡿⣿⣿⣷⣶⣁⢇⢆⠎⢗⡝⣎⢏⢸⡸⡲⡕⢎⠥⠉⣨⣴⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⡿⣟⣿⣿⢿⡠⡣⡃⡇⡯⡺⣜⠰⡝⣎⢗⡡⡣⢹⣿⣿⣿⣿⢿⣻⣷⣿
      ⣿⣿⣷⣿⣿⣿⡿⣿⡗⡕⡕⢌⢪⢺⢄⢸⢸⢊⢔⢎⢪⢸⣿⣿⣟⣿⣿⣿⣿⣿
      ⣿⣿⣟⣿⡿⣯⡿⠉⢌⢎⢎⠜⡜⡜⡜⡜⡜⣜⢰⠱⡁⠂⣿⣷⣿⣿⣯⣷⣿⣿
      ⣿⣿⡿⣿⣿⣿⣧⠁⠄⢉⡆⡕⣱⠱⠑⡱⡑⣅⡆⡃⠐⢠⣿⣿⣿⣽⣿⣿⣟⣿
      ⣿⣿⣿⡿⣿⣽⣿⣿⣶⣄⡃⢝⡨⣳⢨⢜⣏⡢⢃⣪⣾⣿⣿⣽⣾⣿⣿⣾⣿⣿
      ⣿⣿⣷⣿⣿⣿⣿⣽⣿⣿⣿⣷⣦⣍⣒⣁⣥⣶⣿⣿⣿⢿⣟⣿⣿⣟⣷⣿⣿⢿
      '''
    else:
      durability = 0
      damageReduction = 0
      image = '''
      ⣿⣿⡿⠫⣝⢽⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣧⢚⣿⡇⠄⠄⡀⠄⡐⡐⢌⢘⠋⠄⠈⡙⢍⠩⡉⠉⠛⠛⠻⣛⢿⣿⣿⣿
      ⣿⣿⣿⣷⣿⣆⣀⠐⠄⠄⠄⡈⠄⠄⢀⢂⢁⠄⡀⠁⡀⢀⠢⡠⢀⣿⡪⣹⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡆⠄⠄⠂⢌⠢⠡⢢⣶⣶⣶⣶⣷⣮⣴⣧⣵⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢌⠪⡀⢀⠠⠐⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢠⣕⣈⣀⣀⣀⡆⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡹⡽⣯⢿⡽⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣪⣿⣳⣿⢽⣗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣻⣾⢸⡜⡽⣽⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣻⡾⣼⣧⢹⣻⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⢸⢺⢂⣿⣿⡆⣟⡆⡫⣽⡻⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣘⣛⣚⣒⣾⣿⣿⣿⣔⣒⣙⣓⣣⣿⣿⣿⣿⣿⣿⣿⣿
      ⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
      '''
    super().__init__(name, durability)
    self.damageReduction = damageReduction
    self.image = image

  def getDetails(self) -> list:
    return [self.name, self.durability, self.damageReduction, self.image]

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
      self.image = '''
      ⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿
      ⣿⣿⣿⣿⠄⠄⠄⠄⠉⠉⠉⠉⠉⠉⠉⠄⣼⣿⣿⣿
      ⣿⣿⣿⣿⡇⠄⠄⠄⣉⣙⣿⣿⡏⠄⠄⠄⣿⣿⣿⣿
      ⣿⣿⣿⣿⡇⠄⠄⠄⠛⢳⣢⡀⣿⠄⠄⠄⣿⣿⣿⣿
      ⣿⣿⣿⣏⠁⠄⢀⣀⣀⣀⣀⣀⣀⡀⠄⠄⢸⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿=
      '''
    elif name == "Medkit":
      self.image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠻⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⠿⠿⠿⠯⠄⠄⠂⠠⠄⠄⡀⠄⠙⣿⣿⣿
      ⣿⣿⣿⡟⠈⠄⡂⡐⡈⠄⠡⠈⢄⡡⠄⢂⠁⣿⣿⣿
      ⣿⣿⣿⣇⠠⠑⡀⡂⢐⠈⣈⣿⣿⣴⡎⠠⢐⣿⣿⣿
      ⣿⣿⣿⣷⠄⠌⠄⢂⠂⢼⡿⣿⣿⠛⠐⡐⢸⣿⣿⣿
      ⣿⣿⣿⣿⠄⠨⢐⠐⢐⠄⡂⢍⢩⣬⣲⣶⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣌⣄⣌⣤⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
      self.healamount = 50

  def getDetails(self) -> list:
    return [self.name, self.healamount, self.image]

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
      self.durability = 99999
      self.bulletPerAttack = 0
      self.image ='''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣉⣭⣭⡭⠭⢭⡭⢶⣾⣿⣿⣿⣶⣉⡛⠿⢟⣋⣉⡻⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢋⡥⠎⣿⣿⣷⡟⣶⣿⣷⣌⠙⢟⢿⣿⡇⣿⡿⠹⢯⣿⣿⣷⠈⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⠛⣤⣶⣶⣶⣿⣿⣶⣄⠫⣿⣿⣧⣿⣿⣿⣿⣾⣼⣿⣿⣿⣿⣿⣧⡌⠟⣿⣿⡇⣌⢻⣿⣿⣿
      ⣿⣿⣿⣿⠋⡞⡿⣿⣿⣿⣿⠿⣿⣿⣾⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⢻⢹⣿⣿⣿⣿⣇⣿⠄⣿⣿⣿
      ⣿⣿⣿⢉⣾⡆⢰⣽⣿⣿⣿⠄⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣆⣿⣿⣿⣿⣿⣿⣿⠄⣿⣿⣿
      ⣿⣿⣧⠹⢳⠄⣾⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿
      ⣿⣿⣿⡆⣿⡀⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿
      ⣿⣿⣿⣷⠙⡇⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⠄⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿
      ⣿⣿⣿⣿⣧⢹⢻⣿⣿⣿⣿⣿⠄⣿⣿⣿⣿⣿⣿⣿⠄⠁⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⠁⣿⣿⣿
      ⣿⣿⣿⣿⣿⡈⣾⣿⣿⣿⣿⣿⠇⠏⠿⠿⢿⣿⣿⠿⠄⠄⠋⠻⠿⣿⣿⠿⡟⠾⣿⣯⣽⣿⣿⠏⣾⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣤⣜⠓⢚⣿⡥⠄⠈⠄⠐⠂⠠⠭⠄⠄⠄⠄⠚⠓⠂⠄⡀⠠⣤⡒⠒⣒⡿⣡⣾⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣴⣶⣿⣦⣤⣄⣠⣤⣴⠟⠁⡤⠤⢀⣀⣠⣤⣤⣤⡠⣠⣤⡌⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠎⠼⠿⣷⣶⢹⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⠄⠉⠉⣁⡀⠞⠛⠛⠉⠙⠻⠏⢀⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣿⣶⣶⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      '''
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
      self.durability = 100
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
      self.durability = 100
      self.bulletPerAttack = 2

    elif name == "M4A1 Rifle":
      self.maxBullet = 100
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
      self.damage = Damage(60, 50, 30)
      #self.reloadTime = 3
      self.durability = 100
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
      self.damage = Damage(100, 80, 60)
      #self.reloadTime = 5
      self.durability = 100
      self.bulletPerAttack = 1

    elif name == "Cheat Weapon":
      self.maxBullet = 9999
      self.image = '''
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⠛⠛⠛⠋⠉⠛⠛⠻⠛⠉⠉⠙⠻⠿⣿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠋⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⢀⣀⣤⣶⣶⣦⣴⣴⣶⣶⣦⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠄⠄⠄⠄⠄⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀⠄⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠄⠄⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣈⣹⣿⣿⣿⣿⣿⣿⣏⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠿⠿⠻⠿⣿⣿⣿⣿⣿⣿⣿⠟⠿⠟⠻⢿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠄⣿⣿⣿⣿⣧⣤⣤⣆⣄⣓⣬⣾⣿⣿⣿⣿⣷⣤⣐⣤⣶⣤⣤⣿⣿⣿⣿⣿⣿⡍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⡿⠿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣴⣆⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠙⠋⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠉⠉⢻⣿⣿⣿⣿⣿⣋⣁⠄⢤⣤⣤⡤⣤⣉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠉⠻⢿⣿⣿⣿⡟⠁⠄⠄⠄⢊⣻⣿⣿⣿⣿⣿⣿⣿⡟⢛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠉⠁⠄⠄⠄⠄⠄⠄⠄⠄⣷⣾⣿⣿⣾⣿⣾⣿⣿⣿⣿⣿⠛⠉⠄⠄⠙⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
      ⣿⣿⡿⠿⠿⠿⠛⠋⠉⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠻⠿⠿⠿⠿⠿⠿⠿⠟⠁⠄⢀⠄⠁⠄⠄⠄⠄⠄⠄⠄⠈⠉⠙⠛⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿
      ⠉⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠰⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢂⠄⣠⣴⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠙⠛⠿⣿
      ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣷⣤⣀⠄⠄⠄⠄⠄⠄⢰⣤⣶⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄

      '''
      self.damage = Damage(100000, 100000, 10000)
      #self.reloadTime = 5
      self.durability = 1000000
      self.bulletPerAttack = 1
    self.reload()

  def getDetails(self) -> list:
    return [self.name, self.damage, self.maxBullet, self.bullet, self.image, self.durability]

  def shoot(self):
    self.bullet = self.bullet - self.bulletPerAttack
    self.durability = self.durability - 5
    if self.bullet < 0:
      self.bullet += self.bulletPerAttack
      return False
    else:
      return True

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
    # print(self.armor)
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
    weapon = Weapon("Punch")
    self.inventory.addWeapon(weapon)
    self.inventory.equipWeapon(0)
    armor = Armor("No Armor", "No Armor")
    self.inventory.addArmor(armor)
    self.inventory.equipArmor(0)

  def CharacterDetail(self):
    return [self.name, self.hp, self.inventory]

  def heal(self, index):
    self.hp = self.hp + self.inventory.useConsumable(index).getDetails()[1]
    if self.hp > self.maxHP:
      self.hp = self.maxHP

  def attack(self, enemy):
    equippedWeapon = self.inventory.seeEquippedWeapon() #Weapon
    # type(equippedWeapon)
    damage = equippedWeapon.getDetails()[1] #Weapon Damage

    dmg = damage.randomHit()
    shooting = equippedWeapon.shoot()
    if not shooting:
      return False 
    # print("░░░░░░░░░░░░░░░░░░░ Info Phase ░░░░░░░░░░░░░░░░░░░")
    
    if equippedWeapon.durability <= 0:
      self.inventory.getAllWeapon().pop(self.inventory.equippedWeapon)
      self.inventory.equippedWeapon = 0
      # print("░░░░░░░░░░░░░░░░░░░ Player's Move ░░░░░░░░░░░░░░░░░░░")
      print(self.name, "'s Weapon is broken\n")

    enemyArmor = enemy.inventory.seeEquippedArmor() #Enemy Armor
    dmgReduc = enemyArmor.getDetails()[2] #Damage Reduction

    finalDmg = dmg - dmg * dmgReduc/100 #Calc Damage

    enemy.hp = enemy.hp - finalDmg
    enemyArmor.reduceDurability(dmg)
    if enemyArmor.durability <= 0:
      # print(enemy.inventory.getAllArmor())
      # print(enemy.inventory.equippedArmor)
      enemy.inventory.getAllArmor().pop(enemy.inventory.equippedArmor)
      enemy.inventory.equippedArmor = 0
      print(enemy.name, "'s Armor is broken")
      # print(enemy.inventory.getAllArmor())
    return True

  def reload(self):
    self.inventory.seeEquippedWeapon().reload()
    # print("░░░░░░░░░░░░░░░░░░░ Player's Move ░░░░░░░░░░░░░░░░░░░")
    print(self.name, "'s Weapon is reloaded")
    
################
# Player Setup #
################
class Player(Characters):
  def __init__(self):
    super().__init__(200)
    self.feeling = ""
    weapon = Weapon("P250 Pistol")
    self.inventory.addWeapon(weapon)
    self.inventory.equipWeapon(1)

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
      self.inventory.equipArmor(1)
      self.inventory.equipWeapon(1)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      
    if template == 2:
      self.name = "Normal Soldier"
      self.hp = 125
      armor = Armor("Basic Armor", "Basic")
      self.inventory.addArmor(armor)
      weapon = Weapon("Deagle Pistol")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(1)
      self.inventory.equipWeapon(1)
      consumables = Consumables("Bandage")
      consumables1 = Consumables("Bandage")
      consumables2 = Consumables("Bandage")

      self.inventory.addConsumable(consumables)
      self.inventory.addConsumable(consumables1)
      self.inventory.addConsumable(consumables2)

    if template == 3:
      self.name = "Veteran Soldier"
      self.hp = 200
      armor = Armor("Medium Armor", "Medium")
      self.inventory.addArmor(armor)
      weapon = Weapon("M4A1 Rifle")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(1)
      self.inventory.equipWeapon(1)
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
      self.hp = 250
      armor = Armor("Heavy Armor", "Heavy")
      self.inventory.addArmor(armor)
      weapon = Weapon("AWM Sniper Rifle")
      self.inventory.addWeapon(weapon)
      self.inventory.equipArmor(1)
      self.inventory.equipWeapon(1)
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

  def currentEnemyAuto(self, player:Player):
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
      shoot = self.attack(player)
      if not shoot:
        self.reload()
        return "reload"
      return "attack"

#declare object enemy
enemy = Enemy(1)
turn = 1
def Search():
  global turn
  playerHealth=player1.hp
  chanceFindBoss  = max(((turn - 10) * 0.2) + (playerHealth * 0.005),0)
  chanceFindEnemy = (turn * 0.7) + (playerHealth * 0.05)
  chanceGetArmor = (turn * 0.3) + (playerHealth * 0.01)
  chanceGetWeapon = (turn * 0.5) + (playerHealth * 0.01)
  chanceGetHealing = (turn * 0.6) + (playerHealth * 0.01)

  pembagi = (chanceFindBoss + chanceFindEnemy + chanceGetWeapon + chanceGetWeapon + chanceGetHealing)

  realChanceBoss = round(chanceFindBoss / pembagi,2)
  realChanceEnemy = round(chanceFindEnemy / pembagi,3)
  realChanceArmor = round(chanceGetArmor / pembagi,3)
  realChanceWeapon = round(chanceGetWeapon / pembagi,3)
  realChanceHealing = round(chanceGetHealing / pembagi,3)

  # angkaRandom = random.randint(0,10)/10
  angkaRandom = random.random()
  ## cuman buat ngelihat nilai chance (buat ngepasin udah bener sama if if an nya belom)
  # print("boss", realChanceBoss)
  # print("enemy", realChanceEnemy)
  # print("armor", realChanceArmor)
  # print("weapon", realChanceWeapon)
  # print("Healing", realChanceHealing)
  # print("------------")
  # print(angkaRandom)
  turn+=1
  if angkaRandom < realChanceBoss :
      return "get enemy Special Force Soldier"
  elif angkaRandom <= realChanceBoss + realChanceEnemy :
      if turn >= 0 and turn <= 2:
          randomGear = random.randint(1,2)
          if randomGear == 1 :
              return "get weapon"
          else:
              return "get armor"
      elif turn > 2 and turn <= 5 :
          return "get enemy Militia"
      elif turn > 5 and turn <= 8 :
          return "get enemy Normal Soldier"
      elif turn > 8 and turn <=11 :
          return "get enemy Veteran Soldier"
      else :
          return "get enemy Special Force Soldier"
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon :
      return "get weapon"
  elif angkaRandom <= realChanceBoss +  realChanceEnemy + realChanceWeapon +realChanceArmor :
      return "get armor"
  else :
      return "get heal"

# Check if either or both Players is below zero health
def check_win(enemy:Enemy):
  if enemy.name == "Special Force Soldier":
    if player1.hp < 1 and enemy.hp >= 1 :
      player1.game_over = True
      defeatText()
    elif player1.hp >= 1 and enemy.hp < 1:
      player1.game_over = True
      print("Enemy is dead\n")
      winText()
    else:
      player1.game_over = True
      defeatText()
  else:
    if player1.hp < 1 and enemy.hp >= 1 :
      player1.game_over = True
      defeatText()
    elif player1.hp >= 1 and enemy.hp < 1 :
      player1.game_over = False
      print("Enemy is dead\n")
      findBossText()
    elif player1.hp < 1 and enemy.hp < 1:
      player1.game_over = True
      defeatText()
    else:
      print("Something Wrong")

##################################### kd ##################################

##################
# look inventory #
# (use invetory) #
##################
def lookInventory():
  changeSomething = False
  while(True):
    os.system('cls||clear')
    print("The following is a list from your inventory\n⠄View Weapon\n⠄View Armor\n⠄View Consumables\n⠄Back")
    intp = input("\n> ").lower()
    while intp not in ['view weapon', 'view armor', 'view consumables', 'back']:
      print("Unknown action command, please try again.")
      intp = input("\n> ").lower()

    if intp == 'view weapon':
      while(True):
        weapon = player1.inventory.getAllWeapon()
        equip = player1.inventory.seeEquippedWeapon()
        print()
        print("\n░░░░░░░░░░░░░░ Weapon in Use ░░░░░░░░░░░░░░░\n") 
        print(equip.getDetails()[4])
        print("Equipped Weapon :", equip.getDetails()[0])
        print("Head Damage : ", equip.getDetails()[1].headDamage)
        print("Body Damage : ", equip.getDetails()[1].bodyDamage)
        print("Leg Damage : ", equip.getDetails()[1].legDamage)
        print("Max Bullet : ", equip.getDetails()[2])
        print("Current Bullet : ", equip.getDetails()[3])
        print("Durability : ", equip.getDetails()[5])
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 

        for i in range (len(weapon)):
          print("Weapon ",i+1,":", weapon[i].getDetails()[0])
          # print(weapon[i].getDetails()[4])
          # print("Head Damage : ", weapon[i].getDetails()[1].headDamage)
          # print("Body Damage : ", weapon[i].getDetails()[1].bodyDamage)
          # print("Leg Damage : ", weapon[i].getDetails()[1].legDamage)
          # print("Max Bullet : ", weapon[i].getDetails()[2])
          # print("Current Bullet : ", weapon[i].getDetails()[3])
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
        print("What do you want to do?\n⠄Equip Weapon\n⠄Reload\n⠄View Weapon Detail\n⠄Back")
        intp2 = input("\n> ").lower()
        while intp2 not in ['equip weapon', 'reload','view weapon detail', 'view weapon','view detail', 'back']:
          print("Unknown action command, please try again.")
          intp2 = input("\n> ").lower()
        if intp2 == 'equip weapon':
          print("Which weapon do you want to equip? (numbers)")
          intp2 = int(input("\n> "))
          player1.inventory.equipWeapon(intp2-1)
          changeSomething = True
        elif intp2 in ['view weapon detail', 'view weapon', 'view detail']:
          print("Which weapon do you want to view? (numbers)")
          intp2 = int(input("\n> "))
          view = player1.inventory.seeWeaponDetail(intp2-1)
          print("\n░░░░░░░░░░░░░ Weapon's Detail ░░░░░░░░░░░░░░\n") 
          print(equip.getDetails()[4])
          print("Weapon :", view.getDetails()[0])
          print("Head Damage : ", view.getDetails()[1].headDamage)
          print("Body Damage : ", view.getDetails()[1].bodyDamage)
          print("Leg Damage : ", view.getDetails()[1].legDamage)
          print("Max Bullet : ", view.getDetails()[2])
          print("Current Bullet : ", view.getDetails()[3])
          print("Durability : ", view.getDetails()[5])
          print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
          input("Press Enter To Continue")
          os.system('cls||clear')

        elif intp2 == 'reload':
          player1.reload()
          changeSomething = True
        elif intp2 == 'back':
          os.system('cls||clear')
          break
        
    elif intp == 'view armor':
      while (True):
        armors = player1.inventory.getAllArmor()
        equip = player1.inventory.seeEquippedArmor()
        print("░░░░░░░░░░░░░░░ Armor in Use ░░░░░░░░░░░░░░░\n") 
        print(equip.getDetails()[3])
        print("Equipped Armor : ", equip.getDetails()[0])
        print("Durability : ", equip.getDetails()[1])
        print("Damage Reduction : ", equip.getDetails()[2])
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 


        for i in range (len(armors)):
          print("Armor",i+1,":", armors[i].getDetails()[0])
          # print("Durability : ", armors[i].getDetails()[1])
          # print("Damage Reduction : ", armors[i].getDetails()[2])
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 

        print("What do you want to do?\n⠄Equip Armor\n⠄View Armor Detail\n⠄Bac")
        intp2 = input("\n> ")
        while intp2 not in ['equip armor', 'view armor detail', 'view armor','view detail', 'back']:
          print("Unknown action command, please try again.\n")
          intp2 = input("\n> ").lower()
        if intp2 == 'equip armor':
          print("Which armor do you want to equip? (numbers)")
          intp2 = int(input("\n> "))
          player1.inventory.equipArmor(intp2-1)
          changeSomething = True
        elif intp2 in ['view armor detail', 'view armor', 'view detail']:
          print("Which weapon do you want to view? (numbers)")
          intp2 = int(input("\n> "))
          view = player1.inventory.seeArmorDetail(intp2-1)
          print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
          print(view.getDetails()[3])
          print("Armor :", view.getDetails()[0])
          print("Durability : ", view.getDetails()[1])
          print("Damage Reduction : ", view.getDetails()[2])
          print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
          input("Press Enter To Continue")
          os.system('cls||clear')
        elif intp2 == 'back':
          os.system('cls||clear')
          break

    elif intp == 'view consumables':
      while (True):
        consumable = player1.inventory.getAllConsumable()
        print("░░░░░░░░░░░░░░░ Consumable ░░░░░░░░░░░░░░░\n") 
        for i in range (len(consumable)):
          print(consumable[i].getDetails()[2])
          print("Item ",i+1,": ", consumable[i].getDetails()[0])
          print("Heal Amount : ", consumable[i].getDetails()[1])
        if (len(consumable) == 0):
          print("Empty")
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 

        print("What do you want to do?\n⠄Use Consumables\n⠄Back")
        intp2 = input("\n> ").lower()
        while intp2 not in ['use consumables', 'back']:
          print("Unknown action command, please try again.")
          intp2 = input("\n> ").lower()
        if intp2 in ['use consumables', 'back']:
          if intp2 == 'use consumables':
            print("Which consumables do you want to use? (numbers)")
            intp2 = int(input("\n> "))
            player1.heal(intp2-1)
            changeSomething = True
          elif intp2 == 'back':
            os.system('cls||clear')
            break
    
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
  print("Oh no! There is ", currentEnemy.name ,"(",currentEnemy.hp," HP ) in front of you!\n")
  while currentEnemy.hp > 0 and player1.hp > 0:
    print("                  ENEMY")
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    print("      Enemy ",currentEnemy.name, "'s Health: " , currentEnemy.hp)
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    equippedweapon2 = currentEnemy.inventory.seeEquippedWeapon()
    
    print("      Weapon :", equippedweapon2.getDetails()[0])
    print("      Current Bullet : ", equippedweapon2.getDetails()[3],"/",equippedweapon2.getDetails()[2])
    equippedarmor2 = currentEnemy.inventory.seeEquippedArmor()
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    print("      Armor : ", equippedarmor2.getDetails()[0])
    print("      Durability : ", equippedarmor2.getDetails()[1])
    print("      Damage Reduction : ", equippedarmor2.getDetails()[2])
 
    print("\n\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n\n") 
    print("                  PLAYER")
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    print("      ",player1.name, "'s Health: " , player1.hp)
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    equippedweapon = player1.inventory.seeEquippedWeapon()
    print("      Weapon :", equippedweapon.getDetails()[0])
    print("      Current Bullet : ", equippedweapon.getDetails()[3],"/",equippedweapon.getDetails()[2])
    print("      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") 
    equippedarmor = player1.inventory.seeEquippedArmor()
    print("      Armor : ", equippedarmor.getDetails()[0])
    print("      Durability : ", equippedarmor.getDetails()[1])
    print("      Damage Reduction : ", equippedarmor.getDetails()[2])


    print("\n\nWhat do you want to do?\n⠄Attack\n⠄Heal\n⠄Reload\n⠄View Inventory")
    battleInput = input("\n> ")
    acceptable_actions = ['attack', 'shoot', 'heal', 'reload', 'inventory', 'view inventory']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
    while battleInput.lower() not in acceptable_actions:
      print("Unknown action command, please try again.")
      battleInput = input("\n> ")
    # print("What do you want to do?\n⠄Attack\n⠄Heal\n⠄Reload\n⠄View Inventory\n")
    
    os.system('cls||clear')
    print("░░░░░░░░░░░░░░░░░░░░░░ Info Phase ░░░░░░░░░░░░░░░░░░░░░░")
    change = True
    if battleInput.lower() == quitgame:
        sys.exit()
    elif battleInput.lower() in ['attack', 'shoot']:
        shooting = player1.attack(currentEnemy)
        if shooting == False:
          print('''
          ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⣿⣿⣿⣿⣿⣿⡋⠉⠉⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⣿⣿⣿⣿⣿⣿⣶⡄⠄⠄⠄⠈⠍⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⣿⣿⣿⣿⣿⣿⣿⣷⣦⠄⠐⠠⣤⣤⡄⠆⠨⣛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⣿⣿⣿⣿⣿⠿⠛⠉⠄⠄⠄⢀⡤⠛⠛⠓⠂⠵⣮⣵⣄⠙⠛⠿⣿⣿⣿⣿⣿⣿
          ⣿⣿⡿⠋⠁⠄⠄⠄⠄⡠⠂⠁⠄⣄⡀⡘⣀⠄⠄⠈⠛⠓⠂⠠⠘⣟⣿⣿⣿⣿
          ⣿⡋⠄⠄⠄⠄⠄⠔⠁⢀⣤⣴⣶⣮⣟⣻⡿⠿⢣⣤⣤⣄⣀⣀⣤⣬⣌⣱⣩⣿
          ⣿⣿⣦⡀⠄⠄⠄⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ⣿⣿⣿⣿⣷⣶⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
          ''')
          print("Not Enough Bullet To Shoot!! RELOAD")
          print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
          continue

    elif battleInput.lower() in ['reload']:
        player1.reload()
    elif battleInput.lower() in ['heal']:
        consumable = player1.inventory.getAllConsumable()
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
        for i in range (len(consumable)):
          print(consumable[i].getDetails()[2])
          print("Item ",i+1,": ", consumable[i].getDetails()[0])
          print("Heal Amount : ", consumable[i].getDetails()[1])
        if (len(consumable) == 0):
          print("Empty")
        print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
        print("What do you want to do? \n⠄Use consumables\n.Back")
        intp2 = input("\n> ")
        while intp2 not in ['use consumables', 'heal', 'back']:
          print("Unknown action command, please try again.")
          intp2 = input("\n> ").lower()
        if intp2 in ['use consumables', 'heal', 'back']:
          if intp2 in ['use consumables', 'heal']:
            print("Which consumables do you want to use? (numbers)")
            intp2 = int(input("\n> "))
            player1.heal(intp2-1)
            changeSomething = True
          elif intp2 == 'back':
            change = False
    elif battleInput.lower() in ['inventory', 'view inventory']:
        change = lookInventory()

    if change:
      move = currentEnemy.currentEnemyAuto(player1)
      print("░░░░░░░░░░░░░░░░░░░░░ Enemy's Move ░░░░░░░░░░░░░░░░░░░░░") 
      if move == "attack":
        weap = currentEnemy.inventory.seeEquippedWeapon()
        print("Enemy is attacking with" , weap.getDetails()[0], "\n\n")
      elif move == "healMedkit":
        print("Enemy used a medkit\n\n")
      elif move == "healBandage":
        print("Enemy used a bandage\n\n")
      elif move == "reload":
        print("Enemy's weapon reloaded\n\n")
      print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n\n") 


################
# main looping #
################
def main_game_loop():
    global enemy
    os.system('cls||clear')
    print("░"*45)
    print("░ Here begins the adventure...              ░")
    print("░"*45)
    # print("\nYou find yourself in the center of a strange place.\nSeems like you are trapped in a forest.\n")
    speechx = "You find yourself in the center of a clearing. \nSeems like you are trapped in this forest\n"
    for character in speechx:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.001)

    time.sleep(5) #note
    while player1.game_over is False:
      os.system('cls||clear')
      print(f"{player1.name}'s health = {player1.hp}")
      print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
      print("What would you like to do?\n⠄Search\n⠄View Inventory\n⠄Quit game")
      action = input("\n> ")
      acceptable_actions = ['search', 'look', 'view', 'inventory', 'view inventory', 'inspect', 'cheat weapon', 'quit']
      #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
      while action.lower() not in acceptable_actions:
        print("Unknown action command, please try again.")
        action = input("\n> ")
      os.system('cls||clear')
      if action.lower() == quitgame:
          sys.exit()
      elif action.lower() in ['search', 'look', 'view', 'inspect']:
          value = Search()
          #Make new enemy object based on return on function Search()
          # currentEnemy = Enemy(1)

          if value == "get enemy Militia":
            militia = Enemy(1)
            enemy = militia
            militiaImage()
            battleLoop(enemy)
            check_win(enemy)
          elif value == "get enemy Normal Soldier":
            nSoldier = Enemy(2)
            enemy = nSoldier
            NormalSoldierImage()
            battleLoop(enemy)
            check_win(enemy)
          elif value == "get enemy Veteran Soldier":
            vSoldier = Enemy(3)
            enemy = vSoldier
            veteranImage()
            battleLoop(enemy)
            check_win(enemy)
          elif value == "get enemy Special Force Soldier":
            boss = Enemy(4)
            enemy = boss
            SpecialImage()
            battleLoop(enemy)
            check_win(enemy)
          elif value == "get armor":
            print("Congratulation! You found an armor!")
            armor = Armor()
            player1.inventory.addArmor(armor)
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
            print(armor.getDetails()[3])
            print("Armor : ", armor.getDetails()[0])
            print("Durability : ", armor.getDetails()[1])
            print("Damage Reduction : ", armor.getDetails()[2])
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
            print("Equip Armor?\n⠄Yes\n⠄No")
            tanya = input("\n> ")
            if tanya.lower() == 'yes':
              player1.inventory.equipArmor(len(player1.inventory.armor)-1)
            else:
              continue
          elif value == "get weapon":
            print("Congratulation! You found a weapon!")
            weapon = Weapon()
            player1.inventory.addWeapon(weapon)
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
            print(weapon.getDetails()[4])
            print("Weapon : ", weapon.getDetails()[0])
            print("Head Damage : ", weapon.getDetails()[1].headDamage)
            print("Body Damage : ", weapon.getDetails()[1].bodyDamage)
            print("Leg Damage : ", weapon.getDetails()[1].legDamage)
            print("Bullet : ", weapon.getDetails()[2])
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
            print("Equip Weapon?\n⠄Yes\n⠄No")
            tanya = input("\n> ")
            if tanya.lower() == 'yes':
              player1.inventory.equipWeapon(len(player1.inventory.weapon)-1)
            else:
              continue
          elif value == "get heal":
            print("Congratulation! You found a consumable item!")
            consumable = Consumables()
            player1.inventory.addConsumable(consumable)
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
            print(consumable.getDetails()[2])
            print("Item : ", consumable.getDetails()[0])
            print("Heal Amount : ", consumable.getDetails()[1])
            print("\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n") 
          input("\nPress enter to continue ....")
      elif action.lower() in ['cheat weapon']:
        weapon = Weapon("Cheat Weapon")
        player1.inventory.addWeapon(weapon)
        speaker1 = "Mysterious Man: "
        cheatspeech = "Well... well... i guess you cant win without my help after all!! Fine, i will give you this, use it well."
        print(speaker1)
        for character in cheatspeech:
          sys.stdout.write(character)
          sys.stdout.flush()
          time.sleep(0.05)
        time.sleep(2)
        
        
        # player1.inventory.equipWeapon(0)
      elif action.lower() in ['inventory', 'view inventory']:
          lookInventory()
      

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
  # print(b)
  for character in b:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.005)
  time.sleep(5)
  
def title_screen_options():
  option = input("\n> ")
  if option.lower() == ("play"):
    menu()
  elif option.lower() == ("quit"):
    sys.exit()
  elif option.lower() == ("help"):
    help_menu()
  while option.lower() not in ['play', 'help', 'quit']:
    print("Invalid command, please try again.")
    option = input("\n> ")
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
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░          Welcome to text-based shooting game         ░")
  print("░                  Final Project KB 2022!              ░")
  print("░                        WarZone                       ░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Play ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Help ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Quit ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
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
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("           Please select an option to continue.     ")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Play ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Help ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░ Quit ░░░░░░░░░░░░░░░░░░░░░░░░░")
  print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
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
  naration1 = "You find yourself alone in an unfamiliar place and you hear a strange sound...."
  for character in naration1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  os.system('cls||clear')
  naration2 = "\nWHAT IS THIS SOUND?!!\nWHERE AM I??"
  for character in naration2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.001)
  time.sleep(2)
  os.system('cls||clear')
  naration4 = "\nYOU LOOKED BACK AND SEE A FIGURE APPROACHING YOU....\n"
  for character in naration4:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)
  time.sleep(2)
  #Leads the player into the warzone now!
  art1 = '''
⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢸⣷⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣷⣄⠄⠄⠄⠄⠘⢦⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠁⠄⡆⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣷⣤⠄⠄⠄⠄⠙⢿⣷⣤⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠄⠘⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠄⠢⣀⠙⢿⡿⠿⠂⠄⣀⣀⣀⠄⠄⠄⠄⠄⢠⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣀⠄⠄⠄⠄⠄⠄⠄⠄⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡈⠛⠄⠄⠄⠄⠈⠉⠄⠄⠐⠂⡒⠂⠄⠄⢻⣆⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣴⣿⠿⠿⣷⡀⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣤⡄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⣠⣶⣾⠿⣿⣿⣿⡆⣧⠈⣿⣷⡄⠄⠄⠄⡀⠄⠄⠄⢠⣾⣿⢏⣀⠄⢹⣷⡀⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⠙⠍⠄⠄⠄⠄⠄⠄⠄⠄⢠⣾⠏⠁⠒⠄⠄⠙⣿⡇⡱⠁⢸⣿⣿⣄⠄⠄⢳⣄⠄⠄⢸⣿⡿⠸⣿⣿⣾⣿⣧⠄⠄⠄⠄⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⣿⣿⡿⢿⣿⣿⣦⣤⡄⠄⠄⠄⠄⠄⠄⠄⣿⣿⡀⠄⠄⢀⣼⠿⡿⣼⣤⣴⣯⣿⣿⣿⣆⠄⢸⣿⣇⠄⢸⣿⣇⠄⠄⠻⣿⣿⣿⠄⠄⠄⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠋⠉⠄⠈⢿⣿⣿⣿⣿⡂⢁⠄⠄⠄⢰⣼⣿⣿⣷⣦⣈⣉⣡⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⡄⢸⣿⣿⣷⠄⠄⢸⣿⣿⠄⠄⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⢿⣿⣿⣿⣶⣦⣀⠄⠘⢿⣿⣿⡛⣿⣿⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⡿⠄⢀⣾⣿⠃⠄⠄⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢠⠔⠄⠐⠄⠈⣿⣿⣿⣿⣿⣿⣷⣷⣍⣹⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⣶⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠰⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣧⣀⣒⣋⠌⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠄⠄⢀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠃⠄⠙⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠙⠛⠋⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣥⡀⠄⠄⠄⠄⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⢄⠄⠄⠄⠄⠄⠄⠿⠛⠛⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⢧⣿⣿⡄⠄⠄⠄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⢂⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⠄⡄⠄⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠄⠂⠄⠄⠄⠄⠄⠄⠄⠄⢰⣿⣿⣿⠿⠟⣛⣿⡿⠟⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⢸⣿⣿⣿⣿⣿⠆⠾⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠄⠡⠄⠄⠄⠄⠄⠄⠄⠘⠛⣉⣤⣴⠿⠛⠁⠄⠄⠄⢀⣠⢄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠄⠄⠉⠄⠄⠐⠒⠒⡿⣶⣿⣶⣶⣶⣶⣦⣤⣤⡘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠉⠁⠄⠄⠄⣀⠠⣔⣾⣽⣿⣿⣿⣿⣿⡿⠿⠛⠉⠁⠄⠲⠂⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣄⢹⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠄⠄⠄⠄⠄⠄⠄⠄⠰⢒⣿⣾⣿⣿⣿⣿⣿⠿⠟⠉⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠒⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠇⠐⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠄⠄⠄⠄⠄⠄⠄⠘⠛⠋⠉⢸⡿⠟⠉⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⣻⣿⣿⣿⣿⣿⣿⣿⣿⡜⡀⠙⠻⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠤⠿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠄⢀⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠹⠿⠿⠿⠿⠿⢿⣿⣿⣦⡈⢿⣿⣿⣿
  '''
  art2 = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⡀⢀⠀⡀⢀⠀⠄⡀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⢐⢠⠡⣂⢪⢰⢰⢡⢢⢱⢨⢪⢐⢔⡐⡄⢅⢂⠌⠄⢅⢂⢂⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⡂⢅⢱⢸⢜⡮⣗⣧⡳⡵⣝⡮⣯⣳⣽⣺⢝⢮⡪⡮⡣⣇⢏⢮⢢⢣⢢⡑⡅⣅⢂⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢐⢀⠢⡌⡦⣳⢝⡷⣝⣟⡾⣽⣽⣳⣿⣽⣾⢷⣯⣯⣯⣯⣿⣽⢾⡽⣕⡯⡺⣜⢮⡺⣼⣲⢱⢠⠨⠠⠐⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠡⢑⢌⢪⢪⢪⣫⡺⣕⡯⣷⢯⣿⢿⣾⢿⣾⣿⣾⣿⣿⣾⣿⣿⣾⣿⣿⣽⣗⣯⢯⢮⣳⢯⣗⡯⣯⡺⣸⠨⡪⡐⡐⠡⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠄⢅⢂⠆⡕⡕⣕⢖⣝⢞⡮⣿⣽⣾⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣾⣿⣽⢾⣻⡯⣿⢽⣞⢽⡺⣜⡎⣇⢆⢕⠄⡅⡂⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢐⠠⠈⢔⠰⡰⢱⢱⢱⢝⣕⢯⡳⡯⣷⣻⣽⣿⣽⣿⣿⣿⣿⣿⣿⣿⣻⣿⣾⢿⡾⣗⣿⣻⣷⢿⣽⣟⡾⣝⣝⢮⢺⡪⡣⡣⡑⢌⠌⠌⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⡂⠅⡢⡑⡌⡆⢗⢝⢮⡪⣗⢯⢯⢷⣻⣞⣿⡾⣿⣾⣿⣟⣯⣷⣿⣿⣿⣟⣿⣿⣟⣿⣽⡾⣟⡷⡯⣻⣺⣺⡪⡧⣣⡣⡪⡪⢢⢱⠡⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠢⢑⢐⢑⢌⠪⡊⢎⢎⢎⢮⢫⡳⣝⣗⢿⣺⣟⣿⢾⣿⣻⣿⣟⣿⣯⣿⣟⣿⣽⣻⡽⣞⡿⡽⣯⢟⢗⢗⠵⠹⡘⢆⠣⠣⠡⠡⠡⠑⠁⠄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠌⠌⡂⡂⡂⠢⢑⠨⠨⠊⠜⢜⢎⢞⢜⢪⢳⢳⢝⡞⡯⣟⣯⣟⡯⣟⣷⣻⢽⡺⣕⢏⠯⡓⡍⢏⠪⠉⠊⠀⠀⠁⠀⠀⠀⠀⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠁⠀⠀⠀⠈⠀⠅⠑⠅⢇⢏⢞⢮⢳⢝⡕⡇⡗⢕⠅⠅⠅⠡⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠠⠡⠣⡣⡣⡣⢃⠅⠁⠀⠀⠀⠀⠀⠀⠀⠀⡄⣔⢔⠴⡰⡠⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⠐⠰⢤⠠⠐⠀⠀⠀⠀⠀⠀⠀⠡⢑⢕⢕⢜⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⡢⡫⠂⠀⠀⠈⠸⡽⡐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢌⢖⠈⠀⠀⠀⠈⢝⣦⢀⠀⠀⠀⠀⠀⠀⠀⠅⣳⡹⡜⢔⠀⠀⠀⠀⠀⠀⠀⠀⡬⣺⠀⠀⠘⠀⠀⠀⠕⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⡇⠀⠀⠈⠁⠀⢰⢫⠣⠀⠀⠀⠀⠀⠀⠀⠐⡜⡮⡫⡢⠂⠀⠀⠀⠀⠀⠀⠀⠉⠊⠑⠀⠀⠀⠀⠨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠄⠠⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠅⡇⡯⡪⡂⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢕⢕⢽⢕⢇⠆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠨⡪⡽⡽⡽⡵⡱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢅⢧⣫⢯⣿⢽⣣⢣⠡⠐⡀⠄⠠⠀⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⠀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠢⡣⡯⣯⣿⡽⡮⡇⡇⢅⢢⢡⢑⢱⢠⢡⠠⡨⠀⡂⢂⠐⡐⠠⡡⢌⢢⣑⢆⡆⡇⠄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠤⣱⣱⢔⣕⢥⡣⡱⣐⢄⢄⠄⢄⠠⢀⠠⡀⢂⠈⢀⠠⡐⢄⢕⢕⣽⣳⣽⡽⣯⣫⢪⢪⢳⢕⣕⢜⠜⡜⡜⡜⡴⡌⣆⢜⢔⢕⡜⣮⣳⢵⣳⡽⡼⡬⡠⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡀⣆⢯⡾⣽⣯⣯⡷⣯⢯⡮⣗⢵⢱⠱⡨⡐⠐⠀⠀⢀⠐⡌⡌⢆⢇⢷⢽⣷⣿⣿⣿⢾⡵⡕⣕⢕⣗⢵⢝⢜⢬⢢⢑⠹⡸⢸⣑⢷⢽⣺⣺⢽⣳⡿⣽⣺⢸⠠⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡐⡔⣵⣻⣽⢿⣞⣷⢿⣽⣻⢯⢗⢧⢓⢕⠐⠠⠡⡑⠄⢂⠌⡂⠊⠐⠈⢪⢯⢿⢝⡯⣟⡯⡏⠅⠑⠑⠕⠝⠕⣕⢷⢕⡆⡕⡘⢜⢜⢪⡳⣳⢽⢯⣷⣻⢷⣝⢮⢪⢈⠀⠀⠀⠀
⠀⠀⠀⠀⢐⢜⢜⣷⣻⢾⣻⣽⢯⣟⣗⢯⢳⢹⢨⢂⠂⡨⡸⣸⢸⡘⣄⣅⠪⡠⣀⢀⠈⢓⢝⡕⡯⡳⡝⡀⡀⣆⢆⢆⣢⣣⢯⣗⢷⢽⣸⢠⠀⡈⠂⢇⢳⠽⣽⣺⡽⡽⡮⡳⡑⠄⠄⠀⠀⠀
⠀⠀⠀⠀⢂⢪⢪⢞⣽⣻⡽⡾⣝⣞⢮⢪⠪⠂⠅⢀⠰⣕⢯⢾⡵⣝⡮⣞⡽⡮⡾⣜⣞⣆⢧⡣⣑⢍⢮⣪⣳⡳⣝⡮⣞⣞⣿⣺⡯⣗⡇⢇⢣⠢⡀⠄⠁⢫⢺⢪⢯⡫⡳⡑⠌⠌⠄⠀⠀⠀
⠀⠀⠀⠀⢂⢎⠪⡣⡳⣕⢯⡫⣺⢸⠸⠨⠈⠀⡀⡢⡣⣳⢯⢯⡯⣯⢯⣷⣻⣟⣿⣳⡿⣾⢿⣾⣯⢿⣻⡷⣷⣻⣗⣿⡽⡷⣯⢷⡯⣗⢝⢜⠜⡈⢢⠱⡐⡀⠈⠜⡜⡜⡕⡈⠨⠨⠀⠀⠀⠀
⠀⠀⠀⠀⢂⠢⡃⢕⢕⢕⢗⢝⢜⠬⠈⠀⡀⢂⠌⢜⢜⢼⣹⡳⣯⣻⢽⢾⢽⢾⡽⣷⣻⡿⣿⢷⡿⣟⣿⣻⡽⣯⢿⣞⣟⡯⣟⣟⢮⢇⠇⠇⠅⠌⡐⢑⠰⠨⠀⢡⢣⢪⠢⠀⠐⡈⠀⠀⠀⠀
⠀⠀⠀⠀⠪⡨⡂⠡⡊⡇⣏⢮⠣⡁⠀⠁⠊⢂⠑⡑⠌⡲⠱⡙⠮⡺⡹⡝⡯⡻⡽⣝⢷⣻⣻⣽⣻⢯⣟⡷⣻⢽⢝⢞⠎⠏⠎⠊⠊⠠⠁⠁⠁⠀⠀⠀⠀⠀⠠⢸⢸⢢⠑⠀⠐⠀⠀⠀⠀⠀
⠀⠀⠀⠈⢌⢆⢎⠀⠂⡕⣕⢇⢇⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠈⠐⠈⠀⠁⠁⠃⠃⠃⠃⠃⠁⡁⣀⠁⡀⠈⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⢄⢐⡵⣝⢎⠌⠀⠐⠀⠀⠀⠀⠀
⠀⠀⠀⠠⠑⢔⢕⠠⠀⠕⠵⣝⢮⡢⡀⠀⠀⠀⠀⠀⠠⠀⡀⠀⢡⣢⡀⢲⢧⡡⠀⣜⣾⣽⣾⣤⢀⠰⣴⣳⣟⣷⣇⢐⣁⡮⠀⣐⠬⠀⠄⠀⠀⠀⠠⠀⣐⣕⣗⢽⡺⡨⠀⠐⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠡⢡⠣⡡⠀⠈⢪⢪⣳⢽⡪⡀⠀⠠⠀⠀⠀⠀⠈⠀⠠⡫⡊⢜⢿⣯⠂⡼⣿⣿⢾⣯⡣⣻⣿⣿⣿⣿⣞⠼⡿⡝⠠⡻⡭⠀⠀⡀⠀⠀⢠⢸⣪⣗⣯⢳⢑⠀⠀⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠂⡑⢜⠄⠈⠀⡣⢯⣳⢯⣺⡐⡀⠀⠐⠜⠀⣤⢀⠠⠈⠀⠀⡙⠯⠅⠺⡯⡿⡿⣻⢌⢞⢿⡽⣞⡿⢎⠂⡁⡡⠀⢘⠀⠠⠐⠀⠠⡨⣮⣺⣗⣟⢞⠌⠀⠠⠨⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠄⠣⡑⠅⠀⢈⢳⡽⡯⣞⣮⡢⡁⡀⠀⠐⠈⠠⢹⠱⠀⡓⡦⡈⣆⣆⡌⢄⣁⢆⡁⡈⣑⢉⠨⡨⣢⢀⢢⡣⡃⠃⠃⡀⠄⡢⣫⣟⣾⣳⣻⢮⢇⠃⠀⠌⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠐⠈⠌⠀⠀⢘⢞⣽⣳⣳⢯⣎⢆⡂⠀⠀⠀⠀⠁⠀⠑⠘⠐⠐⡟⡏⡂⢯⢗⠅⠪⡿⡳⠀⠝⠊⠂⢁⢈⠠⠠⡁⡆⡵⡽⣷⢿⣽⡺⡮⡳⡑⠀⠁⠄⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠄⠀⠀⢑⢗⣟⣞⡷⡽⣕⡧⣇⢆⡢⡐⡠⢐⠠⠠⡐⠠⡀⡂⠔⢠⠡⡢⡑⡔⡔⡕⣕⢭⢫⢪⢣⡱⣱⣱⢵⡯⣟⣿⣻⡺⣝⢝⠕⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠣⡳⡽⡽⡯⣗⡯⣯⣗⡯⣞⣼⣲⢕⡧⣣⡳⣕⢕⣝⢎⣗⡳⣝⢮⡳⣝⢮⣺⡪⣯⡳⣯⣗⣯⡿⣽⣗⣗⢗⢝⠜⠨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠪⡹⡹⣝⢵⣫⣗⣯⢿⣽⢾⣞⣯⣯⢷⣻⢮⡯⣞⣷⣳⣯⡿⣽⢾⣽⢽⡮⣟⣮⣟⣷⣻⣞⡯⣗⣗⢵⢙⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠈⢌⠜⡎⣞⢞⣞⣯⢿⣻⣽⡷⣟⣯⣿⢯⣿⣯⣿⣿⣷⣿⣿⣿⣯⣿⣻⣽⢾⡽⣞⡷⣯⣻⡪⡊⡂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡁⢊⠪⡺⡪⣟⡽⣯⢷⡿⣟⣿⡾⣿⣷⣿⣿⣿⣿⣿⣿⣷⣿⣿⣯⣟⣯⢿⡽⣯⡳⡱⠡⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠪⢪⢪⢯⡻⡽⡯⡷⣟⣿⢾⣟⣿⣿⣿⣻⣿⡿⣷⢿⡾⣽⡺⡯⡺⠸⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠠⠑⠱⠹⡹⡹⡝⣞⢯⢿⢽⡾⣿⣟⡯⣟⢯⢟⢮⢳⠹⢘⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠐⠈⠨⠘⠨⢓⢍⠳⡙⠮⡚⡎⢎⠳⡑⡑⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⠀⠐⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  '''
  os.system('cls||clear')
  print(art1)
  naration5 = "SLOWLY BUT GETTING CLOSER....... AND CLOSER...."
  for character in naration5:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)
  time.sleep(2)
  os.system('cls||clear')
  print(art2)
  time.sleep(3)
  speaker1 = "Mysterious Man: "
  print(speaker1)
  question1 = "HAHAHA no need to be afraid buddy. What is your name?\n"
  for character in question1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  player_name = input("\n> ")
  print()
  player1.name = player_name

  print(speaker1)
  question2 = "My dear friend " + player1.name + ", how are you feeling? You look messed up\n"
  for character in question2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  feeling = input("\n> ")
  print()
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

  print(speaker1)
  question3 = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
  for character in question3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)

  speech3 = "I bet you don't know where you are now.\n"  
  speech4 = "Well... look around you!\n"
  art = '''
  ⠄⠂⢀⠄⠄⡠⠄⠄⠠⠄⠄⡀⠂⡀⢀⠄⡀⢐⠄⡂⡐⠔⡀⡀⡢⠂⡂⠄⠄⠄⠄⢀⠄⢔⠄⡈⡂⠄⠄⡐⠠⢈⠢⢊⢄⢃⠢⡈⠔⠠⠐⠄⡀⡀⢂⠄⠄⠄⠄⢀⢀⠄⠄⠄⢀⠄⠠⠄⠄⡀⠄⠄⠄⠄⠄⠠⢀⠄⢀⠄⠠⠄⡀⠄⠄⠄⢀⠄⡀⠄
  ⠠⠁⠄⠂⡁⠐⠄⠐⠄⠌⠠⠄⠠⠄⠄⠄⠂⢀⢂⠐⡈⡂⡂⡂⢌⠐⠄⢀⠈⠄⡁⠄⠄⡑⡀⡐⠨⡘⢄⠕⡁⢢⠣⢡⠢⡑⡨⡀⠅⡂⠨⢀⠄⢂⢂⠂⡀⠁⠄⠂⢀⠄⢁⠠⠄⠂⠠⠐⠁⠄⢀⠐⠈⠄⢈⠄⠠⠐⡀⠄⠈⠄⢀⠄⠁⠄⢀⠐⠄⠄
  ⢈⢐⠈⠄⡂⢈⠄⢈⠠⢁⠨⠄⠡⢐⠄⠌⢈⢀⢂⢂⠂⡐⠐⠄⢁⢀⠂⢀⠄⢁⠄⠌⠄⡎⢄⢨⢐⠐⡅⢣⠢⢑⠕⠥⡑⡑⢔⠠⢅⢂⠅⢌⠈⠄⡁⠄⠐⠈⠠⠐⠄⡐⠄⠄⠂⢁⠠⢀⠂⡈⠄⠄⡀⠂⠄⠄⠐⠄⠂⢂⠈⠄⠄⠄⠐⠈⠄⠄⢀⠄
  ⢐⠐⡈⠄⢂⠄⠠⠠⠨⠄⡂⠡⠈⠠⡀⠅⠄⠠⠠⠠⠨⡂⠡⠨⡐⠔⠈⠄⠐⠄⠄⠂⠡⡌⡐⢠⢣⢊⢜⠬⣊⢲⡱⡑⡜⡌⡢⢑⠔⡠⠡⠂⢌⢐⠄⠆⡁⠡⠨⡈⠌⡐⢐⠠⢈⠠⠠⠄⠄⠠⠄⢁⠄⠠⠈⢀⠐⠄⠠⠄⢀⠄⠁⡀⠂⠄⢀⠠⠄⠄
  ⠠⡁⡂⠈⠄⠂⠠⠐⠨⠄⠔⠠⠁⠅⢂⢂⠊⡨⡊⠌⢂⠄⡃⡣⠢⠣⢁⠈⠠⠁⡐⢈⠰⢬⢂⠢⠭⢌⠆⡎⡆⣗⡣⡫⡢⡕⡜⣔⠥⡪⠨⡨⡰⢄⢧⡢⠠⢁⠅⠄⠡⠢⠄⠆⠠⠐⢀⠒⡐⠄⢈⠄⠠⠐⠄⠄⠄⢈⠠⠄⠠⠄⠂⠄⠄⠄⠄⢀⠄⡀
  ⠨⡀⡂⠡⢈⠄⠄⠨⠨⠈⠄⡡⠨⠈⠄⡂⡐⢐⢅⢅⠢⢑⢐⢕⡙⢌⠄⠌⠐⢐⠄⡂⢒⠦⢌⢘⡱⠱⣡⢳⡱⡪⡎⣗⢭⢮⡪⡲⡱⡡⡝⡮⣋⡷⢏⢆⠡⠨⡂⠅⡡⠡⡁⡊⠄⠌⠄⢌⢢⠈⢀⠐⠄⠂⡁⠐⠈⢀⠠⠈⡀⠄⠂⠈⢀⠄⠄⠄⡀⠄
  ⢐⢐⠠⠁⡂⠄⠄⢂⠡⢈⢂⠐⡈⠄⡁⡂⡐⠰⡈⡢⢑⢌⢊⢖⢰⠱⠄⠌⠠⢁⠢⡈⢄⢝⢜⢜⣝⣵⣲⢵⣹⣪⢯⢾⢽⢵⢭⣳⢽⣝⢽⣺⣻⡪⣟⡥⠡⡱⡠⡑⡔⡭⡂⡂⢨⠐⡅⡑⡐⡐⠄⠄⠁⠄⠠⠁⠅⠠⠄⢂⠠⠠⠐⠈⠄⠄⢀⠠⠄⠄
  ⢐⢐⠠⠁⡂⠄⠂⡐⢈⠄⡐⡀⢂⠡⢐⢐⠨⡈⠆⡊⡢⠂⡂⡅⡆⡧⠁⠌⡐⡐⢢⠂⢍⡚⣌⢧⣻⣺⡾⣽⣺⣺⡿⣟⣿⢯⡿⣾⣟⣾⣟⣾⢷⣟⣧⠪⢌⢆⢞⣆⢳⢐⠬⠢⡂⡕⡕⡱⡰⡁⠂⠄⢁⠐⠈⡌⢌⢂⠡⠐⡀⢂⠌⢀⠁⡈⠄⡀⢂⠐
  ⢐⠐⠄⡑⡀⢀⠁⡐⢀⠂⡐⡀⡂⢌⢂⠂⠅⡌⡊⡂⠢⠢⣑⢭⢸⡘⡈⡐⡐⠨⡂⢅⢵⢝⢺⢲⡕⣯⣟⣿⣳⣿⣿⣿⣿⡿⣿⣻⣯⢷⣿⣾⡿⣯⣯⢣⠣⣯⣟⢮⡪⡳⡱⡑⡕⡕⡵⡱⡱⡑⡈⠄⠂⡈⠄⡂⠕⡐⡑⢌⢂⠢⢈⠄⡂⠠⠄⠐⠠⡁
  ⠔⠅⡁⡂⠄⠄⠄⠌⡐⠨⢐⢀⢂⢂⠢⠨⠈⢌⢢⢢⢱⢩⢪⡺⠜⡨⡰⠐⠌⢔⠨⠢⣕⠝⡧⣗⣿⣽⣾⣿⢿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⡾⡪⡪⣷⡯⡧⣣⢳⣣⡣⣳⡹⣜⠮⠝⠆⢐⠄⠡⠐⡀⢇⢣⢱⢘⢔⢑⢌⠢⡂⡢⠐⠄⡁⢂⠢
  ⢕⠅⠢⡂⠅⠐⢈⢐⠄⢅⠢⠐⠄⠅⡊⠌⢌⠢⣑⢕⢜⠼⠜⡨⡪⡱⠠⠡⢑⡐⡝⢌⣎⣿⢮⣳⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⡞⡜⣜⣝⣿⡿⣜⣿⣵⣻⣜⢮⣳⠭⡫⡌⠄⠨⢀⠡⠐⡕⡕⡕⡕⢜⢌⢆⢕⢌⢢⠁⠄⠐⢐⡑
  ⢕⠅⢕⢌⠐⠈⠄⡢⠊⠔⠡⡁⡅⠌⠢⡁⠆⢕⢜⠜⡎⡡⡮⠣⡉⠄⡑⠡⢢⠡⢍⢲⣹⣿⡷⣭⣳⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣾⡯⡪⣎⣿⣿⡿⡵⣿⣷⣷⣯⣻⣺⣽⢯⡇⢌⢐⠐⡠⢁⢇⢇⢯⢪⢪⡪⡢⡱⡱⡱⠌⢐⠈⡐⡑
  ⢕⠅⡅⡢⠈⠄⠅⡢⠡⡑⢅⢊⡪⢘⢌⠢⡑⡱⡑⠅⡂⡔⣖⢯⡺⡇⠠⠡⠥⡡⢱⢑⣝⣿⡯⣟⣿⣿⣷⣟⡿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⡿⣯⡪⣞⣾⣿⡿⡽⣿⣿⣿⣗⣗⣿⢾⣿⡇⠅⡂⡂⡂⡂⣕⠹⢱⢕⢧⡳⡱⡱⡸⣜⢕⢀⠂⠌⢮
  ⢕⠕⡕⣐⠡⠈⠔⡜⢌⢮⢑⢕⠮⠰⣅⠅⡎⢪⡲⣪⣎⣞⡾⡵⣝⡆⠡⠨⢑⠌⡢⢱⢹⢳⡯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⡿⣿⣿⣣⡳⣵⢿⣿⡿⡽⣿⣿⣿⣗⣗⣿⣟⣶⡇⠕⡐⡐⡐⡐⢕⣙⡲⡱⣕⢳⢱⢱⢱⢱⡢⠂⠌⠨⡪
  ⢕⠅⡇⡢⢂⠡⢁⢝⢔⢕⢕⢵⡏⣕⢵⠡⡢⣫⡯⡮⣞⡾⣯⢯⣬⡄⠅⠌⡐⠔⡈⡆⡲⣥⡫⢷⣿⣿⣿⣯⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⡪⣞⢞⣿⣿⣿⢽⣿⣿⣿⣧⢯⣿⢮⣿⡇⢕⢐⢐⢐⠨⣘⠼⣺⣪⡲⡽⣸⢸⢜⢮⢌⠌⠨⠐⢬
  ⡱⡡⢕⠌⡀⡢⠡⡳⡱⡹⡸⣕⢗⢜⢾⢸⢸⣪⡯⣯⣳⡟⣟⣽⢾⠡⢈⠨⠢⡑⢐⢰⢘⣻⢽⢦⡛⣽⣿⣯⣷⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⢿⣺⡪⡯⣿⣿⣿⡽⣽⣿⣿⣯⡷⣿⣟⣟⣏⢢⢑⢐⠌⡢⠸⢝⢾⣜⢾⣝⢮⡪⡮⣪⢧⠨⠨⡈⡢
  ⡪⠌⡢⡑⡐⢌⠜⡔⣎⠮⡣⣳⡣⣫⢧⢣⡳⣽⢚⣵⣳⣿⡿⣹⣸⠈⠄⡨⢐⢐⢐⠐⡕⣿⢷⣭⣯⣳⡝⣿⣟⣿⣿⣿⣿⣟⣿⣿⣿⣿⣯⣿⣿⣿⣺⡪⡯⣿⣿⣯⣟⣿⣿⣿⣿⢽⣻⣽⣿⡧⡣⡱⡐⡑⢌⢊⢷⣺⣼⡳⣯⢷⢝⡮⡺⣱⠨⡊⠔⠸
  ⡪⢸⠰⡁⡪⡂⡇⣇⢧⣫⢳⠵⣹⢜⢵⢱⢩⣪⢯⣗⡞⢔⣭⢶⠾⡀⠅⡊⠄⢢⢂⢑⢸⣿⣟⣾⡿⣿⣿⣗⣯⣟⣿⣿⣿⣽⣾⣿⣿⣿⢿⣿⣿⣿⣪⡺⣝⣿⣿⣿⣽⣾⣿⣿⣿⣻⢿⣻⣽⡷⡱⡱⡘⡌⢎⢪⢹⣻⡾⡽⣽⢽⢵⢯⢯⠾⡐⢌⢊⢊
  ⠪⠢⡃⡊⡢⡃⣅⢗⢗⢕⡧⡟⡮⡫⡵⣪⣳⡻⣋⡵⢞⣻⣽⢗⡍⠨⠐⡀⡊⠔⡁⡢⠱⡹⣗⣽⣿⣿⣿⣿⣻⣿⣷⣿⣿⡿⣾⣿⣿⣿⣿⣿⣿⡿⡮⡺⣜⡿⣿⣿⣾⣻⣿⣿⣿⣻⡿⣿⣿⣟⢜⢔⢕⢜⢌⢆⢏⣿⣽⢽⡽⡽⣝⡽⣪⢯⠐⢅⠢⡑
  ⠨⠨⡂⢕⢘⢜⢔⢗⢝⣓⢝⢕⠵⢫⢕⡱⡡⡮⣗⣟⣟⢿⣱⣿⠃⠅⢂⠂⡂⠅⣢⢑⠥⣫⣛⢽⣟⣯⣿⣻⢿⣻⣿⣟⣿⡿⣟⣿⣟⣿⣻⣟⣿⡯⣏⢯⢮⢿⣻⡿⣾⣻⣿⣽⣯⢿⣻⣟⣯⣗⢕⢕⢜⢜⢔⢢⢚⢾⢽⢽⢽⢽⢮⢯⡳⣝⠨⡂⡑⠄
  ⠈⠔⠨⠠⡃⠢⡑⢜⢘⢜⢐⠕⢍⠪⡊⢎⠎⡎⡎⡆⡗⢝⢵⠹⠠⢁⢂⢂⠂⡅⢅⠊⢎⠸⣲⢱⡪⡳⡫⢽⢽⡺⡽⢽⢳⢻⢫⢯⢫⡻⡝⡝⡗⡻⡪⢯⢫⠯⠯⡯⡫⢗⢯⢺⢺⡫⡯⣫⢻⡪⡪⡪⡪⡊⡎⡎⡎⣎⢕⠭⡫⡣⢫⠪⡪⡢⡑⣑⠨⡑
  ⠄⡁⠈⠄⢂⢁⠂⡂⡂⡂⡂⢌⠢⠑⠌⠢⢑⢑⢘⠨⠪⡘⢜⠨⠨⠐⡐⡐⡐⠄⣃⠱⢱⢘⠜⢌⢊⢎⠪⠢⡃⢎⠪⡱⢱⢱⢱⢱⢱⢡⢣⢑⠕⡌⡪⡘⠔⢅⢃⠪⡨⢊⢌⠪⡊⢎⢎⠎⡎⢎⠎⠇⢇⠇⢇⠇⢇⠣⡑⢕⢘⠌⠪⠨⢂⠢⠑⠄⡃⠌
  ⠄⠠⠈⡀⢂⠄⡂⢐⠄⡂⢐⠐⢈⠈⡈⠈⠄⠂⡐⠈⠄⢂⠂⠌⠄⠅⡂⠢⡈⠆⠢⡡⢃⠢⡑⡑⢔⠐⠅⢕⠨⢐⠡⠂⢅⠢⢂⠕⡐⡐⠅⠅⢕⠡⢊⠌⡊⠔⡡⠑⢌⢂⠢⠑⢌⠐⢄⢑⠨⢐⠨⢈⠂⠌⡐⠨⠐⡈⢐⠄⢂⠨⠈⠐⠠⠈⠄⠁⠄⠂
  ⠄⠄⠂⠄⠄⠠⠄⠄⠠⠐⠄⠐⡀⠐⢀⠁⠄⠡⠄⡁⠂⠡⠈⠄⠡⠁⠌⡐⠠⠁⠅⢂⠡⢈⠐⡈⠄⠡⠁⡂⠌⢐⠈⡈⠄⡈⠄⢂⠐⠠⢁⠁⡂⠌⢐⠈⡠⠁⠄⡁⠂⠄⠨⠈⠠⠈⠄⢂⠐⢐⠄⢂⠈⠄⠐⢀⠁⠠⢀⠈⡀⠠⠈⡀⠂⠐⠄⡁⠄⠂
  ⠄⠈⠄⠐⠄⠄⠄⠐⠄⠐⠈⠄⠄⡈⠄⡀⠄⠂⠄⠄⠈⡀⠂⡈⢀⠂⢁⠄⢂⠁⠐⡀⠐⡀⠔⠠⠈⠄⢁⠐⡈⠄⢐⠄⢂⠐⢈⠠⠈⡐⢀⠂⡀⠂⡂⢐⠄⠅⠠⠐⠈⡀⠂⡁⠌⠐⢈⠄⡐⢀⠈⡀⠐⢀⠁⠄⠐⠄⠄⠂⢀⠐⠄⠠⠄⠁⠄⠠⠈⠄

  '''
  speech5 = "Yes! You are now in the middle of the forest and it seems your friend left you here.\n"
  speech6 = "I can't stay for too long. You looks like a good person. Here, take my backpack and go before they catch you.\n\n"
  speak1 = "THEY? WHO?\n\n"
  speech7 = "It seems this is where we must part, " + player1.name + ".\n" + "Goodluck "+ player1.name + "!\n\n"
  speak2 = "WAIT DON'T GO!\n\n"
  
  for character in speech3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)
  for character in speech4:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  time.sleep(2)
  os.system('cls||clear')
  print(art)
  time.sleep(1)
  print(speaker1)
  for character in speech5:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speech6:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speak1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.2)
  time.sleep(1)
  print(speaker1)
  for character in speech7:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speak2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.2)
  time.sleep(2)
  main_game_loop()

def killedByBossText():
      print("⣛⠛⢻⡿⠛⠋⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠈⢉⣿⠋⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⠉⣉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠉⠉⢸⡏⠁⢰⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿")
      print("⣿⡄⠈⠃⢠⣼⣿⣿⡿⠿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⠄⢨⣿⠄⠄⣿⠟⠛⠛⢻⣿⠟⠋⠉⣹⣿⣿⣿⡅⠄⠁⢠⣿⡿⠛⠻⣿⣿⠟⠛⢻⣿⠛⠛⠿⠿⢿⣿⣿⣿⠄⠐⠷⣦⢸⡇⠄⢸⡿⠛⠛⠛⣿⣄⠼⡛⠛⡻⠿⠿")
      print("⣿⣿⡇⠄⢸⣿⣿⠄⣤⢀⠄⣷⠄⢸⡀⠄⣿⣿⣿⣿⠄⢠⣄⠄⠄⡟⠄⣾⠆⠸⣇⡀⠉⠁⣿⣿⣿⣿⡇⠄⣶⠄⠉⠄⠼⣂⣘⡇⠠⢟⣀⢹⠄⠄⣤⠄⢸⣿⣿⣿⠷⣶⣄⠄⠙⡇⠄⢸⠃⢰⣿⠄⢿⠄⠐⡇⠄⣠⡀⠄")
      print("⣿⣿⡇⠄⣼⣿⣿⠄⠿⠿⢀⣿⡀⠈⠄⠄⣸⣿⣿⣿⠄⣸⣿⡅⡄⣷⢋⣴⠦⠄⡇⠈⠙⠄⣸⣿⣿⣿⣇⢀⠄⣴⣦⡀⠛⠄⠄⣇⠘⠛⠄⢸⠄⠄⣿⠄⢸⣿⣿⣿⡇⠄⡀⠄⢠⡇⡄⢸⡞⢩⣶⠄⢸⠄⢰⡇⠄⢸⡇⠄")
      print("⣿⣿⣷⣵⣿⣿⣿⣦⣰⣴⣾⣿⣿⣶⣸⣦⣿⣿⣿⣿⣷⣿⣿⣷⣿⣿⣶⣤⣶⣨⣿⣤⣶⣿⣿⣿⣿⣿⣿⣼⣷⣿⣿⣿⣶⣤⣼⣿⣷⣶⣴⣾⣶⢰⣿⣶⣼⣿⣿⣿⣧⣴⣧⣾⣾⣿⣷⣼⣷⣦⣴⣆⣼⣶⣼⣧⣦⣾⣷⣄")
      print("                                                                                                              ")
      print("                                                                                                              ")
      print("           ⣿⡟⠁⠄⠉⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠄⠉⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿                      ")
      print("           ⡿⠁⢠⣼⡄⠄⢹⣿⡿⠿⢿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⡟⠄⢠⣤⠄⠄⢸⣿⣿⠿⣿⠿⠿⣻⣿⣿⢿⣿⣿⣿⣿⣿⢿⡿⣿                      ")
      print("           ⡅⠄⡼⡿⠧⠾⢿⠏⠄⣠⡄⠸⣿⡆⠄⠉⠙⠋⠄⠄⠍⣿⠋⠄⣤⠄⠹⣿⣿⣿⣿⣧⠄⢸⣿⡞⠄⢸⣦⠄⠄⣿⠄⢰⡿⠉⠠⣤⠄⢹⣯⠄⠄⠈⠄⢸                      ")
      print("           ⡇⠄⠻⣄⡄⠄⢸⢀⣤⠿⠛⠄⢹⡇⠄⣸⠄⠄⢿⡇⠄⡟⠄⢈⣡⠤⠤⢿⣿⣿⣿⣇⠄⠈⠛⠁⠄⣾⣿⣧⠄⠁⢀⣾⡇⠄⣈⣩⠤⠤⣿⣆⠄⢰⣿⣿                      ")
      print("           ⣧⡀⠄⠄⠄⠄⣾⡋⠤⡾⠗⠄⢸⡇⡄⣿⡇⣠⣸⡇⡆⣷⣄⠈⠋⢀⡀⣼⣿⣿⣿⣿⣄⢀⢀⣠⣶⣿⣿⣿⡆⠄⢸⣿⣧⣀⠈⠋⠄⠄⣿⣏⠄⢀⣿⣿                      ")
      print("           ⣿⣷⣷⣷⣾⣇⣿⣿⣦⣤⣾⣆⣼⣷⣷⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣼⣧⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣴⣶⣿⣷⡇⣾⣿⣿                      ")

def gameDrawText():
  print("⣿⣿⣿⠿⣿⣿⣿⣿⣿⠛⠛⠛⣿⣿⠛⣿⣿⣿⣿⡿⠉⢹⡟⠛⠋⠉⠉⢹⣿⣿⣿⣿⠛⠻⢿⣿⣿⣿⣿⡛⠛⠛⠿⢿⣿⣿⡟⠛⠛⢹⣿⠿⢿⣿⣿⣿⣿⣿⠛⢻")
  print("⡿⠛⠄⣀⡀⠘⣿⣿⣿⠄⠄⠄⢻⣿⠄⠘⢿⣿⣿⠃⠄⢸⡇⠄⢰⣶⣿⣾⣿⣿⣿⣿⠄⢠⣀⠄⠛⢿⣿⠄⠄⣤⣀⠄⢹⣿⠃⠄⡀⢸⣿⠄⠸⣿⡟⢻⣿⡿⠄⢸")
  print("⡇⠄⣸⣿⣇⣀⣸⣿⡇⠄⡀⠄⢸⣿⠄⠄⠈⢿⠉⠄⠄⢸⡇⠄⢸⣿⣿⣿⣿⣿⣿⣿⠄⢸⣿⣶⠄⠈⣿⠄⠄⣿⡿⠄⢸⣿⠄⢰⡇⠈⣿⡀⠄⣿⠇⠈⣿⠃⠄⣾")
  print("⡇⠄⣿⣿⣿⠿⢿⣿⠁⠄⣷⠄⠄⣿⠄⢠⡄⠄⠄⡆⠄⢸⡇⠄⠙⠛⠛⣿⣿⣿⣿⣿⠄⢸⣿⣿⠄⠄⣿⠄⠄⠟⠁⢀⣿⡟⠄⣾⡇⠄⢿⣧⠄⠚⠄⠄⠸⠄⢸⣿")
  print("⡇⠄⣿⣀⡀⠄⢸⡿⠄⠈⠉⠄⠄⣿⠄⢸⣿⡀⣰⣇⠄⢸⡇⠄⢰⣶⣾⣿⣿⣿⣿⣿⠄⢸⡿⠉⢀⣼⣿⠄⠄⠄⠄⣿⣿⠁⠄⠉⠁⠄⢸⣿⠄⠄⢰⡆⠄⠄⣾⣿")
  print("⣧⠄⠘⠟⠃⠄⢸⠇⠄⣶⣶⡆⠄⢻⠄⢸⣿⣿⣿⡏⠄⢸⡇⠄⠈⠉⠉⣿⣿⣿⣿⣿⠄⠈⠄⣤⣿⣿⡇⠄⠄⣦⠄⠘⡏⠄⢠⣶⣶⠄⠄⣿⡄⢀⣾⣧⡀⢠⣿⣿")
  print("⣿⣿⣤⣤⣄⣀⣸⣿⣿⣿⣿⣷⣶⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣾⣿⣿⣿⣿⣷⣶⣶⣿⣦⣴⣾⣿⣿⣿⣿⣶⣿⣿⣿⣾⣿⣿⣧⣾⣿⣿")

def defeatText():
  a = '''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡀⡀⡀⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢄⠄⢄⠤⡰⡠⡔⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣰⢵⠻⠹⡑⢑⠵⣳⣵⣢⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢴⣿⢞⠃⠁⠀⠁⠀⠈⡈⠳⣕⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣔⣽⡿⡉⠂⠈⠀⠀⠀⠀⠑⢝⣿⡺⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢮⣟⡟⠔⠀⠀⠀⢀⠀⠀⠀⠀⢳⢷⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢬⡲⡽⣟⠎⠀⠀⠀⠠⠀⠀⠀⠀⠐⢸⢝⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢎⢞⢌⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣻⣳⠅⠀⠀⠀⠀⠀⠀⠀⢀⢐⢜⢼⢝⣿⣯⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢸⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢈⠪⡪⠀⠀⠀⠀⠀⠀⠀⢀⠐⣜⢾⢝⠍⠄⠀⠀⠀⠀⠀⠀⠀⠈⠌⢪⢫⢷⣟⡧⡁⠀⠀⠀⠀⠀⠀⠀⢄⢇⢕⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡈⠪⡀⠀⠀⠀⠀⡀⠄⡪⠘⠈⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠘⠪⠻⡘⠄⠐⠀⠀⠀⢀⢌⢎⠎⠂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠁⠀⠁⠠⠐⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠂⠁⠈⠀⠁⠀⠂⠑⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠐⠀⠀⠂⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⢄⠀⠠⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢢⢢⡲⡱⡰⣽⢿⢵⢨⢾⣽⣎⢂⢔⣕⢄⠄⡢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⢀⠪⡳⡽⣝⢾⡽⣯⡳⡱⣻⣗⡷⡡⣳⢳⢕⢌⢎⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠙⠈⠃⠉⡃⠃⢉⠚⠪⠩⠀⠑⠙⠐⠀⠂⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⡀⠑⠌⢄⢢⠀⢄⠄⢀⢀⠄⡀⢄⠀⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠀⠑⠡⠑⠍⠐⠜⠌⠜⠜⠐⠐⡈⠀⢀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠠⠂⠀⠐⠈⠀⠀⠀⠂⠄⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  '''
  print(a)
  naration5 = "HA.. HA... HA.... YOU ARE NOT GOOD ENOUGH TO DEFEAT US.\n You will be trapped and continue to suffer until death"
  for character in naration5:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.1)
  time.sleep(4)
  os.system('cls||clear')
  print('''
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀
  ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⣶⡆⠀⣰⣿⠇⣾⡿⠛⠉⠁
  ⠀⣠⣴⠾⠿⠿⠀⢀⣾⣿⣆⣀⣸⣿⣷⣾⣿⡿⢸⣿⠟⢓⠀⠀
  ⣴⡟⠁⣀⣠⣤⠀⣼⣿⠾⣿⣻⣿⠃⠙⢫⣿⠃⣿⡿⠟⠛⠁⠀
  ⢿⣝⣻⣿⡿⠋⠾⠟⠁⠀⠹⠟⠛⠀⠀⠈⠉⠀⠉⠀⠀⠀⠀⠀
  ⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⣀⢀⣠⣤⣴⣤⣄⠀
  ⠀⠀⠀⠀⣀⣤⣤⢶⣤⠀⠀⢀⣴⢃⣿⠟⠋⢹⣿⣣⣴⡿⠋⠀
  ⠀⠀⣰⣾⠟⠉⣿⡜⣿⡆⣴⡿⠁⣼⡿⠛⢃⣾⡿⠋⢻⣇⠀⠀
  ⠀⠐⣿⡁⢀⣠⣿⡇⢹⣿⡿⠁⢠⣿⠷⠟⠻⠟⠀⠀⠈⠛⠀⠀
  ⠀⠀⠙⠻⠿⠟⠋⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  ''')

## nanti aku bikinin text nya masih binggung mau ditulisin apa
def findBossText() :
  a = ("Something seems to have changed. Looks like I'm closer to something bigger...\nhmmm....")
  for character in a:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  time.sleep(2)
  # print(" ⣿⠛⣿⣿⡟⠛⠋⠛⡟⠛⠛⠛⣿⠉⣿⣿⠟⠉⠻⣿⣿⣿⣿⡿⠟⠛⢻⡟⠛⣿⠻⣿⣏⠄⣿⡛⠛⠻⣿⣿⣿⣿⡿⠛⠛⠛⢻⣿⡟⢻⣿⠛⠛⠙⣿⣿⣿⣿⠛⠛⠻⣿⣿⣿⠟⠛⢻⣿⣿⠟⠉⢿⣿⣿⠟⠉⠻⣿")
  # print(" ⣿⠄⣿⣿⡇⠄⣿⣿⣷⡆⠄⣿⣿⣤⣿⠁⠰⣦⣠⣿⣿⣿⣿⡇⢰⣶⣾⡇⢠⣿⠄⠸⣿⠄⣿⠇⢰⣦⡈⢻⣿⣿⣷⡆⠄⣿⠉⣽⡇⢸⣿⠄⣿⣿⣿⣿⣿⣿⠄⣶⡄⠘⣿⠃⢠⣦⠄⣿⠃⠰⣦⣠⣿⡏⠠⣶⣠⣽")
  # print(" ⡏⠄⣿⣿⡇⠄⠿⢿⣿⡇⠄⣿⣿⣿⣿⣦⣤⡀⠙⢻⣿⣿⣿⡇⢸⣿⣿⡇⢸⣿⠄⠄⢻⠄⣿⠄⣸⣿⡇⢸⣿⣿⣿⡇⠄⡟⠄⣿⡇⢸⣿⠄⠿⠿⣿⣿⣿⣿⠄⠿⠁⣸⣿⠄⣿⣿⠄⢻⣧⣤⡈⠙⢻⣷⣤⣀⠉⢻")
  # print(" ⡇⠄⣿⣿⡇⠄⣶⣾⣿⡇⠈⣿⣿⣿⣿⠋⢩⣿⠂⢸⣿⣿⣿⡇⢠⣤⣼⡇⢸⣿⠄⢰⡀⠄⣿⡄⠹⠋⣠⣿⣿⣿⣿⡇⠈⣧⠄⣤⡄⠸⡿⠄⣶⣶⣿⣿⣿⡟⠄⣤⣄⠉⣷⠄⢻⡿⠄⣿⡏⢹⣿⠄⢸⡏⠉⣿⡇⢸")
  # print(" ⣇⣀⣠⣼⣇⣀⣁⣸⣿⣇⣀⣿⣿⣿⣿⣧⣈⣉⣠⣾⣿⣿⣿⣇⣸⣿⣿⣇⣸⣿⣠⣼⣿⡄⣿⣀⣤⣾⣿⣿⣿⣿⣿⣇⣀⣗⣀⣿⡇⢸⣇⣀⣈⣀⣿⣿⣿⣏⠄⢉⣁⣴⣿⣦⣀⣁⣴⣿⣧⣈⣉⣠⣿⣿⣀⣉⣠⣼")

def winText():
  # speak = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
  print('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠲⣶⣾⣿⣿⣷⣄⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀
⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⡿⠁⢻⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠘⣿⣿⠛⣿⣿⣿⣿⣿⣿⡿⠁⠛⢀⣶⡈⡿⠋⢻⣿⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣶⣿⣅⣽⣿⣿⣿⠃⣰⡀⢺⣿⡇⢀⣴⡀⠻⣿⣶⣶⡆⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣦⣼⣿⣇⣰⣿⣷⣾⣏⣠⣾⣿⣿⣄⣽⣿⣿⣷⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣧⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣯⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⠛⣿⣿⣿⣿⣷⣤⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣁⣿⠿⣿⠿⣿⠛⣿⣁⣽⣿⣿⣿⡏⣹⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣶⣷⣴⣿⣾⣿⣿⣿⣿⣿⣿⣿⣋⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠙⠻⢿⡿⠋⠛⣿⡀⠀⠀
⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⠀⠀⠀⣼⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠛⣿⡿⠟⣿⣿⣿⣿⣿⣋⣡⣴⣾⣶⣌⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠻⠟⠋⠀⠀⠀⠀⠛⠛⠛⠛⠛⠛⠛⠛⠿⠿⠿⠿⠿⠇⠀
  ''')
  speak1 = "\nYou see a paper and a key in the boss' pocket. Turns out it's a map that leads somewhere...\nIs this my way out?\n"
  speak2 = "You find yourself on top of the building and the key fits well with the helicopter."
  speak3 = "Do you want to follow the map??"
  treasureInput = ("\n> ")
  if treasureInput == ' yes':
    print('''
    ⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠰⠿⠿⠿⢿⣿⣷⣶⣶⣶⣦⣤⣤⣤⣤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⣶⣦⠀⣶⣤⣤⣤⣤⣍⣉⣉⣉⡙⠛⠛⠛⠛⠏⣰⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣆⠸⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡇⢸⣿⣿⣿⣿⣿⣿⣿⡏⠀⠹⠟⠙⣿⣿⣿⠄⢻⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠊⣉⡉⢋⣩⡉⠻⠛⠁⣾⣀⣴⡀⢛⡉⢠⣷⠈⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣼⣿⣿⣿⣿⣿⣷⣿⠀⢿⣿⣿⣿⡿⢁⠚⠛⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠤⠾⠿⣿⡿⠛⣿⣿⣿⣿⣿⣷⣦⣌⣉⣉⣠⣾⡷⠂⣠⠀⠀⠀⠀
⠀⠀⠀⣿⢰⣶⣶⣶⣦⠀⠀⣤⣌⣉⠉⣉⡙⠛⠛⠛⠻⠟⢁⣴⣾⣿⠀⠀⠀⠀
⠀⠀⠀⣿⣆⠻⣿⣿⢇⣸⠀⣯⢉⣿⠀⣿⣿⣿⣿⣿⣷⠀⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣷⡔⠐⣾⣿⠀⠛⠚⠿⠀⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠿⠋⠀⠀⠀⠀
⠀⠀⠰⣦⡄⠀⠀⠈⠉⠉⠉⠉⠛⠛⠛⠛⠻⠿⠿⠿⠿⠀⠛⢁⣀⡀⠲⠖⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀
    ''')
    treasure = "CONGRATULATION!\nYou find a treasure...\nYour journey is not over yet.\nThis is a new beginning\nTO BE CONTINUED ...."
    for character in treasure:
      sys.stdout.write(character)
      sys.stdout.flush()
      time.sleep(0.05)
  else:
    print("CONGRATULATION!\nYou survive!\nYour journey is not over yet.\nThis is a new beginning\nTO BE CONTINUED ....")
  for character in speak1:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speak2:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)
  for character in speak3:
    sys.stdout.write(character)
    sys.stdout.flush()
    time.sleep(0.05)


  # print("                 ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⡏⠉⠉⢹                     ")
  # print("                 ⣿⠿⠛⣿⣿⠇⠄⠈⣹⣿⠟⠁⠄⠄⠄⠄⠹⣿⣿⡏⠉⠉⣿⣿⣿⠉⠉⢹⣿⣿⣿⣿⣿⣿⡇⠄⠐⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⣼⡇⠄⠄⣼⣿⡇⠄⠹⣿⣿⣧⠄⠄⢸                     ")
  # print("                 ⣇⠄⠄⢿⣿⠄⠄⢸⣿⡏⠄⠄⢠⣶⡀⠄⠄⢻⣿⡇⠄⠄⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⡇⠄⠄⣿⣿⡿⠄⢹⣿⣿⠃⠄⢀⣿⡇⠄⠄⣿⣿⡇⠄⠄⢹⣿⣷⠄⠄⢸                     ")
  # print("                 ⣿⠄⠄⢸⡇⠄⠄⣼⣿⠄⠄⢀⣿⣿⣷⠄⠄⢸⣿⡇⠄⠄⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⣧⠄⠄⣿⣿⡇⠄⢸⣿⡿⠄⠄⣸⣿⣧⠄⠄⣿⣿⡇⠄⠄⠘⣿⣿⠄⠄⢸                     ")
  # print("                 ⣿⡄⠄⠸⠃⠄⢠⣿⡏⠄⠄⣸⣿⣿⣿⠄⠄⠘⣿⡇⠄⢀⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⡀⠄⢸⡿⠄⠄⠘⣿⡇⠄⠄⣿⣿⡏⠄⠄⣿⣿⡇⠄⠄⠄⢹⣿⠄⠄⢸                     ")
  # print("                 ⣿⣧⠄⠄⠄⠄⣾⣿⡇⠄⠄⣻⣿⣿⣿⠄⠄⠄⣿⡇⠄⠄⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⡇⠄⢸⠇⠄⠄⠄⢻⠃⠄⢸⣿⣿⡇⠄⠄⣿⣿⡇⠄⠄⠄⠄⢿⠄⠄⢸                     ")
  # print("                 ⣿⣿⡀⠄⠄⢰⣿⣿⣇⠄⠄⣿⣿⣿⣯⠄⠄⢰⣿⡇⠄⢸⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠄⡀⠄⠈⠄⠄⣾⣿⣿⡇⠄⠄⣿⣿⡇⠄⠄⣆⠄⠈⠄⠄⢸                     ")
  # print("                 ⣿⣿⡇⠄⠄⢸⣿⣿⣿⠄⠄⢸⣿⣿⡇⠄⠄⢸⣿⡀⠄⢸⣿⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⢠⣿⠄⠄⠄⢠⣿⣿⣿⡟⠄⠄⣿⣿⡇⠄⠄⣿⣄⠄⠄⠄⢸                     ")
  # print("                 ⣿⣿⡇⠄⠄⣿⣿⣿⣿⡆⠄⠄⠛⠟⠄⠄⠄⣼⣿⡄⠄⠈⠿⠛⠋⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⡆⠄⢀⣼⣿⣦⠄⠄⣾⣿⣿⣿⡇⠄⠄⣿⣿⠃⠄⠄⣿⣿⣧⠄⠄⢸                     ")
  # print("                 ⣿⣿⠄⠄⢸⣿⣿⣿⣿⣿⣄⡀⠄⠄⢀⣠⣼⣿⣿⣷⣀⠄⠄⠄⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣼⣿⣿⣿⡀⠄⣿⣿⣿⣿⡇⠄⠄⣿⣿⣃⣀⣀⣻⣿⣿⣧⠄⢘                     ")
  # print("                 ⣿⣏⣀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼                     ")
  # print("                                                                                                                           ")
  # print("                                                                                                                           ")
  # print("⣿⣿⡿⠛⠛⢿⣿⣿⣿⣿⠟⠛⠻⣿⣿⡿⢿⣿⣿⡏⠉⢻⣿⣿⣿⣿⠿⠿⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣿⠿⠛⠋⣿⣿⠿⠿⠿⠿⠛⢛⣿⣿⣿⣿⣿⣿⡟⠛⣿⣿⣿⣿⣿⠿⠟⠛⣿⡿⠿⠿⠿⠿⠟⠛⣿⣿⣿⣿⠟⠛⠻⣿⣿⡿⢿⣿⣿⡏⠉⢹")
  # print("⣿⠁⠄⣠⠄⠄⢿⣿⡏⠄⢀⡀⠄⠘⣿⡇⠄⢹⣿⡇⠄⢸⣿⡿⠃⠄⢀⠄⠸⣿⣿⠄⠄⣀⣀⠄⠹⣿⡿⠄⠄⠄⢹⣇⣀⠄⠄⣠⡤⠼⢿⣿⡇⠄⢸⣿⠇⠄⣿⣿⣿⣿⣿⠄⠄⠄⢹⣇⣀⠄⢀⣤⣤⣴⣿⣿⡟⠄⢀⣀⠄⠘⣿⡇⠄⠹⣿⡇⠄⢸")
  # print("⡏⠄⢸⣿⣄⣀⣸⣿⠄⠄⣿⣷⠄⠄⣿⡇⠄⠄⣿⡇⠄⢸⡿⠁⠄⣸⣿⠄⠄⣿⣿⠄⠄⣿⣿⠄⠄⣿⡇⠄⣸⠄⢸⣿⣿⠄⠄⣿⡇⠄⢸⣿⡇⠄⢸⣿⠄⠄⣿⣿⣿⣿⡿⠄⢸⠄⠸⣿⣿⠄⢸⣿⠄⠄⣿⣿⠄⠄⣼⣿⠄⠄⣻⡇⠄⠄⣿⡇⠄⢸")
  # print("⠃⠄⣾⣿⣿⣿⣿⡏⠄⢰⣿⣿⠆⠄⢹⡇⠄⠄⢹⡇⠄⢸⡇⠄⢰⣿⣿⣶⣾⣿⣿⠄⠄⣿⣿⠄⢰⣿⠃⠄⣿⠄⢸⣿⣿⠄⠄⣿⡇⠄⢸⣿⡇⠄⢸⣿⠄⠄⣿⣿⣿⣿⡗⠄⣸⠄⠄⣿⣿⠄⢸⣿⠄⠄⣿⡏⠄⢰⣿⣿⠆⠄⢹⡇⠄⠄⢹⡇⠄⢸")
  # print("⠄⠄⢾⣿⣿⣿⣿⡃⠄⢸⣿⣿⠃⠄⣸⡇⠄⢀⠄⠃⠄⢸⡇⠄⢸⡿⠿⠛⠛⢻⣿⠄⠄⠋⠄⣀⣼⣿⠄⢸⣿⠄⠈⣿⣿⠄⠄⣿⡇⠄⣸⣿⡇⠄⢸⣿⠄⠄⣿⣿⣿⣿⠁⠄⣿⡀⠄⢻⣿⠄⢸⣿⠁⠄⢿⡇⠄⢸⣿⣿⠃⠄⣸⡇⠄⢀⠄⠃⠄⢸")
  # print("⡆⠄⢸⣿⣿⣿⣿⣇⠄⠘⣿⣿⠄⠄⣿⡇⠄⢸⡄⠄⠄⢸⣧⠄⠘⣧⣠⡄⠄⢸⣿⠄⠄⡄⠄⣿⣿⡏⠄⠈⠉⠄⠄⣿⣿⠄⠄⣿⡇⠄⢹⣿⡇⠄⣼⣿⠄⠄⣿⣿⣿⡏⠄⠄⠉⠁⠄⢸⣿⠄⢸⣿⠃⠄⢺⣇⠄⠘⣿⣿⠄⠄⣿⡇⠄⢸⡄⠄⠄⢸")
  # print("⣷⡀⠈⠉⠁⢈⣿⣿⡄⠄⠙⠃⠄⣰⣿⡇⠄⢸⣿⡆⠄⢸⣿⣆⠄⠘⠉⠄⠄⢸⣿⠄⠄⣧⠄⠈⢿⠁⠄⣰⣶⡆⠄⢸⣿⠄⠄⣿⡇⠄⠘⠋⠄⢀⣿⣿⠄⠄⠉⠁⢙⡇⠄⣰⣶⣶⠄⢸⣿⠄⢸⣿⡇⠄⣿⣿⡄⠄⠙⠋⠄⢰⣿⡇⠄⢸⣿⡆⠄⢸")
  # print("⣿⣿⣶⣶⣶⣿⣿⣿⣿⣶⣤⣤⣾⣿⣿⣷⣶⣾⣿⣿⣇⣸⣿⣿⣶⣤⣤⣆⣀⣸⣧⣤⣤⣿⣧⣀⣰⣶⣶⣿⣿⣧⣴⣾⣿⣶⣶⣿⣿⣤⣤⣤⣶⣿⣿⣷⣶⣶⣶⣿⣿⣷⣶⣿⣿⣿⣤⣾⣿⣶⣾⣿⣇⣀⣿⣿⣿⣶⣤⣤⣾⣿⣿⣷⣶⣾⣿⣿⣇⣸")

def militiaImage():
  a='''
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⢻⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢀⠔⠁⠄⠄⠄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⠄⢀⠄⣀⡀⣀⡀⠊⠾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣤⣤⡇⠄⡦⣸⢷⣦⢷⡼⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣳⣅⠝⠻⣦⣷⡍⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡥⡂⠄⢼⣇⠉⣇⡎⠋⡛⠛⠻⠉⠿⣿⣿⡿⠋⢠⣶⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠁⡁⠘⠛⣠⠨⢠⣾⣟⠐⠉⠁⠶⠙⢉⣸⣴⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⡟⠋⠄⠂⢣⠄⠄⢀⠹⣰⣿⠋⠄⠄⠁⠄⡠⢤⣟⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⠟⠁⠄⠄⠄⠄⠄⢷⡀⠠⣰⠟⠄⠁⠄⢀⠄⠄⠄⠈⢿⣟⣿⣿⣿⣿
  ⣿⣿⣿⠃⠄⠄⠄⠠⣐⠄⠄⠈⢗⠴⡿⠄⠄⡤⠁⠁⠄⠄⠄⠄⠐⣻⣞⣿⣿⣿
  ⣿⡟⠄⠄⠄⠄⡀⡴⡆⠄⠄⠄⠄⢠⠠⡒⢵⣧⠄⠄⠄⠄⠄⡀⠄⠄⢻⢿⣿⣿
  ⣿⡅⠄⠄⠘⢔⣽⣾⣿⡀⢀⠄⠄⠓⠑⠄⠄⠹⠿⣸⣷⣷⠄⠄⠄⠄⠄⡿⣿⣿
  ⣿⣿⡀⠴⢾⣿⣿⣯⢀⠁⠄⠄⠄⠄⠄⠄⠄⠁⠺⠯⣿⡏⡠⡀⠄⠄⡀⣳⣿⣿
  ⣿⣿⣧⡀⠐⠉⠉⢋⠈⡴⣇⠂⠄⠄⠄⠄⠡⠄⠄⠄⠑⣸⢶⣶⣶⣶⣿⣿⣿⣿
  ⣿⣿⣿⣿⣆⠄⠠⣀⢅⣿⣿⡀⠄⠄⠄⠄⠂⠄⠄⠄⠄⣈⣿⣾⣿⣿⣿⣿⣿⣿
  ⣿⣿⡿⠉⠁⢀⣮⣴⣾⣿⣿⣷⣶⣶⣤⣤⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⡇⠄⣀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  '''
  print(a)

def NormalSoldierImage():
  a = '''
  ⠄⠄⠄⠄⠄⠄⠄⠄⣀⣤⣤⣄⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⠄⠄⠄⠄⠄⢨⣿⣿⣿⣿⣷⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⠄⢀⣤⣴⣶⣿⣿⣿⣿⣿⡛⣠⣄⣀⡀⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⢀⣾⣿⣿⣿⣿⣿⣿⡟⢛⣻⣿⣿⣿⡷⠿⠶⠶⠾⠤⠤⠤⠄
  ⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠿⢋⣽⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⢼⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣴⣿⡏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⣿⣿⣿⣿⣿⣿⡏⠄⠘⠿⠿⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⣼⣿⣿⣿⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⣿⣿⣿⣿⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠸⣿⣿⣿⣿⣿⣷⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⢻⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⠄⣿⣿⣿⣿⣿⣿⣧⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⣼⣿⣿⡟⢈⣿⣿⣿⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⣿⣿⠇⠄⣼⣿⣿⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⢀⣿⡇⠄⠐⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⣾⣿⣷⣦⣶⣿⣿⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠛⠛⠉⠉⢹⣿⣿⣿⣤⣤⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  ⠄⠄⠄⠄⠄⠈⠉⠉⠛⠛⠛⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
  '''
  print(a)

def veteranImage():
  a = '''
  ⡯⡯⣫⢯⣫⢯⣫⢯⣫⢯⣫⢯⣫⢯⣺⢽⢕⡯⡯⣺⢝⡮⡯⣺⢝⡮⡯⣺⢝⡮⡯⣺⢝⡮⡯⣺⢝⡮⡯⣺⢝⡮⣯⡺⡽⣕⢯⣫⢞⡽⣕⢯⣫⢞⡽⣕⡯⣫
  ⣯⡯⣗⣟⡮⣗⡯⡷⣝⢷⣝⢷⣝⢷⢽⠕⠙⡎⣟⡺⢝⠞⢝⢾⣕⢯⣞⢵⣫⢞⡽⣺⢵⣫⢯⣺⡳⡽⣝⢾⢝⣞⡮⡯⡯⣺⢽⡺⣝⢾⢝⡽⣺⣝⢾⣕⡯⣗
  ⣿⣽⣳⣳⢯⣗⡯⣯⢯⣗⡯⡷⡽⣝⡇⠁⠄⠘⡐⡘⠆⠁⢫⢗⡷⣝⣮⡻⡮⣻⢮⢗⡯⣞⣗⢷⢽⢽⣺⢽⣝⣞⣞⡽⣝⡾⣝⡾⡽⡽⡽⣺⢵⣫⢗⡷⡽⣺
  ⣿⣷⣷⣯⣟⣾⣽⣳⣻⢮⡯⣯⢿⣕⠇⠄⣠⠓⠄⠄⠄⢃⠄⣫⡺⡳⣳⢽⣝⣗⢯⡻⡮⣗⣗⡯⣯⡳⣏⣗⣷⣳⡳⣝⢷⣝⢷⢽⢽⢽⢽⢽⣝⢾⢽⣺⣝⣗
  ⣿⣿⣾⣿⡽⣿⣞⣗⣯⣟⡾⣽⣳⣅⠥⠊⠃⠠⠈⡀⠄⠄⠄⠃⠢⠩⡘⡑⠗⠽⡽⣽⣝⣗⣗⣟⡮⠣⠓⠓⠛⠙⠙⠪⢳⢽⢽⢽⢽⢽⣝⢷⢽⢽⢽⣺⣺⣺
  ⣿⢿⡺⡷⡟⡕⠵⡱⡓⡗⣟⣷⣳⢯⣟⣮⢤⡶⣤⣀⠐⠄⠄⢶⢖⣔⠄⠌⠄⠌⢠⠣⢁⠏⣗⣯⠁⠄⠠⣠⡠⠐⡀⠄⠄⢹⢽⣫⣟⣽⣺⢽⢯⢯⣟⣞⡾⣺
  ⣟⢵⢑⢕⢑⢱⢑⢕⢡⢫⢱⣗⣯⣟⣾⣺⡽⣞⡷⣽⡻⣶⢈⠵⢽⠼⣕⢦⣀⠁⡀⠕⡠⠠⡫⢚⠄⠄⠅⢄⡂⠫⢊⠠⢀⣀⣯⢷⣳⣗⡯⣯⢿⢽⣺⢾⢽⣳
  ⢍⢣⠑⠄⢂⠰⡡⠤⢃⠆⡇⣟⢾⡺⣞⣾⢽⣳⣟⣗⣯⢷⣄⠪⠠⠘⠜⢜⢾⢽⢲⢤⢀⣈⠠⠑⠩⢂⠄⠂⠚⠐⠄⢠⣟⡾⣵⣻⣞⡾⣽⢽⣽⣻⣺⣽⣻⣺
  ⢅⢅⠇⠝⠄⠎⢄⠅⡣⠹⡨⡸⡑⣼⢽⣞⣯⣷⣻⢾⣽⣻⣞⡿⣄⠆⠊⡀⠐⡜⠣⡊⡇⡇⡏⢦⢢⢄⡀⡐⢀⢆⢪⠋⠘⢙⢤⢖⢮⡹⣽⡽⣞⣾⣳⣗⣿⣺
  ⢡⠕⢨⠘⢌⠮⡪⠌⡂⠑⢤⠱⡹⡸⡏⣷⣻⢾⣽⣻⣞⡷⣯⢿⡽⢃⠂⠐⢈⠂⠡⠘⠨⠨⡊⡪⡘⢢⢃⢇⢍⠫⡕⢝⠪⢽⡝⢽⡆⣏⢷⣻⣽⣞⣷⣻⣞⡷
  ⢢⢩⠪⡒⡕⠅⡘⢌⢠⢱⢒⢝⢎⢪⢜⡷⣽⣻⣾⣳⣯⡿⣽⡯⣿⠆⠂⡈⢀⢰⣦⣤⡑⠈⡂⠆⠪⠠⠑⢸⠨⠣⡙⡎⢗⣅⢹⢦⠑⠎⢜⣿⣺⣗⣿⣺⢷⣻
  ⢨⠠⡑⢍⠢⢁⠆⡒⢌⢎⠨⢠⠠⢣⠣⣫⣺⣷⢯⣷⣿⣽⡷⣟⣿⣿⡆⠄⠄⢸⣿⣻⡟⠄⡤⠂⢀⠁⠐⠄⠁⠁⠄⠪⠈⠨⠄⡁⠄⠂⡱⣻⢞⡽⣪⢯⡻⣻
  ⠔⡡⡸⡐⡨⠐⡨⢐⠡⢐⢔⢇⠹⢰⠟⣟⢞⡯⣟⣞⣞⡾⣽⣫⣗⢿⢁⠠⠈⠈⠛⠅⡂⠁⡂⢭⠄⡢⡅⡠⠄⠁⠄⠂⠄⠂⠁⠄⠄⠂⢐⡎⡯⣺⢵⢳⢝⣜
  ⠜⢐⢈⠢⡈⡢⠄⢅⢩⢸⠠⡂⠌⣀⢓⠸⣺⡺⣵⣳⡳⡯⣳⡳⡵⣻⡀⢂⠄⠁⠄⠂⠄⠰⠈⢀⠉⠆⠃⢉⠊⠈⠄⠠⠐⠄⡀⡣⡣⠄⣘⢼⢜⢵⢕⢏⡪⡪
  ⠌⡐⠤⠡⡂⢣⠣⡑⢅⢅⢑⢌⡊⡆⠆⡝⡪⣝⢮⣞⣞⢽⢵⡻⡽⡵⡅⠂⢀⠁⠄⠄⠄⠑⣕⠡⠢⡄⠄⡀⠄⠄⠁⠠⢔⣔⡪⢪⠹⢀⢬⠺⣸⢸⡸⣔⢕⠱
  ⢨⢐⠐⡐⠨⡐⡑⠄⡑⠈⠜⢐⢑⡅⣕⢝⠱⢑⡳⣕⣗⢯⢏⡯⣳⡫⣗⡐⠄⠄⢈⢠⡐⣝⠐⢨⢪⠐⠠⠄⡀⠄⠠⢡⢐⠕⡎⡜⡑⠈⢮⢣⠪⢪⢸⢢⢂⠅
  '''
  print(a)

def SpecialImage():
  a = '''
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡂⠵⠆⡂⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⠿⠿⠿⣿⣿⡿⠿⠷⡀⠄⠄⠄⠾⠿⣿⣿⣿⠿⠿⠿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⠁⡂⠌⠄⢅⠨⠐⠠⢁⠂⡢⠡⡂⠡⢨⢮⡫⣫⡣⡅⠂⡄⢌⢄⠂⡂⠂⠌⠄⡂⡂⠌⠄⠌⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠑⡀⡂⠢⠡⢑⢐⠠⠁⠅⡂⢌⠢⡑⢌⠪⡠⢳⣯⣾⡟⠠⡑⢌⡢⠢⡑⠠⠡⠨⠐⡐⠄⠅⢅⢂⢐⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⡿⢛⢛⢐⢐⠨⠨⠨⢐⢐⠨⢈⢐⠠⡡⡑⢌⠢⡑⢔⢈⠛⢛⠠⡨⡨⠪⡻⢑⠌⠌⠄⡡⢂⠂⢅⢑⠐⡐⡀⡂⡛⡛⢿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⡿⠫⣰⠶⣝⢖⡶⡠⠡⠨⢐⢐⠨⢐⢀⢂⠪⠠⢑⠨⢈⠢⡡⡑⢔⢑⠔⠌⢂⢂⠂⠅⠅⠌⡐⠄⡑⡐⢐⢐⣰⡲⣝⢮⢖⢦⠙⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⠡⣝⢮⡫⣞⢵⡫⣫⢮⠐⡐⠠⡑⢀⢂⠐⢅⢑⢐⠨⡐⡑⠔⢌⠢⠢⡑⢅⢂⢂⠅⡡⢁⠂⡂⠅⡂⢂⢂⣖⢧⢯⢮⡳⣝⢽⡱⡘⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⢀⡗⣗⣝⢮⡳⣝⢮⡳⣳⣢⡡⣇⠂⡐⡈⠢⡑⢌⢌⠢⠪⡘⢌⢘⠌⡌⡢⠪⡐⡑⢌⠐⡐⢀⢷⡨⡴⣺⣪⡳⣓⢧⢯⢮⡳⡝⠄⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣆⡜⢕⣗⢵⡫⡮⡳⣝⢮⡺⡺⣜⢄⠂⠄⠅⠌⡂⠢⡑⠡⢊⠐⢄⢑⠨⢐⢑⠨⠨⢐⢀⢂⡲⣕⢯⣫⡺⡲⣝⢮⡳⣳⡣⡯⢊⣼⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣞⢮⡳⣝⢮⡫⡮⡳⣝⢞⢮⣫⡳⣣⣌⢐⠌⠢⠨⠨⢐⠨⢐⢐⠨⢐⢐⠨⠨⢠⡴⣫⢞⢮⡳⡵⣹⢝⢮⡳⣝⢮⢮⣷⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣷⡝⡮⡳⣝⢮⠯⡮⡫⡧⡳⡝⡞⣎⠢⠨⠨⠨⡈⡢⡈⡂⡢⢈⢂⠢⠨⠨⢸⢝⢮⣫⡳⣝⢮⡳⣝⢵⢝⢮⣺⣽⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣝⢮⡳⣝⢭⢯⡺⣹⡱⣽⣾⠄⠁⠁⠁⠄⢢⠱⡨⡂⠁⠄⠈⠈⠈⢸⣗⡕⣇⡗⣗⡳⣝⢮⡳⣽⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣯⡮⣳⢳⣹⣼⣿⣿⣿⢐⢄⢂⢂⢂⠪⡘⢔⠡⡂⡢⢂⢂⠢⢸⣿⣿⣾⣸⡺⣚⢮⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⠰⡐⡑⢌⠢⡑⢌⠢⡑⠔⢌⠢⡡⡑⣹⣿⣿⣿⣿⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
  '''
  print(a)
  
title_screen()