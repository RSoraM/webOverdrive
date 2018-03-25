if __name__ == '__main__':
    # env setting
    activate_this = '.pyenv/Scripts/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))

    from bin.app import application

    application.run()
