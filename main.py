import time
from PIL import Image
from pywinauto import application, mouse
from selenium.webdriver.common.by import By
from selenium import webdriver
import random
import string
import ddddocr
import os
import winreg


def change_uuid():
    print('remove file')
    machineInfo = os.path.expanduser('~') + r'\AppData\Local\CHITUBOXPro\machineInfo.cfg'
    userLogin = os.path.expanduser('~') + r'\AppData\Local\CHITUBOXPro\userLogin.cfg'
    print(machineInfo)
    if os.path.isfile(machineInfo):
        modify_machineInfo(machineInfo)
        # os.remove(machineInfo)
    else:
        print('没有machineInfo,请先打开一次chitubox')
    print(userLogin)
    if os.path.isfile(userLogin):
        os.remove(userLogin)


def register():
    driver = webdriver.Chrome()
    driver.delete_all_cookies()
    driver.get("https://cc.chitubox.com/register")
    driver.execute_script("document.body.style.zoom='0.8'")
    email = driver.find_element(By.XPATH,
                                '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[1]/div/input')
    password = driver.find_element(By.XPATH,
                                   '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[2]/div/input')
    password2 = driver.find_element(By.XPATH,
                                    '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[3]/div/input')
    verify_code = driver.find_element(By.XPATH,
                                      '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[6]/div/input')
    verify_code_img = driver.find_element(By.XPATH,
                                          '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[6]/div/img')

    # click_box = driver.find_element(By.XPATH,
    #                                 '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/div[7]/div/div/label/input')
    submit = driver.find_element(By.XPATH,
                                 '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div[2]/div[1]/form/button')
    ran_email = ''.join(random.sample(string.ascii_letters + string.digits, 10)) + '@163.com'
    # ran_password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    ran_password = 'Chitubox123'
    email.send_keys(ran_email)
    password.send_keys(ran_password)
    password2.send_keys(ran_password)
    ocr = ddddocr.DdddOcr()
    driver.save_screenshot('verify_code_img.png')
    left = verify_code_img.location['x']  # x点的坐标
    top = verify_code_img.location['y']  # y点的坐标
    right = verify_code_img.size['width'] + left  # 上面右边点的坐标
    bottom = verify_code_img.size['height'] + top  # 下面右边点的坐标
    verify_code_img_pic = Image.open('verify_code_img.png')
    verify_code_img_pic = verify_code_img_pic.crop((left, top, right, bottom))
    verify_code_img_pic.save('verify_code_img.png')
    with open("verify_code_img.png", "rb") as f:
        res = ocr.classification(f.read())
        verify_code.send_keys(res)
    # click_box.click()
    driver.execute_script(
        'document.querySelector("body > app-root > app-layout > div > section > div > div > app-register > div > div.account-content.mx-auto.shadow.border.bg-white > div.form-container > form > div:nth-child(7) > div > div > label > input").click()')
    time.sleep(5)
    submit.submit()
    time.sleep(5)
    driver.close()
    return ran_email, ran_password


def login(email, password):
    handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\CHITUBOXPro', 0, winreg.KEY_READ)
    location, _type = winreg.QueryValueEx(handle, '')
    print('CHITUBOXPro in ' + location)
    location = location + r'\CHITUBOXPro.exe'
    app = application.Application(backend="uia").start(location)
    print('wait 15s for loading')
    time.sleep(15)
    window_login = app['CHITUBOXPro']
    window_login.set_focus()
    # window_login.print_control_identifiers(depth=99999)
    left = window_login.rectangle().left
    top = window_login.rectangle().top
    window_login['Edit0'].type_keys(email)
    window_login['Edit2'].type_keys(password)
    # 坑人的chitu找不到按钮,只能采用鼠标点击的方式
    mouse.click(button='left', coords=(left + 600, top + 400))
    print('wait 5s')
    time.sleep(5)
    print(window_login.rectangle())
    left = window_login.rectangle().left
    top = window_login.rectangle().top
    mouse.click(button='left', coords=(left + 520, top + 325))
    print('wait 5s')
    time.sleep(5)
    print(window_login.rectangle())
    left = window_login.rectangle().left
    top = window_login.rectangle().top
    mouse.click(button='left', coords=(left + 800, top + 540))


def modify_machineInfo(path):
    with open(path, 'rb+') as f:
        origin = f.read()
        f.seek(0)
        modify = []
        start = False
        for i in origin:
            if i == 20:
                start = True
                modify.append(i)
                continue
            if start:
                modify.append(random.randint(0, 255))
                continue
            modify.append(i)
        print(modify)
        f.write(bytes(modify))


if __name__ == '__main__':
    print('start register a new account')
    (email, password) = register()
    print('new email=' + email)
    print('new password=' + password)
    print('start change uuid')
    change_uuid()
    print('start auto login')
    print('if auto login fail, you can login manually')
    print('email=' + email)
    print('password=' + password)
    # email = 'Qto3LSHjlc@163.com'
    # password = 'Chitubox123'
    login(email, password)
