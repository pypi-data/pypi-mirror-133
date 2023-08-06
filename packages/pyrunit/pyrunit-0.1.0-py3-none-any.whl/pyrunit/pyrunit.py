#! /usr/bin/env python

from pyrunit.arg import ArgumentParser
import subprocess as sub

desc = """
██████╗ ██╗   ██╗██████╗ ██╗   ██╗███╗   ██╗██╗████████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██║   ██║████╗  ██║██║╚══██╔══╝
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║   
██╔═══╝   ╚██╔╝  ██╔══██╗██║   ██║██║╚██╗██║██║   ██║   
██║        ██║   ██║  ██║╚██████╔╝██║ ╚████║██║   ██║   
╚═╝        ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝ v.0.1.0
Simple shortcut to manage runit service.
"""

class runit:

    def __init__(self):
        arg = ArgumentParser(description=desc, allow_abbrev=False, add_help=False)
        arg.add_argument("-h", "--help", action="help", help="Display this message")
        arg.add_argument("-l", "--list-service", help="Enable service list", action="store_true")
        arg.add_argument("-la", "--list-all-service", help="List a service", action="store_true")
        arg.add_argument("-c", "--check-status", help="Check service status")
        arg.add_argument("-r", "--run", type=str, help="Run service")
        arg.add_argument("-s", "--stop", type=str, help="Stop service")
        arg.add_argument("-R", "--restart", type=str, help="Restart service")
        arg.add_argument("-e", "--enable", type=str, help="Enable service")
        arg.add_argument("-d", "--disable", type=str, help="Disable service")
        self.args = arg.parse_args()
        self.service = sub.check_output(["ls", "/etc/sv/"], text=True).strip().split("\n")
        self.enable_service = sub.check_output(["ls", "/var/service/"], text=True).strip().split("\n")

    def allService(self):
        for i, key in enumerate(self.service):
            if (i + 1) % 2:
                print('*','{:15}'.format(key), end='\t')
            else:
                print('*',key, end='\n')

    def serviceActive(self):
        status_all = sub.check_output(["sudo sv status /var/service/*"], shell=True, text=True).strip().split("\n")
        status = {}
        for st in status_all:
            sts = st.replace(":", "").split()
            del sts[2:5]
            sr = sts[1].split("/")
            del sr[0:3]
            status.update({sr[0]: sts[0]})
        print("="*24)
        print("{:<15} {:<15}".format('Service', '| Status'))
        print("="*24)
        for key, value in status.items():
            x = key
            y = value
            print("{:<15} | {:<15}".format(x, y))
        print("="*24)

    def checkService(self, serv, src):
        if serv not in src:
            print("Service not found !")
            exit()
        else:
            service = serv
            return service

    def Service(self, opt, serv):
        if serv not in self.enable_service and serv in self.service :
            print(f"Service {serv} is disable")
            exit()
        else:
            serv = self.checkService(serv, self.enable_service)
        if opt == "up" or opt == "down":
            print(f"Service {serv} {opt} !")
            Serv = f"sudo sv {opt} {serv}".split()
            sub.run(Serv)
        elif opt == "status":
            Serv = sub.check_output([f"sudo sv status {serv}"], shell=True, text=True).strip().split(":")
            st = Serv[0]
            print(f"Service {serv} is {st}")

    def enableService(self, serv):
        serv = self.checkService(serv, self.service)
        serv = f"sudo ln -s /etc/sv/{serv} /var/service/".split()
        sub.run(serv)
        print(f"Service {self.args.enable} enabled !")

    def disableService(self, serv):
        serv = self.checkService(serv, self.service)
        serv = f"sudo rm /var/service/{serv}".split()
        ask = input("Are you sure disable this service ? (y/N) : ")
        if ask == "Y" or ask == "y":
            sub.run(serv)
            print(f"Service {self.args.disable} disabled !")
        else:
            exit()

    def pyrunit(self):
        if self.args.list_service:
            self.serviceActive()
        elif self.args.list_all_service:
            self.allService()
        elif self.args.check_status != None:
            self.Service("status", self.args.check_status)
        elif self.args.run != None:
            self.Service("up", self.args.run)
        elif self.args.stop != None:
            self.Service("down", self.args.stop)
        elif self.args.restart != None:
            self.Service("restart", self.args.restart)
        elif self.args.enable != None:
            self.enableService(self.args.enable)
        elif self.args.disable != None:
            self.disableService(self.args.disable)
