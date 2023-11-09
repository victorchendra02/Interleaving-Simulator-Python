import tkinter as tk
from tkinter import messagebox
from time import sleep
import random


def cls_termninal() -> None:
    import sys, subprocess

    operating_system = sys.platform
    if operating_system == 'win32':
        subprocess.run('cls', shell=True)
    elif operating_system == 'linux' or operating_system == 'darwin':
        subprocess.run('clear', shell=True)
    
    
def processing_text_input(text: str) -> tuple[list[str], list[str]]:
    splitted_text = text.split(" ")
    return ['  '.join(word) for word in splitted_text], ['\n'.join(column) for column in zip(*splitted_text)]


def get_widget_size(widget: tk.Label | tk.Button) -> tuple[int, int]:
    return widget.winfo_reqwidth(), widget.winfo_reqheight()


def generate_broken_message(array: list[str], indicator: list[bool], orient: str) -> tuple[list[str], list[bool]]:
    """
    array       : list of words/packets
    indicator   : [True, False, ...] 
    orient      : 'row' | 'col'
    """
    
    orient = orient.lower()
    n = len(array)
    
    
    result = [None] * n
    
    text_length = len(array[0])
    for i in range(n):
        if indicator[i]:
            if orient == 'row':
                result[i] = "#" * text_length
            elif orient == 'col':
                current_message = array[i].replace('\n', '')
                
                result[i] = "#\n" * len(current_message)
                result[i] = result[i][:-1]
            else:
                raise TypeError('orient parameter only take \'row\' or \'col\'')
        else:
            result[i] = array[i]
            
    return result, indicator


