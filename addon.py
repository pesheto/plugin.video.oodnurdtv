#!/usr/bin/python
#Plugin to watch BG TV on XBMC through the www.drundoo.com web site
#Copyright (C) 2014  pesheto
#
#Note: The program requires an account set up through http://www.drundoo.com

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xbmcswift2 import Plugin
import xbmc, xbmcgui
import sys

from resources.drundoo import drundoo

plugin = Plugin()
my_drundoo = drundoo(plugin.get_setting('username'),plugin.get_setting('password'))

tv_links = dict(BTV='http://www.drundoo.com/channels/97/btv_hd/',
                BNT='http://www.drundoo.com/channels/2/bnt/',
                Nova='http://www.drundoo.com/channels/3/nova/',
                TV7='http://www.drundoo.com/channels/4/tv7/',
                btvComedy='http://www.drundoo.com/channels/12/btv_comedy/',
                btvAction='http://www.drundoo.com/channels/10/btv_action/',
                kinoNova='http://www.drundoo.com/channels/15/kino_nova/',
                Diema='http://www.drundoo.com/channels/16/diema/'
                )

tv_shows = dict(Slavi='http://www.drundoo.com/watch/slavi_show/24/',
                Gospodari = 'http://www.drundoo.com/watch/gospodari_na_efira/105/',
                Stolichani = 'http://www.drundoo.com/watch/stolichani_v_poveche_sezon_6/294/',
                Pod_Prikritie = 'http://www.drundoo.com/watch/pod_prikritie_sezon_4/477/',
                Familiata_2 = 'http://www.drundoo.com/watch/family/38/',
                Familiata_1 = 'http://www.drundoo.com/watch/familiyata_sezon_1/458/',
                Legenda_3 ='http://www.drundoo.com/watch/legendata_za_ispaniya_sezon_3/452/',
                Domashen_Arest = 'http://www.drundoo.com/watch/domashen_arest/292/',
                BTV_Novini = 'http://www.drundoo.com/watch/btv_news/27/',
                Imperium = 'http://www.drundoo.com/watch/imperium/478/',
                Pirati = 'http://www.drundoo.com/watch/pirati_izgubenoto_sukrovishte/422/',
                Styklen_Dom3 = 'http://www.drundoo.com/watch/stuklen_dom_sezon_3/492/')


@plugin.route('/')
def index():
    
    items = [{'label':'Live', 'path':plugin.url_for('test')},
             {'label':'Timeshift', 'path':plugin.url_for('time')},
             {'label':'Playlist', 'path':plugin.url_for('playlist')},
             {'label':'ZAPIS', 'path':plugin.url_for('zapis')}
            ]
        
    return items

######################################
#This section is for the live stations
######################################

@plugin.route('/test/')
def test():
    test_list = my_drundoo.get_list('http://www.drundoo.com/channels/',4)
    items=[]
    for link in test_list:
        items.append({'label':link,'path': plugin.url_for('test2',test=test_list[link])})
        
    return items

@plugin.route('/test2/<test>')
def test2(test):
    url = test
    #items = []
    #items.append({'label': 'play','path': my_drundoo.play_url(url), 'is_playable':True})
    #return items
    xbmc.Player().play(my_drundoo.play_url(url))

######################################
#End of live section 
######################################

######################################
#Timeshift section
######################################

@plugin.route('/time/')
def time():
    items=[]
    
    timeshift_list = my_drundoo.get_list('http://www.drundoo.com/channels/',2)
    
    for link in timeshift_list:
        items.append({'label':link,'path': plugin.url_for('time_stations',url=timeshift_list[link])})
        
    return items

@plugin.route('/time_stations/,<url>')
def time_stations(url):
    
    time_list = my_drundoo.get_list(url,3)

    items = []
    for link in time_list:
        items.append({'label':link,'path': plugin.url_for('time_url',url=time_list[link])})
    return items

@plugin.route('/time_url/<url>')
def time_url(url):
    url = url
    xbmc.Player().play(my_drundoo.play_url(url))

#####################################
#End of timeshift section
#####################################

#####################################
#Playlist section
#####################################

@plugin.route('/playlist/')
def playlist():
    play_list = dict()

    for i in range(1,20):
        temp = my_drundoo.get_list('http://www.drundoo.com/watch/playlists/?page='+str(i))
        play_list.update(temp)

    items=[]
    for link in play_list:
        items.append({'label':link,'path': plugin.url_for('playlist_stations',playlist=play_list[link])})
        
    return items

@plugin.route('/playlist/,<playlist>')
def playlist_stations(playlist):
    
    play_link, play_title = my_drundoo.make_shows(playlist,'list')

    items = []
    for my_title,my_link in zip(play_title,play_link):
        items.append({'label': my_title,'path': my_link, 'is_playable':True})
    return items

#####################################
#End of playlist section
#####################################

#####################################
#Zapis section
#####################################

@plugin.route('/zapis/')
def zapis():
    zapis_list = my_drundoo.get_list('http://www.drundoo.com/channels/',2)
    items=[]
    for link in zapis_list:
        items.append({'label':link,'path': plugin.url_for('oshte',zapis=zapis_list[link])})
        
    return items

@plugin.route('/oshte/<zapis>')
def oshte(zapis):
    #oshte_list = my_drundoo.get_list('http://www.drundoo.com/channels/97/btv_hd/')
    oshte_list = my_drundoo.get_list(zapis)
    items=[]
    for link in oshte_list:
        items.append({'label':link,'path': plugin.url_for('oshte_stations',oshte=oshte_list[link])})
        
    return items

@plugin.route('/oshte_stations/,<oshte>')
def oshte_stations(oshte):
    
    play_link, play_title = my_drundoo.make_shows(oshte,'list')

    items = []
    for my_title,my_link in zip(play_title,play_link):
        items.append({'label': my_title,'path': my_link, 'is_playable':True})
    return items

#####################################
#End of zapis section
#####################################


#@plugin.route('/live/')
#def live():
#    url = 'http://www.drundoo.com/live/'
#    play_link, play_title = my_drundoo.make_shows(url,'live')
#    items = []
#    for my_title,my_link in zip(play_title,play_link):
#        items.append({'label': my_title,'path': my_link, 'is_playable':True})
#    return items


if __name__ == '__main__':
    plugin.run()
