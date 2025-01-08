import subprocess
import re

# Global variable to hold the default player
player = None

def set_global_player(player_name):
    """
    Set the global player to be used for all actions when a player is not specified.
    :param player_name: The name of the player (string).
    """
    global player
    player = player_name
    print(f"Global player set to: {player}")

def list_players():
    """
    List all active media players.
    :return: List of player names (strings).
    """
    try:
        result = subprocess.run(["playerctl", "-l"], check=True, text=True, capture_output=True)
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error listing players: {e}")
        return []

def list_players_with_grouped_instances():
    """
    List all active media players, including wildcard options for programs with multiple instances.
    :return: List of player names (strings), with wildcard entries for grouped programs.
    """
    try:
        result = subprocess.run(["playerctl", "-l"], check=True, text=True, capture_output=True)
        players = result.stdout.strip().split("\n")

        # Group players by their base names
        grouped_players = {}
        for player in players:
            # Extract the base name before the first separator
            match = re.match(r"([^.:_]+)[.:_]?.*", player)
            if match:
                base_name = match.group(1)
                if base_name not in grouped_players:
                    grouped_players[base_name] = []
                grouped_players[base_name].append(player)

        # Add wildcard entries for programs with multiple instances
        for base_name, instances in grouped_players.items():
            # Only add wildcard if there are multiple instances
            if len(instances) > 1:
                players.append(f"{base_name}.*")


        print("Returning players: ", players)

        return players
    except subprocess.CalledProcessError as e:
        print(f"Error listing players: {e}")
        return []


def button_play(velocity, button_name, player_name=None):
    """
    Play media.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    play(player_name)

def play(player_name=None):
    """
    Play media.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("play", player_name)

def button_pause(velocity, button_name, player_name=None):
    """
    Pause media.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    pause(player_name)

def pause(player_name=None):
    """
    Pause media.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("pause", player_name)

def button_play_pause(velocity, button_name, player_name=None):
    """
    Toggle play/pause.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    play_pause(player_name)

def play_pause(player_name=None):
    """
    Toggle play/pause.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("play-pause", player_name)

def button_stop(velocity, button_name, player_name=None):
    """
    Stop media playback.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    stop(player_name)

def stop(player_name=None):
    """
    Stop media playback.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("stop", player_name)

def button_next_track(velocity, button_name, player_name=None):
    """
    Skip to the next track.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    next_track(player_name)

def next_track(player_name=None):
    """
    Skip to the next track.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("next", player_name)

def button_previous_track(velocity, button_name, player_name=None):
    """
    Go to the previous track.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    previous_track(player_name)

def previous_track(player_name=None):
    """
    Go to the previous track.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command("previous", player_name)

def get_position(player_name=None):
    """
    Get the current playback position.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    :return: Current playback position in milliseconds (int).
    """
    try:
        result = subprocess.run(
            ["playerctl", "position"] + (["--player", player_name or player] if player_name or player else []),
            check=True, text=True, capture_output=True
        )
        return int(float(result.stdout.strip()) * 1000)  # Convert seconds to milliseconds
    except subprocess.CalledProcessError as e:
        print(f"Error getting position: {e}")
        return None

def button_set_position(velocity: int, button_name: str, position: float, player_name=None):
    """
    Set the playback position.
    :param velocity: The velocity of the button press (int).
    :param button_name: The name of the button (string).
    :param position: Position in milliseconds (float).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    set_position(position, player_name)

def set_position(position, player_name=None):
    """
    Set the playback position.
    :param position: Position in milliseconds (int).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command(f"position {position}", player_name)


def knob_seek_position(value, knob_number, player_name=None):
    print(f"Knob: {knob_number}, Value: {value}, Player: {player_name}")
    if value == 1:
        seek_position("1+", player_name)
    elif value == -1:
        seek_position("1-", player_name)

def seek_position(offset, player_name=None):
    """
    Seek to a specific position relative to the current playback time.
    :param offset: Offset in seconds (positive for forward, negative for backward).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    
    _execute_playerctl_command(f"position {offset}", player_name)

def get_volume(player_name=None):
    """
    Get the current playback volume.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    :return: Current volume as a float (0.0 to 1.0).
    """
    try:
        result = subprocess.run(
            ["playerctl", "volume"] + (["--player", player_name or player] if player_name or player else []),
            check=True, text=True, capture_output=True
        )
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error getting volume: {e}")
        return None

def fader_set_volume(volume, fader_number, player_name=None):
    set_volume(volume, player_name)

def set_volume(volume, player_name=None):
    """
    Set the playback volume.
    :param volume: Volume as a float (0.0 to 1.0).
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    _execute_playerctl_command(f"volume {volume}", player_name)

def _execute_playerctl_command(command, player_name=None):
    """
    Helper function to execute playerctl commands.
    :param command: The command to execute.
    :param player_name: (Optional) Specific player to target. If None, uses the global player.
    """
    try:
        if player_name and player_name.endswith(".*"):
            # Handle wildcard by looping over matching players
            base_name = player_name[:-2]  # Remove the ".*" suffix
            players = list_players()
            for p in players:
                if re.match(fr"^{re.escape(base_name)}[.:_]", p):  # Match base name with separators
                    args = ["playerctl", "--player", p] + command.split()
                    subprocess.run(args, check=True)
        else:
            # Normal execution for a specific or global player
            args = ["playerctl"] + (["--player", player_name or player] if player_name or player else []) + command.split()
            subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}' for player '{player_name}': {e}")
        print("Possibly the specific player is not running or does not support the command")
