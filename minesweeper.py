'''MineSweeper
   Abel Svoboda
   22/07/15'''
from tkinter import Tk, Canvas, StringVar, Label, PhotoImage, Frame, IntVar, Radiobutton, Entry, Scale, HORIZONTAL, Button
from random import randrange
import os, sys


class Top(object):
    classes = {}


class GUI(Top):
    def __init__(self, window, canvas, size):
        self.classes['gui'] = self
        self.window = window
        self.canvas = canvas
        self.size = size

        self.after = None
        self.on = {}
        self.time = 0

        self.time_var = StringVar()
        self.time_var.set('000')
        self.time_label=Label(self.window,textvariable=self.time_var,font=('Arial Rounded MT Bold',self.size*10),bg='#000000',fg='#FF0000')
        self.time_label.grid(row=0,column=2,ipadx=1,padx=(0,30))

        self.get_highscores()

        self.create_images()
        self.create_drop_down()

        self.create_drop_down_2()


        self.count()
        self.restart_button()
        self.win_screen()

    def get_highscores(self):
        try:
            file = open('highscores.dat','r')
        except FileNotFoundError:
            file = open('highscores.dat','w')
            for i in range(3):
                for i in range(10):
                    file.write('None 999\n')
                file.write('\n')
            file.close()
            file = open('highscores.dat','r')

        lines = [x.strip('\n') for x in file.readlines() if x != '\n']
        self.highscores = []
        for p in range(3):
            self.highscores.append([])
            for i in range(10):
                i = i + 10*p
                name, score = lines[i].split()
                self.highscores[p].append((score, name))
        file.close()

    def change_highscore_panel(self, widget, frame):
        options = set([self.easy_menu, self.med_menu, self.hard_menu])
        different = options - set([frame])
        frame.grid(row=2, column=0, columnspan=3)
        for i in different:
            i.grid_forget()

        #change button colour
        options = set([self.easy_button, self.med_button, self.hard_button])
        different = options - set([widget])
        widget.configure(bg='#BEBEBE')
        for i in different:
            i.configure(bg='#F0F0F0')

    def create_drop_down_2(self):
        self.highscores_menu = Frame(self.window, bd=1, relief='solid')
        #self.highscores_menu.config(highlightbackground='red')

        #Name
        Label(self.highscores_menu,text='#').grid(row=1,column=0)
        self.name_label = Label(self.highscores_menu, text='Name')
        self.name_label.grid(row=1, column=1, padx=48)
        self.score1_label = Label(self.highscores_menu, text='Time')
        self.score1_label.grid(row=1,column=2)

        self.highscores_menu_drop = Label(self.window, text='♕',bg='#6E6E6E', font=9, bd=1, relief='solid', highlightbackground='red')
        self.highscores_menu_drop.grid(row=0, column=0, sticky='ne',ipadx=4,ipady=1,columnspan=3)
        self.highscores_menu_drop.bind('<Button-1>', lambda event, dropdown=self.highscores_menu, d='ne':self.open_options('♕','highscores ♕',event,dropdown,d))
        self.on[self.highscores_menu] = False

        self.c = '#6E6E6E'
        self.highscores_menu_drop.bind("<Enter>", lambda event,c='#E5F3FF':self.highlight_button(event,c))
        self.highscores_menu_drop.bind("<Leave>", lambda event,c=None:self.highlight_button(event,c))

        #EASY
        self.easy_menu = Frame(self.highscores_menu)
        self.easy_menu.grid(row=2, column=0, columnspan=3)
        self.easy_hs_vars = []
        for i in range(10):
            self.easy_hs_vars.append([StringVar(),StringVar()])
            self.easy_hs_vars[i][1].set(self.highscores[0][i][0])
            self.easy_hs_vars[i][0].set(self.highscores[0][i][1])
            Label(self.easy_menu,text=str(i+1)).grid(row=i+2,column=0,padx=8)
            Label(self.easy_menu, textvariable=self.easy_hs_vars[i][0], width=15).grid(row=i+2,column=1,pady=2,padx=12)
            Label(self.easy_menu, textvariable=self.easy_hs_vars[i][1]).grid(row=i+2,column=2,pady=2,padx=10)

        #MEDIUM
        self.med_menu = Frame(self.highscores_menu)
        self.med_menu.grid(row=2, column=0, columnspan=3)
        self.med_hs_vars = []
        for i in range(10):
            self.med_hs_vars.append([StringVar(),StringVar()])
            self.med_hs_vars[i][1].set(self.highscores[1][i][0])
            self.med_hs_vars[i][0].set(self.highscores[1][i][1])
            Label(self.med_menu,text=str(i+1)).grid(row=i+2,column=0,padx=8)
            Label(self.med_menu, textvariable=self.med_hs_vars[i][0], width=15).grid(row=i+2,column=1,pady=2,padx=12)
            Label(self.med_menu, textvariable=self.med_hs_vars[i][1]).grid(row=i+2,column=2,pady=2,padx=10)

        #HARD
        self.hard_menu = Frame(self.highscores_menu)
        self.hard_menu.grid(row=2, column=0, columnspan=3)
        self.hard_hs_vars = []
        for i in range(10):
            self.hard_hs_vars.append([StringVar(),StringVar()])
            self.hard_hs_vars[i][1].set(self.highscores[2][i][0])
            self.hard_hs_vars[i][0].set(self.highscores[2][i][1])
            Label(self.hard_menu,text=str(i+1)).grid(row=i+2,column=0,padx=8)
            Label(self.hard_menu, textvariable=self.hard_hs_vars[i][0], width=15).grid(row=i+2,column=1,pady=2,padx=12)
            Label(self.hard_menu, textvariable=self.hard_hs_vars[i][1]).grid(row=i+2,column=2,pady=2,padx=10)

        scores=self.easy_menu
        self.easy_button = Button(self.highscores_menu, text='Easy',
                                  command=lambda:self.change_highscore_panel(self.easy_button, self.easy_menu))
        self.easy_button.grid(row=0,column=0,pady=10)
        self.med_button = Button(self.highscores_menu, text='Medium',
                                 command=lambda:self.change_highscore_panel(self.med_button, self.med_menu))
        self.med_button.grid(row=0,column=1)
        self.hard_button = Button(self.highscores_menu, text='Hard', bg='#BEBEBE',
                                  command=lambda:self.change_highscore_panel(self.hard_button, self.hard_menu))
        self.hard_button.grid(row=0,column=2)


        self.c = '#6E6E6E'
        self.options_drop.bind("<Enter>", lambda event,c='#E5F3FF':self.highlight_button(event,c))
        self.options_drop.bind("<Leave>", lambda event,c=None:self.highlight_button(event,c))

    def create_drop_down(self):
        self.options = Frame(self.window, bd=1, relief='solid')
        #self.options.config(highlightbackground='red')


        #self.difficulty_label = Label(self.options, text='Difficulty')
        #self.difficulty_label.grid(row=1, column=0)
        func = self.options.register(self.validate_value)
        #(self.options.register(self.validate_value), '%P', 10)


        Label(self.options, text='rows').grid(row=0,column=2,pady=10)
        Label(self.options, text='cols').grid(row=0,column=3)
        Label(self.options, text='mines').grid(row=0,column=4,padx=(0,10))
        #Easy
        self.easy_label = Label(self.options, text='Easy')
        self.easy_label.grid(row=1, column=1)
        self.button_var = IntVar()
        self.button_var.set(0)
        self.radio0 = Radiobutton(self.options, variable=self.button_var, value=0, command=self.select)
        self.radio0.grid(row=1,column=0,sticky='e')
        Label(self.options, text='9').grid(row=1,column=2)
        Label(self.options, text='9').grid(row=1,column=3)
        Label(self.options, text='12').grid(row=1,column=4,padx=(0,10))

        self.med_label = Label(self.options, text='Medium')
        self.med_label.grid(row=2, column=1)
        #medium_var = IntVar()
        self.radio1 = Radiobutton(self.options, variable=self.button_var, value=1, command=self.select)
        self.radio1.grid(row=2,column=0,padx=(9,0),sticky='e')
        Label(self.options, text='16').grid(row=2,column=2)
        Label(self.options, text='16').grid(row=2,column=3)
        Label(self.options, text='40').grid(row=2,column=4,padx=(0,10))

        self.hard_label = Label(self.options, text='Hard')
        self.hard_label.grid(row=3, column=1)
        #hard_var = IntVar()
        self.radio2 = Radiobutton(self.options, variable=self.button_var, value=2, command=self.select)
        self.radio2.grid(row=3,column=0,sticky='e')
        Label(self.options, text='16').grid(row=3,column=2)
        Label(self.options, text='30').grid(row=3,column=3)
        Label(self.options, text='75').grid(row=3,column=4,padx=(0,10))

        self.custom_label = Label(self.options, text='Custom')
        self.custom_label.grid(row=4, column=1)
        #self.button_var = IntVar()
        self.radio3 = Radiobutton(self.options, variable=self.button_var, value=3, command=self.select)
        self.radio3.grid(row=4,column=0,sticky='e')

        #self.x_label = Label(self.options, text='rows')
        #self.x_label.grid(row=4, column=1)
        self.row_var = StringVar()
        self.entry_x = Entry(self.options, textvariable=self.row_var, width=4, validate='key', validatecommand=(func, '%P', 100))
        self.entry_x.grid(row=4, column=2, padx=5)

        #self.y_label = Label(self.options, text='cols')
        #self.y_label.grid(row=5, column=1)
        self.col_var = StringVar()
        self.entry_y = Entry(self.options, textvariable=self.col_var, width=4, validate='key', validatecommand=(func, '%P', 100))
        self.entry_y.grid(row=4, column=3, padx=5)

        self.mine_var = StringVar()
        self.entry_m = Entry(self.options, textvariable=self.mine_var, width=4, validate='key', validatecommand=(func, '%P', 10000))
        self.entry_m.grid(row=4, column=4, padx=(0,10))

        self.size_label = Label(self.options, text='Size')
        self.size_label.grid(row=6, column=1, columnspan=1, sticky='s', pady=3)
        self.size_scale = Scale(self.options, from_=1, to=5, orient=HORIZONTAL)
        self.size_scale.grid(row=6, column=2, columnspan=4, padx=(0,13))

        Button(self.options, text='Start new game', command=lambda:self.restart(False)).grid(row=7, column=0, columnspan=5, padx=1, pady=5)

        self.options_drop = Label(self.window, text='⚙',bg='#6E6E6E', font=9, bd=1, relief='solid', highlightbackground='red')
        self.options_drop.grid(row=0, column=0, sticky='nw',ipadx=4,ipady=1,columnspan=3)
        self.options_drop.bind('<Button-1>', lambda event, dropdown=self.options, d='nw': self.open_options('⚙','⚙ options',event,dropdown,d))
        self.on[self.options] = False

        self.c = '#6E6E6E'
        self.options_drop.bind("<Enter>", lambda event,c='#E5F3FF':self.highlight_button(event,c))
        self.options_drop.bind("<Leave>", lambda event,c=None:self.highlight_button(event,c))

        self.easy_label.bind("<Button-1>", lambda event, value=0:self.select(event,value))
        self.med_label.bind("<Button-1>", lambda event, value=1:self.select(event,value))
        self.hard_label.bind("<Button-1>", lambda event, value=2:self.select(event,value))
        self.custom_label.bind("<Button-1>", lambda event, value=3:self.select(event,value))

    def highlight_button(self, event, c):
        if c is None:
            c = self.c
        event.widget.config(bg=c)

    def open_options(self, word1, word2, event, dropdown, direction, icon=None):
        if event is None:
            w = icon
        else:
            w = event.widget
        if self.on[dropdown]:
            dropdown.grid_remove()
            w.config(bg='#6E6E6E', text=word1)
            self.c = '#6E6E6E'
            self.on[dropdown] = False
        else:
            dropdown.grid(row=0, column=0, pady=(23,0), columnspan=3, rowspan=2, sticky=direction)
            dropdown.lift()
            w.config(bg='#F0F0F0', text=word2)
            self.c = '#F0F0F0'
            self.on[dropdown] = True

    def create_images(self):
        self.smile_image = PhotoImage(file='img/smile.gif')
        if self.size != 1:
            self.smile_image = self.smile_image.zoom(int(self.size))

    def timer(self):
        self.time += 1
        if self.time <= 999:
            self.time_var.set('0'*(3-len(str(self.time)))+str(self.time))
            self.after = self.canvas.after(1000, self.timer)

    def count(self):
        self.count_var = StringVar()
        self.count_label = Label(self.window, textvariable=self.count_var,font=('Arial Rounded MT Bold',self.size*10),bg='#000000',fg='#FF0000')
        self.count_label.grid(row=0,column=0,ipadx=1,padx=(30,0))

    def validate_length(self, word):
        return len(word) < 10

    def validate_value(self, value, max_value):
        max_value = int(max_value)
        try:
            return int(value) < max_value
        except ValueError:
            if value == '':
                return True
            return False

    def win_screen(self):
        self.win_frame = Frame(self.window, bd=5)
        self.win_frame.grid(row=1,column=0, columnspan=3)
        self.win_frame.grid_remove()
        #self.win_frame.lift()
        self.win_label = Label(self.win_frame, text='YOU WIN!')
        self.win_label.grid(row=0, column=0, columnspan=2)
        self.name_label = Label(self.win_frame, text='Enter Name:')
        self.name_label.grid(row=1, column=0, columnspan=2)
        self.final_name = StringVar()
        vcmd = (self.win_frame.register(self.validate_length), '%P')

        self.name_entry = Entry(self.win_frame, textvariable=self.final_name, width=15, validate='key', validatecommand=vcmd)
        self.name_entry.grid(row=2, column=0)
        self.final_time_label = Label(self.win_frame, text='Score:')
        self.final_time_label.grid(row=3, column=0)
        self.final_score = StringVar()
        self.final_score.set('435')
        self.final_time_score = Label(self.win_frame, textvariable=self.final_score)
        self.final_time_score.grid(row=3, column=1)

        self.submit_button = Button(self.win_frame, text='Submit', command=self.submit_score)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def submit_score(self):
        difficulty = self.classes['game'].difficulty
        if difficulty == 3:
            difficulty = 2
        highscores = self.highscores[difficulty]
        score = self.final_score.get()
        name = self.final_name.get()
        if name == '':
            return

        highscores.append((score, name))
        highscores.sort()
        highscores.pop()
        self.highscores[difficulty] = highscores
        self.win_frame.lower()
        self.win_frame.grid_remove()
        self.update_highscore_values(difficulty)


    def update_highscore_values(self, difficulty):
        highscores = self.highscores[difficulty]
        difficulty_vars = [self.easy_hs_vars, self.med_hs_vars, self.hard_hs_vars][difficulty]

        i = 0
        for score, name in difficulty_vars:
            score.set(highscores[i][1])
            name.set(highscores[i][0])
            i += 1

        #Write data to file for future use
        file = open('highscores.dat', 'w')
        for level in self.highscores:
            for score, name in level:
                file.write(name + ' ' + score + '\n')
            file.write('\n')
        file.close()

    def restart_button(self):
        self.restart_b = Button(self.window,image=self.smile_image,bd=self.size, command=self.restart)
        self.restart_b.grid(row=0,column=1,pady=self.size*4)

    def restart(self, default=True):
        self.win_frame.lower()
        self.win_frame.grid_remove()
        self.time = 0
        self.time_var.set('000')
        if self.after is not None:
            self.canvas.after_cancel(self.after)

        difficulty = self.button_var.get()
        if default:
            mines = self.classes['game'].num_bombs
            self.count_var.set('0'*(3-len(str(mines)))+str(mines))
            self.classes['game'].restart()
            return
        elif difficulty == 0:
            cols = 9
            rows = 9
            mines = 12
        elif difficulty == 1:
            cols = 16
            rows = 16
            mines = 40
        elif difficulty == 2:
            cols = 30
            rows = 16
            mines = 75
        else:
            cols = int(self.col_var.get())
            rows = int(self.row_var.get())
            mines = int(self.mine_var.get())

        self.count_var.set('0'*(3-len(str(mines)))+str(mines))

        size = int(self.size_scale.get())
        self.count_label.configure(font=('Arial Rounded MT Bold',size*10))
        self.time_label.configure(font=('Arial Rounded MT Bold',size*10))
        self.count_label.grid(row=0,column=0,ipadx=size*2-1,padx=(30,0))
        self.time_label.grid(row=0,column=2,ipadx=size*2-1,padx=(0,30))

        self.classes['game'].restart(difficulty, cols, rows, size, mines)
        self.open_options('⚙','⚙ options',None,self.options,'nw',self.options_drop)

    def select(self, event=None, value=None):
        if event is not None:
            self.button_var.set(value)

    def win_game(self):
        self.canvas.after_cancel(self.after)
        self.restart_b.configure(image=self.classes['game'].smile_win_image)
        self.final_score.set(self.time)
        if self.classes['game'].difficulty != 3:
            self.win_frame.grid()
            self.win_frame.lift()

