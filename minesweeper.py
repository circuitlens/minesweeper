import tkinter
import random

mines_tl = [[]]

root = tkinter.Tk()
root.title("Minesweeper")

columns = None
rows = None
mines_amount = None

game_going = True

mines_tl = []
mines = []
revealed = []
row = []
flags = 0

wins_losses = [0, 0]

def generate():
    global rows, columns, mines_tl, mines, revealed, row, map, mines_amount, slider_rows, slider_columns, slider_mines, game_going, status, flags, wins_losses
    
    stats_update()
    map.destroy()
    rows = slider_rows.get()
    columns = slider_columns.get()
    mines_amount = slider_mines.get()
    flags = mines_amount
    mines_tl = []
    mines = []
    revealed = []
    row = []

    for i in range(0, columns+2):
        row.append(None)
    for i in range(0, rows+2):
        mines_tl.append(row[:])
        mines.append(row[:])
        revealed.append(row[:])

    map = tkinter.Frame(root)
    map.grid(row=3, column=0)

    for i in range(mines_amount):
        random_r = random.randint(1, rows)
        random_s = random.randint(1, columns)
        if mines[random_r][random_s] != 1:
            mines[random_r][random_s] = 1
    for i in range(1, rows+1):
        for j in range(1, columns+1):
            mines_tl[i][j] = tkinter.Button(map, text="", font=("Arial", 14, "bold"), bg="lightgray", width=3, command=lambda row=i, col=j: leftclick(row,col))
            mines_tl[i][j].grid(row=i, column=j)
            mines_tl[i][j].bind("<Button-3>", lambda event, row=i, col=j: rightclick(row,col))
    update_status()
    game_going = True

def gameover(coordinates): # [[x1, y1], [x2, y2]]
    global game_going, wins_losses
    for i in range(1, columns+1):
        for j in range(1, rows+1):
            if mines[j][i] == 1 and revealed[j][i] != -1:
                mines_tl[j][i].config(text="💣")
    for xy in coordinates:
        x, y = xy[0], xy[1]
        mines_tl[x][y].config(text="💥")
    status.config(text="You blew up! Try again!")
    wins_losses[1] += 1
    stats_update()
    game_going = False

def check_mine(row, col, first):
    global rows, columns, game_going
    if game_going == True:
        if first == True and mines[row][col] == 1:
            gameover([[row, col]])
        else:
            sum = 0
            flags = 0
            correct = 0
            incorrect = []
            for i in range(max(row-1, 1), min(row+2, rows+1)):  #range(row-1, row+2):
                for j in range(max(col-1,1), min(col+2, columns+1)):   #range(col-1, col+2):
                    if revealed[i][j] == -1:
                        flags += 1
                    if mines[i][j] == 1:
                        sum += 1
                        if revealed[i][j] == -1:
                            correct += 1
                            incorrect.append([i, j])
            if first == True and sum > 0 and flags > 0 and sum <= flags and sum == correct:
                for k in range(max(row-1, 1), min(row+2, rows+1)):
                    for l in range(max(col-1,1), min(col+2, columns+1)):
                        if revealed[k][l] == None:
                            check_mine(k,l, False)
            elif first == True and sum > 0 and flags > 0 and sum > correct:
                gameover(incorrect)
                return
            else:
                if sum != 0:
                    revealed[row][col] = sum
                    if mines_tl[row][col] != None:
                        mines_tl[row][col].config(text=str(sum), bg="gray")
                else:
                    revealed[row][col] = 0
                    if mines_tl[row][col] != None:
                        mines_tl[row][col].config(text="0", bg="gray")
                    for k in range(max(row-1, 1), min(row+2, rows+1)):
                        for l in range(max(col-1,1), min(col+2, columns+1)):
                            if revealed[k][l] == None:
                                check_mine(k, l, False)
        win_check()

def stats_update():
    global wins_losses
    statistiky.config(text=f"Stats: {wins_losses[0]} wins, {wins_losses[1]} losses")

def win_check():
    global game_going, wins_losses
    empty_count = rows*columns
    for sublist in revealed:
        for element in sublist:
            if element != None:
                empty_count = empty_count - 1
    if empty_count <= 0:
        game_going = False
        status.config(text=f"You've found every mine! Generate a new map to play again.")
        wins_losses[0] += 1
        stats_update()

def update_status():
    global flags
    status.config(text=f"Flags left: {flags}")

def mark(row, col):
    global game_going, flags, revealed
    if game_going == True:
        if revealed[row][col] == None:
            flags -= 1
            update_status()
            mines_tl[row][col].config(text="F", bg="red")
            revealed[row][col] = -1
        elif revealed[row][col] == -1:
            flags += 1
            update_status()
            mines_tl[row][col].config(text="", bg="lightgray")
            revealed[row][col] = None
        win_check()

def leftclick(row,col):
    check_mine(row,col, True)

def rightclick(row,col):
    mark(row, col)

def save():
    global wins_losses
    with open("mines_save.txt", "w") as file:
        file.write(f"{wins_losses[0]},{wins_losses[1]}")

def load():
    global wins_losses
    with open("mines_save.txt", "r") as file:
        temp = file.read().split(",")
        wins_losses[0], wins_losses[1] = int(temp[0]), int(temp[1])
    stats_update()

titleframe = tkinter.Frame(root)
titleframe.grid(row=0, column=0)
title = tkinter.Label(titleframe, text="Minesweeper", font=("Arial", 32, "bold"))
title.grid(row=0, column=0)

stats_frame = tkinter.Frame(root)
stats_frame.grid(row=1, column=0)

statistiky = tkinter.Label(stats_frame, text="Stats: 0 wins, 0 losses", font=("Arial", 12, "bold"))
statistiky.grid(row=0, column=0)
savebtn = tkinter.Button(stats_frame, text="Save", font=("Arial", 12, "bold"), bg="lightgray", width=10, command=lambda: save())
savebtn.grid(row=0, column=1)
loadbtn = tkinter.Button(stats_frame, text="Load", font=("Arial", 12, "bold"), bg="lightgray", width=10, command=lambda: load())
loadbtn.grid(row=0, column=2)


interface = tkinter.Frame(root)
interface.grid(row=2, column=0)

columns_text = tkinter.Label(interface, text="Columns:", font=("Arial", 12, "bold"))
columns_text.grid(row=0, column=0)
slider_columns = tkinter.Scale(interface, variable = columns, from_ = 5, to = 30, orient = "horizontal")
slider_columns.grid(row=0, column=1)
slider_columns.set(10)

rows_text = tkinter.Label(interface, text="Rows:", font=("Arial", 12, "bold"))
rows_text.grid(row=0, column=2)
slider_rows = tkinter.Scale(interface, variable = rows, from_ = 5, to = 30, orient = "horizontal")
slider_rows.grid(row=0, column=3)
slider_rows.set(10)

mines_text = tkinter.Label(interface, text="Amount of mines:", font=("Arial", 12, "bold"))
mines_text.grid(row=1, column=0)
slider_mines = tkinter.Scale(interface, variable = mines_amount, from_ = 5, to = 100, orient = "horizontal")
slider_mines.grid(row=1, column=1)
slider_mines.set(10)

generate_btn = tkinter.Button(interface, text="Generate", font=("Arial", 12, "bold"), bg="lightgray", width=10, command=lambda: generate())
generate_btn.grid(row=1, column=2, columnspan = 2)

status = tkinter.Label(interface, text="", font=("Arial", 20, "bold"))
status.grid(row=2, column=0, columnspan = 4)


map = tkinter.Frame(root)
map.grid(row=3, column=0)

generate()
root.mainloop()

