from action import actions, OffensiveAction, SelfAction, Action
from combatant import Player, Abaddon, Combatant, CombatantEvent, CombatantEventType
from effects import PersistentEffect
from menu import Menu
from util import pause_for_user

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
        .add_action(actions.mp_absorb)
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

    def apply_events(self, user: Combatant, events: list[CombatantEvent]):
        for event in events:
            if event.special_text:
                print(f"\n{event.special_text}")
                pause_for_user()

            if event.type_ == CombatantEventType.ANNOUNCEMENT:
                # This is covered by the special_text
                pass
            elif event.type_ == CombatantEventType.HP_DELTA:
                event.combatant.hp.delta(event.value)
                if event.value <= 0:
                    print(event.combatant.name, "takes", abs(event.value), "damage!")
                else:
                    print(
                        event.combatant.name,
                        "restores",
                        event.value,
                        "HP!",
                        f"(Current: {event.combatant.hp})",
                    )

            elif event.type_ == CombatantEventType.MP_DELTA:
                event.combatant.mp.delta(event.value)
                if event.value <= 0:
                    print(event.combatant.name, "takes", abs(event.value), "MP damage!")
                else:
                    print(event.combatant.name, "restores", event.value, "MP!")

            elif event.type_ == CombatantEventType.EVADE:
                print(f"{event.combatant.name} evades {user.name}'s attack!")

    def loop(self):
        while not self.game_over:
            action_params = {}

            self.print_separator()
            events = []

            if self.player_turn:
                perform_action = self.get_player_action()

                action_params["user"] = self.player
                action_params["multipliers"] = [
                    self.player.get_stat_by_effect_type(perform_action.effect_type)
                ]

                if isinstance(perform_action, OffensiveAction):
                    action_params["target"] = self.enemy
                    action_params["damage_range"] = self.player.base_damage
                elif isinstance(perform_action, SelfAction):
                    pass
                else:
                    raise Exception("wat")

                if perform_action:
                    events.extend(perform_action(**action_params))

                events.extend(self.player.handle_persistent_effects())

                self.player_turn = False
            else:
                print(self.enemy.stat_block, "\n")
                action_name = self.enemy.take_turn()
                perform_action = actions[action_name]
                events.extend(
                    perform_action(self.enemy, self.player, self.enemy.base_damage, [])
                )

                self.player_turn = True

            if events:
                self.apply_events(
                    self.player if self.player_turn else self.enemy, events
                )
                pause_for_user()

        if self.player.hp <= 0:
            print(
                self.player.name,
                f"has fallen. The world's only hope succumbed to {self.enemy.name}'s ferocity and might...",
            )
        elif self.enemy.hp <= 0:
            print(self.enemy.name, "is kill. Rejoice!")


if __name__ == "__main__":
    from effects import Element, Ailment
    from random import choice

    player = Player()
    player.persistent_effects.append(PersistentEffect(Ailment.POISON, 2))
    enemy = Abaddon()
    f = Element.all()
    enemy.affinity = choice(Element.all())
    battle = Battle(player, enemy)
    try:
        battle.loop()
    except (KeyboardInterrupt, EOFError):
        print("\n\nYES, FLEE COWARD.")
