from tkinter import *
import numpy as np
import random
import time


class tic_tac_toe:
    btn_dict = {i: [j for j in range(9)] for i in range(9)}
    frames = [0 for i in range(9)] 
    current_value = 'X'
    win_position = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    temp = [" " for i in range(9)]
    flag = 1


    def __init__(self):
        self.game = Tk()
        self.start()
        self.game.mainloop()

    def start(self):

        self.game.title('Tic Tac Toe')
        self.game.geometry('400x550')
        self.game.resizable(False,False)
        self.game.config(bg= 'grey',padx=25 ,pady=25)
        self.Title_frame = Frame(self.game)
        self.Title_frame.pack(side=TOP,padx=35,fill=X)
        self.player_frame = Frame(self.game,bg='grey')
        self.player_frame.pack(side=TOP,padx=35,fill=X)
        self.game_frame = Frame(self.game)
        self.game_frame.pack(side=BOTTOM,padx=20,pady=20)
        
        title =  Label(self.Title_frame,text='Ultimate Tic Tac Toe' ,font=15 , pady=5)
        title.pack(side=TOP)
        self.player =  Label(self.Title_frame,text="X's Turn" ,font=15 , pady=15 ,bg='grey',fg='blue')
        self.player.pack(side=TOP,fill=X)

        m,n=0,0
        for i in range(9):
            if n % 3 == 0:
                n = 0
                m += 1
            self.frames[i] = Frame(self.game_frame , bg='black', bd=1)
            self.frames[i].grid(row=m , column=n)
            n += 1

        for i in range(9):
            m,n = 0,0
            for j in range(9):
                if n % 3 == 0:
                    n = 0
                    m += 1

                self.btn_dict[i][j] = Button(self.frames[i] , text=" " ,width=2 , font=100 , relief=RIDGE , command= lambda i=i,j=j : self.place_value(i,j,self.flag))
                self.btn_dict[i][j].grid(row=m , column=n)
                n += 1

    
    def place_value(self,i,j , flag):

        self.btn_dict[i][j].config(text = self.current_value , state = DISABLED,disabledforeground='black')
        self.change_player()

        winner = self.check_blockwin(i)
        if  winner:
            self.assign_pos(i ,winner)

        win = self.check_victory()
        if(win):
            print("winner--",win)
            self.disabled_all()
            self.final_winner(win)
            return

        if self.check_final_draw():
            self.disabled_all()
            self.final_winner(-1)
            return
        
        active_frame = self.change_frame(j)
        print("--->>> current frame is ",active_frame)
        

        if((flag == 1) and (self.current_value == 'O')):
            print('current value is' , self.current_value)
            self.game.after(700, lambda: self.system_turn(active_frame))


    
    def change_player(self):
        if self.current_value == 'X':
            self.player.config(text="O's Turn" , fg='red')
            self.current_value = 'O'
        else:
            self.player.config(text="X's Turn" , fg='blue')
            self.current_value = 'X'

    def check_blockwin(self , i):
        for j in self.win_position:
            if ((self.btn_dict[i][j[0]]['text'] == self.btn_dict[i][j[1]]['text'] == self.btn_dict[i][j[2]]['text']) and (self.btn_dict[i][j[1]]['text'] != " ")):
                return self.btn_dict[i][j[1]]['text']
        return False
    
    def check_final_draw(self):
        for i in range(9):
            if (len(self.frames[i].winfo_children()) != 1):
                for j in range(9):
                    if self.btn_dict[i][j]['text'] == " ":
                        return False
        for j in self.win_position:
            print(self.temp)
            if((self.temp[j[0]] == self.temp[j[1]]  == self.temp[j[2]] ) and (self.temp[j[0]]!= " ")):
                print('final winner is ',self.temp[j[0]])
                return False
        return True

    def assign_pos(self,i, winner):
        
        for j in self.frames[i].winfo_children():
            j.destroy()

        new_frame = Frame(self.frames[i], bd=1 ,padx=23,pady=32)
        new_frame.grid(row=0, column=0)

        new_btn = Button(new_frame, text=winner, state=DISABLED, fg='black', relief=FLAT,padx=15,pady=15)
        new_btn.grid(row=0, column=0)

        self.frames[i] = new_frame

       
    def check_victory(self):
        print('temp in check_victory',self.temp)
        for i in range(9):
            if(len(self.frames[i].winfo_children()) == 1):
                self.temp[i] = self.frames[i].winfo_children()[0].cget('text')


        for j in self.win_position:
            if((self.temp[j[0]] == self.temp[j[1]]  == self.temp[j[2]] ) and (self.temp[j[0]]!= " ")):
                return self.temp[j[1]]
                
        return False
    
    def disabled_all(self):
        for i in range(9):
            if(len(self.frames[i].winfo_children()) != 1):
                for j in self.btn_dict[i]:
                    j.config(state = DISABLED)
                    print('button disabled', j)

    def final_winner(self,win):
        if win == -1:
            self.player.config(text="Game Draw" , fg='black')
        elif win:
            self.player.config(text="Winner is "+ win , fg='black')



    def change_frame(self,i):
        if((len(self.frames[i].winfo_children()) == 1) or (self.block_draw(self.frames[i]))):
            print("length of child",len(self.frames[i].winfo_children()) ,"is block draw", self.block_draw(self.frames[i]) )
            for j in range(9):
                if(len(self.frames[j].winfo_children()) != 1):
                    print('-->> in change frame , possible frame is ', j)
                    for k in self.btn_dict[j]:
                        k.config(bg='white')
                        if((k.cget('text') !="X") and (k.cget('text') != "O")):
                            print('state is normal')
                            k.config(state = NORMAL)
                        else:
                            k.config(state = DISABLED)
            return -1
     

        else:
            for j in range(9):
                if((len(self.frames[j].winfo_children()) != 1)  and ( j != i)):
                    for k in self.btn_dict[j]:
                        k.config(state = DISABLED , bg='white')
                    

            for j in range(9):
                self.btn_dict[i][j].config(bg='red')
                if((self.btn_dict[i][j].cget('text') !="X") and (self.btn_dict[i][j].cget('text') != "O")):
                    self.btn_dict[i][j].config(state = NORMAL)
                else:                        
                    self.btn_dict[i][j].config(state = DISABLED)
            
            return i

    def block_draw(self,frame):
        for i in frame.winfo_children():
            if(i.cget('text')== " "):
                return False
        return True

    def system_turn(self, j):
        possible_position = []
        best_choice = []

        if (j == -1):
            print('finding in all frame')
            possible_position = self.efficient_position_all_frame()
        else:
            print('finding in one frame')
            possible_position = self.efficient_position_one_frame(j)
            best_choice = self.next_to_the_win(best_choice,j,'X')
            for a,b in possible_position:
                for c,d in best_choice:
                    if ([a,b]==[c,d]):
                        print('from best choice')
                        possible_position = [[a,b]]
                        break

        print('possible position found is : ' , possible_position)

        if(len(possible_position)>0):

            system_choice = random.choice(possible_position)
            print('exact choice found is : ',system_choice)
            self.place_value(system_choice[0],system_choice[1],self.flag)
        else:
            print('no possible position')
    
    def efficient_position_one_frame(self , i):
        possible_position = []

        possible_position = self.next_to_the_win(possible_position,i,'O')
        print('*1*  possible position found blockwin : ' , possible_position)
        if(len(possible_position)>0):
            print('*1* final position returning with blockwin')
            return possible_position
        else:
            all_move = []
            danger_pos = []
            for j in range(9):
                if (self.btn_dict[i][j]['state'] == 'normal'):
                    all_move.append(j)
            
            print('*1*  all move out of 9 :',all_move)

            danger_pos = self.block_oppenient_next(all_move)
            print('*1*  danger possition ', danger_pos)
            if(len(danger_pos)>0):
                for k in all_move:
                    possible_position.append([i, k])
                for m, n in danger_pos:
                    possible_position.remove([i,m])
                print('*1*  possible position after removing danger ', possible_position)
                if len(possible_position) == 0:
                    for j in all_move:
                        possible_position.append([i,j])
                    return possible_position
            else:
                print('*1* no danger position')
                for j in all_move:
                    possible_position.append([i,j])

        print('final possible position without returning blockwin')   
        return possible_position
    
    def next_to_the_win(self,possible_position,i,key):

        for j in self.win_position:
            if((self.btn_dict[i][j[0]]['text']  == self.btn_dict[i][j[1]]['text'] == key) and (self.btn_dict[i][j[2]]['text'] == " ")):
                possible_position.append([i,j[2]])
                break
            elif((self.btn_dict[i][j[0]]['text']  == self.btn_dict[i][j[2]]['text'] == key) and (self.btn_dict[i][j[1]]['text'] == " ")):
                possible_position.append([i,j[1]])
                break
            elif((self.btn_dict[i][j[2]]['text']  == self.btn_dict[i][j[1]]['text'] == key) and (self.btn_dict[i][j[0]]['text'] == " ")):
                possible_position.append([i,j[0]])
                break
        
        return possible_position
    
    def block_oppenient_next(self,all_move):
        reduced_list = []
        final_list = []
        list_ = []
        
        for i in all_move:
            if((len(self.frames[i].winfo_children()) == 1) or (self.block_draw(self.frames[i]))):
                final_list.append([i,-1])
            else:
                reduced_list.append(i)
        for i in reduced_list:
            final_list = self.next_to_the_win(final_list,i,'X')
        

        return final_list
    
    def efficient_position_all_frame(self):
        possible_position = []
        efficient_position = []
        possible_frame = []
        for i in self.frames:
            for j in i.winfo_children():
                if ((j.cget('text')!='X')  and (j.cget('text')!='O')):
                    j.config(state = NORMAL)


        for i in range(9):
            if((len(self.frames[i].winfo_children()) == 1) or (self.block_draw(self.frames[i]))):
                continue      
            else:
                possible_frame.append(i)
        print('* 9 * possible frame is :',possible_frame)

        for i in possible_frame:
            possible_position = self.next_to_the_win(possible_position,i,'O')

        if(len(possible_position)>0):
            # check for best one
            print('* 9 * the final possible position and blockwin is :',possible_position)
            return possible_position

        else:
            for i in possible_frame:
                for j in possible_frame:
                    if(self.btn_dict[i][j]['state'] == 'normal'):
                        possible_position.append([i,j])

            if(len(possible_position)==0):
                for i in possible_frame:
                    for j in range(9):
                        if (self.btn_dict[i][j]['state'] == 'normal'):   
                            possible_position.append([i,j])
                print('* 9 * final possible position but risky' , possible_position)
                return possible_position
            else:
                print('* 9 * non risky final position',possible_position)
                return possible_position


game_start = tic_tac_toe()