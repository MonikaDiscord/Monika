from monika import Monika
from argparse import ArgumentParser

parser = argparse.ArgumentParser(description='Monika - the Discord bot!')
parser.add_argument('--testing', help='doesn\'t load any cogs (and other small things)', action='store_true')
args = parser.parse_args()
if args.testing:
  bot = Monika(testing=True)
else:
  bot = Monika()

if __name__ == "__main__":
  bot.run()
