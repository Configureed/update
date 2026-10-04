import os
import sys
import time
import subprocess
import importlib
from termcolor import colored
import requests
import json
import webbrowser
import ctypes
from ctypes import *
from ctypes.wintypes import *
import math
import onnxruntime as ort
from ultralytics import YOLO
import threading
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from bettercam import create
import dearpygui.dearpygui as dpg
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import *
import win32api, win32con, win32gui
import cv2
import uuid
import gc
from keyboard import is_pressed
import signal
import random
import string
import psutil
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import binascii
import platform
import win32security
import wmi
import socket
import hashlib
from uuid import uuid4
import base64
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as crypto_padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256 as CryptoSHA256
from cryptography.hazmat.backends import default_backend
import winreg
import pygetwindow
import ctypes

p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)

os.system('cls' if os.name == 'nt' else 'clear')


# COOL PRINT THINGY

print(colored('''
https://discord.gg/SkVcaaEB5y NewReality

 ▄████▄   ██▓    ▄▄▄       ██▀███   ██▓▄▄▄█████▓▓██   ██▓
▒██▀ ▀█  ▓██▒   ▒████▄    ▓██ ▒ ██▒▓██▒▓  ██▒ ▓▒ ▒██  ██▒
▒▓█    ▄ ▒██░   ▒██  ▀█▄  ▓██ ░▄█ ▒▒██▒▒ ▓██░ ▒░  ▒██ ██░
▒▓▓▄ ▄██▒▒██░   ░██▄▄▄▄██ ▒██▀▀█▄  ░██░░ ▓██▓ ░   ░ ▐██▓░
▒ ▓███▀ ░░██████▒▓█   ▓██▒░██▓ ▒██▒░██░  ▒██▒ ░   ░ ██▒▓░
░ ░▒ ▒  ░░ ▒░▓  ░▒▒   ▓▒█░░ ▒▓ ░▒▓░░▓    ▒ ░░      ██▒▒▒ 
  ░  ▒   ░ ░ ▒  ░ ▒   ▒▒ ░  ░▒ ░ ▒░ ▒ ░    ░     ▓██ ░▒░ 
░          ░ ░    ░   ▒     ░░   ░  ▒ ░  ░       ▒ ▒ ░░  
░ ░          ░  ░     ░  ░   ░      ░            ░ ░     
░                                                ░ ░     
upd by: ccodix
              ''', "magenta"))

time.sleep(1)

# BETTERCAM STUFF

MONITOR_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
MONITOR_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

MAX_FOV = 200

FRAME_SIZE = MAX_FOV * 2

FRAME_WIDTH = int(FRAME_SIZE//2)
FRAME_HEIGHT = int(FRAME_SIZE//2)

region = (
    int(MONITOR_WIDTH/2 - FRAME_WIDTH),
    int(MONITOR_HEIGHT/2 - FRAME_HEIGHT),
    int(MONITOR_WIDTH/2 - FRAME_WIDTH) + int(FRAME_SIZE),
    int(MONITOR_HEIGHT/2 - FRAME_HEIGHT) + int(FRAME_SIZE)
    )

x,y,width,height = region
screenshotcentre = [int((width-x)/2),int((height-y)/2)]
camera = create(region=region, output_color="BGR")

def generaterandomstring(length=random.randint(10, 30)):
    characters = string.ascii_letters + string.digits + string.punctuation
    randomstring = ''.join(random.choice(characters) for _ in range(length))
    return randomstring

keymapping = {
    "RightMouse": 0x02,
    "LeftMouse": 0x01,
    "MiddleMouse": 0x04,
    "X1Mouse": 0x05,
    "X2Mouse": 0x06,
    "Tab": 0x09,
    "Shift": 0x10,
    "Control": 0x11,
    "Alt": 0x12,
    "CapsLock": 0x14,
    **{chr(i): i for i in range(0x41, 0x5B)},
    **{chr(i): i for i in range(0x30, 0x3A)},
}

def getkeycode(combobox_name):
    value = dpg.get_value(combobox_name)
    return keymapping.get(value)

hwnd2 = None
loaded = False
model = None
modelselected = None
previousads = None
gamepad = None

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def mousemove(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(
        dx=int(x),
        dy=int(y),
        mouseData=0,
        dwFlags=MOUSEEVENTF_MOVE,
        time=0,
        dwExtraInfo=ctypes.pointer(extra)
    )
    command = Input(type=INPUT_MOUSE, ii=ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def mouseclick():
    extra = ctypes.c_ulong(0)
    # Mouse down
    ii_down = Input_I()
    ii_down.mi = MouseInput(
        dx=0, dy=0, mouseData=0,
        dwFlags=MOUSEEVENTF_LEFTDOWN, time=0, dwExtraInfo=ctypes.pointer(extra)
    )
    command_down = Input(type=INPUT_MOUSE, ii=ii_down)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command_down), ctypes.sizeof(command_down))
    # Mouse up
    ii_up = Input_I()
    ii_up.mi = MouseInput(
        dx=0, dy=0, mouseData=0,
        dwFlags=MOUSEEVENTF_LEFTUP, time=0, dwExtraInfo=ctypes.pointer(extra)
    )
    command_up = Input(type=INPUT_MOUSE, ii=ii_up)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command_up), ctypes.sizeof(command_up))


def ads():
    return win32api.GetKeyState(0x02) in (-127, -128)

dpg.create_context()

def using_gamepad():
    global gamepad
    try:
        return gamepad is not None and dpg.get_value("mouseinputradiobutton") == "GamePadEmu"
    except Exception:
        return gamepad is not None

def mousemove(x, y):
    global gamepad
    if using_gamepad():
        try:
            max_dist = 60.0
            rx = max(-1.0, min(1.0, x / max_dist))
            ry = max(-1.0, min(1.0, y / max_dist))
            gamepad.right_joystick_float(x_value_float=rx, y_value_float=ry)
            gamepad.update()
        except Exception:
            pass
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(dx=int(round(x)), dy=int(round(y)), mouseData=0, dwFlags=MOUSEEVENTF_MOVE, time=0, dwExtraInfo=ctypes.pointer(extra))
    command = Input(type=INPUT_MOUSE, ii=ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))

def mouseclick():
    extra = ctypes.c_ulong(0)
    ii_down = Input_I()
    ii_down.mi = MouseInput(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTDOWN, time=0, dwExtraInfo=ctypes.pointer(extra))
    command_down = Input(type=INPUT_MOUSE, ii=ii_down)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command_down), ctypes.sizeof(command_down))

    ii_up = Input_I()
    ii_up.mi = MouseInput(dx=0, dy=0, mouseData=0, dwFlags=MOUSEEVENTF_LEFTUP, time=0, dwExtraInfo=ctypes.pointer(extra))
    command_up = Input(type=INPUT_MOUSE, ii=ii_up)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command_up), ctypes.sizeof(command_up))

class MenuTheme:
    with dpg.theme() as globaltheme:
        with dpg.theme_component(0):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 5)

            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (107, 38, 130, 255))

            dpg.add_theme_color(dpg.mvThemeCol_Border, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15, 255))

            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (112, 112, 112, 255))

            dpg.add_theme_color(dpg.mvThemeCol_Button, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (147, 78, 170, 255))

            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (107, 38, 130, 255))

            dpg.add_theme_color(dpg.mvThemeCol_Header, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (147, 78, 170, 255))

            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (147, 78, 170, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (28, 28, 28, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (28, 28, 28, 255))

            dpg.add_theme_color(dpg.mvThemeCol_Tab, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (147, 78, 170, 255))

            dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, (107, 38, 130, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, (147, 78, 170, 255))

            dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, (147, 78, 170, 255))

            dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (67, 0, 90, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (67, 0, 90, 255))

            dpg.add_theme_color(dpg.mvPlotCol_Crosshairs, (107, 38, 130, 255))

title_bar_drag = False
           
