from customtkinter import *
import pyperclip
import json
import threading
import time
import keyboard

set_appearance_mode("dark")
set_default_color_theme("dark-blue")

clip = []
shown = set()

def load_clipboard():
    global clip

    try:
        with open("clipboard.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        clip = data.get("clipboard", [])

    except:
        clip = []

    current = pyperclip.paste()

    if current and current not in clip:
        clip.insert(0, current)
        save_clipboard()


def save_clipboard():
    try:
        with open("clipboard.json", "w", encoding="utf-8") as f:
            json.dump(
                {"clipboard": clip},
                f,
                ensure_ascii=False,
                indent=4
            )

    except Exception as e:
        print(e)

root = CTk()

root.geometry("420x520+700+250")
root.overrideredirect(True)
root.configure(fg_color="#111111")

root.withdraw()

root.attributes("-topmost", True)

opened = False


def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + event.x - root.x
    y = root.winfo_y() + event.y - root.y
    root.geometry(f"+{x}+{y}")

main = CTkFrame(
    root,
    corner_radius=18,
    fg_color="#1A1A1A",
    border_width=1,
    border_color="#2B2B2B"
)

main.pack(fill="both", expand=True, padx=4, pady=4)


topbar = CTkFrame(
    main,
    fg_color="transparent",
    height=45
)

topbar.pack(fill="x", padx=10, pady=(10, 5))

topbar.bind("<Button-1>", start_move)
topbar.bind("<B1-Motion>", do_move)

title = CTkLabel(
    topbar,
    text="Clipboard",
    font=("Segoe UI", 20, "bold")
)

title.pack(side="left", padx=5)

title.bind("<Button-1>", start_move)
title.bind("<B1-Motion>", do_move)


def hide_window():
    global opened

    root.withdraw()
    opened = False

close_btn = CTkButton(
    topbar,
    text="✕",
    width=32,
    height=32,
    corner_radius=10,
    fg_color="#222222",
    hover_color="#CC3333",
    command=hide_window
)

close_btn.pack(side="right", padx=2)


def clear_all():

    clip.clear()
    shown.clear()

    save_clipboard()

    for widget in scroll.winfo_children():
        widget.destroy()

clear_btn = CTkButton(
    topbar,
    text="Clear",
    width=70,
    height=32,
    corner_radius=10,
    fg_color="#333333",
    hover_color="#444444",
    command=clear_all
)

clear_btn.pack(side="right", padx=5)


scroll = CTkScrollableFrame(
    main,
    fg_color="transparent"
)

scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))


def add_clip_item(text):

    item = CTkFrame(
        scroll,
        fg_color="#222222",
        corner_radius=14
    )

    item.pack(fill="x", pady=5)

    label = CTkLabel(
        item,
        text=text[:150],
        justify="left",
        anchor="w",
        wraplength=240
    )

    label.pack(
        side="left",
        padx=12,
        pady=12,
        fill="x",
        expand=True
    )


    def copy():
        pyperclip.copy(text)

    copy_btn = CTkButton(
        item,
        text="Copy",
        width=60,
        height=30,
        corner_radius=10,
        command=copy
    )

    copy_btn.pack(side="right", padx=5)


    def delete():

        if text in clip:
            clip.remove(text)

        if text in shown:
            shown.remove(text)

        save_clipboard()

        item.destroy()

    delete_btn = CTkButton(
        item,
        text="✕",
        width=30,
        height=30,
        corner_radius=10,
        fg_color="#992222",
        hover_color="#CC3333",
        command=delete
    )

    delete_btn.pack(side="right", padx=(10, 0))


def refresh_ui():

    for item in clip:

        if item not in shown:
            shown.add(item)
            add_clip_item(item)

    root.after(500, refresh_ui)


def clipboard_listener():

    while True:

        try:
            current = pyperclip.paste()

            if current and current not in clip:

                clip.insert(0, current)

                save_clipboard()

        except:
            pass

        time.sleep(0.2)


def toggle_window():

    global opened

    if opened:

        root.withdraw()
        opened = False

    else:

        root.deiconify()

        root.lift()

        root.focus_force()

        opened = True


def unfocus(event):

    global opened

    root.withdraw()
    opened = False

root.bind("<FocusOut>", unfocus)


keyboard.add_hotkey(
    "ctrl+shift+v",
    toggle_window
)


load_clipboard()

for item in clip:
    shown.add(item)
    add_clip_item(item)

threading.Thread(
    target=clipboard_listener,
    daemon=True
).start()

refresh_ui()

root.mainloop()