from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from TkinterDnD2 import *
from pathlib import Path
from PIL import Image, ImageChops, ImageOps
import subprocess
import glob
import os


root = TkinterDnD.Tk()
root.title('Pbr2Source')
root.geometry('300x300')
root.resizable(False, False)

tabControl = ttk.Notebook(root, takefocus=0)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Convert')
tabControl.add(tab2, text ='Settings')
tabControl.pack(expand = 1, fill ="both")

ao_list = ['ao', 'AmbiantOcclusion']
roughness_list = ['rough', 'Roughness']
normal_list = ['nor', 'Normal']

def basetexture():
    global basecolor, oclusion, metal
    img = albedo.convert('RGB')
    img2 = occlusion.convert('RGB')
    base = ImageChops.multiply(img2, img)
    base.save(base_name+'_base.png')


def specular():
    global occlusion, roughness
    img = occlusion.convert('RGB')
    img2 = roughness.convert('RGB')
    img2 = ImageOps.invert(img2)
    s = ImageChops.multiply(img, img2)
    s.save(base_name+'_specular.png')


def writte_vmt(base):
    os.makedirs(os.path.dirname('ExportedPBR/'+base+'.vmt'), exist_ok=True)
    with open('ExportedPBR/'+base+'.vmt', 'w') as vmt:
        vmt.write('"VertexlitGeneric"\n')
        vmt.write('{\n')
        vmt.write('	      $basetexture '+base+'\n')
        vmt.write('	      $surfaceprop ''\n')
        vmt.write('	      $bump '+base+'_normal\n')
        vmt.write('	      \n')
        vmt.write('	      $envmap env_cubemap''\n')
        vmt.write('	      $envmapmask '+base+'_specular\n')
        vmt.write('}')


def convert_textures(texture):
    try:
        with open("path_save.txt", "r") as f:
            g = f.read()
            f.close()
    except:
        messagebox.showerror('Error', 'Counter Strike Global Offensive path undefined !')
    vtex_path = '"'+g+'/bin/vtex" -quiet -nopause -mkdir -outdir "Exported PBR" -game "'+g+'/csgo" "'+str(os.getcwd()+'ExportedPBR/'+texture+'.tga')+'"'
    subprocess.call(vtex_path)


def convert(event):
    global occlusion, roughness, albedo, base_name
    file = event.data
    base_name = Path(event.data).stem
    base = Path(event.data).stem
    list = ['_', 'base', 'albedo', 'TexturesCom', 'Metallic', 'metal', 'Height', 'Normal', 'nor', 'Roughness', 'rough', 'AmbiantOcclusion', 'occ', 'BaseColor' '256', '512', '1024', '2048']
    list_base = ['base', 'albedo']
    for i in list:
        base_name = base_name.replace(i, '')
    for i in list_base:
        base = base.replace(i, '')
    files = []
    file_list = os.listdir(os.path.dirname(file))
    for x in file_list:
        if base in x:
            files.append(x)
    for i in files:
        if any(file in i for file in ao_list):
            occlusion = Image.open(os.path.dirname(file)+'/'+i)
        elif any(file in i for file in roughness_list):
            roughness = Image.open(os.path.dirname(file)+'/'+i)
        elif any(file in i for file in normal_list):
            normal = Image.open(os.path.dirname(file)+'/'+i)
    albedo = Image.open(event.data)
    basetexture()
    specular()
    writte_vmt(base_name)
    convert_textures(base_name)
    convert_textures(base_name+'_normal')
    convert_textures(base_name+'_specular')
    messagebox.showinfo('Info', 'Your files have been created !')


def game_config(event):
    game = event.data
    game_path.insert(0, game+'/')
    with open('path_save.txt', 'w') as save:
        save.write(game+'/')


canvas = Canvas(tab1, width=300, height=300, bg='white')
canvas.pack()
canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', convert)
canvas.create_text(150, 150, text='Drop base texture here')


Label(tab2, text='Game path :').pack()
game_path = ttk.Entry(tab2)
game_path.pack()
game_path.drop_target_register(DND_FILES)
game_path.dnd_bind('<<Drop>>', game_config)
game_path.bind('<Enter>', game_config)


root.mainloop()
