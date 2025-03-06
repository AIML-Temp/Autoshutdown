import customtkinter as ct
from CTkSpinbox import *
import datetime
import os
import threading
from win10toast import ToastNotifier

ct.set_appearance_mode("system")
ct.set_default_color_theme("red.json")
themeSelected = "Red"
mode = "shutdown"
toaster = ToastNotifier()

main_window = ct.CTk()
main_window.resizable(False,False)

timer = None
notification_timer = None
remaining_time_label = None
countdown_timer = None


def window_clear():
    win_inf = main_window.winfo_children()
    for i in range(0, len(win_inf)):
        win_inf[i].destroy()
    return


def send_notification():
    """Send a Windows notification when 1 minute remains."""
    toaster.show_toast(
        "AutoShutdown Notification",
        "Only 1 minute left before the PC will execute the action!",
        icon_path=None,
        duration=5,
        threaded=True
    )


def execute(mode):
    """Perform the selected action (shutdown, restart, etc.)."""
    global timer, notification_timer
    if timer:
        timer.cancel()
    if notification_timer:
        notification_timer.cancel()

    mode = mode.lower()
    if mode == "shutdown":
        os.system("shutdown /s /t 0")
    elif mode == "restart":
        os.system("shutdown /r /t 0")
    elif mode == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif mode == "signout":
        os.system("shutdown -l")
    else:
        print(f"Invalid mode: {mode}. No action will be performed.")


def update_countdown(seconds_left):
    """Update the countdown timer label."""
    global countdown_timer, remaining_time_label

    if seconds_left <= 0:
        return

    hours, remainder = divmod(seconds_left, 3600)
    minutes, seconds = divmod(remainder, 60)

    remaining_time_label.configure(
        text=f"{hours:02}:{minutes:02}:{seconds:02}"
    )

    countdown_timer = threading.Timer(1, update_countdown, args=(seconds_left - 1,))
    countdown_timer.start()


def stop():
    """Stop the timers and reset the application."""
    global timer, notification_timer, countdown_timer

    if timer:
        timer.cancel()
        timer = None
    if notification_timer:
        notification_timer.cancel()
        notification_timer = None
    if countdown_timer:
        countdown_timer.cancel()
        countdown_timer = None

    window_clear()
    main()


def main_logic():
    """Set up timers for execution and notification."""
    global hour_spinbox, minute_spinbox, second_spinbox, timer, notification_timer, countdown_timer, remaining_time_label, mode

    main_window.geometry("380x140")

    hour, minute, second = hour_spinbox.get(), minute_spinbox.get(), second_spinbox.get()

    window_clear()
    main_window.title(f"EzShut: {mode}")

    TitleLabel = ct.CTkLabel(
        master=main_window,
        text=f"Time remaining:",
        font=("Century Gothic", 20, "bold")
    )
    TitleLabel.pack(side="top")

    remaining_time_label = ct.CTkLabel(
        master=main_window,
        text=" Calculating...",
        font=("Century Gothic", 25, "bold"),
    )
    remaining_time_label.pack(pady=5)

    TitleLabel = ct.CTkLabel(
        master=main_window,
        text=f"Mode: {mode}",
        font=("Century Gothic", 20, "bold")
    )
    TitleLabel.pack(side="top")

    stopButton = ct.CTkButton(
        master=main_window,
        width=200,
        text="STOP",
        font=("Century Gothic", 18, "bold"),
        command=stop
    )
    stopButton.pack(side="bottom", pady=2)

    time_now = datetime.datetime.now()

    hour_now, min_now, sec_now = time_now.hour, time_now.minute, time_now.second

    time_execute_seconds = (hour * 3600) + (minute * 60) + second
    time_now_seconds = (hour_now * 3600) + (min_now * 60) + sec_now
    seconds_delay = int(time_execute_seconds - time_now_seconds)
    seconds_notification = max(seconds_delay - 60, 0)

    notification_timer = threading.Timer(seconds_notification, send_notification)
    notification_timer.start()

    timer = threading.Timer(seconds_delay, execute, args=(mode,))
    timer.start()

    update_countdown(seconds_delay)



def changetheme(theme_selected):
    """Change the theme of the application."""
    global themeSelected
    themeSelected = theme_selected
    theme_selected = f"{theme_selected.lower()}.json"
    ct.set_default_color_theme(theme_selected)
    main()


def setmode(mode_get):
    """Set the mode of action (shutdown, restart, etc.)."""
    global mode
    mode = mode_get


def main():
    """Initialize the main application window."""
    global hour_spinbox, minute_spinbox, second_spinbox, themeSelected, mode

    main_window.geometry("380x300")
    main_window.title("EzShut")

    theme_list = ["Carrot", "Coffee", "Marsh", "Metal", "Pink", "Red", "Sky", "Violet", "Yellow"]
    TitleLabel = ct.CTkLabel(
        master=main_window,
        text="EzShut",
        font=("Century Gothic", 34, "bold", "underline")
    )
    TitleLabel.place(x=20, y=10)

    themeLabel = ct.CTkLabel(master=main_window, text="Theme:", font=("Century Gothic", 18, "bold"))
    themeLabel.place(x=222, y=60)
    themeCombobox = ct.CTkComboBox(
        master=main_window,
        values=theme_list, state="readonly", command=changetheme
    )
    themeCombobox.place(x=222, y=90)
    themeCombobox.set(themeSelected)

    modeLabel = ct.CTkLabel(master=main_window, text="Mode:", font=("Century Gothic", 18, "bold"))
    modeLabel.place(x=20, y=60)
    combobox = ct.CTkComboBox(
        master=main_window,
        values=["Shutdown", "Restart", "Sleep", "Signout"], state="readonly", command=setmode
    )
    combobox.place(x=17, y=90)
    combobox.set("Shutdown")

    time_now = datetime.datetime.now()

    hour_now, min_now, sec_now = time_now.hour, time_now.minute, time_now.second

    spin_var = ct.IntVar()

    hourLabel = ct.CTkLabel(master=main_window, text="Hours", font=("Century Gothic", 18, "bold"))
    hourLabel.place(x=20, y=145)
    hour_spinbox = CTkSpinbox(
        main_window,
        start_value=hour_now,
        min_value=0,
        max_value=24,
        scroll_value=2,
        variable=spin_var,
    )
    hour_spinbox.place(x=20, y=170)

    minuteLabel = ct.CTkLabel(master=main_window, text="Minutes", font=("Century Gothic", 18, "bold"))
    minuteLabel.place(x=140, y=145)
    minute_spinbox = CTkSpinbox(
        main_window,
        start_value=min_now,
        min_value=0,
        max_value=60,
        scroll_value=2,
        variable=spin_var,
    )
    minute_spinbox.place(x=140, y=170)

    secondLabel = ct.CTkLabel(master=main_window, text="Seconds", font=("Century Gothic", 18, "bold"))
    secondLabel.place(x=260, y=145)
    second_spinbox = CTkSpinbox(
        main_window,
        start_value=sec_now,
        min_value=0,
        max_value=60,
        scroll_value=2,
        variable=spin_var,
    )
    second_spinbox.place(x=260, y=170)

    startButton = ct.CTkButton(
        master=main_window,
        width=200,
        text="START",
        font=("Century Gothic", 25, "bold"),
        command=main_logic
    )
    startButton.place(x=90, y=255)

    main_window.mainloop()

main()
