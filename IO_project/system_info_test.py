import subprocess
import os
import csv
import json
import re
import platform
from datetime import datetime
from app_paths import get_app_folder

IS_WINDOWS = platform.system() == 'Windows'

def _run_powershell_json(command): #執行PowerShell指令並把JSON輸出轉成Python物件，失敗回傳None
    result = subprocess.run(
        ['powershell', '-Command', command],
        capture_output=True,
        text=True,
        encoding='big5', #跟專案其他模組一致，正確解碼中文字
        errors='replace' #遇到無法解碼的位元組不要讓讀取執行緒崩潰
    )
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, TypeError):
        return None

def _run_shell(command): #跑一個shell指令，回傳stdout文字，失敗回傳空字串
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except (OSError, subprocess.SubprocessError):
        return ''

def _read_dmi(field): #讀取Linux /sys/class/dmi/id/下的硬體識別資訊，讀不到就回傳Unknown
    try:
        with open(f'/sys/class/dmi/id/{field}', encoding='utf-8') as f:
            value = f.read().strip()
            return value if value else 'Unknown'
    except (OSError, PermissionError):
        return 'Unknown'

def _collect_windows_info(): #用PowerShell/CIM撈Windows的硬體資訊
  computer_system = _run_powershell_json(
      'Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer,Model,TotalPhysicalMemory | ConvertTo-Json'
  ) or {}
  
  ram = _run_powershell_json(
    'Get-CimInstance Win32_PhysicalMemory | Select-Object Manufacturer,PartNumber,Capacity,Speed | ConvertTo-Json'
) or []
  if isinstance(ram, dict):
    ram = [ram]
    
 
  ram_details = [] #用來存每條 RAM 的詳細資訊
  for item in ram:#逐條讀取 RAM 資料。
    manufacturer = item.get('Manufacturer', 'Unknown')
    model = item.get('PartNumber', 'Unknown')
    capacity = item.get('Capacity', 0)
    capacity_gb = round(capacity / (1024 ** 3))
    speed = item.get('Speed', 0)
    ram_details.append(
        f'{manufacturer} {model} {capacity_gb}GB {speed}MHz'
    )
  ram_summary = '\n '.join(ram_details)#把每條 RAM 的詳細資訊組成一個字串,


  bios = _run_powershell_json(
      'Get-CimInstance Win32_BIOS | Select-Object SerialNumber,SMBIOSBIOSVersion | ConvertTo-Json'
  ) or {}

  cpu = _run_powershell_json(
      'Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors | ConvertTo-Json'
  ) or {}
  if isinstance(cpu, list): #多顆實體CPU時PowerShell會回傳陣列，取第一顆代表這台機器
    cpu = cpu[0] if cpu else {}

  os_info = _run_powershell_json(
      'Get-CimInstance Win32_OperatingSystem | Select-Object Caption,OSArchitecture | ConvertTo-Json'
  ) or {}

  disks = _run_powershell_json(
      'Get-PhysicalDisk | Select-Object FriendlyName,MediaType,Size,HealthStatus | ConvertTo-Json'
  ) or []
  if isinstance(disks, dict): #只有一顆硬碟時PowerShell會回傳單一物件而非陣列
    disks = [disks]

  gpu = _run_powershell_json(
      'Get-CimInstance Win32_VideoController | Select-Object Name | ConvertTo-Json'
  ) or []
  if isinstance(gpu, dict): #只有一張顯示卡時PowerShell會回傳單一物件而非陣列
    gpu = [gpu]

  disk_summary = '; '.join(
      f"{d.get('FriendlyName', '?')} {round(d.get('Size', 0) / (1024 ** 3))}GB [{d.get('HealthStatus', '?')}]"
      for d in disks
  ) if disks else 'None detected'

  gpu_summary = ', '.join(g.get('Name', '?') for g in gpu) if gpu else 'Unknown'

  return {
      'manufacturer': computer_system.get('Manufacturer', 'Unknown'),
      'model': computer_system.get('Model', 'Unknown'),
      'serial_number': bios.get('SerialNumber', 'Unknown'),
      'cpu_name': cpu.get('Name', 'Unknown'),
      'cores_threads': f"{cpu.get('NumberOfCores', '?')}C/{cpu.get('NumberOfLogicalProcessors', '?')}T",
      'ram_gb': round(computer_system.get('TotalPhysicalMemory', 0) / (1024 ** 3), 1),
      'ram_summary': ram_summary, #每條 RAM 的詳細資訊組成的字串
      'os_caption': os_info.get('Caption', 'Unknown'),
      'bios_version': bios.get('SMBIOSBIOSVersion', 'Unknown'),
      'disk_summary': disk_summary,
      'gpu_summary': gpu_summary,
  }

