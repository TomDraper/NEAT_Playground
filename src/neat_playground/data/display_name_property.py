class DisplayNameProperty():
    def __init__(self, name, display_name):
        self.name = name
        self.display_name = display_name

    def hasName(self, name):
        return (self.name == name or self.display_name == name)

    def __str__(self):
        return f"Display Name: {self.display_name}. Name: {self.name}."