class InputMessageUI():
    def __init__(self) -> None:
        self.message: str = 0
        self.n: int = 0
        
        self.root = tk.Tk()
        self.message_label = None
        self.small_note = None
        self.message_entry = None
        
        self.n_label = None
        self.n_entry = None
        
        self.lets_go_button = None
        self.error_input_text = None
        
        # self.is_input_correct = False

        self.WIN_WIDTH = 920
        self.WIN_HEIGHT = 508
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        x = (self.screenwidth // 2) - (self.WIN_WIDTH // 2)
        y = (self.screenheight // 2) - (self.WIN_HEIGHT // 2)

        # small_icon = tk.PhotoImage(file="assets/icons8-thin-client-70.png")
        # large_icon = tk.PhotoImage(file="assets/icons8-thin-client-70.png")
        # self.root.iconphoto(False, large_icon, small_icon)
        self.root.title("Computer Network Interleaving Simulator")
        self.root.configure(bg="#93B1A6")
        self.root.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}+{x}+{y}")
 
    def validate_input(self):
        splitted_message = self.message.split(" ")
        longest_string = max(splitted_message, key=len)

        if len(self.message) == 0:
            self.error_input_text.config(text="Please provide a message", fg="blue")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False
        elif len(longest_string) > 8:
            self.error_input_text.config(text="Packets with more than 8 characters is not allowed!", fg="red")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False
        elif len(splitted_message) > 8:
            self.error_input_text.config(text="Please input no more than 8 words/packets", fg="blue")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False
        elif len(self.n) == 0:
            self.error_input_text.config(text="Please input number of broken words/packets", fg="blue")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False
        elif int(self.n) > min(len(longest_string), len(splitted_message)) :
            self.error_input_text.config(text="Number of broken packets is too big!", fg="red")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False
        elif int(self.n) < 0:
            self.error_input_text.config(text="Number of broken packets must be positive!", fg="red")
            self.error_input_text.pack(side="top", pady=(40, 0))
            return False

        splitted = self.message.split(" ")
        if len(splitted) < 8:
            splitted.extend(["_" * 8] * (8 - len(splitted)))
        
        temp = " ".join([s.ljust(8, "_") for s in splitted])
        # print(temp)
        self.message = temp

        self.n = int(self.n)
        return True
        
    def lets_go_button_event(self):
        self.message = str(self.message_entry.get()).strip()
        self.n = str(self.n_entry.get()).strip()

        is_verified = self.validate_input()
        
        if is_verified:
            # print("DONE")
            self.error_input_text.pack_forget()
            self.root.destroy()
        
    def initialize(self):
        # Message
        self.message_label = tk.Label(
            self.root,
            text="Input message",
            font=("Fira Code", 14, "bold"),
            width=25
            )
        self.message_label.pack(side='top', pady=(92,0))
        self.small_note = tk.Label(
            self.root,
            text="max. 8 words/packets",
            font=("Fira Code", 9),
            width=22
            )
        self.small_note.pack(side='top', pady=(0,0))
        self.message_entry = tk.Entry(
            self.root,
            width=74,
            justify='center',
            font=("Fira Code", 14)
            )
        self.message_entry.insert(0, "matahari membakar sebagian material berwarna kebiruan 01234567")
        self.message_entry.pack(side='top')
        

        # n
        self.n_label = tk.Label(
            self.root,
            text="Number of broken packets",
            font=("Fira Code", 14, "bold"),
            width=29
            )
        self.n_label.pack(side='top', pady=(30,0))
        self.n_entry = tk.Entry(
            self.root,
            width=25,
            justify='center',
            font=("Fira Code", 14)
            )
        self.n_entry.insert(0, 3)
        self.n_entry.pack(side='top')
        
        
        # Let's go button
        self.lets_go_button = tk.Button(
            self.root,
            text="Let's go",
            font=("Fira Code", 14, "bold"),
            width=16,
            command=self.lets_go_button_event
        )
        self.lets_go_button.pack(side='top', pady=(50,0))
        

        # error message
        self.error_input_text = tk.Label(
            self.root,
            text="",
            font=("Fira Code", 10),
            width=57
        )
        
    def run(self):
        self.initialize()
        self.root.mainloop()
        

class AppSimulator():
    def __init__(self, n: int, message: str):
        self.root = tk.Tk()
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.row_message, self.col_message = processing_text_input(message)

        self.is_running = False
        self.font_FiraCode = "Fira Code"
        
        
        # -------------------------------------------------------------
        # font_root = font.Font(family="Inter", size=60)
        
        # self.root.option_add("*Font", font_root)
        self.bg_root = "#93B1A6"
        self.xy_color_label = "#ffffff"
        self.root.configure(bg=self.bg_root)
        
        
        self.root.title("Computer Network Interleaving Simulator")
        self.root.attributes('-fullscreen', True)
        # self.root.geometry(f"{int(self.screenwidth/1.15)}x{int(self.screenheight/1.15)}")
        # self.root.state('zoomed')  # Maximize screen
        
        # Icon App
        # small_icon = tk.PhotoImage(file="assets/icons8-thin-client-70.png")
        # large_icon = tk.PhotoImage(file="assets/icons8-thin-client-70.png")
        # self.root.iconphoto(False, large_icon, small_icon)
        # -------------------------------------------------------------
        
        
        self.x = []
        self.y = []
        self.x_start, self.x_initial = 138, 138
        self.y_start, self.y_initial = 250, 250


        # Exit button
        self.exit_button = None
        
        # Header label
        self.header = None
        
        self.sender_text = None
        self.info_text, self.info_text_indicator = None, []
        self.reciever_text = None
        self.interleaving_explenation_text = None
        self.post_text = None
        
        # Normal simulation button
        self.normal_button = None
        
        # Reset button
        self.restart_button = None
        
        # Interleaving simulation button
        self.simulation_button = None
        
        # x label
        self.x_labels = []
        self.x_label_width = 0  #260
        self.x_label_height = 0  #50

        # y label
        self.y_labels = []
        self.y_label_width = 0
        self.y_label_height = 0


        # Create random broken message
        indicator = [True]*n + [False]*(abs(8-n))
        random.shuffle(indicator)

        self.broken_row_message, self.row_indicator = generate_broken_message(self.row_message, indicator, orient='row')
        self.broken_col_message, self.col_indicator = generate_broken_message(self.col_message, indicator, orient='col')
        
    
        # self.col_message = self.broken_col_message
        # self.row_message = self.broken_row_message
        
    def wait_in_the_middle(self, n:int=100):
        for _ in range(n):
            if self.is_running:
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
       
    def pop_up_info_text(self, i):
        # pop up info text
        self.info_text_indicator.append(i+1)
        self.info_text = tk.Label(self.root,
            text=f"Oops! Paket data ke {self.info_text_indicator} rusak",
            font=(self.font_FiraCode, 11),
            fg='red'
            )
        _info_text_width = get_widget_size(self.info_text)[0]
        self.info_text.place(x=self.screenwidth//2 - _info_text_width//2, y=160, width=_info_text_width + 30)
    
    
    def start_normal_simulation(self, i, label):
        # 0 - 0.5
        for j in range(1, 390, 6):
            if self.is_running:
                label.place(x=self.screenwidth//4 - (get_widget_size(label)[0]+70)//2 +j, y=self.y[i], width=self.x_label_width, height=self.x_label_height)
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
        
        # wait stop in the middle
        self.wait_in_the_middle()
            
        # broken message
        if self.row_indicator[i]:
            label.place_forget()
            label = self.create_label(self.broken_row_message[i])
            label.place(x=self.screenwidth//4 - (get_widget_size(label)[0]+70)//2 +j, y=self.y[i], width=self.x_label_width, height=self.x_label_height)

            # pop up info text
            self.pop_up_info_text(i)
            
            self.wait_in_the_middle(80)
        
        # 0.5 - 1
        for k in range(j, 800, 6):
            if self.is_running:
                label.place(x=self.screenwidth//4 - (get_widget_size(label)[0]+70)//2 +k, y=self.y[i], width=self.x_label_width, height=self.x_label_height)
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
            
        for _ in range(80):
            if self.is_running:
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
        
        return "FINISH"
        
    def button_normal_event(self) -> None:
        print("Normal simulation button Clicked")
        self.is_running = True
        
        self.normal_button.config(state=tk.DISABLED)
        self.simulation_button.config(state=tk.DISABLED)
        self.header.config(text="Normal Simulation STARTED".upper())
        self.header.config(bg="red")

        # explenation text
        text_mengirim = tk.Label(self.root,
            text="Mengirim...",
            font=(self.font_FiraCode, 11),
            fg='red'
            )
        _tm_width = get_widget_size(text_mengirim)[0]
        add_pad = 40
        text_mengirim.place(x=self.screenwidth//2 - _tm_width//2 - add_pad//2, y=self.screenheight - 150, width=_tm_width + add_pad)

        
        for i, label in enumerate(self.x_labels):
            result = self.start_normal_simulation(i, label)
            if result == "RESTART":
                break

        text_mengirim.place_forget()
        
        # pup up post text
        if result == "FINISH":
            # Post text
            self.post_text = tk.Label(self.root,
                text="Sebagai Receiver, apakah Anda bisa menebak keseluruhan pesan yang telah rusak sebagian saat dalam pengiriman?\nCoba bandingkan dengan simulasi Interleaving dan amatilah perbedaannya!",
                font=(self.font_FiraCode, 11),
                fg='blue'
                )
            _post_text_width = get_widget_size(self.post_text)[0]
            self.post_text.place(x=self.screenwidth//2 - _post_text_width//2, y=self.screenheight - 170, width=_post_text_width + 30)
        
        self.init_header()


    def start_interleaving_simulation(self, i, label):
        # 0 - 0.5
        for j in range(1, abs(752 - self.x[i]), 6):
            if self.is_running:
                label.place(x=self.x[i] + j + 32, y=self.y_initial, width=self.y_label_width, height=self.y_label_height)
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
            
        # wait stop in the middle
        self.wait_in_the_middle()
        
        # broken message
        if self.col_indicator[i]:
            label.place_forget()
            label = self.create_label(self.broken_col_message[i])
            label.place(x=self.x[i] + j + 32, y=self.y_initial, width=self.y_label_width, height=self.y_label_height)

            # pop up info text
            self.pop_up_info_text(i)
                        
            self.wait_in_the_middle(75)
            
        
        # 0.5 - 1
        for k in range(j, 1000 - 200, 6):
            if self.is_running:
                label.place(x=self.x[i] + k + 32, y=self.y_initial, width=self.y_label_width, height=self.y_label_height)
                self.root.update()
                sleep(0.002)
            else:
                return "RESTART"
        
        return "FINISH"

    def button_simulation_event(self) -> None:
        print("Interleaving simulation button Clicked")
        self.destroy_x_label()
        self.init_y_label()
        
        self.is_running = True
        
        self.normal_button.config(state=tk.DISABLED)
        self.simulation_button.config(state=tk.DISABLED)
        self.header.config(text="Interleaving Simulation STARTED".upper())
        self.header.config(bg="blue")

        # explenation text
        self.interleaving_explenation_text = tk.Label(self.root,
            text="Pada teknik Interleaving, cara pengiriman paket data berubah yaitu dari orientasi row menjadi column.\nPerhatikan perubahan data saat hendak dikirim.",
            font=(self.font_FiraCode, 11),
            fg='green'
            )
        _post_text_width = get_widget_size(self.interleaving_explenation_text)[0]
        self.interleaving_explenation_text.place(x=self.screenwidth//2 - _post_text_width//2, y=self.screenheight - 170, width=_post_text_width + 30)

        self.wait_in_the_middle(200)
            
        for i, label in enumerate(self.y_labels):
            result = self.start_interleaving_simulation(i, label)
            if result == "RESTART":
                break
            
        # pup up post text
        self.interleaving_explenation_text.place_forget()
        if result == "FINISH":
            # Post text
            self.post_text = tk.Label(self.root,
                text="Kerusakan paket saat dalam perjalanan berada diluar kendali kita.\nWalaupun demikian, pesan lebih bisa ditebak (predictable) menggunakan teknik Interleaving bukan?",
                font=(self.font_FiraCode, 11),
                fg='green'
                )
            _post_text_width = get_widget_size(self.post_text)[0]
            self.post_text.place(x=self.screenwidth//2 - _post_text_width//2, y=self.screenheight - 170, width=_post_text_width + 30)

        self.init_header()


    def _exit(self):
        print("Button Exit pressed")
        result = messagebox.askokcancel("Exit?", "Are you sure you want to exit?")
        if result:
            print(f"Exit state: {result}")
            self.root.destroy()
            print("Program terminated!")
        else:
            print(f"Exit state: {result}")
            
    def _restart(self):
        result = messagebox.askokcancel("Restart?", "Do you wish to Restart?")
        if result:
            print("Restarting...")
            self.is_running = False
            self.destroy_all_widgets()
            self.initialize()
            print("Restart complete")
            self.normal_button.config(state=tk.NORMAL)
            self.simulation_button.config(state=tk.NORMAL)
            
        else:
            print("Restart cancel")
    
    def destroy_all_widgets(self):
        self.info_text, self.info_text_indicator = None, []
        self.post_text = None
        self.interleaving_explenation_text = None
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def destroy_x_label(self):
        for xlabel in self.x_labels:
            xlabel.place_forget()
    
    def destroy_y_label(self):
        for ylabel in self.y_labels:
            ylabel.place_forget()
    
    def init_header(self):
        self.header = tk.Label(self.root,
            text="Interleaving Simulator".upper(),
            font=(self.font_FiraCode, 28, "bold"),
            # foreground="orange",
            # background="Green",
            )
        self.header.config(text="Interleaving Simulator".upper())
        self.header.config(bg="white")
        self.header.place(y=56, width=self.screenwidth)
    
    def create_label(self, text):
        label = tk.Label(self.root, text=text.upper())
        label.config(font=(self.font_FiraCode, 20, "bold"))
        return label
    
    def init_x_label(self):
        # 1. x label
        y_interval = 0
        self.y = []
        self.x_labels= []
        for x_word in self.row_message:
            label = tk.Label(self.root, text=x_word.upper())
            label.config(font=(self.font_FiraCode, 20, "bold"))

            self.x_label_width = get_widget_size(label)[0] + 70
            self.x_label_height = get_widget_size(label)[1]

            self.x_labels.append(label)
            self.y.append(self.y_initial + y_interval)
            
            y_interval += 50
            
        for i, label in enumerate(self.x_labels):
            label.place(x=self.screenwidth//4 - (get_widget_size(label)[0]+70)//2, y=self.y[i], width=self.x_label_width, height=self.x_label_height)

    def init_y_label(self):
        # 2. y label
        x_interval = 0
        self.y_labels = []
        self.x = []
        for y_word in self.col_message:
            label = tk.Label(self.root, text=y_word.upper())
            label.config(font=(self.font_FiraCode, 20, "bold"))

            self.y_label_width = get_widget_size(label)[0] + 30
            self.y_label_height = get_widget_size(label)[1] + 50
            
            self.y_labels.append(label)
            self.x.append(self.x_initial + x_interval)
            
            x_interval += 53
            
        for j, label in enumerate(self.y_labels):
            label.place(x=self.x[j] + 32, y=self.y_initial, width=self.y_label_width, height=self.y_label_height)

    def initialize(self):
        self.is_running = False
        
        # Exit button
        self.exit_button = tk.Button(self.root,
            text="❌",
            font=(self.font_FiraCode, 10, "bold"),
            command=self._exit,
            )
        self.exit_button.place(x=self.screenwidth - 50, y=0, width=50, height=42)
        
        
        # Header label
        self.init_header()
        
        
        # Sender label
        self.sender_text = tk.Label(self.root,
            text="SENDER",
            font=(self.font_FiraCode, 24, "bold"),
            background="Gray",
            width=12
            )
        _sender_text_width = get_widget_size(self.sender_text)[0]
        # print(f"_sender_text_width: {_sender_text_width} pixels")
        self.sender_text.place(x=self.screenwidth//4 - _sender_text_width//2, y=148)
        
        
        # Receiver label
        self.reciever_text = tk.Label(self.root,
            text="RECEIVER",
            font=(self.font_FiraCode, 24, "bold"),
            background="Yellow",
            width=12
            )
        _reciever_text_width = get_widget_size(self.reciever_text)[0]
        # print(f"_reciever_text_width: {_reciever_text_width} pixels")
        self.reciever_text.place(x=(self.screenwidth*3)//4 - _reciever_text_width//2, y=148)
        
        
        # Normal simulation button
        self.normal_button = tk.Button(self.root, 
            text="Start Normal Simulation", 
            command=self.button_normal_event,
            font=("Lucia Console", 12, "bold")
            )
        self.normal_button.place(x=140, y=self.screenheight - 84, width=300, height=40)
        
        
        # Reset button
        self.restart_button = tk.Button(self.root, 
            text="Reset", 
            command=self._restart,
            font=("Lucia Console", 10, "bold"),
            # width=7
            )
        self.restart_button.place(x=(self.screenwidth//2) - 33, y=self.screenheight - 84, width=66, height=40)
        
        
        # Interleaving simulation button
        self.simulation_button = tk.Button(self.root, 
            text="Start Interleaving Simulation",
            command=self.button_simulation_event,
            font=("Lucia Console", 12, "bold")
            )
        self.simulation_button.place(x=self.screenwidth - 300 - 140, y=self.screenheight - 84, width=300, height=40)
        
        
        # 1. x label
        self.init_x_label()
        
    def run(self):
        self.initialize()
        self.root.mainloop()
        

if __name__ == '__main__':
    InputUI = InputMessageUI()
    InputUI.run()
    
    message, n = InputUI.message, InputUI.n

    App = AppSimulator(n=n, message=message)
    App.run()
    