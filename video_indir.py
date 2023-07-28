import os
from tkinter import *
from tkinter import ttk
from pytube import YouTube
from tkinter import messagebox


def sanitize_filename(title):
   
    return re.sub(r'[\\/:*?"<>|]', '_', title)

def indir():
    # Girilen 
    url = url_entry.get()
    yt = YouTube(url)

    # Dosyanın bulunduğu dizini alır
    bulunduğu_dizin = os.getcwd()
    os.chdir(bulunduğu_dizin)

    # Combobox dan seşilen veri çekiliyor
    video_kalite = kalite_combobox.get()

    # Seçilen veriye göre indirme işlemi yapılıyor
    if video_kalite == "360p" or video_kalite == "720p" or video_kalite == "1080p":
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=video_kalite).first()
    elif video_kalite == "mp3":
        stream = yt.streams.filter(only_audio=True).first()
    else:
        messagebox.showerror("Hata", "Geçersiz kalite seçimi.")
        return

    if stream:
        # Dosya adı için özel bir isim oluştur
        if video_kalite == "mp3":
            dosya_adi = sanitize_filename(yt.title) + ".mp3"  # Videonun adını alıp .mp3 uzantısını ekliyoruz
        else:
            dosya_adi = sanitize_filename(yt.title) + ".mp4"  # Video kalitesine göre isim oluşturuyoruz

        # İndirilecek dosyanın tam yolunu oluşturuyoruz
        dosya_yolu = os.path.join(bulunduğu_dizin, dosya_adi)

        # İndirme işlemi yapılıyor
        stream.download(filename=dosya_yolu)

        messagebox.showinfo("İşlem Tamamlandı", "Video başarıyla indirildi.")
    else:
        messagebox.showerror("Hata", "Seçilen kalitede video bulunamadı.")

# Pencere ve pencere üzerindeki öğeler oluşturuluyor
pencere = Tk()
pencere.title("Youtube Video İndir")
pencere.geometry("400x150")

url_entry = Entry(width=40, relief=RAISED)
url_entry.place(x=50, y=40)
url_label = Label(text="URL:")
url_label.place(x=10, y=40)

kaliteler = ["mp3", "360p", "720p", "1080p"]
kalite_combobox = ttk.Combobox(values=kaliteler, state="readonly")
kalite_combobox.place(x=120, y=70)

indir_button = Button(text="İndir", width=10, command=indir, relief=RAISED)
indir_button.place(x=140, y=110)

pencere.mainloop()
