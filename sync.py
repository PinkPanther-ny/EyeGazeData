import subprocess

command = 'wsl sh sync.sh'

# Run the command and show all output like running it in CMD
subprocess.run(command, shell=True)
