import GUI
from boggle_board_randomizer import randomize_board


if __name__ == '__main__':
    board = randomize_board()
    gui = GUI.Gui(board)
    gui.start()
