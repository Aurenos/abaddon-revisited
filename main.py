from action import ACTIONS, DamagingAction, SelfAction, DamageType
from combatant import Player, Abaddon
from menu import Menu

PLAYER_MENU = (
    Menu()
        .add_action(ACTIONS.get("attack"))
    )

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
            print("-" * 50, "\n")
            if self.player_turn:
                print(self.player.stat_block)
                action_name = PLAYER_MENU.show()
                perform_action = ACTIONS.get(action_name)

                if isinstance(perform_action, DamagingAction):
                    multipliers = []
                    if perform_action.damage_type == DamageType.Physical:
                        multipliers.append(player.strength)
                    elif perform_action.damage_type == DamageType.Magical:
                        multipliers.append(player.magic)
                    perform_action(player, enemy, player.base_damage, multipliers)

                elif isinstance(perform_action, SelfAction):
                    perform_action(player)

                else:
                    raise Exception('wat')

                self.player_turn = False
            else:
                self.enemy.take_turn()
                self.player_turn = True


if __name__ == "__main__":
    player = Player()
    enemy = Abaddon()
    battle = Battle(player, enemy)
    battle.loop()
