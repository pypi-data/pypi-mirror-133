"""
Saving GonioAnalysis wide settings and related widget(s).
"""

import tkinter as tk

from tk_steroids.colors import ColorPicker

import gonioanalysis.settings as settings


DEFAULT_SAVEFN = 'gonioanalysis-tkgui-settings.json'

def set(*args, fn=DEFAULT_SAVEFN, **kwargs):
    return settings.set(*args, fn=fn, **kwargs)

def get(*args, fn=DEFAULT_SAVEFN, **kwargs):
    return settings.get(*args, fn=fn, **kwargs)


class PlotSettings(tk.Frame):
    '''
    Plot related settings such as colors, DPIs and so on.
    '''
    
    def __init__(self, tk_parent):
        tk.Frame.__init__(self, tk_parent)
    
        
        

class Settings(tk.Frame):
    '''
    Main settings widget (meant to be opened in a new window).
    '''
    
    def __init__(self, tk_parent):
        tk.Frame.__init__(self, tk_parent)

        # What is needed
        
        # movement measurement
        # - tracking rois
        # - maximum movement
        # - multiprocessing settings
        # - other movemeter settings but not so important

        # plotting colors
        # plot save dpi
        
        # .gonioimsoft folder location
        # default datadir location (always open / use previous / work directory)

