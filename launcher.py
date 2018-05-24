import subprocess
import sys
from argparse import ArgumentParser

i = sys.executable()

def getreqs():
  a = [i, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt']
  c = subprocess.call(a)
  if c != 0: print('The requirements could not be installed.')
  sys.exit(1)

def updatepip():
  a = [i, '-m', 'pip', 'install', '--upgrade', 'pip']
  c = subprocess.call(a)
  if c != 0: print('pip could not be updated.')

def updatesource():
  try:
    c = subprocess.call(('git', 'pull'))
  except:
    return print('git was not found, so Monika will not be updated.')
  if c != 0: print('Monika could not update.')

def runmonika():
  if sys.version_info >= (3, 6):
    while True:
      try:
        if t:
          c = subprocess.call((i, 'monika.py', '--testing'))
        else:
          c = subprocess.call((i, 'monika.py'))
      except KeyboardInterrupt:
        break
    print("Well, goodbye! I hope to see you again sometime!")
  else:
    print("Monika needs Python 3.6 or higher.")

def main():
    updatepip()
    getreqs()
    updatesource()
    runmonika()

main()
