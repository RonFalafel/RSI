class ILightChanger:
    def changeColor(self, r, g, b, br):
        raise NotImplementedError

    def defaultColor(self):
        raise NotImplementedError