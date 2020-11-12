from random import randint


class ClampedStat:
    def __init__(self, maximum: int, minimum: int = 0):
        self.maximum = maximum
        self.minimum = minimum
        self.current = maximum

    def delta(self, other: int):
        value = self.current + other
        self.current = self.__clamp(value)

    def __str__(self):
        return f"{str(self.current)} / {str(self.maximum)}"

    def __clamp(self, value: int):
        return max(self.minimum, min(value, self.maximum))


class Combatant:
    def __init__(self, name: str, hp: int, mp: int, evasion: int):
        self.name = name
        self.hp = ClampedStat(hp)
        self.mp = ClampedStat(mp)
        self.evasion = evasion

    @property
    def defeated(self) -> True:
        return self.hp.current <= 0

    def take_turn(self):
        raise NotImplemented


class Player(Combatant):
    def __init__(self):
        super().__init__(
            name="Spero",
            hp=randint(8000, 9999),
            mp=randint(380, 550),
            evasion=randint(10, 20),
        )

    @property
    def stat_block(self) -> str:
        return f"{self.name}\n\nHP: {self.hp}\nMP: {self.mp}"

    def take_turn(self):
        print(self.stat_block)


class Abaddon(Combatant):
    def __init__(self):
        super().__init__(
            name="Abaddon",
            hp=randint(480000, 520000),
            mp=randint(2500, 3000),
            evasion=randint(5, 10),
        )

    def take_turn(self):
        print("Enemy Turn")
        input()
