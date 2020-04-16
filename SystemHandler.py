# -*- coding: utf-8 -*-
'''
@author: PurePeace
@version: 0.2
@date: 2020-4-16

SystemHandler nice meme
'''

import locale
import wmi
import os, json, sys
from Utils import getTime, logg
import win32api as _a
import ctypes
import subprocess


c = wmi.WMI()
cwd = os.getcwd()


def cpu():
    tmpdict = {}
    tmpdict['CpuCores'] = 0
    for cpu in c.Win32_Processor():     
        tmpdict['Cpuid'] = cpu.ProcessorId.strip()
        tmpdict['CpuType'] = cpu.Name
        tmpdict['SystemName'] = cpu.SystemName
        try:
            tmpdict['CpuCores'] = cpu.NumberOfCores
        except:
            tmpdict['CpuCores'] += 1
        tmpdict['CpuClock'] = cpu.MaxClockSpeed 
        tmpdict['DataWidth'] = cpu.DataWidth
    return tmpdict


def mainboard():
    boards = []
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]
        tmpmsg['SerialNumber'] = board_id.SerialNumber
        tmpmsg['Manufacturer'] = board_id.Manufacturer 
        tmpmsg['Product'] = board_id.Product
        boards.append(tmpmsg)
    return boards


def bios():
    bioss = []
    for bios_id in c.Win32_BIOS():
        tmpmsg = {}
        tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics   #BIOS特征码
        tmpmsg['Version'] = bios_id.Version                           #BIOS版本
        tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()                 #BIOS固件生产厂家
        tmpmsg['ReleaseDate'] = bios_id.ReleaseDate                   #BIOS释放日期
        tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion       #系统管理规范版本
        bioss.append(tmpmsg)
    return bioss


def disk():
    disks = []
    for disk in c.Win32_DiskDrive():
        tmpmsg = {}
        tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
        tmpmsg['DeviceID'] = disk.DeviceID
        tmpmsg['Caption'] = disk.Caption
        tmpmsg['Size'] = disk.Size
        tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
        disks.append(tmpmsg)
    return disks


def memory():
    memorys = []
    for mem in c.Win32_PhysicalMemory():
        tmpmsg = {}
        tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
        tmpmsg['BankLabel'] = mem.BankLabel
        tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
        tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
        tmpmsg['Capacity'] = mem.Capacity
        tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
        memorys.append(tmpmsg)
    return memorys


def battery():
    isBatterys = False
    for b in c.Win32_Battery():
        isBatterys = True
    return isBatterys


def mac():
    macs = []
    for n in  c.Win32_NetworkAdapter():
        mactmp = n.MACAddress
        if mactmp and len(mactmp.strip()) > 5:
            tmpmsg = {}
            tmpmsg['MACAddress'] = n.MACAddress
            tmpmsg['Name'] = n.Name
            tmpmsg['DeviceID'] = n.DeviceID
            tmpmsg['AdapterType'] = n.AdapterType
            tmpmsg['Speed'] = n.Speed
            macs.append(tmpmsg)
    return macs


def user():
    return {
        'Username': os.getenv('USERNAME'), 
        'UserDomain': os.getenv('USERDOMAIN') or os.getenv('USERDOMAIN_ROAMINGPROFILE'), 
        'UserProfile': os.getenv('USERPROFILE')
    }


def system():
    return {
        'Lang': os.getenv('LANG') or locale.getdefaultlocale()[0],
        'Root': system_root(),
        'Temp': os.getenv('TEMP') or os.getenv('TMP'),
        'HomeDirve': os.getenv('HOMEDRIVE'),
        'OS': os.getenv('OS'),
        'Appdata': os.getenv('APPDATA'),
        'LocalAppdata': os.getenv('LOCALAPPDATA')
    }


def system_root():
    return os.getenv('SYSTEMROOT') or os.getenv('WINDIR')


def get_all():
    return {
        'User': user(),
        'CreateTime': getTime(1),
        'System':system(),
        'Cpu': cpu(),
        'Mainboard': mainboard(),
        'Bios': bios(),
        'Disk': disk(),
        'Memory': memory(),
        'Battery': battery(),
        'Mac': mac()
    }