def _collect_linux_info(): #用/sys、/proc與常見指令撈Linux的硬體資訊
  manufacturer = _read_dmi('sys_vendor')
  model = _read_dmi('product_name')
  serial_number = _read_dmi('product_serial') #通常需要root權限，拿不到就是Unknown
  bios_version = _read_dmi('bios_version')

  cpuinfo = _run_shell('cat /proc/cpuinfo')
  cpu_name_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
  cpu_name = cpu_name_match.group(1).strip() if cpu_name_match else 'Unknown'
  logical_cores = os.cpu_count() or 0
  physical_cores = len(set(re.findall(r'core id\s*:\s*(\d+)', cpuinfo))) or logical_cores
  cores_threads = f'{physical_cores}C/{logical_cores}T'

  meminfo = _run_shell('cat /proc/meminfo')
  mem_match = re.search(r'MemTotal:\s*(\d+)\s*kB', meminfo)
  ram_gb = round(int(mem_match.group(1)) / (1024 ** 2), 1) if mem_match else 0.0

  os_release = _run_shell('cat /etc/os-release')
  os_match = re.search(r'PRETTY_NAME="(.+)"', os_release)
  os_caption = os_match.group(1) if os_match else platform.platform()

  disk_summary = 'None detected'
  lsblk_output = _run_shell('lsblk -d -b -J -o NAME,SIZE,MODEL,TYPE 2>/dev/null')
  try:
    lsblk_data = json.loads(lsblk_output) if lsblk_output else {}
    disk_list = [d for d in lsblk_data.get('blockdevices', []) if d.get('type') == 'disk']
    if disk_list:
      disk_summary = '; '.join(
          f"{d.get('name', '?')} {(d.get('model') or '').strip()} {round(int(d.get('size', 0)) / (1024 ** 3))}GB"
          for d in disk_list
      )
  except json.JSONDecodeError:
    pass

  gpu_summary = 'Unknown'
  lspci_output = _run_shell('lspci 2>/dev/null | grep -i -E "vga|3d controller"')
  if lspci_output:
    gpu_summary = '; '.join(line.split(': ', 1)[-1] for line in lspci_output.splitlines())

  return {
      'manufacturer': manufacturer,
      'model': model,
      'serial_number': serial_number,
      'cpu_name': cpu_name,
      'cores_threads': cores_threads,
      'ram_gb': ram_gb,
      'os_caption': os_caption,
      'bios_version': bios_version,
      'disk_summary': disk_summary,
      'gpu_summary': gpu_summary,
  }

def start_system_info_test():

  #取得程式（或打包後的exe）實際所在的資料夾
  app_folder = get_app_folder()

  log_folder = os.path.join(app_folder, 'Logs')

  #組合資料夾或檔案路徑
  os.makedirs(log_folder, exist_ok=True)

  csv_file = os.path.join(log_folder, 'system_info_results.csv')

  # 檢查 CSV 檔案是否存在，如果不存在則建立並寫入標題列
  file_exists = os.path.isfile(csv_file)
  with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    if not file_exists:
      writer.writerow(['Test Time', 'Manufacturer', 'Model', 'Serial Number', 'CPU',
                        'Cores/Threads', 'RAM(GB)', 'RAM Details', 'OS', 'BIOS Version', 'Disks', 'GPU'])

  print('Collecting system hardware information...')

  info = _collect_windows_info() if IS_WINDOWS else _collect_linux_info()

  manufacturer = info['manufacturer']
  model = info['model']
  serial_number = info['serial_number']
  cpu_name = info['cpu_name']
  cores_threads = info['cores_threads']
  ram_gb = info['ram_gb']
  ram_summary = info.get('ram_summary', 'Unknown')
  os_caption = info['os_caption']
  bios_version = info['bios_version']
  disk_summary = info['disk_summary']
  gpu_summary = info['gpu_summary']

  test_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  report = f"""===System Hardware Overview===
Test Time     : {test_time}
Manufacturer  : {manufacturer}
Model         : {model}
Serial Number : {serial_number}
CPU           : {cpu_name} ({cores_threads})
RAM           : {ram_gb} GB
RAM Details   : {ram_summary.replace('; ', chr(10) + '                ')}
OS            : {os_caption}
BIOS Version  : {bios_version}
Disks         : {disk_summary}
GPU           : {gpu_summary}
"""
  print(report)

  with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow([test_time, manufacturer, model, serial_number, cpu_name, cores_threads,
                      ram_gb, ram_summary,os_caption, bios_version, disk_summary, gpu_summary])

  print(f'Result saved to {csv_file}')

