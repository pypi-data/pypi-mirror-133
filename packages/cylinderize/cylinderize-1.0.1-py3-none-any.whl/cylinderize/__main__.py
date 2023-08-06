from questionary import path
from . import cylinderize
from sys import argv
def main(): cylinderize(open(argv[1] if len(argv) > 1 else path('Path to file').ask()).read())
if __name__ == "__main__": main()