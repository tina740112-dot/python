import csv
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from app_paths import get_app_folder
import system_info_test

#廠商關鍵字 -> 官方保固/支援頁網址範本，{serial}=序號、{model}=型號
VENDOR_URLS = {
    'dell': 'https://www.dell.com/support/home/en-us/product-support/servicetag/{serial}/overview',
    'lenovo': 'https://pcsupport.lenovo.com/us/en/search?query={serial}',
    'hp': 'https://support.hp.com/us-en/checkwarranty',
    'hewlett': 'https://support.hp.com/us-en/checkwarranty',
    'asus': 'https://www.asus.com/support/search?keyword={model}',
    'acer': 'https://www.acer.com/us-en/support/search?q={serial}',
    'msi': 'https://www.msi.com/search/{model}',
}
FALLBACK_URL = 'https://www.google.com/search?q={query}'
USER_AGENT = 'Mozilla/5.0 (compatible; IO_PeripheralTestTool)'

def build_url(manufacturer, model, serial): #依廠商挑官方網址，沒有對應的就退回搜尋頁
    key = (manufacturer or '').lower()
    quote = lambda s: urllib.parse.quote(str(s))
    for vendor, template in VENDOR_URLS.items():
        if vendor in key:
            return template.format(serial=quote(serial), model=quote(model))
    return FALLBACK_URL.format(query=quote(f'{manufacturer} {model} {serial} warranty'))

def fetch_page(url, timeout=15): #抓網頁，回傳(狀態, 文字)；失敗時文字為錯誤訊息
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            return response.status, response.read().decode(charset, errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, str(e)
    except (urllib.error.URLError, OSError) as e:
        return 0, str(e)

def parse_page(html): #擷取標題與看起來像保固到期日的字串；JS動態頁面可能抓不到
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
    title = re.sub(r'\s+', ' ', title_match.group(1)).strip() if title_match else ''
    text = re.sub(r'<(script|style).*?</\1>|<[^>]+>', ' ', html, flags=re.S | re.I)
    text = re.sub(r'\s+', ' ', text)
    warranty = re.findall(
        r'(?:warranty|expir\w*|保固)[^.]{0,60}?(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|[A-Z][a-z]{2,8}\.? \d{1,2}, \d{4})',
        text, re.I)
    return title, '; '.join(dict.fromkeys(warranty))

def collect_usb_devices(): #列出目前偵測到的USB周邊(不含Hub/控制器)，回傳字串
    if system_info_test.IS_WINDOWS:
        devices = system_info_test._run_powershell_json(
            'Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like "USB\\VID*" } '
            '| Select-Object FriendlyName | ConvertTo-Json'
        ) or []
        if isinstance(devices, dict):
            devices = [devices]
        names = [d.get('FriendlyName') or '?' for d in devices]
        names = [n for n in names if 'hub' not in n.lower()]
    else:
        lines = system_info_test._run_shell('lsusb').splitlines()
        names = [line.split(' ', 6)[-1] for line in lines if 'root hub' not in line.lower()]
    return re.sub(r'\s+', ' ', '; '.join(dict.fromkeys(names)).replace('\ufffd', '?')) or 'None detected'

def start_web_lookup():
    print('Collecting system info for web lookup...')
    info = (system_info_test._collect_windows_info() if system_info_test.IS_WINDOWS
            else system_info_test._collect_linux_info())
    manufacturer, model, serial = info['manufacturer'], info['model'], info['serial_number']
    ram_gb = info['ram_gb']
    ram_summary = re.sub(r'\s+', ' ', info.get('ram_summary') or 'Unknown')
    usb_summary = collect_usb_devices()
    disk_summary = info['disk_summary']
    gpu_summary = info['gpu_summary']
    print(f'Detected: {manufacturer} / {model} / {serial}')
    print(f'RAM       : {ram_gb} GB ({ram_summary})')
    print(f'Disks     : {disk_summary}')
    print(f'GPU       : {gpu_summary}')
    print(f'USB       : {usb_summary}')

    url = build_url(manufacturer, model, serial)
    print(f'Querying: {url}')
    status, body = fetch_page(url)
    title, warranty = parse_page(body) if status == 200 else ('', '')
    note = '' if warranty else 'No warranty date parsed (page may need JavaScript); open the URL manually'

    print(f'HTTP status : {status}')
    print(f'Page title  : {title}')
    print(f'Warranty    : {warranty or "N/A"}')
    if note:
        print(note)

    log_folder = os.path.join(get_app_folder(), 'Logs')
    os.makedirs(log_folder, exist_ok=True)
    csv_file = os.path.join(log_folder, 'web_lookup_results.csv')
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Lookup Time', 'Manufacturer', 'Model', 'Serial Number',
                             'RAM(GB)', 'RAM Details', 'Disks', 'GPU', 'USB Devices',
                             'URL', 'HTTP Status', 'Page Title', 'Warranty', 'Note'])
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), manufacturer, model,
                         serial, ram_gb, ram_summary, disk_summary, gpu_summary, usb_summary,
                         url, status, title, warranty, note])
    print(f'Result saved to {csv_file}')

if __name__ == '__main__':
    start_web_lookup()
