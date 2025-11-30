#!/usr/bin/env python3
"""
Simple SSH Honeypot using Paramiko
Logs all authentication attempts and commands
"""

import socket
import sys
import threading
import paramiko
import json
import logging
from datetime import datetime
import os

# Configure logging
LOG_DIR = '/app/logs'
os.makedirs(LOG_DIR, exist_ok=True)

# JSON logger
json_handler = logging.FileHandler(f'{LOG_DIR}/ssh_honeypot.json')
json_handler.setLevel(logging.INFO)

# Console logger
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[json_handler, console_handler]
)

logger = logging.getLogger(__name__)

HOST_KEY = paramiko.RSAKey(filename='/app/ssh_host_rsa_key')
SSH_PORT = 222

class SSHServerHandler(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'login_attempt',
            'src_ip': self.client_ip,
            'username': username,
            'password': password,
            'auth_method': 'password'
        }
        logger.info(json.dumps(log_entry))
        # Always reject but log the attempt
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'login_attempt',
            'src_ip': self.client_ip,
            'username': username,
            'key_type': key.get_name(),
            'key_fingerprint': key.get_fingerprint().hex(),
            'auth_method': 'publickey'
        }
        logger.info(json.dumps(log_entry))
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def handle_connection(client, addr):
    client_ip = addr[0]
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': 'connection',
        'src_ip': client_ip,
        'src_port': addr[1]
    }
    logger.info(json.dumps(log_entry))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        transport.set_subsystem_handler('sftp', paramiko.SFTPServer)

        server = SSHServerHandler(client_ip)
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            return

        server.event.wait(10)
        if not server.event.is_set():
            return

        channel.send(b'Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-42-generic x86_64)\r\n\r\n$ ')

        # Simple command loop
        command = b''
        while True:
            char = channel.recv(1)
            if not char:
                break

            if char == b'\r' or char == b'\n':
                cmd = command.decode('utf-8', errors='ignore').strip()
                if cmd:
                    log_entry = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'event_type': 'command',
                        'src_ip': client_ip,
                        'command': cmd
                    }
                    logger.info(json.dumps(log_entry))

                    # Fake command responses
                    if cmd == 'ls':
                        channel.send(b'\r\nDesktop  Documents  Downloads  Pictures\r\n')
                    elif cmd.startswith('cat'):
                        channel.send(b'\r\nPermission denied\r\n')
                    elif cmd == 'whoami':
                        channel.send(b'\r\nroot\r\n')
                    elif cmd == 'pwd':
                        channel.send(b'\r\n/root\r\n')
                    elif cmd == 'exit':
                        channel.send(b'\r\nlogout\r\n')
                        break
                    else:
                        channel.send(b'\r\ncommand not found\r\n')

                channel.send(b'$ ')
                command = b''
            else:
                command += char

    except Exception as e:
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'error',
            'src_ip': client_ip,
            'error': str(e)
        }
        logger.info(json.dumps(log_entry))
    finally:
        try:
            transport.close()
        except:
            pass
        client.close()

def main():
    print(f'[*] SSH Honeypot starting on port {SSH_PORT}...')

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', SSH_PORT))
        server_socket.listen(100)

        print(f'[*] Listening for connections on 0.0.0.0:{SSH_PORT}...')

        while True:
            client, addr = server_socket.accept()
            print(f'[*] Connection from {addr[0]}:{addr[1]}')

            thread = threading.Thread(target=handle_connection, args=(client, addr))
            thread.daemon = True
            thread.start()

    except Exception as e:
        print(f'[!] Error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