def get_port_pid(port):
    logg(f'检查端口占用({port})...')
    res = execute_cmd(f'netstat -aon|findstr "{port}"').split('\n')
    result = []
    for line in res:
        temp = [i for i in line.split(' ') if i != '']
        if len(temp) > 4:
            result.append({'pid': temp[4], 'address': temp[1], 'state': temp[3]})
    for process in result:
        if process['address'] == f'0.0.0.0:{port}':
            logg('发现端口被占用！')
            return process['pid']
    logg('good，未发现端口占用！')
    return -1


def kill_process_by_port(port):
    pid = get_port_pid(port)
    return kill_process_by_pid(pid)


def kill_process_by_pid(pid):
    if pid != -1:
        try:
            logg(f'尝试杀死进程({pid})...')
            handle = _a.OpenProcess(1, False, int(pid))
            _a.TerminateProcess(handle, -1)
            _a.CloseHandle(handle)
            logg('成功杀死进程！')
            return True
        except Exception as err:
            logg(f'杀死进程：执行方法1：{err} 将使用方法2执行！')
            return execute_cmd(f"taskkill -pid {pid} -f -t")


def kill_self():
    kill_process_by_port(13377)


def run_nginx():
    logg('启动nginx服务...')
    stop_nginx()
    kill_process_by_port(443)
    kill_process_by_port(80)
    try:
        if __run_nginx() == True:
            logg('nginx启动成功！')
            return True
    except Exception as err:
        logg(err)
    logg('nginx启动失败！')
    return False


def __run_nginx():
    os.chdir(base_path('nginx\\'))
    r = _a.ShellExecute(0, 'open', 'nginx.exe', '', '', 0)
    if r > 32:
        return True
    else:
        logg(f'启动失败返回值：{r}')
        return False


def check_nginx():
    #logg('检查nginx运行情况...', dont_write=True)
    result = len(execute_cmd('tasklist | findstr "nginx.exe"').split('\n'))
    if result >=1:
        #logg('发现nginx已经运行了！', dont_write=True)
        return True
    logg('nginx没有运行！')
    return False


def stop_nginx():
    logg('准备停止nginx服务...')
    os.chdir(base_path('nginx\\'))
    is_running = check_nginx()
    result = False
    if is_running == True:
        try:
            result = execute_cmd('{} -s stop'.format('nginx.exe'))
            result = execute_cmd('taskkill /f /t /im nginx.exe')
        except Exception as err:
            logg(f'停止nginx时遇到错误：{err} ')
            
    else:
        logg('无需停止！')
        result = True
    return result


def execute_cmd(cmd, dev=False):
    proc = subprocess.Popen('chcp 65001 &' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    proc.stdin.close()
    proc.wait()
    result = proc.stdout.read().decode()
    result = '\n'.join(result.split('\n')[1:])
    proc.stdout.close()
    if dev == True: print(result)
    return result


def exit_api():
    logg('KafuuService API STOPPED.')
    sys.exit(0)
    return False


def exit_all_service():
    logg('KafuuService ALL STOPPED.')
    stop_nginx()
    sys.exit(0)
    return False


def base_path(path):
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)


def write_out(dict_data):
    create_time = dict_data.get('create_time', getTime(1)).replace(':', '-').replace('.', '_')
    backup_dir = os.getcwd()
    os.chdir(cwd)
    with open(f'sys_info_{create_time}.json', 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, indent=2)
    os.chdir(backup_dir)
    return True


def change_path_base():
    os.chdir(base_path(''))


def change_path_cwd():
    os.chdir(cwd)


def write_all():
    logg('写出所有数据')
    return write_out(get_all())


def hideConsole():
    """
    Hides the console window in GUI mode. Necessary for frozen application, because
    this application support both, command line processing AND GUI mode and theirfor
    cannot be run via pythonw.exe.
    """

    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        # if you wanted to close the handles...
        #ctypes.windll.kernel32.CloseHandle(whnd)


def showConsole():
    """Unhides console window"""
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 1)

