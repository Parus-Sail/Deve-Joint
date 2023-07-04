class One:

    def __init__(self):
        print('Initializing: class One')


class Two(One):

    def __init__(self):
        print('Initializing: class Two')
        super().__init__()


class Three(Two):

    def __init__(self):
        print('Initializing: class Three')
        super().__init__()


class Four_One(Three):

    def __init__(self):
        print('Initializing: class Four')
        super(Two, self).__init__()  # Наследовать от наследника Two


t = Three()
# Initializing: class Three
# Initializing: class Two
# Initializing: class One

print()

f = Four_One()
# Initializing: class Four