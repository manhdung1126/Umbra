 attack_hitbox = player.get_attack_hitbox()
    if attack_hitbox:
        for enemy in enemies:
            already_hit = enemy in player.enemies_hit_attack
            if enemy.alive and attack_hitbox.colliderect(enemy.hitbox) and not already_hit:
                enemy.take_damage(10)
                player.enemies_hit_attack.add(enemy)