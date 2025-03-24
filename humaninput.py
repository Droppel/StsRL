from envs.combatenv import Combat

if __name__ == '__main__':
    # Initialize the Tetris game
    combat = Combat(True)

    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        action = int(input())

        combat.step(action)