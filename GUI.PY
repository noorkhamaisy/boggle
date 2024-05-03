import tkinter as tk
import tkinter.messagebox
import ex12_utils
from boggle_board_randomizer import randomize_board

def load_dictionary():
    """Openning the word file and puts the words in a list"""
    dict_list = []
    with open("boggle_dict.txt") as d:
        for line in d:
            line = line[:-1]
            dict_list.append(line)
    return dict_list

class Gui:
    def __init__(self,board):
        self.timer_after = None
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.first_page()
        self.board = board
        self.dict_list = load_dictionary()

    def first_page(self):
        """The first page of the game """
        self.canvas = tk.Canvas(self.root, width=700, height=500)
        self.backpic = tk.PhotoImage(file="background.png")
        self.canvas.create_image(1, 1, image=self.backpic, anchor=tk.NW)
        self.canvas.pack()
        self.button = tk.Button(self.canvas, text="START", height=5, width=50, command=self.game_page)
        self.button.place(x=180, y=200)

    def game_page(self):
        """The play page of the game"""
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, width=700, height=500)
        self.backpic = tk.PhotoImage(file="background.png")
        self.canvas.create_image(1, 1, image=self.backpic, anchor=tk.NW)
        self.canvas.pack()
        self.text = ""
        self.path = []
        self.buttoncounter = 0
        self.min = 3
        self.sec = 0
        self.score = 0
        self.guessedwords = []
        self.submit_button()
        self.score_view()
        self.already_guessed()
        self.build_wordbox()
        self.build_buttons(self.board)
        self.check_word()
        self.start_timer()

    def score_view(self):
        """showing the score on a label in the playing page"""
        self.score_text = tk.Label(self.canvas, text="SCORE :", height=2, width=7)
        self.score_text.place(x=550, y=180)
        self.score_label = tk.Label(self.canvas, height=2, width=7, text=self.score)
        self.score_label.place(x=550, y=210)

    def already_guessed(self):
        """showing the words that the player had already guessed"""
        self.guessedwords_text = tk.Label(self.canvas, text="WORDS :", height=4, width=8)
        self.guessedwords_text.place(x=60, y=100)
        self.guessedwords_label = tk.Label(self.canvas, height=17, width=8)
        self.guessedwords_label.place(x=60, y=170)


    def start_timer(self):
        """Showing the time in the playing page and starting it"""
        self.time_text = tk.Label(self.canvas,text="TIME :", height=2, width=7)
        self.time_text.place(x=550, y=110)
        self.time_label=tk.Label(self.canvas, height=2, width=7)
        self.time_label.place(x=550, y=140)
        self.timer()

    def timer(self):
        """The timer starts to count down until reaches zero"""
        self.time_label.configure(text= str(self.min) + ":" + str(self.sec))
        if self.min == 0 and self.sec == 0:
            self.root.after_cancel(self.timer_after)
            self.end_game()
            return
        if self.sec == 0:
            self.min -= 1
            self.sec = 59
        else: self.sec -= 1
        self.timer_after = self.root.after(1000, self.timer)

    def end_game(self):
        """Asking the player to play again or end the game"""
        ansewr = tk.messagebox.askquestion("End Game", "Want to play again ?")
        if ansewr == "yes":
            self.board = randomize_board()
            self.game_page()
        else: self.root.destroy()


    def build_wordbox(self):
        """Label to show the letters that the player entered"""
        self.wordbox = tk.Label(self.canvas, text='', height=2, width=50)
        self.wordbox.place(x=160, y=90)

    def build_buttons(self, board):
        """Building the buttons of the game and putting letters on them"""
        self.board = board
        self.buttons_frame = tk.Frame(self.canvas, width=365, height=240)
        self.buttons_frame.place(x=160, y=140)
        x = 1
        y = 1
        for i in range(4):
            for j in range(4):
                button = tk.Button(self.buttons_frame, width=12, height=4, text=board[i][j], command=self.button_letter(board[i][j],i,j))
                button.place(x=x, y=y)
                x += 90
            y += 55
            x = 1

    def button_letter(self, letter,i,j):
        """When pressing a button:
        1)adding the 'coord' of the button to path to check if the path is valid
        2)showing the letter of the button on a label
        3)adding 1 to the counter(to decide the score)"""
        def add_letter():
            self.path.append((i,j))
            self.text += letter
            self.wordbox.configure(text=self.text)
            self.buttoncounter += 1
        return add_letter

    def submit_button(self):
        """Button to submit the word to check it"""
        self.submitbutton = tk.Button(self.canvas, text="SUBMIT", height=2, width=50, command=self.check_word)
        self.submitbutton.place(x=160, y=400)

    "When pressing the button submit:" \
    "checking if the word in our words file , if it's path is correct and if it hadn't guessed before" \
    "if the word is good: 1)adding the score and showing it. 2)adding the word to the guessed words and showing it" \
    "in the end we restarting the path, counter and deleting the text that we had entered"
    def check_word(self):
       correct_path = ex12_utils.is_valid_path(self.board, self.path,self.dict_list)
       if self.text in self.dict_list and self.text not in self.guessedwords and correct_path is not None:
           self.score += (self.buttoncounter**2)
           self.score_label.configure(text=self.score)
           self.guessedwords.append(self.text)
           self.guessedwords_label.configure(text="\n".join(self.guessedwords))
       self.path = []
       self.text = ""
       self.buttoncounter = 0
       self.wordbox.configure(text=self.text)


    def start(self):
        """STARTING THE GAME"""
        self.root.mainloop()
