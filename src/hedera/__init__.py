from . import generated

for i in dir(generated):
    if not i.startswith("__"):
        vars()[i] = generated.__dict__[i]
        # does not work because they are functions not classes
        # vars()[i].__repr__ = vars()[i].toString
