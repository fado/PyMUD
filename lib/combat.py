from lib.models.creature import Creature
from lib.models.player import Player


class CombatHandler():

    combat_instances = []

    def add_instance(self, instance: CombatInstance):
        self.combat_instances.append(instance)

    def advance_rounds(self):
        for instance in combat_instances:
            instance.advance_round()


class CombatInstance():
    
    participants = []
    waiting_participants = []

    def add_participant(self, participant: Creature):
        self.waiting_participants.append(participant)

    def advance_round(self):
        
        # Are we waiting to add any new participants?
        for participant in self.waiting_participants:
            # Handle any pre-combat stuff now.
            participant.roll_initiative()
            # Add them to the battle.
            self.participants.append(participant)

        # Sort participants into initiative order.
        self.participants.sort(key=lambda x: x.initative, reverse=False)
