import subprocess
import sys

i = sys.executable

def getreqs():
  print("Getting requirements...")
  a = [i, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt']
  c = subprocess.call(a)
  if c != 0:
    print('The requirements could not be installed.')
    sys.exit(1)
  else: print("Done!")

def updatepip():
  print("Updating pip...")
  a = [i, '-m', 'pip', 'install', '--upgrade', 'pip']
  c = subprocess.call(a)
  if c != 0: print('pip could not be updated.')
  else: print("Done!")

def updatesource():
  print("Updating Monika's source code...")
  try:
    c = subprocess.call(('git', 'pull'))
  except:
    return print('git was not found, so Monika will not be updated.')
  if c != 0: print('Monika could not update.')
  else: print("Done!")

def runmonika():
  if sys.version_info >= (3, 6):
    while True:
      try:
        c = subprocess.call((i, 'monika.py'))
      except KeyboardInterrupt:
        break
    print("Well, goodbye! I hope to see you again sometime!")
  else:
    print("Monika needs Python 3.6 or higher.")

def main():
    updatesource()
    updatepip()
    getreqs()
    runmonika()

main()
