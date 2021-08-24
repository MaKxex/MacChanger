import re
import subprocess
import optparse


def cmd_options():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface",dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac",dest="new_mac", help="New MAC address")
    (option, argument) = parser.parse_args()
    if not option.interface:
        parser.error("Use --help")
    elif not option.new_mac:
        parser.error("enter new mac, use --help for more information")
    return option


def get_argument(ifconfigOutput):
    Mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigOutput.decode(encoding="utf-8"))
    return Mac.group()

def get_current_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    return get_argument(ifconfig)

def check_changing(NewMac,OldMac):
    if not NewMac == OldMac:
        print("Mac is changed")
        return NewMac
    else:
        print("Same Mac")

def change_mac(interface, NewMac):
    oldMac = get_current_mac(interface)
    subprocess.call("ifconfig " + interface + " down", shell=True)
    subprocess.call("ifconfig " + interface + " hw ether "+ NewMac, shell=True)
    subprocess.call("ifconfig " + interface + " up", shell=True)
    NewMacCheck = get_current_mac(interface)
    Mac = check_changing(NewMacCheck,oldMac)
    print(f"Old Mac: {oldMac}")
    print(f"New Mac: {Mac}")

options = cmd_options()
change_mac(options.interface,options.new_mac)


