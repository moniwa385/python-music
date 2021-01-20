import pyaudio
import numpy as np
import random
import time
import wave

# サンプリングレートを定義 --- (*1)
RATE = 44100  #音楽業界標準

# BPMや音長を定義 --- (*2)
#debug BPM = 100
BPM = random.randint(40,200) #Beat Per Minute(1分あたりの4分音符の数)

print("BPM=" + str(BPM))

#全分音符(L1)、二分音符(L2)、四分音符(L4)、八分音符(L8)
L1 = (60 / BPM * 4)
L2,L4,L8 = (L1/2,L1/4,L1/8)

music_notes = (L1,L2,L4,L8) 

# ドレミ...の周波数を定義 --- (*3)

C,C_sp,D,D_sp,E,F,F_sp,G,G_sp,A,A_sp,B= (
        261.626, 277.183,293.665, 311.127,
        329.628, 349.228, 369.994,391.995, 
        415.305, 440.000,466.164,493.883)

music_Scale = (A*0.5,A_sp*0.5,B*0.5,
               C,C_sp,D,D_sp,E,F,
               F_sp,G,G_sp,A,A_sp,B,
               C*2,C_sp*2,D*2,)

# サイン波を生成 --- (*4)
def tone(freq, length, gain):
    slen = int(length * RATE)
    t = float(freq) * np.pi * 2 / RATE
    return np.sin(np.arange(slen) * t) * gain

# 再生 --- (*5)
def play_wave(stream, samples):
    stream.write(samples.astype(np.float32).tostring())


# 出力用のストリームを開く --- (*6)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=RATE,
                frames_per_buffer=1024,
                output=True)

# ドレミを再生 --- (*7)
print("play")

time_execute = 0

#実行開始時間取得
time_start = time.time() 

#Waveデータ保存用List
frame = []
frames = []

while (time_execute < 60):

    #乱数発生
    random1 = random.randint(0,3)
    random2 = random.randint(0,len(music_Scale)-1)

    #音出力
    play_wave(stream, tone(music_Scale[random2], music_notes[random1], 1.0)) 

    #Waveデータ保存用データ作成
    frame = tone(music_Scale[random2], music_notes[random1], 1.0)
    frame = np.rint(32767*frame/max(abs(frame))) # [-32767,32767] の範囲に収める
    frame = frame.astype(np.int16) # 16ビット整数に型変換する   
    frames.append(frame)

    #実行中時間取得
    time_end = time.time()
 
    #実行経過時間算出 
    time_execute = time_end - time_start

stream.close()
p.terminate()

#Waveデータ保存
WAVE_OUTPUT_FILENAME = "test.wav"
CHANNELS=2  #チャンネル数
FORMAT=pyaudio.paInt16

#waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile = wave.Wave_write(WAVE_OUTPUT_FILENAME)
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(p.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b"".join(frames))

waveFile.close()

