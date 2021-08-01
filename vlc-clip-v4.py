#######################################################################################
#       vlc-clip ver4                                                                 #
#                                                                         2021/08/01  #
#       Written by Maimai (Twitter:@Maimai22015,@Maimai22016/YTPMV.info)              #
#       Read https://ytpmv.info/vlc-anime-v3                                          #
#######################################################################################

import PySimpleGUI as sg
from sys import platform as PLATFORM
import socket
import threading
import datetime
import subprocess
import configparser
import os
#------- Config ------------------------#
inifile = configparser.ConfigParser()
inifile.read(os.getcwd() + '/setting.ini', 'UTF-8')
print(inifile.get('SETTING', 'save_path'))
ffmpeg_path = inifile.get('SETTING', 'ffmpeg_path')
start_pos = inifile.get('SETTING', 'start_pos')
cut_length = inifile.get('SETTING', 'cut_length')
save_path = inifile.get('SETTING', 'save_path')

'''
ffmpeg command
ffmpeg -ss <time> -t <length> -i "<input file>" -map 0 -map -0:s -map_chapters -1 -vcodec libx264  -preset medium -tune animation "<output file>" -codec:a libfdk_aac -y
'''
ffmpeg_cmd1 = " -ss "
ffmpeg_cmd2 = " -t "
ffmpeg_cmd3 = " -i \""
ffmpeg_cmd4 = "\" -map 0 -map -0:s -map_chapters -1 -vcodec libx264  -preset medium -tune animation \""
ffmpeg_cmd5 = "\" -codec:a libfdk_aac -y"

#------- Key config --------------------#
key_pause = inifile.get('KEYCONFIG', 'key_pause2')
key_pause2 = " "
key_stop = inifile.get('KEYCONFIG', 'key_stop')
key_normnal = inifile.get('KEYCONFIG', 'key_normnal')
key_faster = inifile.get('KEYCONFIG', 'key_faster')
key_slower = inifile.get('KEYCONFIG', 'key_slower')
key_load = inifile.get('KEYCONFIG', 'key_load')
key_back10s = inifile.get('KEYCONFIG', 'key_back10s')
key_skip10s = inifile.get('KEYCONFIG', 'key_skip10s')
key_screenshot = inifile.get('KEYCONFIG', 'key_screenshot')
key_cut = inifile.get('KEYCONFIG', 'key_cut')
key_run = inifile.get('KEYCONFIG', 'key_run')

#------- GUI definition & setup --------#

sg.theme('DarkBlue')

def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(8, 1), pad=(1, 1))

layout = [[ sg.Button('load'),sg.T('command:'),sg.Input(default_text='atrack 1', size=(10, 1), key='-VLC_Control_Command-'),btn('cmd run'),],
          [btn('stop'),btn('screenshot')],
          [btn('10s <-'),btn('pause'),btn('-> 10s')],
          [btn('normal'),btn('slower'),btn('faster')],
          [btn('cut'),sg.Button('Generate .bat and run', size=(17, 1), pad=(1, 1))],
          [sg.Text('Load media to start', key='-MESSAGE_AREA-')],
          [sg.Output(size=(60,10))]]

window = sg.Window('vlc-clip ver.4', layout, element_justification='center', finalize=True, resizable=True,return_keyboard_events=True, use_default_focus=False)

#------------ Media Player Setup ---------#

