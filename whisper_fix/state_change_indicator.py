import logging
import tkinter as tk


class StateChangeIndicator:
    def __init__(self, label: tk.Label):
        self.logger = logging.getLogger(__name__)
        self.label = label

    def display_state_change(self, new_state: str):
        self.logger.info(f"State changed to {new_state}.")
        self.update_label(new_state)

    def update_label(self, new_text: str):
        self.label.config(text=new_text)
        self.label.update_idletasks()