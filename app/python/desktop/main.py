from desktop.bootstrap import Bootstrap
from desktop.run_app import run_app
import os

if __name__ == '__main__':
    run_app(Bootstrap, os.path.join(os.getcwd(), "config"))
