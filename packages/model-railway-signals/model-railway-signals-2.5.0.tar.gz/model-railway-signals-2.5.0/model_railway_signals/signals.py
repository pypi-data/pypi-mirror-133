# --------------------------------------------------------------------------------
# This module (and its dependent packages)is used for creating and managing signal objects
#
# Currently supported types:
#    Colour Light Signals - 3 or 4 aspect or 2 aspect (home, distant or red/ylw)
#           - with or without a position light subsidary signal
#           - with or without route indication feathers (maximum of 5)
#           - with or without a theatre type route indicator
#           - With or without a "Signal Passed" Button
#           - With or without a "Approach Release" Button
#           - Main signal manual or fully automatic
#    Semaphore Signals - Home or Distant
#           - with or without junction arms (RH1, RH2, LH1, LH2 arms supported)
#           - with or without subsidaries (Main, LH1, LH2, RH1, RH2 arms supported) - Home signals only
#           - with or without a theatre type route indicator (for Home signals only)
#           - With or without a "Signal Passed" Button
#           - With or without a "Approach Release" Button
#           - Main signal manual or fully automatic
#     Ground Position Light Signals
#           - normal groud position light or shunt ahead position light
#           - either early or modern (post 1996) types
#           - With or without a "Signal Passed" Button
#     Ground Disc Signals
#           - normal ground disc (red banner) or shunt ahead ground disc (yellow banner)
#           - With or without a "Signal Passed" Button
#
# signal_sub_type (use when creating colour light signals):
#     signal_sub_type.home         (2 aspect - Red/Green)
#     signal_sub_type.distant      (2 aspect - Yellow/Green
#     signal_sub_type.red_ylw      (2 aspect - Red/Yellow
#     signal_sub_type.three_aspect (3 aspect - Red/Yellow/Green)
#     signal_sub_type.four_aspect  (4 aspect - Red/Yellow/Double-Yellow/Green)
# 
# route_type (use for specifying the route):
#     route_type.NONE   (no route indication - i.e. not used)
#     route_type.MAIN   (main route)
#     route_type.LH1    (immediate left)
#     route_type.LH2    (far left)
#     route_type.RH1    (immediate right)
#     route_type.RH2    (rar right)
# These equate to the route feathers for colour light signals or the Sempahore junction "arm":
#
# signal_state_type(enum.Enum):
#     DANGER               (colour light & semaphore signals)
#     PROCEED              (colour light & semaphore signals)
#     CAUTION              (colour light & semaphore signals)
#     PRELIM_CAUTION       (colour light signals only)
#     CAUTION_APP_CNTL     (colour light signals only - CAUTION but subject to RELEASE ON YELLOW)
#     FLASH_CAUTION        (colour light signals only- when the signal ahead is CAUTION_APP_CNTL)
#     FLASH_PRELIM_CAUTION (colour light signals only- when the signal ahead is FLASH_CAUTION)
#
# sig_callback_type (tells the calling program what has triggered the callback):
#     sig_callback_type.sig_switched (signal has been switched)
#     sig_callback_type.sub_switched (subsidary signal has been switched)
#     sig_callback_type.sig_passed ("signal passed" button activated - or triggered by a Timed signal)
#     sig_callback_type.sig_updated (signal aspect has been updated as part of a timed sequence)
#     sig_callback_type.sig_released (signal "approach release" button has been activated)
#
# create_colour_light_signal - Creates a colour light signal
#   Mandatory Parameters:
#       Canvas - The Tkinter Drawing canvas on which the point is to be displayed
#       sig_id:int - The ID for the signal - also displayed on the signal button
#       x:int, y:int - Position of the signal on the canvas (in pixels) 
#   Optional Parameters:
#       signal_subtype:sig_sub_type - type of signal to create - Default is signal_sub_type.four_aspect
#       orientation:int- Orientation in degrees (0 or 180) - Default is zero
#       sig_callback:name - Function to call when a signal event happens - Default is no callback
#                         Note that the callback function returns (item_id, callback type)
#       sig_passed_button:bool - Creates a "signal Passed" button for automatic control - Default False
#       approach_release_button:bool - Creates an "Approach Release" button - Default False
#       position_light:bool - Creates a subsidary position light signal - Default False
#       lhfeather45:bool - Creates a LH route indication feather at 45 degrees - Default False
#       lhfeather90:bool - Creates a LH route indication feather at 90 degrees - Default False
#       rhfeather45:bool - Creates a RH route indication feather at 45 degrees - Default False
#       rhfeather90:bool - Creates a RH route indication feather at 90 degrees - Default False
#       mainfeather:bool - Creates a MAIN route indication feather - Default False
#       theatre_route_indicator:bool -  Creates a Theatre Type route indicator - Default False
#       refresh_immediately:bool - When set to False the signal aspects will NOT be automaticall updated 
#                 when the signal is changed and the external programme will need to call the seperate 
#                 'update_signal' function use for 3/4 aspect signals - where the displayed aspect will
#                 depend on the signal ahead - Default True 
#       fully_automatic:bool - Creates a signal without any manual controls - Default False
#
# create_semaphore_signal - Creates a Semaphore signal
#   Mandatory Parameters:
#       Canvas - The Tkinter Drawing canvas on which the point is to be displayed
#       sig_id:int - The ID for the signal - also displayed on the signal button
#       x:int, y:int - Position of the signal on the canvas (in pixels) 
#   Optional Parameters:
#       distant:bool - True to create a Distant signal - False to create a Home signal - default False
#       associated_home:bool - Option only valid when creating distant signals - Set to True to associate
#                              the distant signal with a previously created home signal - default False
#                              (this option enables a distant signal to "share" the same post as the
#                               home signal - specify the same x and y coordinates as the home signal) 
#       orientation:int - Orientation in degrees (0 or 180) - Default is zero
#       sig_callback:name - Function to call when a signal event happens - Default is no callback
#                           Note that the callback function returns (item_id, callback type)
#       sig_passed_button:bool - Creates a "signal Passed" button for automatic control - Default False
#       approach_release_button:bool - Option only valid for home signals - Creates an "Approach Release"
#                                      button in front of the signal - Default False
#       main_signal:bool - To create a signal arm for the main route - default True
#                       (Only set this to False for the case of creating a distant signal "associated 
#                        with" a home signal where a distant arm for the main route is not required)
#       lh1_signal:bool - To create a LH1 post with a main (junction) arm - default False
#       lh2_signal:bool - To create a LH2 post with a main (junction) arm - default False
#       rh1_signal:bool - To create a RH1 post with a main (junction) arm - default False
#       rh2_signal:bool - To create a RH2 post with a main (junction) arm - default False
#       main_subsidary:bool - To create a subsidary signal under the "main" signal - default False
#       lh1_subsidary:bool - To create a LH1 post with a subsidary arm - default False
#       lh2_subsidary:bool - To create a LH2 post with a subsidary arm - default False
#       rh1_subsidary:bool - To create a RH1 post with a subsidary arm - default False
#       rh2_subsidary:bool - To create a RH2 post with a subsidary arm - default False
#       theatre_route_indicator:bool -  Creates a Theatre Type route indicator - Default False
#       refresh_immediately:bool - When set to False the signal aspects will NOT be automatically updated 
#                 when the signal is changed and the external programme will need to call the seperate 
#                 'update_signal' function. Primarily intended for use with distant signals - Default True
#       fully_automatic:bool - Creates a signal without any manual controls - Default False
# 
# create_ground_position_signal - create a ground position light signal
#   Mandatory Parameters:
#       Canvas - The Tkinter Drawing canvas on which the point is to be displayed
#       sig_id:int - The ID for the signal - also displayed on the signal button
#       x:int, y:int - Position of the signal on the canvas (in pixels) 
#   Optional Parameters:
#       orientation:int- Orientation in degrees (0 or 180) - Default is zero
#       sig_callback:name - Function to call when a signal event happens - Default is no callback
#                         Note that the callback function returns (item_id, callback type)
#       sig_passed_button:bool - Creates a "signal Passed" button for automatic control - Default False
#       shunt_ahead:bool - Specifies a shunt ahead signal (yellow/white aspect) - default False
#       modern_type: bool - Specifies a modern type ground position signal (post 1996) - Default False
#
# create_ground_disc_signal - Creates a ground disc type shunting signal
#   Mandatory Parameters:
#       Canvas - The Tkinter Drawing canvas on which the point is to be displayed
#       sig_id:int - The ID for the signal - also displayed on the signal button
#       x:int, y:int - Position of the signal on the canvas (in pixels) 
#  Optional Parameters:
#       orientation:int- Orientation in degrees (0 or 180) - Default is zero
#       sig_callback:name - Function to call when a signal event happens - Default is no callback
#                         Note that the callback function returns (item_id, callback type)
#       sig_passed_button:bool - Creates a "signal Passed" button for automatic control - Default False
#       shunt_ahead:bool - Specifies a shunt ahead signal (yellow banner) - default False (red banner)
#
# set_route - Set (and change) the route indication (either feathers or theatre text)
#   Mandatory Parameters:
#       sig_id:int - The ID for the signal
#   Optional Parameters:
#       route:signals_common.route_type - MAIN, LH1, LH2, RH1 or RH2 - default 'NONE'
#       theatre_text:str  - The text to display in the theatre route indicator - default "NONE"
# 
# update_signal - update the signal aspect based on the aspect of a signal ahead - Primarily
#                intended for 3/4 aspect colour light signals but can also be used to update 
#                2-aspect distant signals (semaphore or colour light) on the home signal ahead
#   Mandatory Parameters:
#       sig_id:int - The ID for the signal
#   Optional Parameters:
#       sig_ahead_id:int/str - The ID for the signal "ahead" of the one we want to update.
#               Either an integer representing the ID of the signal created on our schematic,
#               or a string representing the identifier of an signal on an external host/node
#               (subscribed to via the MQTT Interface - refer to the section on MQTT interfacing)
#               Default = "None" (no signal ahead to take into account when updating the signal)
#
# toggle_signal(sig_id) - to support route setting (use 'signal_clear' to find the switched state )
# 
# toggle_subsidary(sig_id) - to support route setting (use 'subsidary_clear' to find the switched state)
# 
# lock_signal(*sig_id) - for point/signal interlocking (multiple Signal_IDs can be specified)
# 
# unlock_signal(*sig_id) - for point/signal interlocking (multiple Signal_IDs can be specified)
# 
# lock_subsidary(*sig_id) - for point/signal interlocking (multiple Signal_IDs can be specified)
# 
# unlock_subsidary(*sig_id) - for point/signal interlocking (multiple Signal_IDs can be specified)
# 
# signal_clear(sig_id) - returns the SWITCHED state of the signal - i.e the state of the signal button
#                        (True='OFF') - use for external point/signal interlocking functions
#
# subsidary_clear(sig_id) - returns the SWITCHED state of the subsidary - i.e the state of the subsidary
#                         button (True='OFF') - use for external point/signal interlocking functions
# 
# signal_state(sig_id) - returns the DISPLAYED state of the signal - This can be different to the SWITCHED
#                        state of the signal if the signal is OVERRIDDEN or subject to APPROACH CONTROL
#                        Use this function when you need to get the actual state (in terms of aspect)
#                        that the signal is displaying - returns 'signal_state_type' (see above)
# 
# set_signal_override (sig_id*) - Overrides the signal to DANGER (can specify multiple sig_ids)
#
# clear_signal_override (sig_id*) - Reverts signal to the non-overridden state (can specify multiple sig_ids)
# 
# signal_overridden (sig_id) - returns the signal override state (True='overridden')
#           Function DEPRECATED (will be removed from future releases) - use signal_state instead
# 
# trigger_timed_signal - Sets the signal to DANGER and then cycles through the aspects back to PROCEED
#                       - If a start delay > 0 is specified then a 'sig_passed' callback event is generated
#                       - when the signal is changed to DANGER - For each subsequent aspect change (all the
#                       - way back to PROCEED) a 'sig_updated' callback event will be generated
#   Mandatory Parameters:
#       sig_id:int - The ID for the signal
#   Optional Parameters:
#       start_delay:int - Delay (in seconds) before changing to DANGER (default=5)
#       time_delay:int - Delay (in seconds) for cycling through the aspects (default=5)
# 
# set_approach_control - Used when a diverging route has a lower speed restriction to the main line
#                        Puts the signal into "Approach Control" Mode where the signal will display a more 
#                        restrictive aspect/state (either DANGER or CAUTION) to approaching trains. As the
#                        Train approaches, the signal will then be "released" to display its "normal" aspect.
#                        When a signal is in "approach control" mode the signals behind will display the 
#                        appropriate aspects (when updated based on the signal ahead). These would be the
#                        normal aspects for "Release on Red" but for "Release on Yellow", the signals behind  
#                        would display flashing yellow and flashing double yellow (assuming 4 aspect signals)
#   Mandatory Parameters:
#       sig_id:int - The ID for the signal
#   Optional Parameters:
#       release_on_yellow:Bool - True = Yellow Approach aspect, False = Red Approach aspect (default=False)
# 
# clear_approach_control - This "releases" the signal to display the normal aspect and should be called when
#                          a train is approaching the signal. Note that signals can also be released when the
#                         "release button" (displayed just in front of the signal if specified when the signal
#                          was created) is activated - manually or via an external sensor event#   Mandatory Parameters:
#       sig_id:int - The ID for the signal
# 
# approach_control_set (sig_id) - returns if the signal is subject to approach control (True='active')
#           Function DEPRECATED (will be removed from future releases) - use signal_state instead
#
# -------------------------------------------------------------------------
   
