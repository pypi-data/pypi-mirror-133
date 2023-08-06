from random import choice
from Aly_facts.assets import aly_facts, aly_pics

def get_fact()->str:
  return choice(aly_facts)

def get_all_facts()->list:
  return list(aly_facts)

def get_aly_pics()->str:
  return choice(aly_pics)

def version()->str:
  return "1.0"