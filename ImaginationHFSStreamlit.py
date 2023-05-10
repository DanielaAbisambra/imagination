# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:37:09 2023

@author: abisambra.d
"""

# Proyecto Imagination HFS

#Importamos Paquetes
import numpy as np
import sys
import pandas as pd

from tkinter import *
from PIL import Image,ImageTk, ImageDraw, ImageFont
import tkinter as tk
from PIL import ImageGrab
from tkinter import filedialog

import io
import os
import subprocess


import streamlit
import streamlit as st
from streamlit.web import cli as stcli

from zipfile import ZipFile
from io import BytesIO
import base64

#from streamlit.hashing import _CodeHasher
#import SessionState

#pip install ghostscript
#pip install pillow
# Subir Excel con estructura de combos a los cuales se les debe generar imagen


#Funcion para tomar estados de Streamlit
#def get_state():
    # Create a unique key for the session state
    # This ensures that different users have different session states
#    session_id = st.report_thread.get_report_ctx().session_id
#    hash_funcs = {"sha256": _CodeHasher("sha256")}
#    return SessionState.get(session_id, hash_funcs)

#state = get_state()



#dfpromos = pd.read_excel("C:/Users/abisambra.d/OneDrive - Procter and Gamble/HFS SDO/Rocks/Digital/Fase 3/Imagination Project\Tabla de Entrada Imagination2.xlsx")


#Subir excel desde streamlit
st.title("Imagination", anchor=None)
#st.set_page_config(page_title="Imagination", page_icon="TriquiIcon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)


#Importo el excel subido con rutero
dataset = st.file_uploader("Cargue maestra de combos con columnas: PLU, Descripcion, EAN1, EAN2, EAN3, EAN4, Comunicacion, Disclaimer ", type = ['xlsx'])
if dataset is not None:
    dfpromos = pd.read_excel(dataset)
    st.sidebar.write(' ### Rows and Columns:',dfpromos.shape)

#Colores
gris = (50,50,50)
grisclaro = (70,70,70)
negro = (0,0,0)
naranja = (252,94,3)
azul = (16, 5, 130)
rosado = (255,0,128)
amarillo= (253,218,13)
colorx= naranja
colorname = "gris"

opciones = ""
opciones = st.text_input("Seleccione su color de Preferencia: azul, negro, naranja, gris, rosado, amarillo")

#opciones = st.multiselect("Seleccione 1 Color", ["grisocuro", "grisclaro", "negro", "naranja", "azul"])
#st.write('You selected:', opciones)
if opciones== "":
    colorx= gris
elif opciones=="naranja":
    colorx=naranja
elif opciones=="negro":
    colorx=negro
elif opciones=="gris":
    colorx=gris
elif opciones=="azul":
    colorx=azul
elif opciones=="rosado":
    colorx=rosado
elif opciones=="amarillo":
    colorx=amarillo


#Agrego el Boton de generar    
resultado = st.button("Generar") #Devuleve True cuando el usuario hace click
zipObj = ZipFile("ImaginationResult.zip", "w")

if resultado == True:
    
    
    for i in range(0,dfpromos.shape[0]):
    #for i in range(0,3):
        #Iterar combo a combo
        plu = dfpromos.iloc[i,0]
        ean1 = int(dfpromos.iloc[i,2])
        ean2 = dfpromos.iloc[i,3]
        ean3 = dfpromos.iloc[i,4]
        ean4 = dfpromos.iloc[i,5]
        comunic = dfpromos.iloc[i,6]
        disc = dfpromos.iloc[i,7]
        
        
        #Path para guardar el output
        outpath = "C:/Users/abisambra.d/OneDrive - Procter and Gamble/HFS SDO/Rocks/Digital/Fase 3/Imagination Project/Output"
        
        #Se identifica el tipo de promo con la que se está lidiando
        
        tipo = 0
        
        if np.isnan(ean2):
            tipo = 1 
        elif np.isnan(ean3):
            tipo = 2
        elif np.isnan(ean4):
            tipo = 3
        else: tipo = 4
        
        
        # Si es Tipo 1
        if tipo ==1:
        
            im = Image.open("./imagenes/"+ str(int(ean1)) +".jpg")
            im1 = im.resize((550,550))
            
            dst = Image.new('RGB', (800, 800), (255,255,255))
            dst.paste(im1, (100, 50))
        
            img = Image.new("RGBA", (800, 120), color="white")
            draw = ImageDraw.Draw(img)
            draw_point = (100, 0)
             
            font = ImageFont.truetype("./BebasNeue-Regular.ttf",70)
            draw.text(draw_point, comunic, font=font, fill= colorx, align = 'center')
            
            text_window = img.getbbox()
            img = img.crop(text_window)
              
            imgdisc = Image.new("RGBA", (800, 30), color="white")
            draw = ImageDraw.Draw(imgdisc)
            draw_point = (100, 0)
             
            font = ImageFont.truetype("./arial.ttf",15)
            draw.text(draw_point, disc, font=font, fill=grisclaro, align = 'center')
             
            text_window = imgdisc.getbbox()
            imgdisc = imgdisc.crop(text_window)
              
            dst.paste(img, (0,600))
            dst.paste(imgdisc, (0,720)) 
             
            #dst.show()
            #dst.save(outpath + "/" + colorname + "/" + str(plu) + ".jpg")
            image_bytes = BytesIO()
            dst.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            zipObj.writestr(str(plu) +'.png', image_bytes.read())
            
        elif tipo ==2 :
            
            ean2 = int(ean2)
            im = Image.open("./imagenes/"+ str(int(ean1)) +".jpg")
            im1 = im.resize((300,300))
            
            im = Image.open("./imagenes/"+ str(int(ean2)) +".jpg")
            im2 = im.resize((300,300))
        
            dst = Image.new('RGB', (800, 800), (255,255,255))
            dst.paste(im1, (100, 150))
            dst.paste(im2, (im1.width+100, 150))
        
            img = Image.new("RGBA", (800, 120), color="white")
            draw = ImageDraw.Draw(img)
            draw_point = (100, 0)
            
            font = ImageFont.truetype("./BebasNeue-Regular.ttf",70)
            draw.text(draw_point, comunic, font=font, fill= colorx, align = 'center')
            
            text_window = img.getbbox()
            img = img.crop(text_window)
             
            imgdisc = Image.new("RGBA", (800, 30), color="white")
            draw = ImageDraw.Draw(imgdisc)
            draw_point = (100, 0)
            
            font = ImageFont.truetype("./arial.ttf",15)
            draw.text(draw_point, disc, font=font, fill= grisclaro, align = 'center')
            
            text_window = imgdisc.getbbox()
            imgdisc = imgdisc.crop(text_window)
             
            dst.paste(img, (0,600))
            dst.paste(imgdisc, (0,720)) 
            
            #dst.show()
            #dst.save(outpath + "/" + colorname + "/" + str(plu) + ".jpg")
            image_bytes = BytesIO()
            dst.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            zipObj.writestr(str(plu) +'.png', image_bytes.read())
            
            
        elif tipo ==3 :
            
            ean2 = int(ean2)
            ean3 = int(ean3)
            im = Image.open("./imagenes/"+ str(int(ean1)) +".jpg")
            im1 = im.resize((250,250))
            
            im = Image.open("./imagenes/"+ str(int(ean2)) +".jpg")
            im2 = im.resize((250,250))
            
            im = Image.open("./imagenes/"+ str(int(ean3)) +".jpg")
            im3 = im.resize((250,250))
            
            dst = Image.new('RGB', (800, 800), (255,255,255))
            dst.paste(im1, (150, 100))
            dst.paste(im2, (im1.width+150, 100))
            dst.paste(im3, (int(im1.width/2)+150,im1.height+100))
        
            img = Image.new("RGBA", (800, 120), color="white")
            draw = ImageDraw.Draw(img)
            draw_point = (100, 0)
            
            font = ImageFont.truetype("./BebasNeue-Regular.ttf",70)
            draw.text(draw_point, comunic, font=font, fill=colorx, align = 'center')
            
            text_window = img.getbbox()
            img = img.crop(text_window)
             
            imgdisc = Image.new("RGBA", (800, 30), color="white")
            draw = ImageDraw.Draw(imgdisc)
            draw_point = (150, 0)
            
            font = ImageFont.truetype("./arial.ttf",15)
            draw.text(draw_point, disc, font=font, fill=grisclaro, align = 'center')
            
            text_window = imgdisc.getbbox()
            imgdisc = imgdisc.crop(text_window)
             
            dst.paste(img, (0,600))
            dst.paste(imgdisc, (0,720))    
            
            #dst.show()
            #dst.save(outpath + "/" + colorname + "/" + str(plu) + ".jpg")
            image_bytes = BytesIO()
            dst.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            zipObj.writestr(str(plu) +'.png', image_bytes.read())
        
        
        elif tipo ==4 :
            
            ean2 = int(ean2)
            ean3 = int(ean3)
            ean4 = int(ean4)
            im = Image.open("./imagenes/"+ str(int(ean1)) +".jpg")
            im1 = im.resize((250,250))
            
            im = Image.open("./imagenes/"+ str(int(ean2)) +".jpg")
            im2 = im.resize((250,250))
        
            
            im = Image.open("./imagenes/"+ str(int(ean3)) +".jpg")
            im3 = im.resize((250,250))
        
            
            im = Image.open("./imagenes/"+ str(int(ean4)) +".jpg")
            im4 = im.resize((250,250))
            
            dst = Image.new('RGB', (800, 800), (255,255,255))
            dst.paste(im1, (150, 100))
            dst.paste(im2, (im1.width+150, 100))
            dst.paste(im3, (150,im1.height+100))
            dst.paste(im4, (im1.width+150,im1.height+100))
            
            img = Image.new("RGBA", (800, 120), color="white")
            draw = ImageDraw.Draw(img)
            draw_point = (150, 0)
        
            font = ImageFont.truetype("./BebasNeue-Regular.ttf",70)
            draw.text(draw_point, comunic, font=font, fill= colorx, align = 'center')
        
            text_window = img.getbbox()
            img = img.crop(text_window)
            
            
            imgdisc = Image.new("RGBA", (800, 30), color="white")
            draw = ImageDraw.Draw(imgdisc)
            draw_point = (100, 0)
        
            font = ImageFont.truetype("./arial.ttf",15)
            draw.text(draw_point, disc, font=font, fill=grisclaro, align = 'center')
            #draw.text(text= disc, font=font, fill=(50,50,50), align = 'center')
        
            text_window = imgdisc.getbbox()
            imgdisc = imgdisc.crop(text_window)
            
            dst.paste(img, (0,600))
            dst.paste(imgdisc, (0,720))
            
            #dst.show()
            #dst.save(outpath + "/" + colorname +"/" + str(plu) + ".jpg")
            image_bytes = BytesIO()
            dst.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            zipObj.writestr(str(plu) +'.png', image_bytes.read())
    



zipObj.close()

ZipfileDotZip = "ImaginationResult.zip"

with open(ZipfileDotZip, "rb") as f:
   bytes = f.read()
   b64 = base64.b64encode(bytes).decode()
   href = f"<a href=\"data:file/zip;base64,{b64}\" download='{ZipfileDotZip}.zip'>\
       Descarga Fotos\
   </a>"
st.sidebar.markdown(href, unsafe_allow_html=True)

#Publicar desde comand prompt con el directorio de este script:
#streamlit run ImaginationHFSStreamlit.py
#Local URL: http://localhost:8501
#Network URL: http://192.168.5.172:8501  
    
