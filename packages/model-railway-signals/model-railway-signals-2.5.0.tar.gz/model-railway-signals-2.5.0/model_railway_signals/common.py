# -------------------------------------------------------------------------
# This module contains all of the parameters, funcions and classes that 
# are used across multiple modules in the model_railway_signalling package
# -------------------------------------------------------------------------

import math
import queue
import logging
from . import mqtt_interface
from . import file_interface

#-------------------------------------------------------------------------
# Function to catch the root window close event so we can perform an
# orderly shutdown of the other threads running in the application
#-------------------------------------------------------------------------

def on_closing():
    global root_window
    if file_interface.save_state_and_quit():
        mqtt_interface.mqtt_shutdown()
        root_window.destroy()
    return()

#-------------------------------------------------------------------------
# Function to find and store the tkinter "root" window as this is used to
# schedule callback events in the main tkinter event loop using the 'after' 
# method and also for feeding custom callback functions into the main tkinter
# thread. We do this as all the information out there on the internet concludes
# tkinter isn't fully thread safe and so all manipulation of tkinter drawing
# objects should be done from within the main tkinter thread.
#-------------------------------------------------------------------------

root_window = None
event_queue = queue.Queue()

def find_root_window (canvas):
    global root_window
    parent = canvas.master
    while parent.master:
        # if this is a subsidary window, we still want to bind the window
        # close event to kill the application when the window is closed
        try: parent.protocol("WM_DELETE_WINDOW",on_closing)
        except: pass
        parent = parent.master
    root_window = parent
    # bind the tkinter event for handling events raised in external threads
    root_window.bind("<<ExtCallback>>", handle_callback_in_tkinter_thread)
    # Bind the window close event so we can perform an orderly shutdown
    root_window.protocol("WM_DELETE_WINDOW",on_closing)
    return(root_window)

#-------------------------------------------------------------------------
# Functions to allow custom callback functions to be passed in (from an external
# thread) and then handled in the main Tkinter thread (to keep everything threadsafe).
# We use the tkinter event_generate method to generate a custom event in the main
# tkinter event loop in conjunction with a (threadsafe) queue to pass the callback function
# Use as follows: execute_function_in_tkinter_thread (lambda: my_function(arg1,arg2...))
#-------------------------------------------------------------------------

def handle_callback_in_tkinter_thread(*args):
    try:
       callback = event_queue.get(False)
    except event_queue.Empty:
        return()
    callback()
    return()
    
def execute_function_in_tkinter_thread(callback_function):
    callback = event_queue.put(callback_function)
    if root_window is not None:
        root_window.event_generate("<<ExtCallback>>", when="tail")
    else:
        logging.error ("execute_function_in_tkinter_thread - cannot execute callback function as root window is undefined")
    return()

# -------------------------------------------------------------------------
# Global variables for how the signals/points/sections buttons appear
# on the screen. This is to allow the appearance to be optimised for
# particular window sizes/screen resolutions.
# -------------------------------------------------------------------------

fontsize = 9  # Used by the Signals, Points and sections modules
xpadding = 4  # Used by the Signals, Points and sections modules
ypadding = 3  # Used by the Signals, Points and sections modules
bgraised = "grey85"   # Used by the Signals and Points modules
bgsunken = "white"    # Used by the Signals and Points modules

# -------------------------------------------------------------------------
# Common functions to rotate offset coordinates around an origin
# The angle should be passed into these functions in degrees.
# -------------------------------------------------------------------------

def rotate_point(ox,oy,px,py,angle):
    angle = math.radians(angle)
    qx = ox + math.cos(angle) * (px) - math.sin(angle) * (py)
    qy = oy + math.sin(angle) * (px) + math.cos(angle) * (py)
    return (qx,qy)

def rotate_line(ox,oy,px1,py1,px2,py2,angle):
    start_point = rotate_point(ox,oy,px1,py1,angle)
    end_point = rotate_point(ox,oy,px2,py2,angle)
    return (start_point, end_point)

##################################################################################################

