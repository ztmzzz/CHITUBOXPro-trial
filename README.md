# CHITUBOXPro-trial

trial CHITUBOXPro every 7 days

这是一个自动7天试用CHITUBOXPro的脚本,脚本会注册一个新的随机账号,然后修改CHITUBOXPro的配置文件,让它认为这是一台新的机器
接下来自动打开CHITUBOXPro完成试用流程

注意使用前需要打开一次CHITUBOXPro来生成配置文件,这个操作只需要执行一次

# 已知问题

1. 注册时可能会失败,重新运行既可解决
2. 注册成功后会在控制台输出邮箱和密码,如果自动试用失败可以手动进行试用
3. CHITUBOXPro使用QT作为界面,但是登录的窗口找不到按钮的控件,使用inspect也找不到,因此只能采用鼠标点击坐标的方式自动化.这就要求软件运行过程中不要有窗口覆盖CHITUBOXPro