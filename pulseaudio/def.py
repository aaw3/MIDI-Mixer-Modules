# List of function definitions for the EasyEffects plugin

from modules.base import KnobFunction, FaderFunction, ButtonFunction, DynamicArgs
from modules.pulseaudio.pulseaudio import list_applications, list_application_names, set_application_volume, change_application_volume, change_application_volume_fader, mute_application, toggle_application_mute

export = []


# Toggle Mute Application
toggleMuteApplication = ButtonFunction("Toggle Mute Application", "PulseAudio", toggle_application_mute, None, [DynamicArgs("Application Name", str, "", "The name of the application to mute", None, list_application_names())])
export.append(toggleMuteApplication)

# Application Volume
applicationVolume = FaderFunction("Application Volume", "PulseAudio", False, 50, change_application_volume_fader, [DynamicArgs("Application Name", str, "", "The name of the application to adjust", None, list_application_names())])
export.append(applicationVolume)
