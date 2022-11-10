import time
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
    # driver.execute_script("document.body.style.zoom='0.8'")
    time.sleep(5)
    email = driver.find_element(By.XPATH,
                                '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/nz-form-item[1]/nz-form-control/div/div/input')
    password = driver.find_element(By.XPATH,
                                   '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/div[3]/div/div/nz-form-item[1]/nz-form-control/div/div/nz-input-group/input')
    password2 = driver.find_element(By.XPATH,
                                    '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/div[3]/div/div/nz-form-item[2]/nz-form-control/div/div/nz-input-group/input')
    verify_code = driver.find_element(By.XPATH,
                                      '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/nz-form-item[4]/nz-form-control/div/div/div/div[1]/input')
    verify_code_img = driver.find_element(By.XPATH,
                                          '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/nz-form-item[4]/nz-form-control/div/div/div/div[2]/img')

    click_box = driver.find_element(By.XPATH,
                                    '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/nz-form-item[5]/nz-form-control/div/div/label/span[1]/input')
    submit = driver.find_element(By.XPATH,
                                 '/html/body/app-root/app-layout/div/section/div/div/app-register/div/div/app-register-form-dialog/form/div[2]/div[5]/button')
    driver.execute_script('document.querySelector("#fb-root").remove()')
    driver.execute_script(
        'document.querySelector("body > app-root > app-layout > div > section > app-global-alert").remove()')
    ran_email = ''.join(random.sample(string.ascii_letters + string.digits, 10)) + '@163.com'
    # ran_password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    ran_password = 'Chitubox123'
    email.send_keys(ran_email)
    password.send_keys(ran_password)
    password2.send_keys(ran_password)
    ocr = ddddocr.DdddOcr()
    verify_code_img.screenshot("verify_code_img.png")
    with open("verify_code_img.png", "rb") as f:
        res = ocr.classification(f.read())
        verify_code.send_keys(res)
    click_box.click()
    time.sleep(5)
    submit.click()
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
    try:
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
        login(email, password)
    except Exception as e:
        print('some error happen')
        print(e)
    finally:
        input('Press any key to quit program.')
