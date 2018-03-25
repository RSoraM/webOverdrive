from os import system
import platform  

system('pip install virtualenv')
system('virtualenv --no-site-packages .pyenv')

if platform.system() == 'Linux':
  activate_this = '.pyenv/bin/activate_this.py'
else:
  activate_this = '.pyenv/Scripts/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))
system('pip install -r requirement')
