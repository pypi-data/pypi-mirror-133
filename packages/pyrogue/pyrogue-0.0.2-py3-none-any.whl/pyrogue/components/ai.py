from components.fov import is_in_fov

class BasicMonster():
    def take_turn(self, target, fov, game_map, entities):
        results = []
        monster = self.owner
        if is_in_fov(fov, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
                # monster.move_astar(target, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