from . import signals_common
from . import signals_colour_lights
from . import signals_ground_position
from . import signals_ground_disc
from . import signals_semaphores

from typing import Union
from tkinter import *
import logging

# -------------------------------------------------------------------------
# Externally called function to Return the current SWITCHED state of the signal
# (i.e. the state of the signal button - Used to enable interlocking functions)
# Note that the DISPLAYED state of the signal may not be CLEAR if the signal is
# overridden or subject to release on RED - See "signal_displaying_clear"
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def signal_clear (sig_id:int):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": signal_clear - Signal does not exist")
        sig_clear = False
    else:
        sig_clear = signals_common.signals[str(sig_id)]["sigclear"]
    return (sig_clear)

# -------------------------------------------------------------------------
# Externally called function to Return the displayed state of the signal
# (i.e. whether the signal is actually displaying a CLEAR aspect). Note that
# this can be different to the state the signal has been manually set to (via
# the signal button) - as it could be overridden or subject to Release on Red
# Function applicable to ALL signal types - Including REMOTE SIGNALS
# -------------------------------------------------------------------------

def signal_state (sig_id:Union[int,str]):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": signal_state - Signal does not exist")
        sig_state = signals_common.signal_state_type.DANGER
    else:
        sig_state = signals_common.signals[str(sig_id)]["sigstate"]
    return (sig_state)

