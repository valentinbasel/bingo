#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2012 Valentin Basel <valentin@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import random, time, pygame

pygame.init()
COLOR_FONDO=(90,190,90)

class BOLILLA(object):
    """ Class doc """
    
    def __init__ (self,img,x,y,ventana,texto):
        """ Class initialiser """
        self.x=x
        self.y=y
        self.imagen = pygame.image.load("imagenes/96/"+img+".png")
        self.rect=self.imagen.get_rect()
        self.ventana=ventana
    def update(self):
        self.rect[0]=self.x
        self.rect[1]=self.y
        self.ventana.blit(self.imagen,(self.rect))
    def CambiarImg(self,img):
        self.imagen = pygame.image.load("imagenes/96/"+img+".png")
        self.rect=self.imagen.get_rect()
class TEXTO (object):
    def __init__(self, ventana,FontName = None, FontSize = 40):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize
        self.ventana=ventana
    def render(self,  text, color, pos):
        #text = unicode(text, "UTF-8")
        x, y = pos
        for i in text.split("\r"):
            self.ventana.blit(self.font.render(i, 1, color), (x, y))
            y += self.size 

class VENTANA(object):
    """ Clase manejadora de la ventana pygame"""
    
    def __init__ (self):
        """ Class initialiser """
        self.pantalla=pygame.display.set_mode((800,600),pygame.FULLSCREEN,16)
        self.pantalla.fill(COLOR_FONDO)
    def update(self):
        pygame.display.update()

class FICHA(pygame.sprite.Sprite):
    """ Class doc """
    
    def __init__ (self,valor,estado,ventana,x,y,txt,azar):
        """ Class initialiser """
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.valor=valor
        self.estado=estado
        self.ventana=ventana
        self.texto=txt
        self.imagen = pygame.image.load("imagenes/ficha.png")
        self.rect=self.imagen.get_rect()
        self.imagen2 = pygame.image.load("imagenes/ficha2.png")
        self.AzarLista=azar
    def update(self):
        self.rect[0]=self.x
        self.rect[1]=self.y

        if self.AzarLista[self.valor-1][1]==1:
            self.ventana.blit(self.imagen2,(self.rect))
            self.texto.render(str(self.valor),(255,255,255),(self.x+5,self.y+10))
        else:
            self.ventana.blit(self.imagen,(self.rect))
            self.texto.render(str(self.valor),(255,255,255),(self.x+5,self.y+10))
class AZAR(object):
    """ clase que maneja los parametros de azar del sistema """
    
    def __init__ (self,ini,fini):
        """ Class initialiser """
        self.lista=[]
        self.ini=ini
        self.fini=fini
        self.valores=["00","00","00"]
        self.contador=0
        for valor in range(self.ini,self.fini):
            self.lista.append((valor,0))
        self.rand=0
    def TirarNumero(self):
        self.rand=random.randint(self.ini,self.fini)
        return self.rand
    def BuscarEnGrilla(self,valor):
        for ValorLista in range(len(self.lista)):
            if valor==self.lista[ValorLista][0]:
                if self.lista[ValorLista][1]==0:
                    self.lista[ValorLista][1]==1
                    return 1
        return 0

    def limpiar(self):
        print self.lista
        for a in range(len(self.lista)):
            self.lista[a]=(a,0)
            
    def ActualizarValores(self,val):
        if val<10:
            cadena="0"+str(val)
        else:
            cadena=str(val)
        aux1=self.valores[0]
        aux2=self.valores[1]
        self.valores[1]=aux1
        self.valores[2]=aux2

        self.valores[0]=cadena
        if self.contador>1:
            self.contador=0
        else:
            self.contador +=1
class BOTON(pygame.sprite.Sprite):
    
    """ Clase para definir botones """
    def __init__ (self,img,x,y,ventana,txt):
        """ Class initialiser """
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.ventana=ventana
        self.texto=txt
        self.imagen = pygame.image.load("imagenes/"+img)
        self.rect=self.imagen.get_rect()
        self.pulsado=0
    def update(self):
        self.rect[0]=self.x
        self.rect[1]=self.y
        MouseXY=pygame.mouse.get_pos()
        MouseBoton=pygame.mouse.get_pressed()
        if self.pulsado==0:
            if  self.rect.collidepoint(MouseXY) and MouseBoton[0]==1:
                time.sleep(0.1)
                self.pulsado=1
                return 1
        if MouseBoton[0]==0:
            self.pulsado=0
        self.ventana.blit(self.imagen,(self.rect))
        return 0

class EMPEZAR(BOTON):
    """ Clase derivada de boton """
    #~ def presionado(self):
        
    def buscar(self,azar,texto,ventana,bolilla,bolilla1,bolilla2,bolilla3):
        acum=0
        for a in azar.lista:
            acum=acum+ a[1]
        if acum<90:
            p=0
            while True:
                print "busco",p
                p+=1
                valor=azar.TirarNumero()
                encontrado=azar.BuscarEnGrilla(valor)
                if encontrado==1:
                    azar.lista[valor-1]=(valor-1,1)
                    ventana.pantalla.fill(COLOR_FONDO)
                    #~ texto.render(str(valor),(255,255,255),(500,100))
                    if valor<10:
                        cadena="0"+str(valor)
                    else:
                        cadena=str(valor)
                    bolilla.CambiarImg(cadena)
                    
                    bolilla1.CambiarImg(azar.valores[0])
                    bolilla2.CambiarImg(azar.valores[1])
                    bolilla3.CambiarImg(azar.valores[2])
                    azar.ActualizarValores(valor)
                    print azar.valores
                    return 1
        #~ texto.render("FIN",(255,255,255),(500,100))
        return 0
class RESET(BOTON):
    
    """ Clase derivada de boton """
    pass
class SALIR(BOTON):
    """ Class doc """
    def salir(self):
        exit()
def main():
    ventana=VENTANA()
    texto=TEXTO(ventana.pantalla)
    fichas=pygame.sprite.RenderClear()
    x=0
    y=0
    bolilla=BOLILLA("00",520,100,ventana.pantalla,texto)
    bolilla1=BOLILLA("00",410,250,ventana.pantalla,texto)
    bolilla2=BOLILLA("00",520,250,ventana.pantalla,texto)
    bolilla3=BOLILLA("00",630,250,ventana.pantalla,texto)

    BotonEmpezar=EMPEZAR("empezar.png",400,550,ventana.pantalla,texto)
    BotonReset=RESET("reset.png",530,550,ventana.pantalla,texto)
    BotonSalir=SALIR("salir.png",660,550,ventana.pantalla,texto)
    azar=AZAR(1,91)
    logo=BOTON("logo_bingo.png",529,10,ventana.pantalla,texto)
    for a in range(1,91):
        ficha=FICHA(a,0,ventana.pantalla,x,y,texto,azar.lista)
        fichas.add(ficha)
        x=x+40
        if x==400:
            x=0
            y=y+40
    while(True):
        pygame.event.get()
        bolilla.update()
        bolilla1.update()
        bolilla2.update()
        bolilla3.update()
        presionado=BotonEmpezar.update()
        presionado2=BotonReset.update()
        presionado3=BotonSalir.update()
        logo.update()
        if presionado==1:
            BotonEmpezar.buscar(azar,texto,ventana,bolilla,bolilla1,bolilla2,bolilla3)
        if presionado2==1:
            azar.limpiar()
        if presionado3==1:
            BotonSalir.salir()
        fichas.update()
        ventana.update()
    return 0
    

if __name__ == '__main__':
    main()

