import subprocess
import time
import logging
import platform
import os
import shutil
from logging_config import setup_logger

logger = setup_logger('TorManager')

class TorManager:
    """Manages Tor connections for anonymity - Cross-platform (Windows/Linux/macOS)"""
    
    def __init__(self):
        self.logger = setup_logger('TorManager')
        self.last_identity_change = time.time()
        self.min_identity_change_interval = 30
        self.is_windows = platform.system() == 'Windows'
        self.tor_executable = self._find_tor_executable()
    
    def _find_tor_executable(self) -> str:
        """Find Tor executable path"""
        if self.is_windows:
            common_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Tor', 'tor.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Tor', 'tor.exe'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', 'Tor', 'tor.exe'),
                'tor.exe',
            ]
            for path in common_paths:
                if os.path.isfile(path):
                    return path
            return 'tor.exe'
        else:
            tor_path = shutil.which('tor')
            return tor_path if tor_path else 'tor'

    def _run_command(self, command: str) -> bool:
        """Execute system command safely"""
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def change_identity(self):
        """Change Tor circuit identity"""
        current_time = time.time()
        if current_time - self.last_identity_change < self.min_identity_change_interval:
            return False

        if self.is_windows:
            # On Windows, restart Tor process
            self.stop_tor()
            time.sleep(2)
            self.start_tor()
        else:
            if self._run_command("killall -HUP tor"):
                time.sleep(3)
        
        self.last_identity_change = current_time
        return True

    def change_identity_via_control_port(self, password: str):
        """Change identity using Tor control port"""
        current_time = time.time()
        if current_time - self.last_identity_change < self.min_identity_change_interval:
            return False

        try:
            from stem.control import Controller
            from stem import Signal
            with Controller.from_port(port=9051) as controller:
                controller.authenticate(password=password)
                controller.signal(Signal.NEWNYM)
                self.last_identity_change = current_time
                return True
        except ImportError:
            self.logger.warning("stem library not installed, falling back to process restart")
            return self.change_identity()
        except Exception as e:
            self.logger.error(f"Failed to change identity via control port: {e}")
            return self.change_identity()

    def ensure_tor_running(self):
        """Ensure Tor service is running"""
        if self.is_windows:
            # On Windows, check if tor process exists
            result = subprocess.run('tasklist /FI "IMAGENAME eq tor.exe"', 
                                   shell=True, capture_output=True, text=True)
            if 'tor.exe' not in result.stdout:
                self.start_tor()
                time.sleep(5)
        else:
            if not self._run_command("pgrep tor"):
                self.start_tor()
                time.sleep(5)
        
        if not self.check_tor_status():
            self.restart_tor()
            time.sleep(5)
        return self.check_tor_status()

    def check_tor_status(self):
        """Verify Tor connection is working"""
        try:
            import requests
            proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            response = requests.get('https://check.torproject.org/', proxies=proxies, timeout=10)
            return 'Congratulations' in response.text
        except Exception:
            # Fallback to curl
            if self.is_windows:
                command = "curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/"
            else:
                command = "curl --socks5-hostname localhost:9050 https://check.torproject.org/"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return 'Congratulations' in result.stdout if result.returncode == 0 else False

    def stop_tor(self):
        """Stop Tor service"""
        if self.is_windows:
            subprocess.run('taskkill /F /IM tor.exe', shell=True, capture_output=True)
        else:
            self._run_command("sudo systemctl stop tor 2>/dev/null || pkill tor")

    def start_tor(self):
        """Start Tor service"""
        if self.is_windows:
            try:
                subprocess.Popen(
                    [self.tor_executable],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                )
            except FileNotFoundError:
                self.logger.error("Tor executable not found. Please install Tor Browser.")
        else:
            self._run_command("sudo systemctl start tor 2>/dev/null || tor --daemon")

    def restart_tor(self):
        """Restart Tor service"""
        self.stop_tor()
        time.sleep(2)
        self.start_tor()

    def configure_tor(self):
        """Configure Tor with control port authentication"""
        password = input("Enter control password for Tor: ")
        
        if self.is_windows:
            self.logger.info("On Windows, configure Tor via the Tor Browser settings.")
            self.logger.info("Add the following to your torrc file:")
            self.logger.info(f"  HashedControlPassword (run: tor --hash-password '{password}')")
            self.logger.info("  ControlPort 9051")
        else:
            hashed_password_command = f"tor --hash-password '{password}' > hashed_password.txt"
            self._run_command(hashed_password_command)
            self.logger.info("Please manually add the following to /etc/tor/torrc:")
            self.logger.info(f"  HashedControlPassword (see hashed_password.txt)")
            self.logger.info("  ControlPort 9051")

    def restart_tor_if_needed(self):
        """Restart Tor if not functioning properly"""
        if not self.check_tor_status():
            self.restart_tor()
        else:
            pass

if __name__ == "__main__":
    tor_manager = TorManager()
    
    tor_manager.stop_tor()
    tor_manager.configure_tor()
    tor_manager.start_tor()
    tor_manager.change_identity()
    tor_manager.check_tor_status()
    tor_manager.restart_tor_if_needed()