class player():
    def __init__(self):
        self.is_initiated = False
        self.SEEK_TIME = 10
        self.MAX_VOL = 512
        self.MIN_VOL = 0
        self.DEFAULT_VOL = 256
        self.VOL_STEP = 13
        self.current_vol = self.DEFAULT_VOL
        self.source_path=""
        self.bat_list =[]

    def toggle_play(self,filepath): #Start playing.
        if not self.is_initiated:
            self.is_initiated = True
            self.thrededreq("loop off")
            self.thrededreq("volume 100")
            self.thrededreq('strack -1')
            self.thrededreq("add "+filepath.replace('/', '\\'))
            print("Init Playing")
            return
        self.thrededreq("pause")
        print("Toggle play")
    
    def load(self):
        self.source_path = None
        self.source_path = sg.popup_get_file('Select file.','select file.')
        if self.source_path is not None:
            self.stop()
            print('input file is '+self.source_path)
            self.toggle_play(self.source_path)
        pass

    def stop(self):
        self.is_initiated=False
        self.thrededreq("stop")
        pass

    def volup(self):
        self.current_vol = self.current_vol + self.VOL_STEP
        self.thrededreq("volume " + str(self.current_vol))
        print("Volume up")
        pass

    def voldown(self):
        self.current_vol = self.current_vol - self.VOL_STEP
        self.thrededreq("volume " + str(self.current_vol))
        print("Volume Down")
        pass

    def seek(self, forward: bool):
        if player.is_playing()==1:
            length = self.get_length()
            cur = self.get_time()
            if (forward):
                seekable = cur + self.SEEK_TIME
            else:
                seekable = cur - self.SEEK_TIME
            if seekable > length:
                seekable = length - 5
            if seekable < 0:
                seekable = 0
            self.thrededreq("seek " + str(seekable))
            print("Seek: ",seekable," Cur: ",cur,"Len: ",length)
        pass

    def is_playing(self):
        is_playing=self.req("is_playing")
        try:
            return int(self.req("is_playing"))
        except:
            return 0

    def get_time(self):
        try:
            return int(self.req("get_time"))
        except:
            return None

    def get_length(self):
        try:
            return int(self.req("get_length"))
        except:
            return None

    def cmd_run(self,cmd_text):
        print(self.req(cmd_text,True))
        #self.thrededreq(cmd_text)
        pass

    def cut(self):
        if self.is_initiated == True and self.source_path !=None:
            out_filename = self.source_path.split("/")[-1]
            out_filename = save_path + out_filename.rsplit(".",1)[0] + "_{:02d}-{:02d}.".format(player.get_time()//60, player.get_time() % 60) + out_filename.rsplit(".",1)[-1]
            print("export to: "+ out_filename)
            bat_cmd = ffmpeg_path + ffmpeg_cmd1 + str(self.get_time()+int(start_pos)) + ffmpeg_cmd2 + str(cut_length) + ffmpeg_cmd3 + self.source_path + ffmpeg_cmd4 + out_filename + ffmpeg_cmd5
            print(bat_cmd)
            self.bat_list.append(bat_cmd)

    def run(self):
        if self.bat_list == []:
            return
        else:
            bat_path = self.source_path.rsplit("/",1)[0] + "/vlc-anime-" + datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')+".bat"
            print(bat_path)
            with open(bat_path, mode='a') as f:
                f.write('\n'.join(self.bat_list))
            subprocess.Popen(bat_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.bat_list = []


    def _timeinfo(self, msg):
        length = self.req(msg, True).split("\r\n")
        if (len(length) < 2):
            return None
        length = length[1].split(" ")
        if (len(length) < 2):
            return None
        try:
            num = int(length[1])
            return num
        except:
            return None

    def req(self, msg: str, full=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.settimeout(0.7)
                sock.connect(('127.0.0.1', 44500))
                response = ""
                received = ""
                sock.sendall(bytes(msg + '\n', "utf-8"))
                # if True:
                try:
                    while (True):
                        received = (sock.recv(1024)).decode()
                        response = response + received
                        if full:
                            b = response.count("\r\n")
                            if response.count("\r\n") > 60: #とりあえずhelpコマンドで全部表示されるように。重いようなら変更？
                                sock.close()
                                break
                        else:
                            if response.count("\r\n") > 0:
                                sock.close()
                                break
                except:
                    response = response + received
                    pass
                sock.close()
                return response
        except:
            return None
            pass

    def thrededreq(self, msg):
        threading.Thread(target=self.req, args=(msg,)).start()

#'vlc --intf rc --rc-host 127.0.0.1:44500' you need to run the vlc player from command line to allo controlling it via TCP
player=player()

#------------ The Event Loop ------------#
while True:
    event, values = window.read(timeout=500)       # run with a timeout so that current location can be updated
    if event == sg.WIN_CLOSED:
        break
    if event == 'stop' or event ==key_stop:
        player.stop()
    if event == 'pause' or event ==key_pause or event ==key_pause2:
        player.thrededreq("pause")
    if event == 'faster' or event ==key_faster:
        player.thrededreq("faster")
        print("faster")
    if event == 'slower' or event == key_slower:
        player.thrededreq('slower')
        print("slower")
    if event == 'normal' or event ==key_normnal:
        player.thrededreq('normal')
    if event == 'load' or event == key_load:
        player.load()
    if event == "10s <-" or event ==key_back10s:
        player.seek(0)
    if event =='-> 10s' or event ==key_skip10s:
        player.seek(1)
    if event == 'screenshot' or event ==key_screenshot:
        player.thrededreq('snapshot')
    if event == 'cmd run':
        if values['-VLC_Control_Command-']!='':
            player.cmd_run(values['-VLC_Control_Command-'])
    if event =='cut' or event ==key_cut:
        player.cut()
    if event == 'Generate .bat and run' or event ==key_run:
        player.run()
    
    # update elapsed time if there is a video loaded and the player is playing
    if player.is_playing()==1:
        try:
            window['-MESSAGE_AREA-'].update("{:02d}:{:02d} / {:02d}:{:02d}".format(player.get_time()//60, player.get_time() % 60,player.get_length()//60, player.get_length() % 60))
        except:
            window['-MESSAGE_AREA-'].update('Load media to start' if player.is_playing() == 0 else 'Ready to play media' )
    else:
        window['-MESSAGE_AREA-'].update('Load media to start' if player.is_playing() == 0 else 'Ready to play media' )


window.close()