# -------------------------------------------------------------------------
# ##### DEPRECATED ##### DEPRECATED ##### DEPRECATED ##### DEPRECATED #####
# Externally called function to Return the current state of the signal overide
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def signal_overridden (sig_id:int):
    global logging
    # Validate the signal exists
    logging.warning ("Signal "+str(sig_id)+": signal_overridden - This function is DEPRECATED")
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": signal_overridden - Signal does not exist")
        sig_overridden = False
    else:
        sig_overridden = signals_common.signals[str(sig_id)]["override"]
    return (sig_overridden)

# -------------------------------------------------------------------------
# ##### DEPRECATED ##### DEPRECATED ##### DEPRECATED ##### DEPRECATED #####
# Externally called function to Return the current state of the approach control
# Function applicable to ALL signal types created on the local schematic
# (will return False if the particular signal type not supported)
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def approach_control_set (sig_id:int):
    global logging
    logging.warning ("Signal "+str(sig_id)+": approach_control_set - This function is DEPRECATED")
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": approach_control_set - Signal does not exist")
        approach_control_active = False
    # get the signal state to return - only supported for semaphores and colour_lights
    elif (signals_common.signals[str(sig_id)]["sigtype"] in
          (signals_common.sig_type.colour_light, signals_common.sig_type.semaphore)):
        approach_control_active = (signals_common.signals[str(sig_id)]["releaseonred"]
                               or signals_common.signals[str(sig_id)]["releaseonyel"])
    else:
        approach_control_active = False
    return (approach_control_active)

