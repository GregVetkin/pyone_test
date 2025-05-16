

class Version:
    def __init__(self, version: str):
        self.parts = tuple(map(int, version.split(".")))

    def __repr__(self):
        return '.'.join(map(str, self.parts))
    
    def __eq__(self, version):
        return self.parts == version.parts
    
    def __lt__(self, version):
        return self.parts < version.parts
    
    def __lt__(self, version):
        return self.parts <= version.parts
    
    def __gt__(self, version):
        return self.parts > version.parts

    def __ge__(self, version):
        return self.parts >= version.parts
    

