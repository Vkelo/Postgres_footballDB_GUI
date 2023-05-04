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
                                                        values=["liiga1", "liiga2", "liiga3"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("DB SEARCH"),
                                                    values=["joukkue1", "joukku2", "joukkue3"])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.button_12 = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), command=self.sidebar_button_event, text="SEARCH")
        self.button_12.grid(row=2, column=0, padx=20, pady=10)
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB SEARCH"), text="Search by keyword",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=3, column=0, padx=20, pady=(10, 10))

        # create addview
        self.tabview = customtkinter.CTkTabview(self, width=200, height=400)
        self.tabview.grid(row=0, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("DB ADD")
        self.tabview.tab("DB ADD").grid_columnconfigure(0, weight=1)  
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("DB ADD"), text="LISÄÄ",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Älä paina tätä nappia")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Liigat")
        self.combobox_1.set("empty")
        self.textbox.insert("0.0", "Tähän tulee tietoja haetun kohteen attribuuteista\n\n")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        self.textbox.delete("1.0", "end")
        cursor1 = conn.cursor()
        cursor1.execute("select * from league")
        results = cursor1.fetchall()
        formatted_results = ""
        for row in results:
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