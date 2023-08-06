import toml
import argparse
import subprocess
import shutil

def wrap_cmd(name, cmd_str):
    return f"\"printf '\\033]2;%s\\033\\\\' '{name}' && {cmd_str} ; read\"" 

def main():

    tmux_path = shutil.which('tmux')
    if not tmux_path:
        raise EnvironmentError("tmux is not installed or not in your PATH")

    parser = argparse.ArgumentParser(description="Deploy a branch for testing")

    parser.add_argument(
        "-c", "--conf",
        type=str,
        help="TOML file containing the command definitions",
    )

    args = parser.parse_args()
    file_content = open(args.conf, 'r').read()
    parsed_toml = toml.loads(file_content)
    cmds = []
    for k, v in parsed_toml.items():
        if 'cmd' not in v:
            continue
        cmds.append(wrap_cmd(k, v['cmd']))

    cmd_parts = ['tmux set -g mouse on \\; bind r respawn-pane \\;  bind k kill-session \\; set -g pane-border-status top ']

    first_command = cmds.pop()
    cmd_parts.append(f"\tnew-session -s \"multirun\" {first_command} ")
    for cmd in cmds:
        cmd_parts.append(f"\tsplit-window {cmd}")
    cmd_parts.append("\tselect-layout even-vertical")

    final = " \\; ".join(cmd_parts)
    print(final)
    subprocess.call(final, shell=True)

if __name__ == '__main__':
    main()
