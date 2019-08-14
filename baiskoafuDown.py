import os, sys


if __name__ == '__main__':

    if sys.version_info[0] == 3 and sys.version_info[1] >= 6:

        from baiskoafu_auth import login
        from baiskoafu_download_manager import is_connected
        import config

        if is_connected():
            
            username = config.username
            password = config.password

            if username == "" or password == "":
                input("Enter username and password in 'config.py' file")
            else:
                if len(sys.argv) == 2:
                    login(username, password, sys.argv[1])
                else:
                    login(username, password)
        else:
            input("No connection :(")

    else:
        print("Python 3.6 and later version required!")
        if sys.version_info[0] == 2: raw_input()
        else: input()

