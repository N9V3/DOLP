import tkinter as tk
import time
import threading
import pygame
import random

class TimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Timer App")
        self.geometry("400x300")

        self.btn_90_min = tk.Button(self, text="Iniciar Timer de 90 Minutos", command=self.start_90_min_timer)
        self.btn_90_min.pack(pady=5)

        self.btn_30_min = tk.Button(self, text="Iniciar Timer de 30 Minutos", command=self.start_30_min_timer)
        self.btn_30_min.pack(pady=5)

        self.remaining_time_90_var = tk.StringVar()
        self.remaining_time_30_var = tk.StringVar()

        self.remaining_time_90_label = tk.Label(self, textvariable=self.remaining_time_90_var)
        self.remaining_time_90_label.pack()

        self.remaining_time_30_label = tk.Label(self, textvariable=self.remaining_time_30_var)
        self.remaining_time_30_label.pack()

        self.pause_button = tk.Button(self, text="Pausar", command=self.pause_timer, state="disabled")
        self.pause_button.pack(pady=5)

        self.timer_90_min = None
        self.timer_30_min = None
        self.paused = False

        # Inicializando o mixer do pygame
        pygame.mixer.init()
        pygame.mixer.music.load('shessOriginal.mp3')

    # Função para o timer de 90 minutos
    def start_90_min_timer(self):
        if self.timer_30_min is None or not self.timer_30_min.is_alive():
            self.btn_90_min.config(state="disabled")
            self.btn_30_min.config(state="disabled")
            self.pause_button.config(state="normal")
            self.remaining_time_90_var.set("01:30:00")
            self.timer_90_min = threading.Thread(target=self.update_timer, args=(90 * 60, self.remaining_time_90_var))
            self.timer_90_min.start()

    # Função para o timer de 30 minutos
    def start_30_min_timer(self):
        if self.timer_90_min is None or not self.timer_90_min.is_alive():
            self.btn_90_min.config(state="disabled")
            self.btn_30_min.config(state="disabled")
            self.pause_button.config(state="normal")
            self.remaining_time_30_var.set("00:30:00")
            self.timer_30_min = threading.Thread(target=self.update_timer, args=(30 * 60, self.remaining_time_30_var))
            self.timer_30_min.start()

    # Função para pausar o cronômetro
    def pause_timer(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Continuar")
        else:
            self.pause_button.config(text="Pausar")

    # Função para reproduzir o som de intervalo
    def play_interval_sound(self):
        pygame.mixer.music.load('sheeshOriginal.mp3')
        pygame.mixer.music.play()

    # Função para atualizar o cronômetro
    def update_timer(self, total_seconds, var):
        elapsed_time = 0
        ta_time = random.randint(600, 4500)  # Tempo aleatório para a TA entre 10 e 75 minutos
        ta_occurred = False

        while elapsed_time < total_seconds:
            if not self.paused:
                minutes, seconds = divmod(total_seconds - elapsed_time, 60)
                hours, minutes = divmod(minutes, 60)
                timer_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
                var.set(timer_str)
                time.sleep(1)
                elapsed_time += 1

                # Verifica se é o momento da TA e se ela ainda não ocorreu
                if not ta_occurred and elapsed_time >= ta_time:
                    ta_occurred = True
                    pygame.mixer.music.load('sheeshOriginal.mp3')
                    pygame.mixer.music.play()
                    time.sleep(10)  # Pausa de 10 segundos

        var.set("00:00:00")

        if var is self.remaining_time_90_var:
            self.btn_90_min.config(state="normal")
            self.btn_30_min.config(state="normal")
            self.start_30_min_timer()  # Inicia o timer de 30 minutos (TS) após o TP

        threading.Thread(target=self.play_interval_sound).start()  # Toca o som no final dos 90 minutos

if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()
