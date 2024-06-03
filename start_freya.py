import subprocess

# Start the first script
server = subprocess.Popen(['python', 'start_server.py'])

# Start the second script
client = subprocess.Popen(['python', 'start_client.py'])

# Wait for both scripts to finish
server.wait()
client.wait()
