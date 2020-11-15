from action import actions, DamagingAction, SelfAction, ActionType, Action
from combatant import Player, Abaddon
from menu import Menu

PLAYER_MENU = Menu().add_action(actions.attack).add_submenu(Menu("WHITE MAGIC").add_action(actions.cure))


class Battle:
    def __init__(self, player: Player, enemy: Abaddon):
        self.player = player
        self.enemy = enemy

        self.player_turn = True

    @property
    def game_over(self) -> True:
        return self.player.defeated or self.enemy.defeated

    def print_separator(self):
        sep_char = ">" if self.player_turn else "<"
        print("\n" + (sep_char * 50), "\n")

    def get_player_action(self) -> Action:
        print(self.player.stat_block)
        action_name = PLAYER_MENU.get_action()
        return actions[action_name]

    def get_multiplier_by_action_type(self, action_type: ActionType):
        if action_type == ActionType.Physical:
            return self.player.strength

        if action_type == ActionType.Magical:
            return self.player.magic

    def loop(self):
        while not self.game_over:
            action_params = {}

            self.print_separator()

            if self.player_turn:
                perform_action = self.get_player_action()

                action_params["user"] = self.player
                action_params["multipliers"] = [
                    self.get_multiplier_by_action_type(perform_action.action_type)
                ]

                if isinstance(perform_action, DamagingAction):
                    action_params["target"] = self.enemy
                    action_params["damage_range"] = self.player.base_damage
                elif isinstance(perform_action, SelfAction):
                    pass
                else:
                    raise Exception("wat")

                perform_action(**action_params)
                self.player_turn = False
            else:
                print(self.enemy.stat_block)
                action_name = self.enemy.take_turn()
                perform_action = actions[action_name]
                perform_action(self.enemy, self.player, self.enemy.base_damage, [])

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
