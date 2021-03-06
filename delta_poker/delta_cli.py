import argparse
import json
from logging import root
from numpy import tile
import requests
import time
import tkinter as tk
from cmd import Cmd
from fastapi import status
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import pydash
import tkinter.ttk as ttk
import csv
import threading
import numpy


class MyPrompt(Cmd):
    def server_up():
        global server
        def starter():
            import os
            os.system("uvicorn delta_poker:app --host=0.0.0.0")

        server = threading.Thread(target=starter, daemon=True)
        server.start()

    def stop():
        print ("Stop")
        top.destroy()

    def help_screen():
        help_window = Tk()
        
        help_window.title("Help Screen")
        label1 = Label(help_window, text = 'Have a look at these instructions! This will make you easy to understand the game and the code',bd=8, font=('Helvetica', 26, 'bold'),fg="black")
        label1.grid(column = 10, row = 0)

        label2 = Label(help_window, text = "1. add_player - This is used to register player's to the game \n 2. new_game - Used to start a new game by dealer",fg='black', font=("Helvetica", 16))
        label2.grid(column = 10, row = 10)

        label3 = Label(help_window, text = "3. add_issues - To add the issues for the current game \n 4. current_players - Used to display the list of current players any Team Member can run",fg='black', font=("Helvetica", 16))
        label3.grid(column = 10, row = 20)

        label4 = Label(help_window, text = "5. EOF - This is used to exit from the planning poker game \n 6. current_issue - This is used for displaying the current issue",fg='black', font=("Helvetica", 16))
        label4.grid(column = 10, row = 30)

        label5 = Label(help_window, text = "7. voting_system - To see the voting system to be used in the game, a user can run this command \n 8. next_issue - This is used to go to the next issue",fg='black', font=("Helvetica", 16))
        label5.grid(column = 10, row = 40)

        label6 = Label(help_window, text = "9. previous_issue - This is used to go to the previous issue \n 10. vote_issue - For voting on the current issue",fg='black', font=("Helvetica", 16))
        label6.grid(column = 10, row = 50)

        label7 = Label(help_window, text = "11. exit - This is used to exit from the planning poker game \n 12. help - Each player can run help to see which commands are available and documented.",fg='black', font=("Helvetica", 16))
        label7.grid(column = 10, row = 60)

        label8 = Label(help_window, text = "13. user_count - This is used to show the number of players in the game \n 14. show_report - Used to show For showing the final report on the current issue",fg='black', font=("Helvetica", 16))
        label8.grid(column = 10, row = 70)

        label9 = Label(help_window, text = "15. re set_votes - This is used to reset the votes of an issue \n 16. remove_player - This is used to remove player's from the game",fg='black', font=("Helvetica", 16))
        label9.grid(column = 10, row = 80)

        label10 = Label(help_window, text = "17. current_dealer - This is used to display the current dealer",fg='black', font=("Helvetica", 16))
        label10.grid(column = 10, row = 90)

        help_window.mainloop()
    
    def start_screen():
        
        start_window = Tk()
        start_window.title("Start Screen")
        start_window.geometry('700x500')
        labe1 = Label(start_window, text = 'Welcome! This is the starting page of planning poker',bd=8, font=('Helvetica', 16, 'bold'), relief="groove", fg="black")
        labe1.config(anchor="center")
        labe1.pack()
        username="janardhan"
        def do_add_player():
            player_window=Tk()
            player_window.title("Add Player to the game")
            player_window.geometry("800x300")
            
            def submitaddplayer(): 
                print("name",name_entry.get())
                players.append(name_entry.get())
                print(players)
                tk.messagebox.showinfo("Message",  "You have registered as a player "+name_entry.get())
                
                showNames()

            def showNames():

                for i in range(len(players)):
                    txt = tk.Text(player_window,height="1",width="15", bd=8, relief="groove",fg='green', font=("Helvetica", 16))
                    txt.grid(row=5,column=i)
                    txt.insert(tk.END,players[i])

            name_label = tk.Label(player_window, text = 'Player Name', fg="white", bg="orange",relief="groove", font=("Helvetica", 16))
            name_label.grid(row=0,column=0)

            name_entry = tk.Entry(player_window,font=('roman',15,'normal'))
            name_entry.grid(row=0,column=1)


            sub_btn=tk.Button(player_window,text = 'ADD',height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="green",
            bg="blue",command = submitaddplayer)
            sub_btn.grid(row=2,column=0)
            

            exit_btn1=tk.Button(player_window,text='EXIT', height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=player_window.destroy)
            exit_btn1.grid(row=2,column=1)

            player_window.mainloop()
        
        def user_data():
            user_data= Tk()
            user_data.title("Display User Data")
            user_data.geometry('800x400')

            TableMargin = Frame(user_data, width=500)
            TableMargin.pack(side=TOP)
            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
            tree = ttk.Treeview(TableMargin, columns=("id", "subject", "description"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
            scrollbary.config(command=tree.yview)
            scrollbary.pack(side=RIGHT, fill=Y)
            scrollbarx.config(command=tree.xview)
            scrollbarx.pack(side=BOTTOM, fill=X)
            tree.heading('id', text="id", anchor=W)
            tree.heading('subject', text="subject", anchor=W)
            tree.heading('description', text="description", anchor=W)
            tree.column('#0', stretch=NO, minwidth=0, width=0)
            tree.column('#1', stretch=NO, minwidth=0, width=100)
            tree.column('#2', stretch=NO, minwidth=0, width=200)
            tree.column('#3', stretch=NO, minwidth=0, width=900)
            tree.pack()
            #Change the path of the userstories.csv file from your machine
            with open('/Users/vishnupreethamreddydasari/Downloads/userstories.csv') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    firstname = row['id']
                    lastname = row['subject']
                    address = row['description']
                    tree.insert("", 0, values=(firstname, lastname, address))
            user_data.mainloop()

        def epic_data():
            epic_data = Tk()
            epic_data.title("Tasks Data")
            epic_data.geometry('800x400')

            TableMargin = Frame(epic_data, width=500)
            TableMargin.pack(side=TOP)
            scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
            scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
            tree = ttk.Treeview(TableMargin, columns=("id", "subject", "sprint"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
            scrollbary.config(command=tree.yview)
            scrollbary.pack(side=RIGHT, fill=Y)
            scrollbarx.config(command=tree.xview)
            scrollbarx.pack(side=BOTTOM, fill=X)
            tree.heading('id', text="id", anchor=W)
            tree.heading('subject', text="subject", anchor=W)
            tree.heading('sprint', text="sprint", anchor=W)
            tree.column('#0', stretch=NO, minwidth=0, width=0)
            tree.column('#1', stretch=NO, minwidth=0, width=100)
            tree.column('#2', stretch=NO, minwidth=0, width=500)
            tree.column('#3', stretch=NO, minwidth=0, width=100)
            tree.pack()
            #Change the path of the epics.csv file from your machine
            with open('/Users/vishnupreethamreddydasari/Downloads/tasks.csv') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    firstname = row['id']
                    lastname = row['subject']
                    address = row['sprint']
                    tree.insert("", 0, values=(firstname, lastname, address))
            epic_data.mainloop()
            
        def view_players():
            players_window= Tk()
            players_window.title("Current List of Players")
            players_window.geometry('600x300')
            view_players_window_label = Label(players_window, text = "List of players are:",font=('Helvetica', 24, 'bold'),fg="green")
            view_players_window_label.grid(row = 100, column = 100)
            view_players_window_label.config(anchor=CENTER)
            view_players_window_label.pack()
            
            print(players)
            a = len(players)
            et = ''
            for i in range(a):
                et = et + players[i]+'\n' 
                EOF_lbl1 = Label(players_window, text = et,font=('Helvetica', 20, 'bold'), relief="groove", fg="green")
                EOF_lbl1.config(anchor=CENTER)
                EOF_lbl1.pack()

            btn12=Button(players_window,text = 'CLOSE',font=('Helvetica', 18, 'bold'), relief="groove", fg="red",command=players_window.destroy)
            btn12.pack(fill=NONE)

            players_window.mainloop()
        
        def do_remove_player():
            players_window= Tk()
            players_window.title("Current List of Players")
            players_window.geometry('600x300')
            view_players_window_label = Label(players_window, text = "List of players are:",font=('Helvetica', 24, 'bold'),fg="green")
            view_players_window_label.grid(row = 100, column = 100)
            view_players_window_label.config(anchor=CENTER)
            view_players_window_label.pack()

            listbox = Listbox(players_window,height = 10, width = 15, selectmode=MULTIPLE)
            listbox.pack()

            def remove_item():
                selected_checkboxs = listbox.curselection()
                for selected_checkbox in selected_checkboxs:
                    value = listbox.get(selected_checkbox)
                    listbox.delete(selected_checkbox)
                    players.remove(value)
            
            def refresh():
                listbox.delete(0,END)
                for item in players:
                    listbox.insert(END, item)

            for item in players:
                listbox.insert(END, item)
            
            b = Button(players_window, text="delete",command=remove_item).pack()
            a = Button(players_window, text="refresh",command=refresh).pack()

            players_window.mainloop()

        def get_current_dealer():
 
            if len(players)!=0:
                messagebox.showinfo("Current Dealer", "The current dealer is " +players[0])

            else:

                messagebox.showinfo("Current Dealer", "Please add players ")    

        def user_count():
            z=len(players)
            user_count_players= Tk()
            user_count_players.title("Total Number of Players")
            user_count_players.geometry('600x200')
            view_players_window_label = Label(user_count_players,text = ("The number of users in the game are:",z),font=('Helvetica', 24, 'bold'), relief="groove", fg="green")
            view_players_window_label.grid(row = 100, column = 100)
            view_players_window_label.config(anchor=CENTER)
            view_players_window_label.pack()

            exit_button=tk.Button(user_count_players,text='EXIT', height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=user_count_players.destroy)
            exit_button.config(anchor=CENTER)
            exit_button.pack(fill=NONE)
            exit_button.pack()

            user_count_players.mainloop()        

        def voting_system():
            new_voting_window = Tk()
            new_voting_window.title("Start a New Game")
            new_voting_window.geometry('600x200')
            view_voting_system = Label(new_voting_window,text ="Voting System'['0','1','2','3','5','8','13','21']",font=('Helvetica', 18),fg="black")
            view_voting_system.grid(row = 100, column = 100)
            view_voting_system.config(anchor=CENTER)
            view_voting_system.pack()

            exit_button=tk.Button(new_voting_window,text='EXIT', height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=new_voting_window.destroy)
            exit_button.config(anchor=CENTER)
            exit_button.pack(fill=NONE)
            exit_button.pack()

            view_voting_system.mainloop()

        def new_game():
            players_window= Tk()
            players_window.title("Start a new game")
            players_window.geometry('600x300')
            view_players_window_label = Label(players_window,text ="HELLO! New game has been started and Voting System'['0','1','2','3','5','8','13','21','34','55','89',?,'Coffee']' add players to play",font=('Helvetica', 10),fg="green")
            view_players_window_label.grid(row = 100, column = 100)
            view_players_window_label.config(anchor=CENTER)
            view_players_window_label.pack()

            exit_button=tk.Button(players_window,text='EXIT', height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=players_window.destroy)
            exit_button.config(anchor=CENTER)
            exit_button.pack(fill=NONE)
            exit_button.pack()

            view_players_window_label.mainloop()


        def add_issue():
            addissue=Tk()
            addplayer=tk.StringVar()
            addissue.geometry('600x200')
            addissue.title("Adding Issues")
            def click():
                issue_desc=issue_entry.get()
                
                length=len(issue_list)+1
                issue_count= 'issue'+ str(length)
                new_dict={"title":issue_count,"description":issue_desc}
                issue_list.append(new_dict)
  
                print(issue_list)
   
                print(issue_list)
                tk.messagebox.showinfo("Message",  "You have added issues")
                add_player_name=addplayer.get()
                addplayer.set("")
            issue_label = Label(addissue, text = 'Issue',bg="orange", font=('roman',15, 'bold'))
            issue_entry = Entry(addissue,textvariable = addplayer, font=('roman',15,'normal'))
            sub_btn=Button(addissue,text = 'ADD',height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="green", bg="blue",command = click)
            issue_label.grid(row=0,column=0)
            issue_entry.grid(row=0,column=1)
            sub_btn.grid(row=2,column=1)
            sub_btn1=tk.Button(addissue,text='Exit', height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="red",command=quit)
            sub_btn1.grid(row=2,column=2)
            addissue.mainloop()

        def select_issue():
            selectissue=Tk()
            selectissue.geometry('600x200')
            
           
            def on_click_vote():
                addvalue=tk.StringVar()
                def on_click_submit(vote_issue):
                    print(vote_issue)
                    print(addvalue)
                    val=vote_entry.get()
                    print(val)
                    already_exist=""
                    for i in vote_list:
                        prev_vot_list=i
                        print(prev_vot_list)
                        if (username==prev_vot_list['username']) and (vote_issue==prev_vot_list['description']):
                            already_exist="true"
                    if(already_exist!="true"):
                        add_vote={"username":username,"description":vote_issue,"vote":val}
                        print(add_vote)
                        vote_list.append(add_vote)
                        inp_vote=json.dumps(vote_list)
                      
                        tk.messagebox.showinfo("Message1",  "You have added vote")
                        val.set("")
                        already_exist.set("")
                    else:
                        tk.messagebox.showinfo("Message_already_vote",  "You have already given the vote to the issue")
                issue=menu.get()
                print(issue)
                
                vote_entry=Entry(selectissue, textvariable=addvalue, font=('roman',15,'normal'))
                print(vote_entry)
                
                vote_sub_btn=Button(selectissue,text='Submit',height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="green",
                bg="blue",command = lambda:on_click_submit(issue))
                vote_sub_btn.grid(row=4,column=3)
                vote_entry.grid(row=4,column=2)
                print("After voting")
            
            
            length_list=len(issue_list)
            string_list=[]
            for list_value in issue_list:
                desc_list= list_value
                string_list.append(desc_list["description"])
            select_issue_label = tk.Label(selectissue, text = 'selectissues',bg="orange", font=('roman',15, 'bold'))
            select_issue_label.grid(row=0,column=0)
            menu=tk.StringVar()
            menu.set("select issue")
            drop=tk.OptionMenu(selectissue,menu,*string_list)
            drop.grid(row=0,column=1)
            print(drop)
            print(menu)
            vote=Button(selectissue, text='Vote',height="1",width="20", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="green", bg="blue", command=on_click_vote)
            vote.grid(row=0,column=2)
            selectissue.mainloop()

        def delete_issue_vote():
            delissue=Tk()
            delissue.geometry('600x300')
            def on_click_refresh_vote():
                global vote_list
                delete_issue=menu.get()
                print(delete_issue)
   
                vote_list = pydash.remove(vote_list, lambda result : result['description'] != delete_issue)
                
                print(vote_list)
            length_list=len(issue_list)
            string_list=[]
            for list_value in issue_list:
                desc_list= list_value
                string_list.append(desc_list["description"])

            select_issue_label = Label(delissue, text = 'selectissue',bg="orange", font=('roman',15, 'bold'))
            select_issue_label.grid(row=0,column=0)
            menu=tk.StringVar()
            menu.set("select issue")
            print(vote_list)
            drop=OptionMenu(delissue,menu,*string_list)
            delete=Button(delissue, text='Refresh the votes',height="1",width="50", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="green", bg="blue",command=on_click_refresh_vote)
            delete.grid(row=0,column=2)
            drop.grid(row=0,column=1)
            delissue.mainloop()
            
        def on_click_show_result():
            showresult=Tk()
            showresult.geometry('600x300')
            global vote_list
            def on_click_ref():
                issue=menu.get()
                print(len(vote_list))
                print(vote_list)
                result_vote=[]
                for i in vote_list:
                    print("i value %s", i)
                    if(issue==i['description']):
                        result_vote.append(i['vote'])
                if(len(result_vote)>0):      
                    print(result_vote)
                    vote_result=Label(showresult,text=result_vote, font=('roman',15, 'bold'))
                else:
                    vote_result=Label(showresult,text="None",bg="black", font=('roman',15, 'bold'))
                vote_result.grid(row=5,column=1)

            length_list=len(issue_list)
            string_list=[]
            for list_value in issue_list:
                desc_list= list_value
                string_list.append(desc_list["description"])

            select_issue_label = Label(showresult, text = 'selectissue',bg="orange", font=('roman',15, 'bold'))
            select_issue_label.grid(row=0,column=0)
            menu=tk.StringVar()
            menu.set("select issue")
            print("vote list %s",vote_list)
            drop=OptionMenu(showresult,menu,*string_list)
            delete=Button(showresult, text='Show result',height="1",width="50", bd=8, font=('arial', 12, 'bold'), relief="groove", fg="green", bg="blue",command=on_click_ref)
            delete.grid(row=0,column=2)

            drop.grid(row=0,column=1)

            showresult.mainloop()
            

        players=[]
        issue_list=[{'title': 'issue1', 'description': 'new issue1'}]
        global vote_list
        vote_list=[]
        vote_list=[{'username':'','description':'null','vote':''}] 
        
        btn3=Button(start_window,text = 'ADD PLAYER',font=('Helvetica', 20, 'bold'), relief="groove", fg="green",command=do_add_player)
        btn3.config(anchor=CENTER)
        btn3.pack(fill=NONE)
        btn3.pack()

        btn5=Button(start_window,text = 'VIEW CURRENT PLAYERS', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command = view_players)
        btn5.config(anchor=CENTER)
        btn5.pack(fill=NONE)
        btn5.pack()
        
        btn10=Button(start_window,text = 'DISPLAY CURRENT DEALER', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command = get_current_dealer)
        btn10.config(anchor=CENTER)
        btn10.pack(fill=NONE)
        btn10.pack()

        btn11=Button(start_window,text = 'DISPLAY CURRENT USER COUNT', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command = user_count)
        btn11.config(anchor=CENTER)
        btn11.pack(fill=NONE)
        btn11.pack()

        btn50=Button(start_window,text = 'DISPLAY USER DATA', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command = user_data)
        btn50.config(anchor=CENTER)
        btn50.pack(fill=NONE)
        btn50.pack()

        btn55=Button(start_window,text = 'DISPLAY TASKS DATA', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command = epic_data)
        btn55.config(anchor=CENTER)
        btn55.pack(fill=NONE)
        btn55.pack()
        
        btn12=Button(start_window,text = 'VOTING SYSTEM', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= voting_system)
        btn12.config(anchor=CENTER)
        btn12.pack(fill=NONE)
        btn12.pack()

        btn14=Button(start_window,text = 'NEW GAME', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= new_game)
        btn14.config(anchor=CENTER)
        btn14.pack(fill=NONE)
        btn14.pack()

        btn12=Button(start_window,text = 'REMOVE PLAYERS', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= do_remove_player)
        btn12.config(anchor=CENTER)
        btn12.pack(fill=NONE)
        btn12.pack()

        btn13=Button(start_window,text = 'ADD NEW ISSUE TO THE SYSTEM', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= add_issue)
        btn13.config(anchor=CENTER)
        btn13.pack(fill=NONE)
        btn13.pack()

        btn14=Button(start_window,text = 'SELECTS ISSUE FOR VOTING', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= select_issue)
        btn14.config(anchor=CENTER)
        btn14.pack(fill=NONE)
        btn14.pack()
        
        btn15=Button(start_window,text = 'REFRESH VOTES FOR THE ISSUE', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= delete_issue_vote)
        btn15.config(anchor=CENTER)
        btn15.pack(fill=NONE)
        btn15.pack()

        btn16=Button(start_window,text = 'SHOW VOTE RESULT', font=('Helvetica', 20, 'bold'), relief="groove", fg="green", command= on_click_show_result)
        btn16.config(anchor=CENTER)
        btn16.pack(fill=NONE)
        btn16.pack()

        

        start_window.mainloop()
    
    root = tk.Tk()
    root.geometry('700x400')

    label = Label(root, text = 'Planning Poker',bd=8, font=('Helvetica', 26, 'bold'), relief="groove", fg="black")
    label.config(anchor=CENTER)
    label.pack()
    
    label1 = Label(root, text = 'Click "START" button to start the game. Click on "HELP" button to know the commands.',bd=8, font=('Helvetica', 16, 'bold'), relief="groove", fg="green")
    label1.config(anchor="center")
    label1.pack()

    btn1=tk.Button(root,text='START', height="1",width="15", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="green",command=start_screen)
    btn1.pack(fill=NONE)

    btn2=tk.Button(root,text='HELP', height="1",width="15", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=help_screen)
    btn2.pack(fill=NONE)
    
    exit_button=tk.Button(root,text='EXIT', height="1",width="20", bd=8, font=('Helvetica', 15, 'bold'), relief="groove", fg="red",command=root.destroy)
    exit_button.config(anchor=CENTER)
    exit_button.pack(fill=NONE)
    exit_button.pack()

    btn30=tk.Button(root,text='Start Server', height="1",width="15", bd=8, font=('Helvetica', 14, 'bold'), relief="groove", fg="Green",command=server_up)
    btn30.pack(fill=NONE)
    btn30.place(x=350,y=350)

    btn31=tk.Button(root,text='Stop Server', height="1",width="15", bd=8, font=('Helvetica', 14, 'bold'), relief="groove", fg="Green",command=root.destroy)
    btn31.pack(fill=NONE)
    btn31.place(x=500,y=350)
    
    mainloop()

    default_config_params = {"max_retries": 5,
                             "show_timeout": 1,
                             "url": "http://localhost:8000"}
    default_keys_set = set(default_config_params.keys())

    def __init__(self, **config_params):
        super().__init__()
        self.username = None

        keys_set = set(config_params.keys())
        common_config_keys = self.default_keys_set.intersection(keys_set)
        difference_config_keys = self.default_keys_set.difference(keys_set)

        if len(difference_config_keys) == 0:
            for config_key, config_value in config_params.items():
                setattr(self, config_key, config_value)
        else:
            if len(difference_config_keys) < len(self.default_keys_set):
                print("Not all parameters found in configuration file.")
                for config_key in common_config_keys:
                    setattr(self, config_key, config_params[config_key])
            print(f"Using default value for {difference_config_keys}")
            for config_key in difference_config_keys:
                setattr(self, config_key,
                        self.default_config_params[config_key])

    def default(self, inp):
        """
        You can also use x or q to exit the game. All commands that are
        not implemented will just be printed with a notification
        message.
        """
        if inp == 'x' or inp == 'q':
            return self.do_exit()

        print(f"Haven't found this command: {inp}")

    @staticmethod
    def print_error_response(response):
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            print(f"{json.loads(response.text)['detail']}")
        elif response.status_code == status.HTTP_412_PRECONDITION_FAILED:
            print(f"{json.loads(response.text)['detail']}")
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            message = json.loads(response.text)['detail'][0]['msg']
            print(f"{message.capitalize()}")
        else:
            print(f"{response.text}")

    @staticmethod
    def print_issue(response):
        crt_issue_title = response['result_message']['title']
        crt_issue_description = response['result_message']['description']
        print(f"'{crt_issue_title}' is the current issue.")
        if len(crt_issue_description) > 0:
            print(f"{crt_issue_description}")

    @staticmethod
    def parse_report(report):
        for vote_value, vote_details in report.items():
            print(f"{vote_details['vote_count']} voted for {vote_value} "
                  f"story points.\n"
                  f"{json.dumps(vote_details['voters'], indent=4)}\n")

    def get_report(self, inp):
        current_status = 'pending'
        retry_count = 0
        while current_status == 'pending' and retry_count < self.max_retries:
            response = self.send_request(method='get',
                                         route='/issue/show_results')
            if response.status_code == status.HTTP_200_OK:
                response_message = json.loads(response.text)['result_message']
                current_status = response_message['status']
                if current_status == 'done':
                    self.parse_report(response_message['report'])
            else:
                current_status = 'error'
                self.print_error_response(response)
            retry_count += 1
            time.sleep(self.show_timeout)

    def send_request(self, method, route, params=None, data=None):
        full_uri = ''.join([self.url, route])
        response = requests.request(method=method, url=full_uri,
                                    params=params, json=data)
        return response

    def do_add_player(self, username):
        """
        Add a player to the current game
        """
        current_players = []

        response = self.send_request(method='get',
                                     route='/user/show_all')

        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            current_players = response_dict['result_message']['current_users']
        else:
            self.print_error_response(response)

        if self.username and self.username in current_players:
            print(f"You already have a username in the current game: "
                  f"{self.username}")
        else:
            crt_dict = {
                'name': username
            }
            response = self.send_request(method='post',
                                         route='/user/add',
                                         data=crt_dict)
            if response.status_code == status.HTTP_200_OK:
                self.username = username
                print(f"Player {self.username} has been added to the current "
                      f"game")
            else:
                self.print_error_response(response)

    def do_current_dealer(self, inp):
        """
        Show current dealer
        """
        response = self.send_request(method='get',
                                     route='/game/get_dealer')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"Current dealer is "
                  f"{response_dict['result_message']['current_dealer']}")
        else:
            self.print_error_response(response)

    def do_current_issue(self, inp):
        """
        Show issue that players are voting on now
        """
        response = self.send_request(method='get',
                                     route='/issue/current')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            self.print_issue(response_dict)
        else:
            self.print_error_response(response)

    def do_current_players(self, inp):
        """
        Show players that are registered for the current game
        """
        response = self.send_request(method='get',
                                     route='/user/show_all')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            current_users = response_dict['result_message']['current_users']
            if len(current_users) == 0:
                print("Please add players to the game")
            else:
                print(f"Currently playing Planning Poker: "
                      f"{json.dumps(current_users)}")
        else:
            self.print_error_response(response)

    def do_current_votes(self, inp):
        """
        Show if all players voted or who still has to vote
        """
        response = self.send_request(method='get',
                                     route='/issue/vote_status')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']}")
        else:
            self.print_error_response(response)

    def do_exit(self):
        """
        Command for exiting planning poker game
        """

        crt_dict = {
            'name': self.username
        }

        response = self.send_request(method='post',
                                     route='/user/exit',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']['user_exit_status']}")
        else:
            self.print_error_response(response)
        print(f"Buh-bye, {self.username}! And in case I don't see you again, "
              f"good afternoon, good evening and good night!")
        return True

    def do_new_game(self, inp):
        """
        Start new game
        """
        crt_dict = {
            'name': self.username
        }
        response = self.send_request(method='post',
                                     route='/game/new',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']}")
        else:
            self.print_error_response(response)

    def do_next_issue(self, inp):
        """
        Jump to next issue, if there is one (i.e. the current issue
        is the last one and we can go back to programming)
        """

        crt_dict = {
            'name': self.username
        }

        response = self.send_request(method='post',
                                     route='/issue/next',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            self.print_issue(response_dict)
        else:
            self.print_error_response(response)

    def do_previous_issue(self, inp):
        """
        Jump to previous issue, if there is one (i.e. we are not on
        the first issue)
        """

        crt_dict = {
            'name': self.username
        }

        response = self.send_request(method='post',
                                     route='/issue/previous',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            self.print_issue(response_dict)
        else:
            self.print_error_response(response)

    def do_remove_player(self, username):
        """
        Remove a player from the current game
        """

        if len(username) < 4:
            print("Please use a more meaningful name")
        else:
            params_dict = {
                'username': username
            }
            data_dict = {
                'name': self.username
            }
            response = self.send_request(method='post',
                                         route='/user/remove',
                                         params=params_dict,
                                         data=data_dict)
            if response.status_code == status.HTTP_200_OK:
                response_dict = json.loads(response.text)
                print(f"{response_dict['result_message']}")
            else:
                self.print_error_response(response)

    def do_reset_votes(self, inp):
        """
        Reset votes on current issue
        """
        crt_dict = {
            'name': self.username
        }
        response = self.send_request(method='post',
                                     route='/issue/votes_reset',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']}")
        else:
            self.print_error_response(response)

    def do_show_report(self, inp):
        """
        Show vote report for current issue
        """
        self.get_report(inp)

    def do_user_count(self, inp):
        """
        Show how many users are registered for the current game
        """
        response = self.send_request(method='get',
                                     route='/user/count')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            user_count = response_dict['result_message']['user_count']
            if user_count == 1:
                verb = 'is'
            else:
                verb = 'are'
            print(f"Currently, there {verb} {user_count} registered "
                  f"players")
        else:
            self.print_error_response(response)

    def do_vote_issue(self, vote_value):
        """
        Vote on the current issue with the registered user here
        """
        crt_dict = {
            'name': self.username,
            'vote_value': vote_value
        }
        response = self.send_request(method='put',
                                     route='/issue/vote',
                                     data=crt_dict)
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']}")
        else:
            self.print_error_response(response)

    def do_voting_system(self, inp):
        """
        Show voting system for the current game
        """
        response = self.send_request(method='get',
                                     route='/game/voting_system')
        if response.status_code == status.HTTP_200_OK:
            response_dict = json.loads(response.text)
            print(f"{response_dict['result_message']}")
        else:
            self.print_error_response(response)

    do_EOF = do_exit


if __name__ == '__main__':

    crt_config_params = {}
    config_path = Path('./configs/cli_config.json')

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str,
                        help="Configuration file name")
    args = parser.parse_args()
    if args.config:
        config_path = Path(args.config)

    if config_path.exists():
        with open(config_path) as f:
            try:
                crt_config_params = json.load(f)
            except json.decoder.JSONDecodeError as je:
                print(f"Please make sure config file contains a dict in json "
                      f"format. An example can be found in "
                      f"'./configs/cli_config.json'. {je} was raised.")
    else:
        print(f"Please make sure the path {config_path} is correct and that "
              f"the file exists. Will use default configuration parameters "
              f"this time.")

    MyPrompt(**crt_config_params).cmdloop()