# -------------------------------------------------------------------------
# Externally called function to Return the current state of the subsidary
# signal - if the signal does not have one then the return will be FALSE
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def subsidary_clear (sig_id:int):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": subsidary_clear - Signal does not exist")
        sig_clear = False
    elif not signals_common.signals[str(sig_id)]["hassubsidary"]:
        logging.error ("Signal "+str(sig_id)+": subsidary_clear - Signal does not have a subsidary")
        sig_clear = False
    else:
        sig_clear = signals_common.signals[str(sig_id)]["subclear"]
    return (sig_clear)

# -------------------------------------------------------------------------
# Externally called function to Lock the signal (preventing it being cleared)
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def lock_signal (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": lock_signal - Signal does not exist")
        else:
            signals_common.lock_signal(sig_id)
    return()

# -------------------------------------------------------------------------
# Externally called function to Unlock the main signal
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def unlock_signal (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": unlock_signal - Signal does not exist")
        else:
            signals_common.unlock_signal(sig_id)
    return() 

# -------------------------------------------------------------------------
# Externally called function to Lock the subsidary signal
# This is effectively a seperate signal from the main aspect
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# (will report an error if the specified signal does not have a subsidary)
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def lock_subsidary (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": lock_subsidary - Signal does not exist")
        elif not signals_common.signals[str(sig_id)]["hassubsidary"]:
            logging.error ("Signal "+str(sig_id)+": lock_subsidary - Signal does not have a subsidary")
        else:
            signals_common.lock_subsidary(sig_id)
    return()

