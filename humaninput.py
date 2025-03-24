from envs.combatenv import Combat

from stssim.enemies.jawworm import JawWorm

if __name__ == '__main__':
    # Initialize the Tetris game
    combat = Combat(JawWorm())

    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        combat.print()
        action = int(input())

        combat.step(action)