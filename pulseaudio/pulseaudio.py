import pulsectl
import threading

# Global Pulse object
pulse = pulsectl.Pulse('volume-control')
lock = threading.Lock()

def list_applications():
    """List all applications currently outputting audio."""
    apps = []
    for sink_input in pulse.sink_input_list():
        apps.append({
            'id': sink_input.index,
            'name': sink_input.proplist.get('application.name', 'Unknown'),
            'volume': sink_input.volume.values,  # Fetch volume directly
        })
    return apps
    
def list_application_names():
    """List all applications currently outputting audio."""
    apps = []
    for sink_input in pulse.sink_input_list():
        apps.append(sink_input.proplist.get('application.name', 'Unknown'))
    return apps

def set_application_volume(app_name, volume):
    """
    Set the volume for a specific application.
    :param app_name: The name of the application.
    :param volume: Volume level as a fraction (0.0 to 1.0).
    """
    for sink_input in pulse.sink_input_list():
        if sink_input.proplist.get('application.name') == app_name:
            pulse.volume_set_all_chans(sink_input, volume)
            print(f"Set volume for {app_name} to {volume * 100}%")
            return
    print(f"Application '{app_name}' not found.")


def change_application_volume_fader(volume, fader_number, app_name):
    with lock:
        change_application_volume(volume, app_name)

def change_application_volume(volume, app_name):
    """
    Adjust the volume for a specific application by a delta.
    :param app_name: The name of the application.
    :param delta: Positive or negative change in volume (e.g., +0.1 or -0.1).
    """
    global pulse
    for sink_input in pulse.sink_input_list():
        if sink_input.proplist.get('application.name') == app_name:
            pulse.volume_set_all_chans(sink_input, volume)
            print(f"New volume: {volume * 100}% for {app_name}")
            return
    print(f"Application '{app_name}' not found.")

def mute_application(app_name, mute=True):
    """
    Mute or unmute a specific application.
    :param app_name: The name of the application.
    :param mute: True to mute, False to unmute.
    """
    for sink_input in pulse.sink_input_list():
        if sink_input.proplist.get('application.name') == app_name:
            pulse.mute(sink_input, mute)
            print(f"{'Muted' if mute else 'Unmuted'} {app_name}")
            return
    print(f"Application '{app_name}' not found.")

def toggle_application_mute(button_velocity, button_name, app_name):
    """
    Toggle the mute state of a specific application.
    :param app_name: The name of the application.
    """
    for sink_input in pulse.sink_input_list():
        if sink_input.proplist.get('application.name') == app_name:
            pulse.mute(sink_input, not sink_input.mute)
            print(f"{'Muted' if sink_input.mute else 'Unmuted'} {app_name}")
            return
    print(f"Application '{app_name}' not found.")

# Example usage
if __name__ == "__main__":
    print("Applications:", list_applications())