class Game(Top):
    def __init__(self, window, cols, rows, size=1, num_bombs=None):
        self.gui = self.classes['gui']
        self.classes['game'] = self
        self.chance = .15625
        if num_bombs is None:
            num_bombs = int(cols*rows*self.chance)
        self.num_bombs = num_bombs
        self.window = window
        self.difficulty = 0
        self.size = size
        self.cols = cols
        self.rows = rows
        self.time = 0
        self.flags = 0
        self.gui.count_var.set('0'*(3-len(str(self.num_bombs-self.flags)))+str(self.num_bombs-self.flags))
        self.clicked = False
        self.colours = ['#0000FF','#007B00','#FF0000','#00007B','#7B0000','#007B7B','#000000','#7B7B7B']
        self.on_button = {}
        self.squares = {}
        self.mines = {}
        self.windows = {}
        self.num_vars = {}
        self.expanded = {}
        self.d={}
        self.grid = Frame(window, background='#7B7B7B')
        self.grid.grid(row=1,column=0,columnspan=3,rowspan=2,pady=(0,0))
        self.create_images()
        self.redo_images()
        self.draw_board()
        self.gui.options.lift()
        self.gui.options_drop.lift()
        self.gui.highscores_menu.lift()
        self.gui.highscores_menu_drop.lift()

    def remove_grid(self):
        self.clicked = False
        self.time = 0
        self.flags = 0

        for i in self.d:
            self.d[i].destroy()
        self.squares = {}
        for i in self.squares:
            self.squares[i].destroy()
        self.squares = {}
        for i in self.windows:
            self.windows[i].destroy()
        self.windows = {}
        for i in self.mines:
            self.mines[i].destroy()
        self.mines = {}

        self.on_button = {}
        self.num_vars = {}
        self.expanded = {}

    def create_images(self):
        self.xsmile_image = PhotoImage(file='img/smile.gif')
        self.xmine_image = PhotoImage(file='img/mine.gif')
        self.xred_mine_image = PhotoImage(file='img/red_mine.gif')
        self.xflag_image = PhotoImage(file='img/flag.gif')
        self.xblock_image = PhotoImage(file='img/block.gif')
        self.xdefault_image = PhotoImage(file='img/default.gif')
        # self.xdefault_small = PhotoImage(file='img/default_small.gif')
        self.xsmile_playing_image = PhotoImage(file='img/smile_playing.gif')
        self.xsmile_lose_image = PhotoImage(file='img/smile_lose.gif')
        self.xsmile_win_image = PhotoImage(file='img/smile_win.gif')

    def redo_images(self):
        self.smile_image = self.xsmile_image
        self.mine_image = self.xmine_image
        self.red_mine_image = self.xred_mine_image
        self.flag_image = self.xflag_image
        self.block_image = self.xblock_image
        self.default_image = self.xdefault_image
        # self.default_small = self.xdefault_small
        self.smile_playing_image = self.xsmile_playing_image
        self.smile_lose_image = self.xsmile_lose_image
        self.smile_win_image = self.xsmile_win_image
        self.resize_images()

    def resize_images(self):
        '''d'''
        if self.size != 1:
            self.smile_image = self.smile_image.zoom(int(self.size))
            self.mine_image = self.mine_image.zoom(int(self.size))
            self.red_mine_image = self.red_mine_image.zoom(int(self.size))
            self.block_image = self.block_image.zoom(int(self.size))
            self.default_image = self.default_image.zoom(int(self.size))
            # self.default_small = self.default_small.zoom(int(self.size))
            self.flag_image = self.flag_image.zoom(int(self.size))
            self.smile_playing_image = self.smile_playing_image.zoom(int(self.size))
            self.smile_lose_image = self.smile_lose_image.zoom(int(self.size))
            self.smile_win_image = self.smile_win_image.zoom(int(self.size))
        self.gui.restart_b.configure(image=self.smile_image)

    def draw_board(self):
        '''creates the minesweeper grid'''
        padx_values = [3,7,11,15,19]
        font_size_values = [8,16,24,33,41]
        for row in range(self.rows):
            for col in range(self.cols):
                #frame
                self.frame = Frame(self.grid,width=self.size*17,height=self.size*17,bg='#555555',bd=0)
                self.frame.grid(row=row,column=col, padx=0, pady=0)
                self.frame.grid_propagate(0)
                self.windows[(row,col)] = self.frame
                #labels
                self.num_vars[(row,col)] = StringVar()
                self.num_vars[(row,col)].set('0')

                self.d[(row,col)] = Label(self.frame, background='#BDBDBD',textvariable=self.num_vars[(row,col)],font=('DINPro-Black',font_size_values[self.size-1]),bd=0)
                self.d[(row,col)].grid(row=0, column=0, ipadx=padx_values[self.size-1], ipady=self.size*1-1)
                self.d[(row,col)].grid_propagate(1)

                self.squares[(row,col)] = Label(self.frame,image=self.block_image,bd=0)
                self.squares[(row,col)].grid(row=0, column=0)

                self.squares[(row,col)].flagged = False

                #binds
                self.squares[(row,col)].bind('<Button-3>', lambda event=0,row=row,col=col:self.right_click(event,row,col))
                self.squares[(row,col)].bind('<Button-1>', lambda event=0,row=row,col=col:self.left_click(event,row,col))
                self.squares[(row,col)].bind('<ButtonRelease-1>', lambda event=0,row=row,col=col:self.left_click_r(event,row,col))
                self.squares[(row,col)].bind("<Enter>", lambda event=0,row=row,col=col:self.enter(event,row,col))
                self.squares[(row,col)].bind("<Leave>", lambda event=0,row=row,col=col:self.leave(event,row,col))

    def enter(self, event, row, col):
        '''sets the on_button variable of that square to be True if the mouse pointer enters it'''
        self.on_button[(row,col)] = True

    def leave(self, event, row, col):
        '''sets the on_button variable of that square to be False if the mouse pointer leaves it'''
        self.on_button[(row,col)] = False

    def check_around_position(self, start_row, start_col, row, col):
        '''checks the square and returns True if it is a square around the one clicked'''
        for r in range(-1,2):
            for c in range(-1,2):
                if (start_row+r,start_col+c) == (row,col):
                    return True
        return False

    def create_mines(self, start_row, start_col):
        '''randomly places mines on the grid until the desired amount is reached'''
        chance = self.chance*100/10
        num_mines = 0
        while True:
            for row in range(self.rows):
                for col in range(self.cols):
                    if randrange(0,100) <= chance and start_row != row and start_col != col and (row,col) not in self.mines:
                        if self.check_around_position(start_row,start_col,row,col):
                            continue
                        else:
                            self.mines[(row,col)] = Label(self.windows[(row,col)], image=self.mine_image, background='#7B7B7B', bd=0)
                            self.mines[(row,col)].grid(row=0, column=0)
                            self.squares[(row,col)].lift()
                            num_mines += 1
                            if num_mines == self.num_bombs:
                                return

    def start(self, start_row, start_col):
        '''calculates and stores the number of mines around each square'''
        self.gui.timer()

        self.create_mines(start_row, start_col)
        for row in range(self.rows):
            for col in range(self.cols):
                if (row,col) not in self.mines:
                    nearby_mines = 0
                    for r in range(-1,2):
                        for c in range(-1,2):
                            if (row+r,col+c) in self.mines:
                                nearby_mines += 1
                    self.num_vars[(row,col)].set(str(nearby_mines))
                    self.d[(row,col)].configure(fg=self.colours[nearby_mines-1])
                    if nearby_mines == 0:
                        self.d[(row,col)].config(fg="#BDBDBD")

        self.gui.options.lift()
        self.gui.options_drop.lift()

    def lose(self, row, col):
        '''puts the game into a restricted state when the game is lost'''
        self.mines[(row,col)].configure(image=self.red_mine_image)
        self.gui.restart_b.configure(image=self.smile_lose_image)
        self.gui.canvas.after_cancel(self.gui.after)
        for i in self.squares:
            self.squares[i].unbind("<Button-1>")
            self.squares[i].unbind("<ButtonRelease-1>")
            self.squares[i].unbind("<Button-3>")
        for mine in self.mines:
            self.mines[mine].lift()
            if mine in self.squares:
                self.squares[mine].destroy()

    def calculate_nearby_mines(self, row, col):
        '''performs an iterative breadth first search to expand an area that is free of mines'''
        nodes = [(row,col)]
        while len(nodes) > 0:
            row, col = nodes.pop()
            if (row,col) not in self.expanded:
                self.expanded[(row,col)] = 0
                if self.num_vars[(row,col)].get() == '0':
                    for r in range(-1,2):
                        for c in range(-1,2):
                            #if r != 0 or c != 0:
                            if (row+r,col+c) not in self.mines and (row+r,col+c)\
                               not in self.expanded and (row+r,col+c) in self.squares:
                                if self.num_vars[(row+r,col+c)].get() == '0':
                                    self.squares[(row+r,col+c)].destroy()
                                    del self.squares[(row+r,col+c)]
                                    nodes.append((row+r,col+c))
                                    #self.calculate_nearby_mines(row+r,col+c)
                                else:
                                    self.squares[(row+r,col+c)].destroy()
                                    del self.squares[(row+r,col+c)]

    def redraw_mine_count(self):
        self.gui.count_var.set('0'*(3-len(str(self.num_bombs-self.flags)))+str(self.num_bombs-self.flags))

    def left_click(self, event, row, col):
        '''provides visual feedback when the left mouse button is clicked'''
        self.squares[(row,col)].configure(image=self.default_image)
        self.gui.restart_b.configure(image=self.smile_playing_image)

    def left_click_r(self, event, row, col, bypass=False):
        '''provides visual feedback and performs actions when the left mouse button is released'''
        self.gui.restart_b.configure(image=self.smile_image)
        if self.on_button[(row,col)] or bypass:
            if self.squares[(row,col)].flagged:
                self.flags -= 1
                self.redraw_mine_count()
            if not self.clicked:
                self.clicked = True
                self.start(row,col)
            self.squares[(row,col)].destroy()
            del self.squares[(row,col)]
            if (row,col) in self.mines:
                self.lose(row,col)
                return
            self.calculate_nearby_mines(row,col)
            if (row,col) in self.squares:
                del self.squares[(row,col)]
            if self.squares.keys() == self.mines.keys():
                for i in self.squares:
                    self.squares[i].unbind("<Button-1>")
                    self.squares[i].unbind("<ButtonRelease-1>")
                    self.squares[i].unbind("<Button-3>")
                self.gui.win_game()
        else:
            self.squares[(row,col)].configure(image=self.block_image)
            self.gui.restart_b.configure(image=self.smile_image)

    def right_click(self, event, row, col):
        '''flags/unflags the square when the right mouse button is clicked'''
        if self.squares[(row,col)].flagged:
            self.squares[(row,col)].configure(image=self.block_image)
            self.squares[(row,col)].flagged = False
            self.flags -= 1
        else:
            self.squares[(row,col)].configure(image=self.flag_image)
            self.squares[(row,col)].flagged = True
            self.flags += 1

        self.redraw_mine_count()

    def restart(self, *args):
        '''resets variables that change throughout gameplay'''
        self.gui.restart_b.configure(image=self.smile_image)
        if args != ():
            difficulty, cols, rows, size, mines = args
            self.difficulty = difficulty
            if mines > cols * rows:
                mines = cols * rows
            self.cols = cols
            self.rows = rows
            self.size = size
            self.num_bombs = mines
        self.remove_grid()
        self.redo_images()
        self.draw_board()


def main():
    '''Intialises the window, game and the gui'''
    window = Tk()
    window.configure(background='#6E6E6E')
    window.wm_title("MineSweeper")
    window.resizable(0,0)
    # window.iconbitmap('icon.gif')
    imgicon = PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'icon.gif'))
    window.tk.call('wm', 'iconphoto', window._w, imgicon)
    canvas = Canvas(window)
    size = 1
    gui = GUI(window, canvas, size)
    game = Game(window, 9, 9, size, 12)

    window.mainloop()


if __name__ == '__main__':
    main()
