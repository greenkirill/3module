from v1 import v1

class Prog:
    def __init__(self, stopc=""):
        self.stopc = stopc
        self.d = {
            "з": self.load_f,
            "н": self.find
        }

    def run(self, c):
        splt = c.split(" ")
        c = splt[0]
        if c == self.stopc:
            return False
        elif c in self.d:
            v = splt[1:]
            return self.d[c](v)
        else:
            self.nf()
        return True

    def load_f(self, file):
        pass

    def find(self, s):
        pass

    def nf(self):
        print("Команда не найдена")
