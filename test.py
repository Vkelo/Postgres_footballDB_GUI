import tkinter as tk
import customtkinter
import psycopg2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("DATABASE GUI.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Pelaajakanta", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.show_info_event, text="INFO")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="disabled button")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))


        #SEARCHVIEW
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search player by name")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        def search_player():
            cur = conn.cursor()
            player_name = self.entry.get()
            cur.execute("SELECT * FROM players WHERE name LIKE %s", (f"%{player_name}%",))
            result = cur.fetchall()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", result)
            conn.commit()
            cur.close()

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.configure(command=search_player)



        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=400, height=450)
        self.textbox.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create searchview
        self.tabview = customtkinter.CTkTabview(self, width=200, height=400)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("DB SEARCH")
        self.tabview.tab("DB SEARCH").grid_columnconfigure(0, weight=1)  

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("DB SEARCH"), dynamic_resizing=False,
                                                        values=["Serie A", "Ligue 1", "Premier League", "Veikkausliiga", "World Cup", "Euro Cup", "LaLiga", "Bundesliga", "Champions", "Allsvenskan"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.button_12 = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), 
                                                command=self.sidebar_button_event, text="SEARCH")
        self.button_12.grid(row=2, column=0, padx=20, pady=10)

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), text="Search by keyword",
                                                           command=self.input_dialog_event)
        self.string_input_button.grid(row=3, column=0, padx=10, pady=(200, 10))

        self.button15 = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), text="Search by team",
                                                           command=self.search_team_event)
        self.button15.grid(row=4, column=0, padx=10, pady=(10, 10))


        # create addview
        self.tabview = customtkinter.CTkTabview(self, width=200, height=400)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("DB ADD")
        self.tabview.tab("DB ADD").grid_columnconfigure(0, weight=1)  

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB ADD"), text="ADD PLAYER",
                                                           command=self.open_player_dialog)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))


        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB ADD"), text="ADD TEAM",
                                                           command=self.open_team_dialog)
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))


        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB ADD"), text="ADD MATCH",
                                                           command=self.open_match_dialog)
        self.string_input_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="DO NOT PRESS THIS")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Liigat")
        self.textbox.insert("0.0", "Information about the search will be shown here\n\n")



    # DIALOGS
    def input_dialog_event(self):
        cur = conn.cursor()
        dialog = customtkinter.CTkInputDialog(text="Keyword:", title="SEARCH")
        keyword = dialog.get_input()
        if keyword is not None:
            cur.execute("""SELECT * FROM teams
                        WHERE teams.city LIKE %s
                        OR teams.country LIKE %s
                        OR teams.name LIKE %s""",
                        (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            result = cur.fetchall()
            self.textbox.delete("1.0", "end")
            for row in result:
                row_str = ' '.join(str(val) for val in row)
                self.textbox.insert("end", row_str + "\n")
        conn.commit()
        cur.close()

    def open_player_dialog(self):
        cur = conn.cursor()
        cur.execute("SELECT MAX(player_id) FROM players")
        max_id = cur.fetchone()[0]
        if max_id is None:
            max_id = 1000
        player_id = max_id + 1
        fields = ["Name", "Age", "Position"]
        dialog = CustomDialog(self, fields, title="Add a player to DB")
        self.wait_window(dialog)        
        if dialog.result is not None:
            name = dialog.result["Name"]
            age = int(dialog.result["Age (num)"])
            position = dialog.result["Position"]            
            cur.execute("INSERT INTO players (player_id, name, age, position) VALUES (%s, %s, %s, %s)", (player_id, name, age, position))
            conn.commit()
            cur.close()


    def open_team_dialog(self):
        cur = conn.cursor()
        cur.execute("SELECT MAX(team_id) FROM teams")
        max_id = cur.fetchone()[0]
        if max_id is None:
            max_id = 160
        team_id = max_id + 1
        fields = ["Name", "City", "Country", "Leagueid"]
        dialog = CustomDialog(self, fields, title="Add a team to DB")
        self.wait_window(dialog)        
        if dialog.result is not None:
            name = dialog.result["Name"]
            city = dialog.result["City"]
            country = dialog.result["Country"] 
            league_id = dialog.result["Leagueid"] 
            cur.execute("INSERT INTO teams (team_id, league_id, name, city, country) VALUES (%s, %s, %s, %s, %s)", (team_id, league_id, name, city, country))
            conn.commit()
            cur.close()

    def search_team_event(self):
        cur = conn.cursor()
        dialog = customtkinter.CTkInputDialog(text="team name:", title="SEARCH")
        cur.execute("SELECT MAX(team_id) FROM teams")

        conn.commit()
        cur.close()


    def open_match_dialog(self):
        cur = conn.cursor()
        cur.execute("SELECT MAX(match_id) FROM matches")
        max_id = cur.fetchone()[0]
        if max_id is None:
            max_id = 1000
        match_id = max_id + 1
        fields = ["Home team id", "Away team id", "League id", "Date", "Location"]
        dialog = CustomDialog(self, fields, title="Add a match to DB")
        self.wait_window(dialog)        
        if dialog.result is not None:
            home_team_id = dialog.result["Home team id"]
            away_team_id = dialog.result["Away team id"]
            league_id = dialog.result["League id"] 
            date = dialog.result["Date"] 
            location = dialog.result["Location"] 
            cur.execute("INSERT INTO matches (match_id, home_team_id, away_team_id, league_id, date, location) VALUES (%s, %s, %s, %s, %s, %s)", (match_id, home_team_id, away_team_id, league_id, date, location))
            conn.commit()
            cur.close()
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    #TODO: BUNDESLIGA & CHAMPPARI EI TOIMI
    #EVEnt which will happen when search button is pressed, depends on which option is selected
    def sidebar_button_event(self):
        self.textbox.delete("1.0", "end")
        if self.optionmenu_1.get() == "Serie A":
            cursor2 = conn.cursor()
            cursor2.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Serie A';")
            results2 = cursor2.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results2[0][0], results2[0][1], results2[0][2], results2[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results2:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info)       
        elif self.optionmenu_1.get() == "Ligue 1":
            self.textbox.delete("1.0", "end")
            cursor3 = conn.cursor()
            cursor3.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Ligue 1';")
            results3 = cursor3.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results3[0][0], results3[0][1], results3[0][2], results3[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results3:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info)   
        elif self.optionmenu_1.get() == "Premier League":
            self.textbox.delete("1.0", "end")
            cursor4 = conn.cursor()
            cursor4.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Premier League';")
            results4 = cursor4.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results4[0][0], results4[0][1], results4[0][2], results4[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results4:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info)   
        elif self.optionmenu_1.get() == "Veikkausliiga":
            self.textbox.delete("1.0", "end")
            cursor5 = conn.cursor()
            cursor5.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Veikkausliiga';")
            results5 = cursor5.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results5[0][0], results5[0][1], results5[0][2], results5[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results5:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "World Cup":
            self.textbox.delete("1.0", "end")
            cursor6 = conn.cursor()
            cursor6.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'World Cup';")
            results6 = cursor6.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results6[0][0], results6[0][1], results6[0][2], results6[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results6:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "Euro Cup":
            self.textbox.delete("1.0", "end")
            cursor7 = conn.cursor()
            cursor7.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Euro Cup';")
            results7 = cursor7.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results7[0][0], results7[0][1], results7[0][2], results7[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results7:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "LaLiga":
            self.textbox.delete("1.0", "end")
            cursor8 = conn.cursor()
            cursor8.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'LaLiga';")
            results8 = cursor8.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results8[0][0], results8[0][1], results8[0][2], results8[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results8:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "Bundesliga":
            self.textbox.delete("1.0", "end")
            cursor9 = conn.cursor()
            cursor9.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Bundesliga';")
            results9 = cursor9.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results9[0][0], results9[0][1], results9[0][2], results9[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results9:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "Champions League":
            self.textbox.delete("1.0", "end")
            cursor10 = conn.cursor()
            cursor10.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Champions League';")
            results10 = cursor10.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results10[0][0], results10[0][1], results10[0][2], results10[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results10:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        elif self.optionmenu_1.get() == "Allsvenskan":
            self.textbox.delete("1.0", "end")
            cursor11 = conn.cursor()
            cursor11.execute("SELECT league.league_id, league.name, league.teams_amount, league.trophy_name, teams.name FROM league JOIN teams ON teams.league_id = league.league_id WHERE league.name = 'Allsvenskan';")
            results11 = cursor11.fetchall()
            league_info = "League ID: {}\nLeague Name: {}\nNumber of Teams: {}\nTrophy Name: {}\n".format(results11[0][0], results11[0][1], results11[0][2], results11[0][3])
            self.textbox.insert("1.0", league_info)
            for row in results11:
                team_info = "{}\n".format(row[4])
                self.textbox.insert("end", team_info) 
        else:
            self.empty_event()

    def empty_event(self):
        cursor1 = conn.cursor()
        cursor1.execute("select * from league")
        results1 = cursor1.fetchall()
        formatted_results = ""
        for row in results1:
            formatted_results += f"ID: {row[0]}\nLeague: {row[1]}\nSeason: {row[2]}\nTrophy: {row[3]}\n\n"
        self.textbox.insert("1.0", formatted_results)

    def show_info_event(self):
        info_window = InfoWindow(self)
        info_window.geometry("400x300+100+100")
        info_window.grab_set() # Make the window modal
        info_window.wait_window() # Wait for the window to close


# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="vilikelo",
    password="password"
)



class InfoWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Info")
        self.label = tk.Label(self, text="V.1.0, Vkelo, 08.06.2023.")
        self.label.pack()
        self.text = tk.Text(self)
        self.text.insert(tk.END, "This database contains information about ten football leagues, 16 teams from each league and made up players of teams.\n\n")
        self.text.insert(tk.END, "Made with python and customkinter GUI library")
        self.text.pack()



class CustomDialog(tk.Toplevel):
    def __init__(self, parent, fields, title="Custom Dialog"):
        super().__init__(parent)
        self.title(title)
        
        self.entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(self, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="we")
            self.entries[field] = entry
            
        button_frame = tk.Frame(self)
        button_frame.grid(row=len(fields), column=1, padx=5, pady=5, sticky="e")
        
        ok_button = tk.Button(button_frame, text="OK", command=self.ok)
        ok_button.pack(side="right", padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="right", padx=5)
        
        self.result = None
        
    def ok(self):
        self.result = {}
        for field, entry in self.entries.items():
            self.result[field] = entry.get()
        self.destroy()
        
    def cancel(self):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

    #TODO: DEFAULT valinta liigahakuun, ADD match betting winnings???, Broaden keyword search and format, team selection with players
