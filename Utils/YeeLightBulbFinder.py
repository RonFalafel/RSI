from yeelight import discover_bulbs

class YeeLightBulbFinder:
    def findBulbs(self):
        bulbs = discover_bulbs()
        return [bulb['ip'] for bulb in bulbs]