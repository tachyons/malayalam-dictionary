# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 <Aboobacker mk> <aboobackervyd@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('ml-dict')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('ml_dict')

from ml_dict_lib import Window
from ml_dict.AboutMlDictDialog import AboutMlDictDialog
from ml_dict.PreferencesMlDictDialog import PreferencesMlDictDialog

# See ml_dict_lib.Window.py for more details about how this class works
class MlDictWindow(Window):
    __gtype_name__ = "MlDictWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(MlDictWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutMlDictDialog
        self.PreferencesDialog = PreferencesMlDictDialog
        
        # Code for other initialization actions should be added here.
        self.toolbar=self.builder.get_object("toolbar1")
        context=self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.notebook=self.builder.get_object("notebook")
        # Hide the notebook tabs
        self.ui.notebook.set_show_tabs(False)
        #h
        self.word_entry = builder.get_object("entry")
        
		self.textbuffer = builder.get_object("textbuffer1")
		#Compleation
		self.completion = Gtk.EntryCompletion()
		self.word_entry.set_completion(self.completion)
		self.liststore = Gtk.ListStore(str)
		self.completion.set_model(self.liststore)
		self.completion.set_text_column(0)
		self.completion.connect("match-selected",self.match_cb)
		self.completion.set_inline_selection(True)
		#
		self.word = {}
		iter = 0
		#/home/tachyons/quickly-projects/ml-dict_0.1_all/usr/share/ml-dict/data.dat
		#for line in open("/home/tachyons/quickly-projects/ml-dict/data/data.dat",'r'):
		for line in open("/usr/share/ml-dict/data.dat",'r'):
			if line[0] != "|": #if english
				iter = 0
				key = line.split("|")[0]
				self.liststore.append([key])
			else:
				if iter == 0:
					self.word[key] = [line.split("|")[1]]
					iter += 1
				else:
					self.word[key].append(line.split("|")[1])
					iter += 1
			
    def on_update_clicked(self,widget):
        self.notebook.set_current_page(1)
        return
        
    def on_home_clicked(self,widget):
        self.notebook.set_current_page(0)
        return
    def on_about_clicked(self,widget):
        self.notebook.set_current_page(2)
        return
        
    def on_entry_activate(self,widget,data=None,pipe=None):
        if pipe == None:
			quiry = self.word_entry.get_text()
		else:
			quiry = pipe
		try:
			str = "Meaning of %s is " % quiry
			temp_str = ""
			for meaning in self.word[quiry]:
				temp_str += meaning
				str+="#";
				str += meaning
				str += ","			
		except KeyError:
			self.textbuffer.set_text("താങ്കള്‍ അന്വേഷിച്ച വാക്ക് ഈ നിഘണ്ടുവിലില്ല")
		else:
			pass
			self.textbuffer.set_text(temp_str)
        
    def match_cb(self, completion, model,iter):
        word = model[iter][0].lower()
        #self.on_update_clicked(self,None,word)
   
