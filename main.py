from action import actions, DamagingAction, SelfAction, Action
from combatant import Player, Abaddon
from menu import Menu

PLAYER_MENU = (
    Menu()
    .add_action(actions.attack)
    .add_submenu(
        Menu("WHITE MAGIC", prompt="What will you cast? ").add_action(actions.cure)
    )
    .add_submenu(
        Menu("BLACK MAGIC", prompt="What will you cast? ")
        .add_action(actions.flare)
        .add_action(actions.blizzard)
        .add_action(actions.bolt)
        .add_action(actions.water)
    )
)


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

    def loop(self):
        while not self.game_over:
            action_params = {}

            self.print_separator()

            if self.player_turn:
                perform_action = self.get_player_action()

                action_params["user"] = self.player
                action_params["multipliers"] = [
                    self.player.get_stat_by_effect_type(perform_action.effect_type)
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
                print(self.enemy.stat_block, "\n")
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
    from effects import Element

    player = Player()
    enemy = Abaddon()
    enemy.affinity = Element.Fire
    battle = Battle(player, enemy)
    try:
        battle.loop()
    except (KeyboardInterrupt, EOFError):
        print("\n\nYES, FLEE COWARD.")