# -------------------------------------------------------------------------
# Externally called function to Unlock the subsidary signal
# This is effectively a seperate signal from the main aspect
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# (will report an error if the specified signal does not have a subsidary)
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def unlock_subsidary (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": unlock_subsidary - Signal does not exist")
        elif not signals_common.signals[str(sig_id)]["hassubsidary"]:
            logging.error ("Signal "+str(sig_id)+": unlock_subsidary - Signal does not have a subsidary")
        else:
            signals_common.unlock_subsidary(sig_id)
    return()

# -------------------------------------------------------------------------
# Externally called function to Override a signal - effectively setting it
# to RED (apart from 2 aspect distance signals - which are set to YELLOW)
# Signal will display the overriden aspect no matter what its current setting is
# Used to support automation - e.g. set a signal to Danger once a train has passed
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def set_signal_override (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": set_signal_override - Signal does not exist")
        else:
            # Set the override and refresh the signal following the change in state
            signals_common.set_signal_override(sig_id)
            signals_common.auto_refresh_signal(sig_id)
        return()

# -------------------------------------------------------------------------
# Externally called function to Clear a Signal Override 
# Signal will revert to its current manual setting (on/off) and aspect
# Multiple signal IDs can be specified in the call
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def clear_signal_override (*sig_ids:int):
    global logging
    for sig_id in sig_ids:
        # Validate the signal exists
        if not signals_common.sig_exists(sig_id):
            logging.error ("Signal "+str(sig_id)+": clear_signal_override - Signal does not exist")
        else:
            # Clear the override and refresh the signal following the change in state
            signals_common.clear_signal_override(sig_id)
            signals_common.auto_refresh_signal(sig_id)
    return() 

# -------------------------------------------------------------------------
# Externally called function to Toggle the state of a main signal
# to enable automated route setting from the external programme.
# Use in conjunction with 'signal_clear' to find the state first
# Function applicable to ALL signal types created on the local schematic
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def toggle_signal (sig_id:int):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": toggle_signal - Signal does not exist")
    else:
        if signals_common.signals[str(sig_id)]["siglocked"]:
            logging.warning ("Signal "+str(sig_id)+": toggle_signal - Signal is locked - Toggling anyway")
        # Toggle the signal and refresh the signal following the change in state
        signals_common.toggle_signal(sig_id)
        signals_common.auto_refresh_signal(sig_id)
    return()

