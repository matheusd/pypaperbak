
import sys
from pypaperbak import PyPaperbakApp



def main(args=None):
    if args is None:
        args = sys.argv[1:]
    app = PyPaperbakApp()
    app.main(sys.argv)    


if __name__ == "__main__":
    main()