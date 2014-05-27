#!/usr/bin/env python
# -*- coding: utf-8 -*-

# indicator-meocloud.py
# indicateur pour meocloud
#	demarre automatiquement meocloud
#	affiche marche/arret/synchronisation en cours
# matefin
# 2014-05-27
# v0.10.29c

# d'apres http://linux.leunen.com/?p=933
# https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators
# http://ubuntuforums.org/showthread.php?t=2056296
# http://zetcode.com/gui/pygtk/menus/
# http://www.siteduzero.com/tutoriel-3-93860-pygtk.html?all=1
# http://conjurecode.com/create-indicator-applet-for-ubuntu-unity-with-python/
# http://tuxion.com/2010/04/16/periodic-timers-in-pygtk.html
# http://ubuntuforums.org/showthread.php?t=755806
# http://fr.openclassrooms.com/forum/sujet/extraction-de-donnees-d-un-txt-31089#.U3ighvimcQo
# http://www.matteomattei.com/en/very-simple-graphical-messagebox-in-python-useful-for-console-applications-with-py2exe/

import appindicator
import gtk, gobject
import os
import webbrowser
import Tkinter as tk
import tkMessageBox as mbox	# boite de dialogue
    
class IndicatorMEO:
  def __init__(self):

    #-------------------------------------------------
    # chaines selon la langue (traduction)
    #-------------------------------------------------  
    # decommentez les lignes des langues
    
    # French
    open_folder = "Ouvrir le dossier MEOCloud"
    open_page = "Ouvrir la page web MEOCloud"
    sync_pause = "Pause synchro"
    sync_resume = "Reprise synchro"
    last_notifications = "Dernières notifications"
    show_status = "Status"
    show_help = "Aide (ligne de commande)"
    syncing = 'Synchro en cours...'


    # English
    



    #-------------------------------------------------
    # creer le menu
    #-------------------------------------------------  
    # l'ordre d'affichage dans la barre depend de CATEGORY
    #CATEGORY_SYSTEM_SERVICES
    #CATEGORY_OTHER
    #self.ind = appindicator.Indicator("MEOCloud","/usr/local/share/pixmaps/Light_Off-32x32.png",appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind = appindicator.Indicator("MEOCloud","meocloud-idle",appindicator.CATEGORY_APPLICATION_STATUS)
 
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    # autre icone si on utilise STATUS_ATTENTION
    #self.ind.set_attention_icon ("meocloud-updating")

    # creer un menu deroulant
    self.menu = gtk.Menu()
    
    #-------------------------------------------------
    # liste des elements du menu (definis dans le bon ordre)
    #-------------------------------------------------   
    #self.item1 = gtk.MenuItem("Firefox")

    # ligne du menu
    # creer
    self.item1 = gtk.MenuItem()
    self.item1.set_label("MEOCloud")
    # afficher dans l'ordre
    self.menu.append(self.item1)
    # afficher
    self.item1.show()
    
    self.item2 = gtk.MenuItem()
    self.item2.set_label("Quota:")
    self.menu.append(self.item2)
    self.item2.show()

    self.item8 = gtk.MenuItem()
    self.item8.set_label("---")
    self.menu.append(self.item8)
    self.item8.hide()

    self.item9 = gtk.MenuItem()
    self.item9.set_label("---")
    self.menu.append(self.item9)
    self.item9.hide()
 
    self.item10 = gtk.MenuItem()
    self.item10.set_label("---")
    self.menu.append(self.item10)
    self.item10.hide()
   
    # separateur
    self.sep1 = gtk.SeparatorMenuItem()
    self.menu.append(self.sep1)
    self.sep1.show()

    self.item5 = gtk.MenuItem()
    self.item5.set_label(open_folder)
    self.item5.connect("activate", self.meocloud_dir)
    self.menu.append(self.item5)
    self.item5.show()

    self.item6 = gtk.MenuItem()
    self.item6.set_label(open_page)
    self.item6.connect("activate", self.meocloud_web)
    self.menu.append(self.item6)
    self.item6.show()

    # separateur
    self.sep2 = gtk.SeparatorMenuItem()
    self.menu.append(self.sep2)
    self.sep2.show()
    
     # pause/reprise
    self.item3 = gtk.MenuItem()
    self.item3.set_label(synch_pause)
    self.item3.connect("activate", self.meocloud_pause)
    self.menu.append(self.item3)
    self.item3.show()

    # separateur
    self.sep3 = gtk.SeparatorMenuItem()
    self.menu.append(self.sep3)
    self.sep3.show()
    
    self.item4 = gtk.MenuItem()
    self.item4.set_label(last_notifications)
    self.item4.connect("activate", self.meocloud_notif)
    self.menu.append(self.item4)
    self.item4.show()

    self.item6 = gtk.MenuItem()
    self.item6.set_label(show_status)
    self.item6.connect("activate", self.meocloud_status)
    self.menu.append(self.item6)
    self.item6.show()
    
    self.item7 = gtk.MenuItem()
    self.item7.set_label(show_help)
    self.item7.connect("activate", self.meocloud_help)
    self.menu.append(self.item7)
    self.item7.show()

    # separateur
    self.sep4 = gtk.SeparatorMenuItem()
    self.menu.append(self.sep4)
    self.sep4.show()

    # ligne quitter
    self.quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    self.quit.connect("activate", self.on_quit)
    self.quit.show()
    self.menu.append(self.quit)
   
    # associer le menu cree avec appindicator
    self.ind.set_menu(self.menu)
 
  #-------------------------------------------------
  # fonctions   
  #------------------------------------------------- 

  def meocloud_dir (self, bidon):
    os.system("xdg-open $HOME/MEOCloud")

  def meocloud_web (self, bidon):
    #webbrowser.open("https://meocloud.pt/home/", new=2, autoraise=True)
    webbrowser.open_new_tab("https://meocloud.pt/home/")
 
    
  def meocloud_pause (self, bidon):
    global icon_type
    status = os.popen("meocloud status", "r").read()
    cherche = 'Status: PAUSED'
    # pause/reprise synchro
    if cherche in status:
      os.system("meocloud resume")
      self.ind.set_status(appindicator.STATUS_ACTIVE)
      icon_type = "active"
      self.item3.set_label(sync_pause)
    else:
      os.system("meocloud pause")
      indicator.ind.set_attention_icon("meocloud-paused")
      self.ind.set_status(appindicator.STATUS_ATTENTION)
      icon_type = "attention"
      self.item3.set_label("Reprise synchro")


  def meocloud_notif (self, bidon):
    global icon_type
    status = os.popen("meocloud not", "r").read()
    print status
    self.window_info(last_notifications, status)
   
  def meocloud_status (self, bidon):
    global icon_type
    status = os.popen("meocloud status", "r").read()
    print status 
    self.window_info(show_status, status)
    # metre a jour affichage (et demarrer)
    self.displayupdate(status)

  def meocloud_help (self, bidon):
    global icon_type
    status = os.popen("meocloud -h", "r").read()
    print status
    self.window_info(show_help, status)

    
  def displayupdate (self, mystatus):
    lines = mystatus.splitlines()
    # mettre a jour l'affichage du quota
    cherche = 'Quota:'
    for line in lines:    
      if cherche in line:
        indicator.item2.set_label(line)
    # mettre a jour l'affichage de synchro/pause
    cherche = 'Status: SYNCING'
    if cherche in mystatus:
      for line in lines:    
        if cherche in line:
          indicator.item8.set_label()
          self.item8.show()
    else:
      cherche = 'Status: PAUSED'
      if cherche in mystatus:
        for line in lines:    
          if cherche in line:
            indicator.item8.set_label('En pause (arrêt synchro)')
            self.item8.show()
      else:
        indicator.item8.set_label("---")
        self.item8.hide()
    # mettre a jour l'affichage de l'upload
    cherche = 'Uploading '
    if cherche in mystatus:
      for line in lines:    
        if cherche in line:
          indicator.item9.set_label(line)
          self.item9.show()
    else:
      indicator.item9.set_label("---")
      self.item9.hide()
    # mettre a jour l'affichage du download
    cherche = 'Downloading '
    if cherche in mystatus:
      for line in lines:    
        if cherche in line:
          indicator.item10.set_label(line)
          self.item10.show()
    else:
      indicator.item10.set_label("---")
      self.item10.hide()
    #
    # changer l'icone selon le status
    cherche = 'Status: SYNCING'
    if cherche in mystatus:
      indicator.ind.set_attention_icon("meocloud-updating")
      self.ind.set_status(appindicator.STATUS_ATTENTION)
      icon_type = "attention"
      self.item3.set_label("Pause synchro")
    else:
      cherche = 'Status: PAUSED'
      if cherche in mystatus:
        self.ind.set_attention_icon("meocloud-paused")
        self.ind.set_status(appindicator.STATUS_ATTENTION)
        icon_type = "attention"
        self.item3.set_label("Reprise synchro")
      else:
        cherche = 'Status: IDLE'
        if cherche in mystatus:
          self.ind.set_status(appindicator.STATUS_ACTIVE)
          icon_type = "active"
          self.item3.set_label("Pause synchro")
        else:
          # si meocloud n'est pas demarre : le demarrer
          cherche='not seem to be running'
          if cherche in mystatus:
            self.ind.set_attention_icon ("meocloud-offline")
            self.ind.set_status(appindicator.STATUS_ATTENTION)
            icon_type = "attention"
            os.system("meocloud start")
            self.item3.set_label("Pause synchro")
          else:
            # erreur
            indicator.ind.set_attention_icon("meocloud-error")
            self.ind.set_status(appindicator.STATUS_ATTENTION)
            icon_type = "attention"
            self.item3.set_label("Pause synchro")

           
  def checkmeocloud (bidon):
    global icon_type, status
    status = os.popen("meocloud status", "r").read()
    # metre a jour affichage (et demarrer)
    indicator.displayupdate(status)
    return True  


  def on_launch(self, widget, data):
    os.system(data)
          
  def on_quit(self, widget, data = None):
    # arreter meocloud
    os.system("meocloud stop")
    gtk.main_quit()
    
  def window_info(self, title, message):
    # afficher un texte dans une boite
    #These two lines get rid of tk root window
    root = tk.Tk()
    root.withdraw()
    #mbox.deiconify()
    mbox.showinfo(title, message)
    
    # process all pending Tk/X window events
    root.update()
    return
            
    
#-------------------------------------------------
# afficher le menu
#-------------------------------------------------
# variables globales
icon_type = "active"
status = ""

if __name__ == "__main__":
  # afficher l'indicateur
  indicator = IndicatorMEO()
  
  # demarrer meocloud si besoin
  # puis tester automatiquement son status toutes les x millisec
  indicator.checkmeocloud
  maintimer = gtk.timeout_add(3000, indicator.checkmeocloud)
  #maintimer = gobject.timeout_add(3000, indicator.checkmeocloud)

  gtk.main()

#### FIN