# -------------------------------------------------------------------------
# Externally called function to Toggle the state of a subsidary signal
# to enable automated route setting from the external programme. Use
# in conjunction with 'subsidary_signal_clear' to find the state first
# Function applicable to ALL signal types created on the local schematic
# (will report an error if the specified signal does not have a subsidary)
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def toggle_subsidary (sig_id:int):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": toggle_subsidary - Signal does not exist")
    elif not signals_common.signals[str(sig_id)]["hassubsidary"]:
        logging.error ("Signal "+str(sig_id)+": toggle_subsidary - Signal does not have a subsidary")
    else:
        if signals_common.signals[str(sig_id)]["sublocked"]:
            logging.warning ("Signal "+str(sig_id)+": toggle_subsidary - Subsidary signal is locked - Toggling anyway")
        # Toggle the subsidary and refresh the signal following the change in state
        signals_common.toggle_subsidary(sig_id)
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            signals_colour_lights.update_colour_light_subsidary(sig_id)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            signals_semaphores.update_semaphore_subsidary_arms(sig_id)
        else:
            logging.error ("Signal "+str(sig_id)+": toggle_subsidary - Function not supported by signal type")
    return()

# -------------------------------------------------------------------------
# Externally called function to set the "approach conrol" for the signal
# Calls the signal type-specific functions depending on the signal type
# Function applicable to Colour Light and Semaphore signal types created on
# the local schematic (will report an error if the particular signal type not
# supported) Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def set_approach_control (sig_id:int, release_on_yellow:bool = False):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": set_approach_control - Signal does not exist")
    else:
        # call the signal type-specific functions to update the signal (note that we only update
        # Semaphore and colour light signals if they are configured to update immediately)
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            # do some additional validation specific to this function for colour light signals
            if signals_common.signals[str(sig_id)]["subtype"]==signals_colour_lights.signal_sub_type.distant:
                logging.error("Signal "+str(sig_id)+": Can't set approach control for a 2 aspect distant signal")
            elif release_on_yellow and signals_common.signals[str(sig_id)]["subtype"]==signals_colour_lights.signal_sub_type.home:
                logging.error("Signal "+str(sig_id)+": Can't set \'release on yellow\' approach control for a 2 aspect home signal")
            elif release_on_yellow and signals_common.signals[str(sig_id)]["subtype"]==signals_colour_lights.signal_sub_type.red_ylw:
                logging.error("Signal "+str(sig_id)+": Can't set \'release on yellow\' approach control for a 2 aspect red/yellow signal")
            else:
                # Set approach control and refresh the signal following the change in state
                signals_common.set_approach_control(sig_id,release_on_yellow)            
                signals_common.auto_refresh_signal(sig_id)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            # Do some additional validation specific to this function for semaphore signals
            if signals_common.signals[str(sig_id)]["distant"]:
                logging.error("Signal "+str(sig_id)+": Can't set approach control for semaphore distant signals")
            elif release_on_yellow:
                logging.error("Signal "+str(sig_id)+": Can't set \'release on yellow\' approach control for home signals")
            else:
                # Set approach control and refresh the signal following the change in state
                signals_common.set_approach_control(sig_id)
                signals_common.auto_refresh_signal(sig_id)
        else:
            logging.error ("Signal "+str(sig_id)+": set_approach_control - Function not supported by signal type")
    return()

# -------------------------------------------------------------------------
# Externally called function to clear the "approach control" for the signal
# Calls the signal type-specific functions depending on the signal type
# Function applicable to Colour Light and Semaphore signal types created on
# the local schematic (will have no effect on other signal types
# Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def clear_approach_control (sig_id:int):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": clear_approach_control - Signal does not exist")  
    else:
        # call the signal type-specific functions to update the signal (note that we only update
        # Semaphore and colour light signals if they are configured to update immediately)
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            # Clear approach control and refresh the signal following the change in state
            signals_common.clear_approach_control (sig_id)
            signals_common.auto_refresh_signal(sig_id)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            # Clear approach control and refresh the signal following the change in state
            signals_common.clear_approach_control (sig_id)
            signals_common.auto_refresh_signal(sig_id)
        else:
            logging.error ("Signal "+str(sig_id)+": clear_approach_control - Function not supported by signal type")
    return()

