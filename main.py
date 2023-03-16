from tictactoe import TicTacToe

game = TicTacToe(3)
player = 1
state = game.get_initial_state()

while True:
    valid_moves = game.get_valid_moves(state)
    print("possible actions: ", [i for i, v in enumerate(valid_moves) if v])

    try:
        action = int(input(f"choose action for p {player}: "))
        if action >= game.action_space or not valid_moves[action]:
            print("invalid action")
            continue
    except ValueError:  # invalid int
        print("invalid action")
        continue

    state = game.get_next_state(state, action, player)
    print(state)

    val, terminated = game.get_value_and_terminated(state, action)

    if terminated:
        if val:
            print("player", player, "won!")
        else:
            print("it's a draw!")
        break
    player = game.get_opponent(player)
