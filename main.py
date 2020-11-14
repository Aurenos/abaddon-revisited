from action import actions, DamagingAction, SelfAction, DamageType
from combatant import Player, Abaddon
from menu import Menu

PLAYER_MENU = Menu().add_action(actions.attack)


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
            sep_char = ">" if self.player_turn else "<"
            print("\n" + (sep_char * 50), "\n")

            if self.player_turn:
                print(self.player.stat_block)
                action_name = PLAYER_MENU.show()
                perform_action = actions[action_name]

                if isinstance(perform_action, DamagingAction):
                    multipliers = []
                    if perform_action.damage_type == DamageType.Physical:
                        multipliers.append(player.strength)
                    elif perform_action.damage_type == DamageType.Magical:
                        multipliers.append(player.magic)
                    perform_action(
                        self.player, self.enemy, self.player.base_damage, multipliers
                    )

                elif isinstance(perform_action, SelfAction):
                    perform_action(player)

                else:
                    raise Exception("wat")

                self.player_turn = False
            else:
                print(self.enemy.stat_block)
                action_name = self.enemy.take_turn()
                perform_action = actions[action_name]
                perform_action(self.enemy, self.player, self.enemy.base_damage)

                self.player_turn = True

        if self.player.hp <= 0:
            print(
                self.player.name,
                f"has fallen. The world's only hope succumbed to {self.enemy.name}'s ferocity and might...",
            )
        elif self.enemy.hp <= 0:
            print(self.enemy.name, "is kill. Rejoice!")


if __name__ == "__main__":
    player = Player()
    enemy = Abaddon()
    battle = Battle(player, enemy)
    try:
        battle.loop()
    except KeyboardInterrupt:
        print("\n\nYES, FLEE COWARD.")