# -------------------------------------------------------------------------
# Externally called Function to update a signal according the state of the
# Signal ahead - Intended mainly for Coulour Light Signal types so we can
# ensure the "CLEAR" aspect reflects the aspect of ths signal ahead
# Calls the signal type-specific functions depending on the signal type
# Function applicable only to Main colour Light and semaphore signal types
# created on the local schematic - but either locally-created or REMOTE
# Signals can be specified as the signal ahead
# -------------------------------------------------------------------------

def update_signal (sig_id:int, sig_ahead_id:Union[int,str]=None):
    global logging
    # Validate the signal exists (and the one ahead if specified)
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": update_signal - Signal does not exist")
    elif sig_ahead_id != None and not signals_common.sig_exists(sig_ahead_id): 
        logging.error ("Signal "+str(sig_id)+": update_signal - Signal ahead "+str(sig_ahead_id)+" does not exist")
    elif sig_id == sig_ahead_id: 
        logging.error ("Signal "+str(sig_id)+": update_signal - Signal ahead "+str(sig_ahead_id)+" is the same ID")
    else:
        # call the signal type-specific functions to update the signal
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            signals_colour_lights.update_colour_light_signal (sig_id,sig_ahead_id)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            signals_semaphores.update_semaphore_signal (sig_id,sig_ahead_id)
        else:
            logging.error ("Signal "+str(sig_id)+": update_signal - Function not supported by signal type")
    return()

# -------------------------------------------------------------------------
# Externally called function to set the route indication for the signal
# Calls the signal type-specific functions depending on the signal type
# Function only applicable to Main Colour Light and Semaphore signal types
# created on the local schematic (will raise an error if signal type not
# supported. Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def set_route (sig_id:int, route:signals_common.route_type = None, theatre_text:str = None):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": set_route - Signal does not exist")
    else:
        # call the signal type-specific functions to update the signal
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            signals_colour_lights.update_feather_route_indication (sig_id,route)
            signals_common.update_theatre_route_indication(sig_id,theatre_text)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            signals_semaphores.update_semaphore_route_indication (sig_id,route)
            signals_common.update_theatre_route_indication(sig_id,theatre_text)
        else:
            logging.error ("Signal "+str(sig_id)+": set_route - Function not supported by signal type")
    return()

# -------------------------------------------------------------------------
# Externally called Function to 'override' a signal (changing it to 'ON') after
# a specified time delay and then clearing the override the signal after another
# specified time delay. In the case of colour light signals, this will cause the
# signal to cycle through the supported aspects all the way back to GREEN. When
# the Override is cleared, the signal will revert to its previously displayed aspect
# This is to support the automation of 'exit' signals on a layout
# A 'sig_passed' callback event will be generated when the signal is overriden if
# and only if a start delay (> 0) is specified. For each subsequent aspect change
# a'sig_updated' callback event will be generated
# Function only applicable to Main Colour Light and Semaphore signal types
# created on the local schematic (will raise an error if signal type not
# supported. Function does not support REMOTE Signals (with a compound Sig-ID)
# -------------------------------------------------------------------------

def trigger_timed_signal (sig_id:int,start_delay:int=0,time_delay:int=5):
    global logging
    # Validate the signal exists
    if not signals_common.sig_exists(sig_id):
        logging.error ("Signal "+str(sig_id)+": trigger_timed_signal - Signal does not exist")
    elif signals_common.signals[str(sig_id)]["override"]:
        logging.error ("Signal "+str(sig_id)+": trigger_timed_signal - Signal is already overriden - not triggering")
    else:
        # call the signal type-specific functions to update the signal
        if signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.colour_light:
            logging.info ("Signal "+str(sig_id)+": Triggering Timed Signal")
            signals_colour_lights.trigger_timed_colour_light_signal (sig_id,start_delay,time_delay)
        elif signals_common.signals[str(sig_id)]["sigtype"] == signals_common.sig_type.semaphore:
            logging.info ("Signal "+str(sig_id)+": Triggering Timed Signal")
            signals_semaphores.trigger_timed_semaphore_signal (sig_id,start_delay,time_delay)
        else:
            logging.error ("Signal "+str(sig_id)+": trigger_timed_signal - Function not supported by signal type")
    return()

##########################################################################################
