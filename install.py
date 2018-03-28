from os import system
from string import Template
import platform


def main():
    print 'Database Setting'
    user = raw_input('Database\'s User: ')
    password = raw_input('Database\'s Password: ')
    domain = raw_input('Database\'s Domian(localhost): ')
    port = raw_input('Database\'s Port(27017): ')

    if user and password:
        if not domain:
            domain = 'localhost'
        if not port:
            port = 27017

        db = Template("""
import urllib
from pymongo import MongoClient

DB_USER = urllib.quote_plus('$user')
DB_PWD = urllib.quote_plus('$password')
DB_DOMAIN = urllib.quote_plus('$domain')
DB_PORT = $port
client = MongoClient('mongodb://%s:%s@%s:%s/' % (DB_USER, DB_PWD, DB_DOMAIN, DB_PORT))
db = client.webOverdrive

def get_db():
    return db
""")
        db = db.substitute(
            user=user, password=password, domain=domain, port=port)
    else:
        print 'Need user and password to finish install'
        return 0

    print 'Api Setting'
    url = raw_input('API URL: ')

    if url:
        api = Template('''
export default 'http://$url'
''')
        api = api.substitute(url=url)
    else:
        print 'Need api url to finish install'
        return 0

    db_file = open('./bin/tools/db.py', 'w')
    db_file.write(db)
    db_file.close()

    js_file = open('./view/src/assets/setting.js', 'w')
    js_file.write(api)
    js_file.close()

    system('pip install virtualenv')
    system('virtualenv --no-site-packages .pyenv')

    if platform.system() == 'Linux':
        activate_this = '.pyenv/bin/activate_this.py'
    else:
        activate_this = '.pyenv/Scripts/activate_this.py'

    execfile(activate_this, dict(__file__=activate_this))
    system('pip install -r requirement')
    system('cd view && npm install && npm run build')
    system('chmod +x log2json.sh && bash log2json.sh')
    print (
    '''
    Finished install.
    ''')

if __name__ == '__main__':
    main()
