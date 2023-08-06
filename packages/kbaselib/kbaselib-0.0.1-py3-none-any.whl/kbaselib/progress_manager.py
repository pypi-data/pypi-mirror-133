"""
@author: Jebin Jolly Abraham 
Date: 08/01/2022
"""

#Libraries 
import winsound

#Functions 
def complete_sound():
    """
    A function to play a sound when the program is complete.

    Parameters:
        None
    Returns:
        None

    """
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
