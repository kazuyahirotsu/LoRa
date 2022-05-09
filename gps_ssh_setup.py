import paramiko

command = "df"

# Update the next three lines with your
# server's information

host = "lora-gateway-rpi7067.local"
username = "pi"
password = "nakaolab"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
stdin, stdout,stderr = client.exec_command("echo a")
print(stdout.read().decode())
stdin, stdout,stderr = client.exec_command("echo b")
print(stdout.read().decode())
stdin, stdout,stderr = client.exec_command("python send_test.py")
print(stdout.read().decode())
stdin, stdout,stderr = client.exec_command("python send_gps.py hello2")
print(stdout.read().decode())
stdin.close()
stdout.close()
stderr.close()
client.close()