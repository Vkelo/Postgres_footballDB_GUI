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
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="tämä kanta")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="nappi")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="älä paina tätä")
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

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Hae nimellä")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="hae")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

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
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("DB SEARCH"),
                                                    values=["joukkue1", "joukku2", "joukkue3"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))

        self.button_12 = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), 
                                                command=self.sidebar_button_event, text="SEARCH")
        self.button_12.grid(row=2, column=0, padx=20, pady=10)

        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), text="Search by keyword",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))

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


        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB ADD"), text="ADD COMMENT",
                                                           command=self.open_match_dialog)
        self.string_input_button.grid(row=4, column=0, padx=20, pady=(10, 10))

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Älä paina tätä nappia")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Liigat")
        self.combobox_1.set("empty")
        self.textbox.insert("0.0", "Tähän tulee tietoja haetun kohteen attribuuteista\n\n")



    # DIALOGS
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Keyword:", title="SEARCH")
        print("CTkInputDialog:", dialog.get_input())

    def open_player_dialog(self):
        prompts = [("Name of the player:", "Add a player to DB"), 
               ("Age of the player:", "Add a player to DB"), 
               ("Position of the player:", "Add a player to DB")]

        inputs = []
        for prompt in prompts:
            dialog = customtkinter.CTkInputDialog(text=prompt[0], title=prompt[1])
            inputs.append(dialog.get_input())
    
        print("Inputs:", inputs)

    def open_team_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Name of the team:", title="Add a team to DB")
        print("CTkInputDialog:", dialog.get_input())

    def open_match_dialog(self):
        dialog = customtkinter.CTkInputDialog(text="Your comment:", title="Add comment on the team")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        self.textbox.delete("1.0", "end")
        if self.optionmenu_1.get() == "Serie A":
            cursor2 = conn.cursor()
            cursor2.execute("select * from league WHERE name = 'Serie A'")
            results2 = cursor2.fetchall()
            self.textbox.insert("1.0", results2)
        elif self.optionmenu_1.get() == "Ligue 1":
            cursor3 = conn.cursor()
            cursor3.execute("select * from league WHERE name = 'Ligue 1'")
            results3 = cursor3.fetchall()
            self.textbox.insert("1.0", results3)
        
        elif self.optionmenu_1.get() == "Premier League":
            cursor4 = conn.cursor()
            cursor4.execute("select * from league WHERE name = 'Premier League'")
            results4 = cursor4.fetchall()
            self.textbox.insert("1.0", results4)
        elif self.optionmenu_1.get() == "Veikkausliiga":
            cursor5 = conn.cursor()
            cursor5.execute("select * from league WHERE name = 'Veikkausliiga'")
            results5 = cursor5.fetchall()
            self.textbox.insert("1.0", results5)
        elif self.optionmenu_1.get() == "World Cup":
            cursor6 = conn.cursor()
            cursor6.execute("select * from league WHERE name = 'World Cup'")
            results6 = cursor6.fetchall()
            self.textbox.insert("1.0", results6)
        elif self.optionmenu_1.get() == "Euro Cup":
            cursor7 = conn.cursor()
            cursor7.execute("select * from league WHERE name = 'Euro Cup'")
            results7 = cursor7.fetchall()
            self.textbox.insert("1.0", results7)
        elif self.optionmenu_1.get() == "LaLiga":
            cursor8 = conn.cursor()
            cursor8.execute("select * from league WHERE name = 'LaLiga'")
            results8 = cursor8.fetchall()
            self.textbox.insert("1.0", results8)
        elif self.optionmenu_1.get() == "Bundesliga":
            cursor9 = conn.cursor()
            cursor9.execute("select * from league WHERE name = 'Bundesliga'")
            results9 = cursor9.fetchall()
            self.textbox.insert("1.0", results9)
        elif self.optionmenu_1.get() == "Champions League":
            cursor10 = conn.cursor()
            cursor10.execute("select * from league WHERE name = 'Champions League'")
            results10 = cursor10.fetchall()
            self.textbox.insert("1.0", results10)
        elif self.optionmenu_1.get() == "Allsvenskan":
            cursor11 = conn.cursor()
            cursor11.execute("select * from league WHERE name = 'Allsvenskan'")
            results11 = cursor11.fetchall()
            self.textbox.insert("1.0", results11)

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


# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="vilikelo",
    password="password"
)



if __name__ == "__main__":
    app = App()
    app.mainloop()