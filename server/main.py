from notif_service import NotifService
# sudo lsof -i tcp:8765 // get process id
def main():
    notif_sevice = NotifService("localhost", 8888)
    notif_sevice.run()

if __name__== "__main__":
    main()