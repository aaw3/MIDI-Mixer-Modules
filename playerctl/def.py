# List of function definitions for the playerctl plugin

from modules.base import KnobFunction, FaderFunction, ButtonFunction, DynamicArgs
from modules.playerctl.playerctl import list_players, list_players_with_grouped_instances,knob_seek_position, button_play, button_pause, button_play_pause, button_next_track, button_previous_track, button_stop, fader_set_volume

export = []


# Play/Pause
togglePlayback = ButtonFunction("Toggle Playback", "Playerctl", button_play_pause, None, [DynamicArgs("Player Name", str, "", "The name of the player to toggle playback", None, list_players_with_grouped_instances)])
export.append(togglePlayback)

# Play
play = ButtonFunction("Play", "Playerctl", button_play, None, [DynamicArgs("Player Name", str, "", "The name of the player to play", None, list_players_with_grouped_instances)])
export.append(play)

# Pause
pause = ButtonFunction("Pause", "Playerctl", button_pause, None, [DynamicArgs("Player Name", str, "", "The name of the player to pause", None, list_players_with_grouped_instances)])
export.append(pause)

# Stop
stop = ButtonFunction("Stop", "Playerctl", button_stop, None, [DynamicArgs("Player Name", str, "", "The name of the player to stop", None, list_players_with_grouped_instances)])
export.append(stop)

# Next Track
nextTrack = ButtonFunction("Next Track", "Playerctl", button_next_track, None, [DynamicArgs("Player Name", str, "", "The name of the player to skip to the next track", None, list_players_with_grouped_instances)])
export.append(nextTrack)

# Previous Track
previousTrack = ButtonFunction("Previous Track", "Playerctl", button_previous_track, None, [DynamicArgs("Player Name", str, "", "The name of the player to go to the previous track", None, list_players_with_grouped_instances)])
export.append(previousTrack)

# Seek Position
seekPosition = KnobFunction("Seek Position", "Playerctl", knob_seek_position, [DynamicArgs("Player Name", str, "", "The name of the player to seek", None, list_players_with_grouped_instances)])
export.append(seekPosition)

# Set Volume
setVolume = FaderFunction("Set Volume - Fader", "Playerctl", False, 10, fader_set_volume, [DynamicArgs("Player Name", str, "", "The name of the player to set the volume", None, list_players_with_grouped_instances)])
export.append(setVolume)