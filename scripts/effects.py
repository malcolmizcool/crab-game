import random


class Effect:

    def on_shoot(self, player, shot):
        pass

    def on_hit(self, player, shot):
        return False


class Rebound(Effect):

    CHANCE = 0.1    

    def on_hit(self, player, shot):
        if random.random() >= self.CHANCE:
            return False                    

       
        shot.direction = (-shot.direction[0], -shot.direction[1])
        shot.inherited = (-shot.inherited[0], -shot.inherited[1])

        shot.owner = "player"
        shot.damage = player.stats["damage"] * 2
        shot.time_active = 0               
        return True

EFFECTS = {
    "rebound": Rebound,
}

