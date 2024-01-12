import os, sys, csv
from termcolor import colored
import smtplib
import random
from cryptography.fernet import Fernet

os.system('cls')

def default(txt_len):
    alphas = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    nums = '1234567890'
    symbs = '!@#$%^&*()'

    char = alphas + nums + symbs 
    password = "".join(random.sample(char, txt_len))

    return password 

def custom(txt_len):
    print(colored('Options:\n1. Numbers and alphabets\n2. Numbers and symbols\n3. Alphabets and symbols', 'yellow'))
    print('-'*20)
    opt = input(colored('Enter option:', 'green'))
    if opt == '1':
        alphas = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
        nums = '1234567890'

        char = alphas + nums 

        password = ''
        for _ in range(txt_len):
            password += random.choice(char)
        return password 
    elif opt == '2':
        nums = '1234567890'
        symbs = '!@#$^%&*()'

        char = nums + symbs 

        password = ""
        for _ in range(txt_len):
            password += random.choice(char)
        return password 
    elif opt == '3':
        alphas = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
        symbs = '!@#$%^&*()'

        char = alphas + symbs 

        password = ""
        for _ in range(txt_len):
            password += random.choice(char)
        return password

def gen_rand_code():
    return random.randint(100000, 999999)

vercode = str(gen_rand_code())

def send_mail(ma):
    from_add = 'yourpassyourpass@gmail.com'
    obj = smtplib.SMTP('smtp.gmail.com', 587)
    obj.ehlo()
    obj.starttls()
    obj.login(from_add, 'aeuc eyrl lapk xwbs')
    obj.sendmail(from_addr=from_add, to_addrs=ma, msg=vercode)
    obj.quit()

def verify(c):
    return c == vercode

path = 'C:/yourpass'



print(colored('#'*28, 'cyan'))
print(colored(' #'+' '*26+'#', 'cyan'))
print(colored('  # YOUR PASS'+' '*16+'#', 'cyan'))
print(colored('   #\t-v1.0'+' '*17+'#', 'cyan'))
print(colored('    #'+'\t A VenDis Production'+' '*3+'#', 'cyan'))
print(colored('     #'+' '*26+'#', 'cyan'))
print(colored('      '+'#'*28, 'cyan'))

print('-'*20)

print(colored("Before running your_pass.py, run 'setup.py' only once\nOnce you quit the program, you logout.\nOnly one user can use this program in a single session.", 'red'))

print('-'*20)

mail_address = input(colored('Enter your mail-address:', 'green')).strip()
send_mail(mail_address)
print(colored('Please check your mailbox for verification code(if you are unable to find it, check spam.)', 'yellow'))

verif_code = input(colored('Enter verification code:', 'green')).strip()
if verify(verif_code) == True:
    if f'{mail_address}.csv' in os.listdir():
        pass
    else:
        file = open(f'c://yourpass//{mail_address}.csv', mode='a')
    print('-'*20)
    print(colored(f'Welcome to YOUR PASS(v1.0), {mail_address}!', 'cyan'))
    print('-'*20)
    print(colored('Your commands:\naddpass(To add password)\ngetpass(To obtain password)\nupdatepass(To update password)\nrmpass(To remove password)\ngettab(To get the passwords table)\nquit(To end the program)', 'yellow'))
    print('-'*20)
    while True:
        cmd = input(colored('Enter command:', 'green')).lower().strip()
        print('-'*20)
        if cmd == 'quit':
            file.close()
            break
        elif cmd == 'addpass':
            key = Fernet.generate_key()
            f = Fernet(key)
            service_name = input(colored('Enter service name:', 'green')).strip()
            service_pass = input(colored("Enter password(Type 'generate') to generate a password:", 'green')).strip()
            print('-'*20)
            file = open(f'c://yourpass//{mail_address}.csv', mode='a', newline='')
            file_writer = csv.writer(file)
            if service_pass != 'generate':
                encrypted_name, encrypted_pass = f.encrypt(service_name.encode()), f.encrypt(service_pass.encode())
                file_writer.writerow([key.decode(), encrypted_name.decode(), encrypted_pass.decode()])
            else:
                print('-'*20)
                gen_opt = input(colored('Default or custom:', 'green')).lower().strip()
                pass_len = int(input(colored('Password length:', 'green')).strip())
                print('-'*20)
                if gen_opt == 'default':
                    service_pass = default(pass_len)
                    encrypted_pass = f.encrypt(service_pass.encode())
                elif gen_opt == 'custom':
                    service_pass = custom(pass_len)
                    encrypted_pass = f.encrypt(service_pass.encode())
                else:
                    print(colored('Option not available'))
                encrypted_name = f.encrypt(service_name.encode())
                file_writer.writerow([key.decode(), encrypted_name.decode(), encrypted_pass.decode()])
                file.close()
        elif cmd == 'getpass':
            service_name = input(colored('Enter service name:', 'green'))
            file = open(f'c://yourpass//{mail_address}.csv', mode='r', encoding='utf-8')
            file_reader = csv.reader(file)
            data1 = list(file_reader)
            for i in range(len(data1)):
                key = data1[i][0].encode()
                f = Fernet(key)
                if service_name == f.decrypt(data1[i][1].encode()).decode():
                    print('-'*20)
                    print(colored('Password:', 'yellow'), colored(f'{f.decrypt(data1[i][-1].encode()).decode()}', 'magenta'))
                    break
            print('-'*20)
            file.close()
        elif cmd == 'updatepass':
            service_name = input(colored('Enter service name:', 'green'))
            file = open(f'c:/yourpass/{mail_address}.csv', mode='r', encoding='utf-8')
            file_reader = csv.reader(file)
            data2 = list(file_reader)
            for i in range(len(data2)):
                key = data2[i][0].encode()
                f = Fernet(key)
                if service_name == f.decrypt(data2[i][1]).decode():
                    print('-'*20)
                    data2[i][-1] = f.encrypt(input(colored('New password:', 'green')).encode()).decode()
                    print('-'*20)
            file.close()
            file = open(f'c://yourpass//{mail_address}.csv', mode='w', newline='')
            file_writer1 = csv.writer(file)
            for i in data2:
                file_writer1.writerow(i)
            file.close()
        elif cmd == 'rmpass':
            new_data = []
            service_name = input(colored('Enter service name:', 'green'))
            file = open(f'c://yourpass//{mail_address}.csv', mode='r', encoding='utf-8')
            file_reader = csv.reader(file)
            data3 = list(file_reader)
            for i in range(len(data3)):
                k = data3[i][0].encode()
                f = Fernet(k)
                if f.decrypt(data3[i][1].encode()).decode() != service_name:
                    new_data.append(data3[i])
            file.close()
            file = open(f"c://yourpass/{mail_address}.csv", mode='w', newline='')
            file_writer2 = csv.writer(file, delimiter=',')
            for i in new_data:
                file_writer2.writerow(i)
            file.close()
            print('-'*20)
else:
    print(colored('Wrong code', 'red'))
    sys.exit()
