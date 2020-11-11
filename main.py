from combatant import Player, Abaddon

class Battle:
    def __init__(self, player: Player, enemy: Abaddon):
        self.player = player
        self.enemy = enemy

        self.player_turn = True

    @property
    def game_over(self) -> True:
        return self.player.defeated or self.enemy.defeated

    def loop(self):
        while not self.game_over:
            if self.player_turn:
                self.player.take_turn()
                self.player_turn = False
            else:
                self.enemy.take_turn()
                self.player_turn = True


if __name__ == "__main__":
    player = Player()
    enemy = Abaddon()
    battle = Battle(player, enemy)
    battle.loop()