class Gui():
    def __init__(self):
        super().__init__()
        self.menutoggled = False
        global titlebardrag
        titlebardrag = False
        self.titlegen = generaterandomstring()
        self._last_streamproof = None

    def closeall(self):
        os._exit(1)

    def initwindow(self):
        dpg.create_context()
        global viewport
        viewport = dpg.create_viewport(title=self.titlegen, decorated=False, resizable=True, width=550, height=550, clear_color=[0.0, 0.0, 0.0, 0.0], x_pos=(int(MONITOR_WIDTH/2)-275), y_pos=(int(MONITOR_HEIGHT/2)-275))
        dpg.set_viewport_always_top(True)
        #dpg.add_viewport_drawlist(front=False, tag="Viewport_back")
        dpg.setup_dearpygui()
        dpg.bind_theme(MenuTheme().globaltheme)
        with dpg.window(label=f"Clarity Lifetime [v2.7 makcu]", tag="MenuWindow", show=False, width=550, height=550, pos=(0,0), no_collapse=True, no_move=True, no_resize=True, on_close=self.closeall) as self.guiwindow:     
            self.fpslabel = dpg.add_text("Starting Main Loop...", tag="fpslabel")
            with dpg.tab_bar() as self.tabbar:
                # COMBAT TAB
                with dpg.tab(label="Combat", tag="combattab") as self.combattab:
                    # AIMBOT SECTION
                    with dpg.tree_node(label="Aimbot", tag="aimbotsection") as self.aimbotsection:
                        self.aimbotcheckbox = dpg.add_checkbox(label="Use Aimbot", default_value=False, callback=self.toggleaimbot, tag="aimbotcheckbox")
                        self.regularstrengthslider = dpg.add_slider_int(label="Regular Strength", default_value=1, min_value=1, max_value=300, callback=self.changeregularstrength, tag="regularstrengthslider")
                        self.adsstrengthslider = dpg.add_slider_int(label="ADS Strength", default_value=1, min_value=1, max_value=300, callback=self.changeadsstrength, tag="adsstrengthslider")
                        self.aimsmoothingslider = dpg.add_slider_int(label="Aim Smoothing", default_value=20, min_value=1, max_value=100, callback=self.changeaimsmoothing, tag="aimsmoothingslider")
                        self.regularfovslider = dpg.add_slider_int(label="Regular FOV", default_value=50, min_value=50, max_value=MAX_FOV, callback=self.changeregularfov, tag="regularfovslider")
                        self.adsfovslider = dpg.add_slider_int(label="ADS FOV", default_value=50, min_value=50, max_value=MAX_FOV, callback=self.changeadsfov, tag="adsfovslider")
                        dpg.add_text("Aim Bone")
                        self.aimboneradiobutton = dpg.add_radio_button(label="Aim Bone", items=["Head", "Neck", "Torso", "Custom"], default_value="Head", horizontal=True, callback=self.changeaimbone, tag="aimboneradiobutton")
                        self.customoffsetslider = dpg.add_slider_int(label="Custom Offset", default_value=1, min_value=1, max_value=20, callback=self.changecustomoffset, tag="customoffsetslider")
                        dpg.add_text("Aimbot Hotkey")
                        self.aimbothotkeycombobox = dpg.add_combo(items=["RightMouse","LeftMouse","MiddleMouse","X1Mouse","X2Mouse","Tab","Shift","Control","Alt","CapsLock","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"], default_value="RightMouse", callback=self.changeaimbothotkey, tag="aimbothotkeycombobox")
                        self.neuralnetworkviewcheckbox = dpg.add_checkbox(label="Neural Network View", default_value=False, callback=self.toggleneuralnetworkview, tag="neuralnetworkviewcheckbox")
                    # TRIGGERBOT SECTION
                    with dpg.tree_node(label="Triggerbot", tag="triggerbotsection") as self.triggerbotsection:
                        self.triggerbotcheckbox = dpg.add_checkbox(label="Use Triggerbot", default_value=False, callback=self.toggletriggerbot, tag="triggerbotcheckbox")
                        dpg.add_text("Mode")
                        self.triggerbotmoderadiobutton = dpg.add_radio_button(items=["Full Auto", "Shotgun / Semi"], default_value="Full Auto", horizontal=True, callback=self.changetriggerbotmode, tag="triggerbotmoderadiobutton")
                        dpg.add_text("Triggerbot Hotkey")
                        self.triggerbothotkeycombobox = dpg.add_combo(items=["RightMouse","LeftMouse","MiddleMouse","X1Mouse","X2Mouse","Tab","Shift","Control","Alt","CapsLock","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"], default_value="RightMouse", callback=self.changetriggerbothotkey, tag="triggerbothotkeycombobox")
                    # ANTI RECOIL SECTION
                    with dpg.tree_node(label="Anti Recoil", tag="antirecoilsection") as self.antirecoilsection:
                        self.antirecoilcheckbox = dpg.add_checkbox(label="Use Anti Recoil", default_value=False, callback=self.toggleantirecoil, tag="antirecoilcheckbox")
                        self.antirecoilstrengthslider = dpg.add_slider_int(label="Anti Recoil Strength", default_value=1, min_value=1, max_value=15, callback=self.changeantirecoilstrength, tag="antirecoilstrengthslider")
                        dpg.add_text("Anti Recoil Hotkey")
                        self.antirecoilhotkeycombobox = dpg.add_combo(items=["RightMouse","LeftMouse","MiddleMouse","X1Mouse","X2Mouse","Tab","Shift","Control","Alt","CapsLock","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"], default_value="RightMouse", callback=self.changeantirecoilhotkey, tag="antirecoilhotkeycombobox")
                # VISUALS TAB
                with dpg.tab(label="Visuals", tag="visualstab") as self.visualstab:
                    # FOV CIRCLE SECTION
                    with dpg.tree_node(label="FOV Circle", tag="fovcirclesection") as self.fovcirclesection:  
                        self.drawfovcirclecheckbox = dpg.add_checkbox(label="Draw FOV Circle", default_value=False, callback=self.toggledrawfovcircle, tag="drawfovcirclecheckbox")
                        self.drawcircleoutlinescheckbox = dpg.add_checkbox(label="Draw Outlines", default_value=False, callback=self.toggleoutlines, tag="drawcircleoutlinescheckbox")
                        dpg.add_text("FOV Circle Color")
                        self.fovcirclecolorpicker = dpg.add_color_picker(no_alpha=True, no_inputs=True, no_side_preview=True, no_small_preview=True, default_value=(255, 255, 255, 255), width=100, height=100, callback=self.changefovcirclecolor, tag="fovcirclecolorpicker")
                    # CROSSHAIR SECTION
                    with dpg.tree_node(label="Crosshair", tag="crosshairsection") as self.crosshairsection:
                        self.drawcrosshaircheckbox = dpg.add_checkbox(label="Draw Crosshair", default_value=False, callback=self.toggledrawcrosshair, tag="drawcrosshaircheckbox")
                        self.crosshairsizeslider = dpg.add_slider_int(label="Crosshair Size", default_value=1, min_value=1, max_value=15, callback=self.changecrosshairsize, tag="crosshairsizeslider")
                        dpg.add_text("Crosshair Color")
                        self.crosshaircolorpicker = dpg.add_color_picker(no_alpha=True, no_inputs=True, no_side_preview=True, no_small_preview=True, default_value=(255, 255, 255, 255), width=100, height=100, callback=self.changecrosshaircolor, tag="crosshaircolorpicker")
                    # TARGET BOXES SECTION
                    with dpg.tree_node(label="Target Boxes", tag="targetboxessection") as self.targetboxessection:  
                        dpg.add_text("Note: Using this WILL reduce ai fps and detection quality.")
                        self.drawtargetboxescheckbox = dpg.add_checkbox(label="Draw Target Boxes", default_value=False, callback=self.toggledrawtargetboxes, tag="drawtargetboxescheckbox")
                        self.drawboxoutlinescheckbox = dpg.add_checkbox(label="Draw Outlines", default_value=False, callback=self.toggleoutlines, tag="drawboxoutlinescheckbox")
                        dpg.add_text("Boxes Type")
                        self.targetboxestyperadiobutton = dpg.add_radio_button(items=["Regular Box", "Corner Box"], default_value="Regular Box", horizontal=True, callback=self.changetargetboxestype, tag="targetboxestyperadiobutton")
                        dpg.add_text("Boxes Color")
                        self.targetboxescolorpicker = dpg.add_color_picker(no_alpha=True, no_inputs=True, no_side_preview=True, no_small_preview=True, default_value=(255, 255, 255, 255), width=100, height=100, callback=self.changetargetboxescolor, tag="targetboxescolorpicker")
                    # TARGET TRACERS SECTION
                    with dpg.tree_node(label="Target Tracers", tag="targettracerssection") as self.targettracerssection:  
                        dpg.add_text("Note: Using this WILL reduce ai fps and detection quality.")
                        self.drawtargettracerscheckbox = dpg.add_checkbox(label="Draw Target Tracers", default_value=False, callback=self.toggledrawtargettracers, tag="drawtargettracerscheckbox")
                        self.drawtraceroutlinescheckbox = dpg.add_checkbox(label="Draw Outlines", default_value=False, callback=self.toggleoutlines, tag="drawtraceroutlinescheckbox")
                        dpg.add_text("Tracers From")
                        self.targettracersfromradiobutton = dpg.add_radio_button(items=["Screen Centre", "Screen Bottom"], default_value="Screen Centre", horizontal=True, callback=self.changetargettracersfrom, tag="targettracersfromradiobutton")
                        dpg.add_text("Tracers To")
                        self.targettracerstoradiobutton = dpg.add_radio_button(items=["Aim Bone", "Target Bottom"], default_value="Aim Bone", horizontal=True, callback=self.changetargettracersto, tag="targettracerstoradiobutton")
                        dpg.add_text("Tracers Color")
                        self.targettracerscolorpicker = dpg.add_color_picker(no_alpha=True, no_inputs=True, no_side_preview=True, no_small_preview=True, default_value=(255, 255, 255, 255), width=100, height=100, callback=self.changetargettracerscolor, tag="targettracerscolorpicker")
                # MISC TAB
                with dpg.tab(label="Misc", tag="misctab") as self.misctab:
                    # AI SECTION
                    with dpg.tree_node(label="AI", tag="aisection") as self.aisection:
                        self.ignorefortniteplayercheckbox = dpg.add_checkbox(label="Ignore Own Player (Fortnite)", default_value=False, callback=self.toggleignorefortniteplayer, tag="ignorefortniteplayercheckbox")
                        self.fortnitebuildfiltercheckbox = dpg.add_checkbox(label="Fortnite Build Filter", default_value=False, callback=self.togglefortnitebuildfilter, tag="fortnitebuildfiltercheckbox")
                        self.aiconfidenceslider = dpg.add_slider_int(label="Confidence", default_value=1, min_value=1, max_value=50, callback=self.changeaiconfidence, tag="aiconfidenceslider")
                        self.aiiouslider = dpg.add_slider_int(label="Overlap Threshold", default_value=1, min_value=1, max_value=50, callback=self.changeaiiou, tag="aiiouslider")
                    # MOUSE INPUT SECTION
                    with dpg.tree_node(label="Mouse Input", tag="mouseinputsection") as self.mouseinputsection:
                        self.mouseinputradiobutton = dpg.add_radio_button(items=["SendInput", "GamePadEmu"], default_value="SendInput", horizontal=True, callback=self.changemouseinput, tag="mouseinputradiobutton")
                    # CONFIGS SECTION
                    with dpg.tree_node(label="Configs", tag="configssection") as self.configssection:
                        self.configscombobox = dpg.add_combo(items=self.getconfigs("extra/configs"), default_value="", callback=self.changeconfig, tag="configscombobox")
                        self.loadconfigbutton = dpg.add_button(label="Load Config", callback=self.loadconfig, tag="loadconfigbutton")
                        self.updateconfigbutton = dpg.add_button(label="Update Config", callback=self.updateconfig, tag="updateconfigbutton")
                        dpg.add_text("New Config Name")
                        self.newconfignameinputtext = dpg.add_input_text(callback=self.changenewconfigname, tag="newconfignameinputtext")
                        self.createnewconfigbutton = dpg.add_button(label="Create New Config", callback=self.createnewconfig, tag="createnewconfigbutton")
                        self.adjustcurrentconfigbutton = dpg.add_button(label="Adjust Current Config", callback=self.adjustcurrentconfig, tag="adjustcurrentconfigbutton")
                        self.configlabel = dpg.add_text(" ", tag="configlabel")
                    # EXTRA SECTION
                    with dpg.tree_node(label="Extra", tag="extrasection") as self.extrasection:
                        self.streamproofcheckbox = dpg.add_checkbox(label="Streamproof GUI", default_value=False, callback=self.togglestreamproof, tag="streamproofcheckbox")
                        self.closecommandbutton = dpg.add_button(label="Hide Command Prompt", callback=self.closecommand, tag="closecommandbutton")
                        dpg.add_text("GUI Theme Color:")
                        self.guithemecolorpicker = dpg.add_color_picker(width=100, height=100, no_alpha=True, no_inputs=True, no_side_preview=True, no_small_preview=True, default_value=(107, 38, 130, 255), callback=self.updatethemecolor, tag="guithemecolorpicker")
            
        def cal_dow(sender,data):
            global titlebardrag
            if dpg.is_mouse_button_down(0):
                x = data[0]
                y = data[1]
                if -2 <= y <=19:
                    titlebardrag = True
                else:
                    titlebardrag = False
        
        def cal(sender,data):
            global titlebardrag
            if titlebardrag:
                pos = dpg.get_viewport_pos()
                x = data[1]
                y = data[2]
                finalx = pos[0]+x
                finaly = pos[1]+y
                dpg.configure_viewport(viewport,x_pos=finalx,y_pos=finaly)
        
        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(0,callback=cal)
            dpg.add_mouse_move_handler(callback=cal_dow)
        
        with dpg.window(label="Clarity Lifetime v2.7", tag="LoaderWindow", show=True, width=550, height=550, pos=(0,0), no_collapse=True, no_move=True, no_resize=True, on_close=self.closeall) as self.loaderwindow:
            dpg.add_text("Press Insert to toggle the gui!")
            with dpg.tab_bar() as self.loadertabbar:
                with dpg.tab(label="Settings", tag="settingstab") as self.settingstab:
                    dpg.add_text("Target FPS")
                    self.targetfpsslider = dpg.add_slider_int(label=" ", default_value=144, min_value=60, max_value=144, callback=self.changetargetfps, tag="targetfpsslider")
                    dpg.add_separator()
                    dpg.add_text("Arduino Host Shield Configuration")
                    self.arduinocheckbox = dpg.add_checkbox(label="Initialise Arduino Host Shield", default_value=False, tag="arduinocheckbox")
                    dpg.add_text("COM Port")
                    self.arduinocomcombo = dpg.add_combo(items=["COM1","COM2","COM3","COM4","COM5","COM6","COM7","COM8","COM9"], default_value="COM1", tag="arduinocomcombo")
                    dpg.add_separator()
                    dpg.add_text("RP2040 (Raw HID)")
                    self.rp2040checkbox = dpg.add_checkbox(label="Initialise RP2040 (HID)", default_value=False, tag="rp2040checkbox")
                    dpg.add_text("No COM port needed - located automatically over USB HID.")
                    dpg.add_separator()
                    dpg.add_text("Makcu")
                    self.makcucheckbox = dpg.add_checkbox(label="Initialise Makcu", default_value=False, tag="makcucheckbox")
                    self.makcu2pccheckbox = dpg.add_checkbox(label="2-PC MAKCU Mode (stream game to this PC yourself)", default_value=False, tag="makcu2pccheckbox")
                    dpg.add_separator()
                    dpg.add_text("GamePadEmu")
                    self.gamepadcheckbox = dpg.add_checkbox(label="Initialise GamePadEmu", default_value=False, tag="gamepadcheckbox")
                    dpg.add_text("(fully working on all EAC titles)")
                    dpg.add_separator()
                    dpg.add_text("AI Model")
                    _models = self.getmodels()
                    self.aimodelcombo = dpg.add_combo(items=_models, default_value=_models[0] if _models else "fortnite-best", tag="aimodelcombo")
                    dpg.add_separator()
                    self.startbutton = dpg.add_button(label="Start", callback=self.start, tag="startbutton")
                    self.savesettingsbutton = dpg.add_button(label="Save Settings", callback=self.savesettings, tag="savesettingsbutton")
                    self.textthing = dpg.add_text(" ", tag="textthing")
        
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, 'extra/configs')

        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)
        
        jsonfilepath = os.path.join(folderpath, '!loadersettings.json')

        if not os.path.isfile(jsonfilepath):
            with open(jsonfilepath, 'w') as jsonfile:
                configvalues = {
                    "targetfps": dpg.get_value("targetfpsslider"),
                    "arduino": False,
                    "arduinocom": "COM1",
                    "rp2040": False,
                    "makcu": False,
                    "makcu2pc": False,
                    "gamepademu": False,
                    "model": "fortnite-best",
                }
                json.dump(configvalues, jsonfile, indent=4)

        with open(jsonfilepath, 'r') as f:
            config = json.load(f)
            dpg.set_value("targetfpsslider", config.get("targetfps", 144))
            dpg.set_value("arduinocheckbox", config.get("arduino", False))
            dpg.set_value("arduinocomcombo", config.get("arduinocom", "COM1"))
            dpg.set_value("rp2040checkbox", config.get("rp2040", False))
            dpg.set_value("makcucheckbox", config.get("makcu", False))
            dpg.set_value("makcu2pccheckbox", config.get("makcu2pc", False))
            dpg.set_value("gamepadcheckbox", config.get("gamepademu", False))
            saved_model = config.get("model", "fortnite-best")
            _all_models = self.getmodels()
            if saved_model in _all_models:
                dpg.set_value("aimodelcombo", saved_model)

        dpg.show_viewport()
        
        self.hwnd = win32gui.FindWindow(None, self.titlegen)

    def changemodel(self, sender, data):
        return data
    
    def changefp(self, sender, data):
        return data
    
    def changeformat(self, sender, data):
        return data
    
    def changepriority(self, sender, data):
        return data
    
    def changekeyinput(self, sender, data):
        return data
    
    
    def changetargetfps(self, sender, data):
        return data
    
    def togglemaxspeed(self, sender, data):
        return data
    
    def savesettings(self, sender, data):
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, 'extra/configs')

        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)
        
        jsonfilepath = os.path.join(folderpath, '!loadersettings.json')

        if os.path.isfile(jsonfilepath):
            with open(jsonfilepath, 'w') as jsonfile:
                configvalues = {
                    "targetfps": dpg.get_value("targetfpsslider"),
                    "arduino": dpg.get_value("arduinocheckbox"),
                    "arduinocom": dpg.get_value("arduinocomcombo"),
                    "rp2040": dpg.get_value("rp2040checkbox"),
                    "makcu": dpg.get_value("makcucheckbox"),
                    "makcu2pc": dpg.get_value("makcu2pccheckbox"),
                    "gamepademu": dpg.get_value("gamepadcheckbox"),
                    "model": dpg.get_value("aimodelcombo"),
                }
                json.dump(configvalues, jsonfile, indent=4)

        dpg.set_value("textthing", "Saved settings!")
    
    def start(self, sender, data):
        time.sleep(0.1)
        os.system('cls' if os.name == 'nt' else 'clear')
        dpg.set_value("textthing", "Loading...")
        global model, modelselected, modeltype, loaded, session, gamepad

        modeltype = dpg.get_value("aimodelcombo") if dpg.get_value("aimodelcombo") else "fortnite-best"
        
        available_providers = ort.get_available_providers()
        if "CUDAExecutionProvider" in available_providers:
            selectedprovider = "CUDAExecutionProvider"
        else:
            selectedprovider = "CPUExecutionProvider"
        
        modelname = f"{modeltype}.onnx"
        nas_asdlolokn3rf97absfljk = "37f730f86676988b92a2354a975b45e6d1f9ac143305b3dc384635f9f0b2c000"
        
        def _93basl04h(input_path, key):
            key = bytes.fromhex(key)
            if len(key) != 32:
                raise ValueError("Key must be 32 bytes for AES-256")

            with open(input_path, "rb") as file:
                data = file.read()

            iv = data[:16]
            encrypteddata = data[16:]

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            paddeddata = decryptor.update(encrypteddata) + decryptor.finalize()

            unpadder = crypto_padding.PKCS7(128).unpadder()
            modeldata = unpadder.update(paddeddata) + unpadder.finalize()

            return modeldata
        
        naswe_bt612v2lu = _93basl04h(f"extra/{modelname}", nas_asdlolokn3rf97absfljk)
        
        try:
            session = ort.InferenceSession(naswe_bt612v2lu, providers=[selectedprovider, "CPUExecutionProvider"])
        except Exception as e:
            print("Failure loading model")
            time.sleep(2)
            os._exit(1)
        
        loaded = True

        try:
            strong_path = os.path.join(os.getcwd(), "extra", "configs", "preset-strong.json")
            if os.path.isfile(strong_path):
                dpg.set_value("configscombobox", "preset-strong.json")
                self.loadconfig(None, None)
                print("[Config] loaded preset-strong as main config")
        except Exception as e:
            print(f"[Config] could not load preset-strong: {e}")

        want_gamepad = dpg.get_value("gamepadcheckbox") or dpg.get_value("mouseinputradiobutton") == "GamePadEmu"
        if want_gamepad:
            try:
                import vgamepad as vg
                gamepad = vg.VDS4Gamepad()
                dpg.set_value("mouseinputradiobutton", "GamePadEmu")
                print("GamePadEmu virtual controller started")
                print("[DS4] virtual DualShock 4 ready (ViGEm)")
                print("[DS4] listening on 127.0.0.1:12345")
            except Exception as e:
                print(f"GamePadEmu error: {e}")
                dpg.set_value("mouseinputradiobutton", "SendInput")

        dpg.configure_item(self.guiwindow, show=True)
        dpg.configure_item(self.loaderwindow, show=False)

        aimbotthread.start()

    def rungui(self):
        self.initwindow()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            if is_pressed("Insert"):
                self.menutoggled = not self.menutoggled
                if self.menutoggled:
                    win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, 
                                        win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | 
                                        win32con.WS_EX_LAYERED | 
                                        win32con.WS_EX_TRANSPARENT |
                                        win32con.WS_EX_TOOLWINDOW)
                    
                    ctypes.windll.user32.SetLayeredWindowAttributes(self.hwnd, 0, 0, win32con.LWA_ALPHA)
                else:
                    extended_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
                    win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, 
                                        (extended_style & ~win32con.WS_EX_TOOLWINDOW) & 
                                        ~win32con.WS_EX_TRANSPARENT)
                    
                    ctypes.windll.user32.SetLayeredWindowAttributes(self.hwnd, 0, 255, win32con.LWA_ALPHA)
                time.sleep(0.2)
            
            streamproof_now = dpg.get_value("streamproofcheckbox")
            if streamproof_now != self._last_streamproof:
                ctypes.windll.user32.SetWindowDisplayAffinity(self.hwnd, 0x00000011 if streamproof_now else 0x00000000)
                self._last_streamproof = streamproof_now

            time.sleep(0.004)

        self.closeall()

    def startwindow(self):
        guithread = threading.Thread(target=self.rungui, daemon=True)
        guithread.start()


    # AIMBOT
    def toggleaimbot(self, sender, data):
        return data

    def changeregularstrength(self, sender, data):
        return data
    
    def changeadsstrength(self, sender, data):
        return data
    
    def changeaimbone(self, sender, data):
        return data
    
    def changecustomoffset(self, sender, data):
        return data
    
    def changeregularfov(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changeadsfov(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changeaimbothotkey(self, sender, data):
        return data
    
    def toggleprediction(self, sender, data):
        return data

    def changexoffset(self, sender, data):
        return data
    
    def changeyoffset(self, sender, data):
        return data
    
    def changepredictionhotkey(self, sender, data):
        return data
    
    def changeaimsmoothing(self, sender, data):
        return data

    def toggleneuralnetworkview(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    # TRIGGERBOT
    def toggletriggerbot(self, sender, data):
        return data

    def changetriggerbotmode(self, sender, data):
        return data

    def changetriggerbothotkey(self, sender, data):
        return data
    

    # ANTI RECOIL
    def toggleantirecoil(self, sender, data):
        return data

    def changeantirecoilstrength(self, sender, data):
        return data
    
    def changeantirecoilhotkey(self, sender, data):
        return data
    

    # FOV CIRCLE
    def toggledrawfovcircle(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changefovcirclecolor(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    

    # CROSSHAIR
    def toggledrawcrosshair(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def changecrosshairsize(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changecrosshaircolor(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    

    # TARGET BOXES
    def toggledrawtargetboxes(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def toggleoutlines(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def changetargetboxestype(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changetargetboxescolor(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    

    # TARGET TRACERS
    def toggledrawtargettracers(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def changetargettracersfrom(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changetargettracersto(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    
    def changetargettracerscolor(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data
    

    # AI
    def togglecollectimages(self, sender, data):
        return data

    def toggleframesquare(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def toggleignorefortniteplayer(self, sender, data):
        return data

    def togglefortnitebuildfilter(self, sender, data):
        return data

    def changeimgsz(self, sender, data):
        return data
    
    def changeaiconfidence(self, sender, data):
        return data
    
    def changeaiiou(self, sender, data):
        return data
    

    # MOUSE INPUT
    def changemouseinput(self, sender, data):
        global gamepad
        if data == "GamePadEmu":
            if gamepad is None:
                try:
                    import vgamepad as vg
                    gamepad = vg.VDS4Gamepad()
                    print("GamePadEmu input active (right stick aim)")
                except Exception as e:
                    print(f"vgamepad error: {e}")
                    dpg.set_value("mouseinputradiobutton", "SendInput")
        else:
            gamepad = None
    

    def getmodels(self):
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, 'extra')
        if not os.path.isdir(folderpath):
            return ["fortnite-best"]
        models = [f[:-5] for f in os.listdir(folderpath) if f.endswith('.onnx')]
        return models if models else ["fortnite-best"]

    # CONFIG
    def getconfigs(self, foldername):
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, foldername)
    
        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)
            time.sleep(2)
            return []
    
        filenames = os.listdir(folderpath)
        filenames = [file for file in filenames if os.path.isfile(os.path.join(folderpath, file)) and file != '!loadersettings.json']
    
        return filenames

    def createconfig(self, foldername, filename, data):
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, foldername)

        if not os.path.isdir(folderpath):
            os.makedirs(folderpath)
            dpg.set_value("configlabel", f"Created '{foldername}' folder")

        jsonfilepath = os.path.join(folderpath, filename)

        with open(jsonfilepath, 'w') as jsonfile:
            configvalues = {
                    "aimbot": {
                        "enabled": dpg.get_value("aimbotcheckbox"),
                        "regularstrength": dpg.get_value("regularstrengthslider"),
                        "adsstrength": dpg.get_value("adsstrengthslider"),
                        "aimsmoothing": dpg.get_value("aimsmoothingslider"),
                        "aimbone": dpg.get_value("aimboneradiobutton"),
                        "customoffset": dpg.get_value("customoffsetslider"),
                        "regularfov": dpg.get_value("regularfovslider"),
                        "adsfov": dpg.get_value("adsfovslider"),
                        "hotkey": dpg.get_value("aimbothotkeycombobox"),
                        "neuralnetworkview": dpg.get_value("neuralnetworkviewcheckbox"),
                    },
                    "triggerbot": {
                        "enabled": dpg.get_value("triggerbotcheckbox"),
                        "mode": dpg.get_value("triggerbotmoderadiobutton"),
                        "hotkey": dpg.get_value("triggerbothotkeycombobox"),
                    },
                    "antirecoil": {
                        "enabled": dpg.get_value("antirecoilcheckbox"),
                        "strength": dpg.get_value("antirecoilstrengthslider"),
                        "hotkey": dpg.get_value("antirecoilhotkeycombobox"),
                    },
                    "fovcircle": {
                        "enabled": dpg.get_value("drawfovcirclecheckbox"),
                        "outlines": dpg.get_value("drawcircleoutlinescheckbox"),
                        "color": list(dpg.get_value("fovcirclecolorpicker"))
                    },
                    "crosshair": {
                        "enabled": dpg.get_value("drawcrosshaircheckbox"),
                        "size": dpg.get_value("crosshairsizeslider"),
                        "color": list(dpg.get_value("crosshaircolorpicker"))
                    },
                    "targetboxes": {
                        "enabled": dpg.get_value("drawtargetboxescheckbox"),
                        "outlines": dpg.get_value("drawboxoutlinescheckbox"),
                        "type": dpg.get_value("targetboxestyperadiobutton"),
                        "color": list(dpg.get_value("targetboxescolorpicker"))
                    },
                    "targettracers": {
                        "enabled": dpg.get_value("drawtargettracerscheckbox"),
                        "outlines": dpg.get_value("drawtraceroutlinescheckbox"),
                        "from": dpg.get_value("targettracersfromradiobutton"),
                        "to": dpg.get_value("targettracerstoradiobutton"),
                        "color": list(dpg.get_value("targettracerscolorpicker"))
                    },
                    "ai": {
                        "ignorefortniteplayer": dpg.get_value("ignorefortniteplayercheckbox"),
                        "buildfilter": dpg.get_value("fortnitebuildfiltercheckbox"),
                        "confidence": dpg.get_value("aiconfidenceslider"),
                        "iou": dpg.get_value("aiiouslider"),
                    },
                    "mouseinput": dpg.get_value("mouseinputradiobutton"),
                    "streamproof": dpg.get_value("streamproofcheckbox"),
                }
            json.dump(configvalues, jsonfile, indent=4)
        dpg.set_value("configlabel", f"'{filename}' has been created in the '{foldername}' folder")

    def changeconfig(self, sender, data):
        global configselected
        configselected = data
        config = self.getconfig("extra/configs", f"{configselected}")
        return config
    
    def getconfig(self, foldername, filename):
        currentdirectory = os.getcwd()
        folderpath = os.path.join(currentdirectory, foldername)

        if not os.path.isdir(folderpath):
            dpg.set_value("configlabel", f"The '{foldername}' folder does not exist in the current directory")
            return None

        jsonfilepath = os.path.join(folderpath, filename)

        if os.path.isfile(jsonfilepath):
            return jsonfilepath
        else:
            dpg.set_value("configlabel", f"The file '{filename}' does not exist in the '{foldername}' folder")
            return None
    
    def loadconfig(self, sender, data):
        global configselected
        configselected = dpg.get_value("configscombobox")
        configpath = self.getconfig("extra/configs", f"{configselected}")
        if configpath is not None:
            with open(configpath, 'r') as f:
                config = json.load(f)
            overlay.update()
            QApplication.processEvents()
            dpg.set_value("aimbotcheckbox", config.get("aimbot", {}).get("enabled", False))
            dpg.set_value("regularstrengthslider", config.get("aimbot", {}).get("regularstrength", 0))
            dpg.set_value("adsstrengthslider", config.get("aimbot", {}).get("adsstrength", 0))
            dpg.set_value("aimsmoothingslider", config.get("aimbot", {}).get("aimsmoothing", 20))
            dpg.set_value("aimboneradiobutton", config.get("aimbot", {}).get("aimbone", "Head"))
            dpg.set_value("customoffsetslider", config.get("aimbot", {}).get("customoffset", 1))
            dpg.set_value("regularfovslider", config.get("aimbot", {}).get("regularfov", 0))
            dpg.set_value("adsfovslider", config.get("aimbot", {}).get("adsfov", 0))
            dpg.set_value("aimbothotkeycombobox", config.get("aimbot", {}).get("hotkey", ""))
            dpg.set_value("neuralnetworkviewcheckbox", config.get("aimbot", {}).get("neuralnetworkview", False))

            dpg.set_value("triggerbotcheckbox", config.get("triggerbot", {}).get("enabled", False))
            dpg.set_value("triggerbotmoderadiobutton", config.get("triggerbot", {}).get("mode", "Full Auto"))
            dpg.set_value("triggerbothotkeycombobox", config.get("triggerbot", {}).get("hotkey", ""))

            dpg.set_value("antirecoilcheckbox", config.get("antirecoil", {}).get("enabled", False))
            dpg.set_value("antirecoilstrengthslider", config.get("antirecoil", {}).get("strength", 0))
            dpg.set_value("antirecoilhotkeycombobox", config.get("antirecoil", {}).get("hotkey", ""))

            dpg.set_value("drawfovcirclecheckbox", config.get("fovcircle", {}).get("enabled", False))
            dpg.set_value("drawcircleoutlinescheckbox", config.get("fovcircle", {}).get("outlines", False))
            dpg.set_value("fovcirclecolorpicker", tuple(config.get("fovcircle", {}).get("color", (0, 0, 0))))

            dpg.set_value("drawcrosshaircheckbox", config.get("crosshair", {}).get("enabled", False))
            dpg.set_value("crosshairsizeslider", config.get("crosshair", {}).get("size", 0))
            dpg.set_value("crosshaircolorpicker", tuple(config.get("crosshair", {}).get("color", (0, 0, 0))))

            dpg.set_value("drawtargetboxescheckbox", config.get("targetboxes", {}).get("enabled", False))
            dpg.set_value("drawboxoutlinescheckbox", config.get("targetboxes", {}).get("outlines", False))
            dpg.set_value("targetboxestyperadiobutton", config.get("targetboxes", {}).get("type", 0))
            dpg.set_value("targetboxescolorpicker", tuple(config.get("targetboxes", {}).get("color", (0, 0, 0))))

            dpg.set_value("drawtargettracerscheckbox", config.get("targettracers", {}).get("enabled", False))
            dpg.set_value("drawtraceroutlinescheckbox", config.get("targettracers", {}).get("outlines", False))
            dpg.set_value("targettracersfromradiobutton", config.get("targettracers", {}).get("from", 0))
            dpg.set_value("targettracerstoradiobutton", config.get("targettracers", {}).get("to", 0))
            dpg.set_value("targettracerscolorpicker", tuple(config.get("targettracers", {}).get("color", (0, 0, 0))))

            dpg.set_value("ignorefortniteplayercheckbox", config.get("ai", {}).get("ignorefortniteplayer", False))
            dpg.set_value("fortnitebuildfiltercheckbox", config.get("ai", {}).get("buildfilter", False))
            dpg.set_value("aiconfidenceslider", config.get("ai", {}).get("confidence", 0))
            dpg.set_value("aiiouslider", config.get("ai", {}).get("iou", 0))

            dpg.set_value("mouseinputradiobutton", config.get("mouseinput", "SendInput"))
            dpg.set_value("streamproofcheckbox", config.get("streamproof", False))

            dpg.set_value("configlabel", "Config loaded successfully.")
            return config
        else:
            dpg.set_value("configlabel", "Failed to load config.")
            return None

    def updateconfig(self, sender, data):
        global configselected
        configselected = dpg.get_value(self.configscombobox)
        configpath = self.getconfig("extra/configs", f"{configselected}")
        if configpath:
            with open(configpath, 'w') as jsonfile:
                configvalues = {
                    "aimbot": {
                        "enabled": dpg.get_value("aimbotcheckbox"),
                        "regularstrength": dpg.get_value("regularstrengthslider"),
                        "adsstrength": dpg.get_value("adsstrengthslider"),
                        "aimsmoothing": dpg.get_value("aimsmoothingslider"),
                        "aimbone": dpg.get_value("aimboneradiobutton"),
                        "customoffset": dpg.get_value("customoffsetslider"),
                        "regularfov": dpg.get_value("regularfovslider"),
                        "adsfov": dpg.get_value("adsfovslider"),
                        "hotkey": dpg.get_value("aimbothotkeycombobox"),
                        "neuralnetworkview": dpg.get_value("neuralnetworkviewcheckbox"),
                    },
                    "triggerbot": {
                        "enabled": dpg.get_value("triggerbotcheckbox"),
                        "mode": dpg.get_value("triggerbotmoderadiobutton"),
                        "hotkey": dpg.get_value("triggerbothotkeycombobox"),
                    },
                    "antirecoil": {
                        "enabled": dpg.get_value("antirecoilcheckbox"),
                        "strength": dpg.get_value("antirecoilstrengthslider"),
                        "hotkey": dpg.get_value("antirecoilhotkeycombobox"),
                    },
                    "fovcircle": {
                        "enabled": dpg.get_value("drawfovcirclecheckbox"),
                        "outlines": dpg.get_value("drawcircleoutlinescheckbox"),
                        "color": list(dpg.get_value("fovcirclecolorpicker"))
                    },
                    "crosshair": {
                        "enabled": dpg.get_value("drawcrosshaircheckbox"),
                        "size": dpg.get_value("crosshairsizeslider"),
                        "color": list(dpg.get_value("crosshaircolorpicker"))
                    },
                    "targetboxes": {
                        "enabled": dpg.get_value("drawtargetboxescheckbox"),
                        "outlines": dpg.get_value("drawboxoutlinescheckbox"),
                        "type": dpg.get_value("targetboxestyperadiobutton"),
                        "color": list(dpg.get_value("targetboxescolorpicker"))
                    },
                    "targettracers": {
                        "enabled": dpg.get_value("drawtargettracerscheckbox"),
                        "outlines": dpg.get_value("drawtraceroutlinescheckbox"),
                        "from": dpg.get_value("targettracersfromradiobutton"),
                        "to": dpg.get_value("targettracerstoradiobutton"),
                        "color": list(dpg.get_value("targettracerscolorpicker"))
                    },
                    "ai": {
                        "ignorefortniteplayer": dpg.get_value("ignorefortniteplayercheckbox"),
                        "buildfilter": dpg.get_value("fortnitebuildfiltercheckbox"),
                        "confidence": dpg.get_value("aiconfidenceslider"),
                        "iou": dpg.get_value("aiiouslider"),
                    },
                    "mouseinput": dpg.get_value("mouseinputradiobutton"),
                    "streamproof": dpg.get_value("streamproofcheckbox"),
                }
                json.dump(configvalues, jsonfile, indent=4)
            dpg.set_value("configlabel", "Config updated successfully.")
        else:
            dpg.set_value("configlabel", "Failed to update config.")

    def updateconfigscombobox(self):
        newitems = self.getconfigs("extra/configs")
        dpg.configure_item("configscombobox", items = newitems)
    
    def changenewconfigname(self, sender, data):
        return data
    
    def createnewconfig(self, sender, data):
        global configselected
        configselected = data
        configdata = {}
        config = self.createconfig("extra/configs", f"{dpg.get_value(self.newconfignameinputtext)}.json", configdata)
        self.updateconfigscombobox()
        return config
    
    def adjustcurrentconfig(self, sender, data):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        try:
            oldsens = float(input("Config's suited sens (listed above post, 4.5 for pre-sets): "))
            oldfps = float(input("Config's suited ai fps (listed above post, 144 for pre-sets): "))
            newsens = float(input("New in-game sens for adjustment (xy, sort ads out yourself): "))
            newfps = float(input("New ai fps (capped or stable): "))

            calculatedstrength1 = int(dpg.get_value("regularstrengthslider") * (oldsens / newsens) * (oldfps / newfps))
            calculatedstrength2 = int(dpg.get_value("adsstrengthslider") * (oldsens / newsens) * (oldfps / newfps))

            dpg.set_value("regularstrengthslider", calculatedstrength1)
            dpg.set_value("adsstrengthslider", calculatedstrength2)

            print(f"Updated strength (regular): {calculatedstrength1}")
            print(f"Updated strength (ads): {calculatedstrength2}")
        except ValueError:
            print("Invalid input. Please enter valid numeric values.")
    

    # EXTRA

    def closecommand(self, sender, data):
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    def togglestreamproof(self, sender, data):
        overlay.update()
        QApplication.processEvents()
        return data

    def updatethemecolor(self, sender, data):
        selectedcolor = list(dpg.get_value("guithemecolorpicker")[:3])
        primarycolor = tuple(selectedcolor)

        lightershade = tuple(min(c + 40, 255) for c in primarycolor)
        darkershade = tuple(max(c - 40, 0) for c in primarycolor)

        with dpg.theme() as globaltheme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, primarycolor)

                dpg.add_theme_color(dpg.mvThemeCol_Border, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (0, 0, 0, 0))

                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 15, 255))

                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (112, 112, 112, 255))

                dpg.add_theme_color(dpg.mvThemeCol_Button, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, lightershade)

                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, primarycolor)

                dpg.add_theme_color(dpg.mvThemeCol_Header, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, lightershade)

                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, lightershade)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (28, 28, 28, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (28, 28, 28, 255))

                dpg.add_theme_color(dpg.mvThemeCol_Tab, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocused, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, lightershade)

                dpg.add_theme_color(dpg.mvThemeCol_ResizeGrip, primarycolor)
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_ResizeGripActive, lightershade)

                dpg.add_theme_color(dpg.mvThemeCol_SeparatorHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_SeparatorActive, lightershade)

                dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, darkershade)
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, darkershade)

                dpg.add_theme_color(dpg.mvPlotCol_Crosshairs, primarycolor)

        dpg.bind_theme(globaltheme)
    
    
# AIMBOT
def mainloop():
    camera.start(target_fps=dpg.get_value("targetfpsslider"), video_mode=True)
    global fps
    framecount = 0
    starttime = time.time()
    minutetime = time.time()
    nextupdate = random.randint(60, 300)
    global accumulatedx, accumulatedy
    accumulatedx = 0.0
    accumulatedy = 0.0
    global fov, strength
    fov = 50
    strength = 1
    aimbot_was_active = False
    triggerbot_enabled = False
    triggerbot_key_was_held = False
    triggerbot_shot_fired = False
    prev_target_center = None
    prev_aim_point = None
    prev_aim_time = None

    def iswithinfov(fovcenter, fovradius, box):
        x1, y1, x2, y2 = box
        circlex, circley = fovcenter
        corners = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
        for cornerx, cornery in corners:
            if math.dist((cornerx, cornery), (circlex, circley)) <= fovradius:
                return True
        if (circlex + fovradius >= x1 and circlex - fovradius <= x2 and
            circley >= y1 and circley <= y2):
            return True
        if (circley + fovradius >= y1 and circley - fovradius <= y2 and
            circlex >= x1 and circlex <= x2):
            return True
        return False

    def calculateiou(box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        box1area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        box2area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
        union = box1area + box2area - intersection
        return intersection / union if union > 0 else 0

    def nms(detections, iouthreshold):
        keep = []
        while len(detections) > 0:
            current = detections[0]
            keep.append(current)
            if len(detections) == 1:
                break
            ious = np.array([calculateiou(current[:4], det[:4]) for det in detections[1:]])
            detections = detections[1:][ious < iouthreshold]
        return keep

    def postprocess(output, confthreshold, iouthreshold, maxdet=10):
        predictions = np.squeeze(output, axis=0)

        # YOLOv8 exports as (4+num_classes, num_anchors) e.g. (5, 2100).
        # Transpose so each row is one detection.
        if predictions.ndim == 2 and predictions.shape[0] < predictions.shape[1]:
            predictions = predictions.T

        num_features = predictions.shape[1]

        if num_features == 6:
            # Legacy format: [x1, y1, x2, y2, conf, class_id]
            filteredpredictions = predictions[predictions[:, 4] >= confthreshold]
            if len(filteredpredictions) == 0:
                return []
            filteredpredictions = filteredpredictions[np.argsort(-filteredpredictions[:, 4])]
            detectionsafternms = np.array(nms(filteredpredictions, iouthreshold))[:maxdet]
            return [[d[0], d[1], d[2], d[3], d[4], int(d[5])] for d in detectionsafternms]

        # YOLOv8 format: [cx, cy, w, h, class_scores...]
        boxes = predictions[:, :4]
        scores_all = predictions[:, 4:]
        class_ids = np.argmax(scores_all, axis=1)
        confidences = np.max(scores_all, axis=1)

        mask = confidences >= confthreshold
        boxes = boxes[mask]
        confidences = confidences[mask]
        class_ids = class_ids[mask]
        if len(boxes) == 0:
            return []

        cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        x1 = cx - w / 2
        y1 = cy - h / 2
        x2 = cx + w / 2
        y2 = cy + h / 2

        dets = np.column_stack([x1, y1, x2, y2, confidences, class_ids])
        dets = dets[np.argsort(-dets[:, 4])]
        detectionsafternms = np.array(nms(dets, iouthreshold))[:maxdet]
        return [[d[0], d[1], d[2], d[3], d[4], int(d[5])] for d in detectionsafternms]

    inputname = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    try:
        model_input_size = int(input_shape[2]) if isinstance(input_shape[2], (int, float)) else 320
    except Exception:
        model_input_size = 320
    print(f"[Model] input size: {model_input_size}x{model_input_size}")

    while True:
        global loaded
        if loaded:
            framecount += 1
            elapsedtime = time.time() - starttime
            if elapsedtime > 0.1:
                fps = framecount / elapsedtime
                dpg.set_value("fpslabel", f"FPS: {int(fps)}")
            if elapsedtime >= 1:
                framecount = 0
                starttime = time.time()
            minuteelapsedtime = time.time() - minutetime
            if minuteelapsedtime >= nextupdate:
                dpg.set_viewport_title(generaterandomstring())
                nextupdate = random.randint(60, 300)
                minutetime = time.time()

            targetdist = float('inf')
            target = -1
            screenshot = camera.get_latest_frame()
            if screenshot is None:
                continue
            resizedframe = cv2.resize(screenshot, (model_input_size, model_input_size))
            img = resizedframe.astype(np.float32) / 255.0
            img = np.transpose(img, (2, 0, 1))
            img = np.expand_dims(img, axis=0)

            inputs = {inputname: img}
            outputs = session.run(None, inputs)
            confthreshold = dpg.get_value("aiconfidenceslider") / 100
            iouthreshold = dpg.get_value("aiiouslider") / 100
            detections = postprocess(outputs[0], confthreshold, iouthreshold)

            detectionresults = []

            model_centre = model_input_size / 2
            aimbothotkey_pre = getkeycode("aimbothotkeycombobox")
            aimbothotkey_held_pre = win32api.GetKeyState(aimbothotkey_pre) in (-127, -128) if aimbothotkey_pre else False
            for det in detections:
                x1, y1, x2, y2, confidence, classid = det
                if confidence < confthreshold:
                    continue
                if dpg.get_value("fortnitebuildfiltercheckbox"):
                    bw = x2 - x1
                    bh = y2 - y1
                    if bh <= 0 or (bw / bh) > 0.9:
                        continue
                centrex = (x1 + x2) / 2
                centrey = (y1 + y2) / 2
                distance = math.hypot(centrex - model_centre, centrey - model_centre)
                # Sticky lock: while holding the aim key and a target was locked last frame,
                # prefer the detection closest to that target so we don't flicker between players.
                if aimbothotkey_held_pre and prev_target_center is not None:
                    stick = math.hypot(centrex - prev_target_center[0], centrey - prev_target_center[1])
                    if stick < (model_input_size * 0.35):
                        distance = stick * 0.5
                if dpg.get_value("ignorefortniteplayercheckbox"):
                    if ads() and x1 >= MAX_FOV / 4 and distance < targetdist:
                        targetdist = distance
                        target = det
                    elif x1 >= MAX_FOV / 2 and distance < targetdist:
                        targetdist = distance
                        target = det
                else:
                    if distance < targetdist:
                        targetdist = distance
                        target = det

            aimbothotkey = getkeycode("aimbothotkeycombobox")
            aimbothotkey_held = win32api.GetKeyState(aimbothotkey) in (-127, -128) if aimbothotkey else False
            aiming_now = False

            if target != -1:
                x1, y1, x2, y2, confidence, class_id = target
                sw = screenshot.shape[1] / model_input_size
                sh = screenshot.shape[0] / model_input_size
                x1, y1, x2, y2 = int(x1*sw), int(y1*sh), int(x2*sw), int(y2*sh)
                detectionresults.append({'bbox': [x1, y1, x2, y2], 'conf': confidence})

                global aimbonediv
                height = y2 - y1
                bone = dpg.get_value("aimboneradiobutton")
                if bone == "Head":
                    aimbonediv = 2.5
                elif bone == "Neck":
                    aimbonediv = 3
                elif bone == "Torso":
                    aimbonediv = 5
                elif bone == "Custom":
                    aimbonediv = dpg.get_value("customoffsetslider")

                prev_target_center = ((target[0] + target[2]) / 2, (target[1] + target[3]) / 2)

                target_x = (x1 + x2) / 2
                target_y = (y1 + y2) / 2 - height / aimbonediv

                now = time.time()
                raw_point = (target_x, target_y)
                if prev_aim_point is not None and prev_aim_time is not None:
                    dt = now - prev_aim_time
                    if 0 < dt < 0.08:
                        vx = (raw_point[0] - prev_aim_point[0]) / dt
                        vy = (raw_point[1] - prev_aim_point[1]) / dt
                        if abs(vx) < 4000 and abs(vy) < 4000:
                            lead = 0.045
                            target_x += vx * lead
                            target_y += vy * lead
                prev_aim_point = raw_point
                prev_aim_time = now

                xdist = target_x - screenshotcentre[0]
                ydist = target_y - screenshotcentre[1]

                if dpg.get_value("aimbotcheckbox") and aimbothotkey_held:
                    if ads():
                        fov = dpg.get_value("adsfovslider")
                        strength = dpg.get_value("adsstrengthslider")
                    else:
                        fov = dpg.get_value("regularfovslider")
                        strength = dpg.get_value("regularstrengthslider")

                    if iswithinfov(screenshotcentre, fov, (x1, y1, x2, y2)):
                        smoothing = max(1, dpg.get_value("aimsmoothingslider"))
                        gain = (strength / 100.0) * (10.0 / smoothing)
                        gain = max(0.02, min(gain, 1.0))
                        mousemove(xdist * gain, ydist * gain)
                        aiming_now = True
            else:
                prev_target_center = None
                prev_aim_point = None
                prev_aim_time = None

                if dpg.get_value("triggerbotcheckbox") and triggerbot_enabled:
                    on_crosshair = x1 <= screenshotcentre[0] <= x2 and y1 <= screenshotcentre[1] <= y2
                    if dpg.get_value("triggerbotmoderadiobutton") == "Full Auto":
                        if on_crosshair:
                            mouseclick()
                    else:
                        if on_crosshair and not triggerbot_shot_fired:
                            mouseclick()
                            triggerbot_shot_fired = True
                        elif not on_crosshair:
                            triggerbot_shot_fired = False

            if not aimbothotkey_held:
                prev_aim_point = None
                prev_aim_time = None

            if using_gamepad() and not aiming_now:
                try:
                    gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                    gamepad.update()
                except Exception:
                    pass

            triggerbothotkey = getkeycode("triggerbothotkeycombobox")
            if triggerbothotkey:
                triggerbot_key_now = win32api.GetKeyState(triggerbothotkey) in (-127, -128)
                if triggerbot_key_now and not triggerbot_key_was_held:
                    triggerbot_enabled = not triggerbot_enabled
                    triggerbot_shot_fired = False
                triggerbot_key_was_held = triggerbot_key_now

            antirecoilhotkey = getkeycode("antirecoilhotkeycombobox")
            if dpg.get_value("antirecoilcheckbox"):
                if antirecoilhotkey and win32api.GetKeyState(antirecoilhotkey) in (-127, -128):
                    mousemove(0, dpg.get_value("antirecoilstrengthslider"))

            global previousads
            currentads = ads()
            if currentads != previousads:
                previousads = currentads
                if dpg.get_value("drawfovcirclecheckbox") and dpg.get_value("regularfovslider") != dpg.get_value("adsfovslider"):
                    overlay.update()
                    QApplication.processEvents()

            overlay.detectionresults = detectionresults
            if dpg.get_value("drawtargetboxescheckbox") or dpg.get_value("drawtargettracerscheckbox"):
                overlay.update()
                QApplication.processEvents()

            if dpg.get_value("neuralnetworkviewcheckbox"):
                overlay.nn_frame = screenshot.copy()
                overlay.nn_boxes = detectionresults
                overlay.nn_targets = len(detectionresults)
                overlay.update()
                QApplication.processEvents()
            elif overlay.nn_frame is not None:
                overlay.nn_frame = None
                overlay.update()
                QApplication.processEvents()
    

class PID:
    def __init__(self, kp, ki, kd, maxintegral=float('inf'), minintegral=-float('inf')):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.maxintegral = maxintegral
        self.minintegral = minintegral
        self.preverr = 0.0
        self.integral = 0.0
        self.lasttime = time.time()

    def compute(self, err):
        now = time.time()
        dt = now - self.lasttime
        if dt <= 0:
            dt = 1e-6
        self.lasttime = now

        proportional = self.kp * err

        self.integral += err * dt
        self.integral = max(self.minintegral, min(self.integral, self.maxintegral))
        integral = self.ki * self.integral

        derivative = self.kd * (err - self.preverr) / dt
        self.preverr = err

        output = proportional + integral + derivative

        return output

    def reset(self):
        self.preverr = 0.0
        self.integral = 0.0
        self.lasttime = time.time()

class Visuals(QMainWindow):      
    def __init__(self, detectionresults):
        super().__init__()

        self.detectionresults = detectionresults
        self.nn_frame = None
        self.nn_boxes = []
        self.nn_targets = 0

        windowname = generaterandomstring()
        self.setWindowTitle(windowname)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint
                            | QtCore.Qt.WindowStaysOnTopHint
                            | QtCore.Qt.WindowDoesNotAcceptFocus
                            | QtCore.Qt.WindowTransparentForInput
                            | QtCore.Qt.Tool
                            )
        self.setGeometry(0,0,int(MONITOR_WIDTH),int(MONITOR_HEIGHT))

        self.hwnd = int(self.winId()) 

    def paintEvent(self, event):  
        Xoffsetfix = int((MONITOR_WIDTH/2) - FRAME_WIDTH)
        Yoffsetfix = int((MONITOR_HEIGHT/2) - FRAME_HEIGHT)

        halfmonitorX = int(MONITOR_WIDTH/2)
        halfmonitorY = int(MONITOR_HEIGHT/2)

        global aimbonediv
        if 'aimbonediv' not in globals() or aimbonediv is None:
            aimbonediv = 2.5

        painter = QPainter(self)
        painter.setOpacity(1)

        if dpg.get_value("drawfovcirclecheckbox"):
            fovcirclecolorchanged = tuple(map(int, dpg.get_value("fovcirclecolorpicker")[:3]))
            fovcirclecolorqcolor = QColor(*fovcirclecolorchanged)

            pen = QPen(fovcirclecolorqcolor, 1, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.Antialiasing, True)

            if dpg.get_value("drawcircleoutlinescheckbox"):
                outlinepen = QPen(QtCore.Qt.black, 1 + 2, QtCore.Qt.SolidLine)
                painter.setPen(outlinepen)

                if not ads():
                    painter.drawEllipse(
                        halfmonitorX - dpg.get_value("regularfovslider"), 
                        halfmonitorY - dpg.get_value("regularfovslider"), 
                        dpg.get_value("regularfovslider") * 2, 
                        dpg.get_value("regularfovslider") * 2
                    )
                else:
                    painter.drawEllipse(
                        halfmonitorX - dpg.get_value("adsfovslider"), 
                        halfmonitorY - dpg.get_value("adsfovslider"), 
                        dpg.get_value("adsfovslider") * 2, 
                        dpg.get_value("adsfovslider") * 2
                    )

            painter.setPen(pen)
            if not ads():
                painter.drawEllipse(
                    halfmonitorX - dpg.get_value("regularfovslider"), 
                    halfmonitorY - dpg.get_value("regularfovslider"), 
                    dpg.get_value("regularfovslider") * 2, 
                    dpg.get_value("regularfovslider") * 2
                )
            else:
                painter.drawEllipse(
                    halfmonitorX - dpg.get_value("adsfovslider"), 
                    halfmonitorY - dpg.get_value("adsfovslider"), 
                    dpg.get_value("adsfovslider") * 2, 
                    dpg.get_value("adsfovslider") * 2
                )
        
        if dpg.get_value("drawcrosshaircheckbox"):
            crosshaircolorchanged = tuple(map(int, dpg.get_value("crosshaircolorpicker")[:3]))
            crosshaircolorqcolor = QColor(*crosshaircolorchanged)
            pen = QPen(crosshaircolorqcolor, 1, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            painter.setRenderHint(QPainter.Antialiasing, False)
            painter.drawLine(int(MONITOR_WIDTH//2) - dpg.get_value("crosshairsizeslider"), int(MONITOR_HEIGHT//2), int(MONITOR_WIDTH//2) + dpg.get_value("crosshairsizeslider"), int(MONITOR_HEIGHT//2))
            painter.drawLine(int(MONITOR_WIDTH//2), int(MONITOR_HEIGHT//2) - dpg.get_value("crosshairsizeslider"), int(MONITOR_WIDTH//2), int(MONITOR_HEIGHT//2) + dpg.get_value("crosshairsizeslider"))
        
        for det in self.detectionresults:
            x1, y1, x2, y2 = det['bbox']
            
            if dpg.get_value("drawtargetboxescheckbox"):
                targetboxescolorchanged = tuple(map(int, dpg.get_value("targetboxescolorpicker")[:3]))
                targetboxescolorqcolor = QColor(*targetboxescolorchanged)

                pen = QPen(targetboxescolorqcolor, 1, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.setRenderHint(QPainter.Antialiasing, False)

                if dpg.get_value("drawboxoutlinescheckbox"):
                    outlineoffset = 0
                    outlinepen = QPen(QtCore.Qt.black, 1 + 2, QtCore.Qt.SolidLine)
                    painter.setPen(outlinepen)
                    
                    if dpg.get_value("targetboxestyperadiobutton") == "Regular Box":
                        painter.drawRect(x1 + Xoffsetfix - outlineoffset, y1 + Yoffsetfix - outlineoffset, 
                                        (x2 - x1) + 2 * outlineoffset, (y2 - y1) + 2 * outlineoffset)
                    elif dpg.get_value("targetboxestyperadiobutton") == "Corner Box":
                        boxwidth = x2 - x1
                        boxheight = y2 - y1
                        cornerlength = int(min(boxwidth, boxheight) * 0.25)

                        painter.drawLine(x1 + Xoffsetfix - outlineoffset, y1 + Yoffsetfix - outlineoffset, 
                                         x1 + Xoffsetfix + cornerlength - outlineoffset, y1 + Yoffsetfix - outlineoffset)
                        painter.drawLine(x1 + Xoffsetfix - outlineoffset, y1 + Yoffsetfix - outlineoffset, 
                                         x1 + Xoffsetfix - outlineoffset, y1 + Yoffsetfix + cornerlength - outlineoffset)

                        painter.drawLine(x2 + Xoffsetfix + outlineoffset, y1 + Yoffsetfix - outlineoffset, 
                                         x2 + Xoffsetfix - cornerlength + outlineoffset, y1 + Yoffsetfix - outlineoffset)
                        painter.drawLine(x2 + Xoffsetfix + outlineoffset, y1 + Yoffsetfix - outlineoffset, 
                                         x2 + Xoffsetfix + outlineoffset, y1 + Yoffsetfix + cornerlength - outlineoffset)

                        painter.drawLine(x1 + Xoffsetfix - outlineoffset, y2 + Yoffsetfix + outlineoffset, 
                                         x1 + Xoffsetfix + cornerlength - outlineoffset, y2 + Yoffsetfix + outlineoffset)
                        painter.drawLine(x1 + Xoffsetfix - outlineoffset, y2 + Yoffsetfix + outlineoffset, 
                                         x1 + Xoffsetfix - outlineoffset, y2 + Yoffsetfix - cornerlength + outlineoffset)

                        painter.drawLine(x2 + Xoffsetfix + outlineoffset, y2 + Yoffsetfix + outlineoffset, 
                                         x2 + Xoffsetfix - cornerlength + outlineoffset, y2 + Yoffsetfix + outlineoffset)
                        painter.drawLine(x2 + Xoffsetfix + outlineoffset, y2 + Yoffsetfix + outlineoffset, 
                                         x2 + Xoffsetfix + outlineoffset, y2 + Yoffsetfix - cornerlength + outlineoffset)

                painter.setPen(pen)
                if dpg.get_value("targetboxestyperadiobutton") == "Regular Box":
                    painter.drawRect(x1 + Xoffsetfix, y1 + Yoffsetfix, (x2 - x1), (y2 - y1))
                elif dpg.get_value("targetboxestyperadiobutton") == "Corner Box":
                    boxwidth = x2 - x1
                    boxheight = y2 - y1
                    cornerlength = int(min(boxwidth, boxheight) * 0.25)

                    painter.drawLine(x1 + Xoffsetfix, y1 + Yoffsetfix, x1 + Xoffsetfix + cornerlength, y1 + Yoffsetfix)
                    painter.drawLine(x1 + Xoffsetfix, y1 + Yoffsetfix, x1 + Xoffsetfix, y1 + Yoffsetfix + cornerlength)

                    painter.drawLine(x2 + Xoffsetfix, y1 + Yoffsetfix, x2 + Xoffsetfix - cornerlength, y1 + Yoffsetfix)
                    painter.drawLine(x2 + Xoffsetfix, y1 + Yoffsetfix, x2 + Xoffsetfix, y1 + Yoffsetfix + cornerlength)

                    painter.drawLine(x1 + Xoffsetfix, y2 + Yoffsetfix, x1 + Xoffsetfix + cornerlength, y2 + Yoffsetfix)
                    painter.drawLine(x1 + Xoffsetfix, y2 + Yoffsetfix, x1 + Xoffsetfix, y2 + Yoffsetfix - cornerlength)

                    painter.drawLine(x2 + Xoffsetfix, y2 + Yoffsetfix, x2 + Xoffsetfix - cornerlength, y2 + Yoffsetfix)
                    painter.drawLine(x2 + Xoffsetfix, y2 + Yoffsetfix, x2 + Xoffsetfix, y2 + Yoffsetfix - cornerlength)
            
            if dpg.get_value("drawtargettracerscheckbox"):
                targettracerscolorchanged = tuple(map(int, dpg.get_value("targettracerscolorpicker")[:3]))
                targettracerscolorqcolor = QColor(*targettracerscolorchanged)

                global startpointx, startpointy, endpointx, endpointy
                
                if dpg.get_value("targettracersfromradiobutton") == "Screen Centre":
                    startpointx = halfmonitorX
                    startpointy = halfmonitorY
                elif dpg.get_value("targettracersfromradiobutton") == "Screen Bottom":
                    startpointx = halfmonitorX
                    startpointy = MONITOR_HEIGHT

                box_center_x = int((x1 + x2) / 2) + Xoffsetfix
                box_center_y = int((y1 + y2) / 2) + Yoffsetfix
                box_height = y2 - y1

                if dpg.get_value("targettracerstoradiobutton") == "Aim Bone":
                    endpointx = box_center_x
                    endpointy = int((y1 + y2) / 2 - box_height / aimbonediv) + Yoffsetfix
                elif dpg.get_value("targettracerstoradiobutton") == "Target Bottom":
                    endpointx = box_center_x
                    endpointy = y2 + Yoffsetfix

                if dpg.get_value("drawtraceroutlinescheckbox"):
                    outlinepen = QPen(QtCore.Qt.black, 1 + 2, QtCore.Qt.SolidLine)
                    painter.setPen(outlinepen)
                    painter.setRenderHint(QPainter.Antialiasing, True)

                    painter.drawLine(startpointx, startpointy, endpointx, endpointy)

                pen = QPen(targettracerscolorqcolor, 1, QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.setRenderHint(QPainter.Antialiasing, True)

                painter.drawLine(startpointx, startpointy, endpointx, endpointy)

        if dpg.get_value("neuralnetworkviewcheckbox") and self.nn_frame is not None:
            try:
                frame = self.nn_frame
                fh, fw = frame.shape[:2]
                rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                qimg = QtGui.QImage(rgb.data, fw, fh, fw * 3, QtGui.QImage.Format_RGB888)

                margin = 20
                view_w = 300
                view_h = int(fh * (view_w / fw))
                header_h = 22
                px = int(MONITOR_WIDTH) - view_w - margin
                py = margin

                painter.setRenderHint(QPainter.Antialiasing, False)

                painter.fillRect(px, py, view_w, header_h, QColor(20, 12, 28))
                painter.setPen(QColor(210, 130, 255))
                painter.drawText(px + 8, py + 15, "CLARITY AI")
                painter.setPen(QColor(255, 255, 255))
                painter.drawText(px + view_w // 2 - 28, py + 15, f"{self.nn_targets} TARGET")
                painter.drawText(px + view_w - 46, py + 15, "LOCK" if self.nn_targets > 0 else "SCAN")
                painter.setBrush(QColor(0, 230, 0) if self.nn_targets > 0 else QColor(220, 50, 50))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(px + view_w - 68, py + 7, 8, 8)
                painter.setBrush(Qt.NoBrush)

                painter.drawImage(QtCore.QRect(px, py + header_h, view_w, view_h), qimg)

                scale_x = view_w / fw
                scale_y = view_h / fh
                for d in self.nn_boxes:
                    bx1, by1, bx2, by2 = d['bbox']
                    rx1 = px + int(bx1 * scale_x)
                    ry1 = py + header_h + int(by1 * scale_y)
                    rx2 = px + int(bx2 * scale_x)
                    ry2 = py + header_h + int(by2 * scale_y)
                    painter.setPen(QPen(QColor(235, 120, 200), 1))
                    painter.drawRect(rx1, ry1, rx2 - rx1, ry2 - ry1)
                    conf = d.get('conf', 0)
                    painter.drawText(rx1, max(ry1 - 2, py + header_h + 10), f"{int(conf * 100)}%")

                adiv = aimbonediv if ('aimbonediv' in globals() and aimbonediv) else 2.5
                for d in self.nn_boxes:
                    bx1, by1, bx2, by2 = d['bbox']
                    ax = px + int(((bx1 + bx2) / 2) * scale_x)
                    ay = py + header_h + int(((by1 + by2) / 2 - (by2 - by1) / adiv) * scale_y)
                    painter.setBrush(QColor(0, 255, 255))
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(ax - 3, ay - 3, 6, 6)
                    painter.setBrush(Qt.NoBrush)

                painter.setPen(QPen(QColor(150, 60, 190), 2))
                painter.drawRect(px, py, view_w, view_h + header_h)
            except Exception:
                pass

        painter.end()


def start_app():
    global app, gui, overlay, aimbotthread
    app = QApplication(sys.argv)
    gui = Gui()
    overlay = Visuals([])
    aimbotthread = threading.Thread(target=mainloop, daemon=True)
    overlay.show()
    gui.startwindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        print("Starting Clarity.moe by ccodix...")
        start_app()
    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to exit...")
