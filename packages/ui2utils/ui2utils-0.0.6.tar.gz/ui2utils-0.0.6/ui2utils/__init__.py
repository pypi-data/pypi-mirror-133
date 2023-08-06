import time

import uiautomator2 as ui2


class ui2Server:
    def __init__(self, serial, waitTime: int = 10):
        self.serial = serial
        self.dev = ui2.connect(serial)
        self.dev.implicitly_wait(seconds=waitTime)    # 设置 元素查找等待时间 10 秒

        # self.appSess = None     # 用来监控 app 的 生命周期

# 设备相关 --------------------------------------------------------------------

    def getInfo(self):
        """
        获取 运行时信息，即当前信息，主要有 前台包名
        :return: {'currentPackageName': 'com.android.launcher3',
                    'displayHeight': 960, 'displayWidth': 540, 'displayRotation': 0,
                    'displaySizeDpX': 360, 'displaySizeDpY': 640,
                    'productName': 'wa0', 'screenOn': True, 'sdkInt': 25,
                    'naturalOrientation': True}
        """
        res = self.dev.info
        return res

    def getDeviceInfo(self):
        """
        获取 设备详细信息
        :return: {
                    'udid': '00e0728b--test1', 'version': '7.1.2', 'serial': '00e0728b',
                    'brand': 'samsung', 'model': 'test1', 'sdk': 25, 'agentVersion': '0.10.0',
                    'display': {'width': 540, 'height': 960},
                    'battery': {
                                    'acPowered': True, 'usbPowered': False, 'wirelessPowered': False,
                                    'status': 2, 'health': 2, 'present': True, 'level': 100, 'scale': 100,
                                    'voltage': 3805, 'temperature': 292, 'technology': ''
                                },
                    'memory': {'total': 1027544, 'around': '1 GB'},
                    'arch': '', 'owner': None,
                    'presenceChangedAt': '0001-01-01T00:00:00Z', 'usingBeganAt': '0001-01-01T00:00:00Z',
                    'product': None, 'provider': None
                }
        """
        res = self.dev.device_info
        return res

    # def getOtherInfo(self):
    #     print("1 ", self.dev.wlan_ip)   # 模拟器返回 None ； 真机返回 ip
    #     print("2 ", self.dev.alive)     # True
    #     print("3 ", self.dev.debug)     # False
    #     print("4 ", self.dev.xpath)     # <uiautomator2.xpath.XPath object at 0x0000026A1C2B2688>
    #     print("5 ", self.dev.clipboard)     # print("29", self.dev.widget)
    #     print("6 ", self.dev.address)   # http://127.0.0.1:13935
    #     print("7 ", self.dev.agent_alive)  # True
    #     print("8 ", self.dev.http)  # <uiautomator2._AgentRequestSession object at 0x0000026A1C18B608>
    #     print("9 ", self.dev.jsonrpc)  # <uiautomator2._BaseClient.jsonrpc.<locals>.JSONRpcWrapper object at 0x0000026A1C29EC88>
    #     print("10", self.dev.last_traversed_text)  # None
    #     print("11", self.dev.orientation)   # natural
    #     print("12", self.dev.pos_rel2abs)   # <function _Device.pos_rel2abs.<locals>._convert at 0x0000026A1C2C0678>
    #     print("13", self.dev.settings)      # {'fallback_to_blank_screenshot': False, 'operation_delay': (0, 0), 'operation_delay_methods': ['click', 'swipe'], 'wait_timeout': 10, 'xpath_debug': False}
    #     print("14", self.dev.swipe_ext)     # <uiautomator2.swipe.SwipeExt object at 0x0000026A1C29EC88>
    #     print("15", self.dev.toast)  # <uiautomator2._Device.toast.<locals>.Toast object at 0x0000026A1C2B6948>
    #     print("16", self.dev.touch)  # <uiautomator2._Device.touch.<locals>._Touch object at 0x0000026A1C2B6948>
    #     print("17", self.dev.uiautomator)  # <uiautomator2._Service object at 0x0000026A1C2B6948>
    #     print("18", self.dev.wait_timeout)  # 10
    #     print("19", self.dev.watcher)  # <uiautomator2.watcher.Watcher object at 0x0000026A1C2B6948>
    #
    #     print("1", self.dev.image())
    #     print("2", self.dev.alibaba())
    #     print("3", self.dev.click_post_delay())
    #     print("4", self.dev.screenrecord())
    #     print("5", self.dev.taobao())
    #     print("6", self.dev.widget())

    def getSize(self):
        """
        获取 屏幕大小
        :return: (540, 960) 宽，高
        """
        size = self.dev.window_size()
        return size

    def getXml(self):
        """
        转储 ui 的 xml 数据
        :return: xml 格式 str
        """
        res = self.dev.dump_hierarchy()
        # xml_dom = parseString(res)
        # print("1 ", xml_dom)    # <xml.dom.minidom.Document object at 0x000001F0C8FC3948>
        # print("2 ", xml_dom.documentElement)     # <DOM Element: hierarchy at 0x1f0c8edc408>
        # print("2 ", xml_dom.documentElement.getElementsByTagName("node"))    # [<DOM Element: node at 0x1f0c8edc728>, <DOM Element: node at 0x1f0c8edc7c8>, ]
        return res

# 对 设备 的操作 ---------------------------------------------------------------------
    def screenShot(self, filename):
        """
        截图
        :param filename: 可以是 文件名，或 路径 + 文件名
        :return:
            1. filename 为空，返回 <PIL.Image.Image image mode=RGB size=540x960 at 0x2B11D219408>
            2. filename 不为空，返回 filename
        """
        # 方式 1
        image = self.dev.screenshot(filename)

        # 方式 2
        # image = self.dev.screenshot(format="pillow")  # default format="pillow"
        # image.save(filename)  # or home.png. Currently, only png and jpg are supported

        # 方式 3
        # image = self.dev.screenshot(format='opencv')
        # cv2.imwrite('screenShot222.jpg', image)

        # 方式 4
        # image = self.dev.screenshot(format='raw')
        # open("screenShot333.jpg", "wb").write(image)

        return image

    def openNotification(self):
        """
        下拉 打开通知栏
        :return: 成功 True， 否则 False
        """
        res = self.dev.open_notification()
        return res

    def openQuickSettings(self):
        """
        下拉 打开快速设置栏
        :return: 成功 True， 否则 False
        """
        res = self.dev.open_quick_settings()
        return res

    def orientation(self, value : str = None):
        """
        获取当前屏幕方向
        :return:
            1. 参数为None : natural > n,   left > l,   right > r,  upsidedown > u
            2. 不为None : 设置成功 True， 否则 False
        """
        try:
            if value is None:
                res = self.dev.orientation
                return res
            else:
                self.dev.set_orientation(value=value)
                return True
        except Exception as e:
            print("orientation ERROR: ", str(e))
            return False

    def openUrl(self, url):
        """
        打开链接， 或 app
        :param url:
            "https://www.baidu.com"     # 浏览器 访问该链接
            "taobao://taobao.com"       # 打开 app， open Taobao app
            "appname://appnamehost"
        :return: 成功 True， 否则 False
        """
        try:
            res = self.dev.open_url(url=url)
            return res
        except Exception as e:
            print("openUrl ERROR:", str(e))
            return False

    def clipboard(self, text: str = None):
        """
        剪贴板
        :param text:
        :return:
        """
        try:
            if text is None:
                return self.dev.clipboard
            else:
                self.dev.set_clipboard(text=text)
                if self.dev.clipboard == text:
                    return True
                else:
                    return False
        except Exception as e:
            print("clipboard ERROR: ", str(e))
            return False

    def settings(self, key: str = None, value=None):
        """
        配置
        :return: {'operation_delay': (0, 0), 'operation_delay_methods': ['click', 'swipe'], 'wait_timeout': 20.0, 'xpath_debug': False}
        """
        try:
            if key is not None and value is not None:
                self.dev.settings[key] = value

            res = self.dev.settings
            return res
        except Exception as e:
            print("settings ERROR: ", str(e))
            return False

# 文件 导入 导出 ---------------------------------------------------------------
    def push(self, source, destination):
        """
        推送 文件 到 设备上
        :param source:      电脑端 目标文件 路径  "D:\\python\\CtrlSys\\测试\\files\\head1.jpg"
        :param destination: 设备端 要存放的 目录  "/sdcard/Pictures/11.jpg" 或 "/sdcard/Pictures/"
        :return: {'isDir': False, 'mode': '0771', 'target': '/sdcard/Pictures/head1.jpg'}
        """
        try:
            res = self.dev.push(src=source, dst=destination)
            return res
        except Exception as e:
            print("push ERROR:", str(e))
            return False

    def pull(self, source, destination):
        """
        导出 文件
        :param source:      设备端 目标文件 路径  "/sdcard/Pictures/11.jpg"
        :param destination: 电脑端 要存放的 目录 + 文件名  "D:/Android/aa/22.jpg"
        :return: 成功 True， 否则 False
        """
        try:
            res = self.dev.pull(src=source, dst=destination)
            return res
        except Exception as e:
            print("pull ERROR:", str(e))
            return False

# app 提取相关 -------------------------------------------------------------

    def getRunAppList(self):
        """
        获取 运行中的 app list
        :return: ['com.android.keychain', 'com.android.launcher3', ...]
        """
        try:
            runlist = self.dev.app_list_running()
            return runlist
        except Exception as e:
            print("installApk ERROR: ", str(e))
            return False

    def getCurrentApp(self):
        """
        获取当前运行的 app 的包名
        :return: {'package': 'com.android.launcher3', 'activity': 'com.android.launcher3.Launcher'}
        """
        res = self.dev.app_current()
        return res

    def getAppInfo(self, pkName):
        """
        获取 app 信息
        :param pkName:
        :return: {'packageName': 'com.android.settings', 'mainActivity': 'Settings', 'label': '设置', 'versionName': '7.1.2', 'versionCode': 25, 'size': 10737559}
        """
        try:
            info = self.dev.app_info(pkName)
            return info
        except Exception as e:
            print("getAppInfo ERROR: ", str(e))
            return False

    def getAppIcon(self, pkName):
        """
        获取 app 图标
        :param pkName:
        :return: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=48x48 at 0x1E91277BEC8>
        """
        try:
            img = self.dev.app_icon(pkName)
            return img
        except Exception as e:
            print("getAppIcon ERROR: ", str(e))
            return False

    def waitAppStart(self, pkName, timeout: float = 5.0, front=False):
        """
        获取 app 运行的 pid
        :param pkName:
        :param timeout: 单位 秒
        :param front: True > 必须前台运行， False > 不需要前台运行(可以此判断 app 是否运行)
        :return: pid > int,  未运行 或 未在前台 > False
        """
        try:
            pid = self.dev.app_wait(package_name=pkName, timeout=timeout, front=front)
            if pid:
                return pid
        except Exception as e:
            print("getAppPid ERROR: ", str(e))
        return False

    def waitActivity(self, activity, timeout: float = 3.0):
        """
        等待 某个界面的出现
        :param activity: 界面 "com.android.settings.Settings"
        :param timeout: 超时
        :return: 出现则 True， 否则 False
        """
        try:
            res = self.dev.wait_activity(activity=activity, timeout=timeout)
            return res
        except Exception as e:
            print("getAppPid ERROR: ", str(e))
            return False

# app 操作相关 -------------------------------------------------------------

    def installApk(self, apkUrl):
        """
        安装 app, 覆盖安装
        默认指令：
            -r 替换已存在的应用程序，也就是说强制安装
            -t 允许测试包
        其他指令：
            -l 锁定该应用程序
            -s 把应用程序安装到sd卡上
            -d 允许进行将见状，也就是安装的比手机上带的版本低
            -g 为应用程序授予所有运行时的权限
        :param apkUrl: apk 路径，
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.app_install(apkUrl)
            return True
        except Exception as e:
            print("installApk ERROR: ", str(e))
            return False

    def uninstallApk(self, pkName):
        """
        卸载 app, 不管 app 是否已安装
        :param pkName: 包名, 传入系统包名时，也会执行，但并不会真正卸载系统应用
        :return: 成功 res=True
        """
        try:
            res = self.dev.app_uninstall(pkName)
            return res
        except Exception as e:
            print("uninstallApk ERROR: ", str(e))
            return False

    def appStart(self, pkName):
        """
        打开 app
        :param pkName:
        :return: 成功打开 True； 否则 False
        """
        try:
            self.dev.app_start(package_name=pkName)

            currentApp = self.getCurrentApp()
            currentAppName = currentApp["package"]
            if currentAppName == pkName:
                return True
        except Exception as e:
            print("appStart ERROR: ", str(e))
        return False

    def appStop(self, pkName):
        """
        停止 app，不管 app是否存在
        :param pkName:
        :return: 成功则 True， 否则 False
        """
        try:
            self.dev.app_stop(pkName)
            return True
        except Exception as e:
            print("appStop ERROR: ", str(e))
            return False

    def appClear(self, pkName):
        """
        清空 app 数据，不管 app是否存在
        :param pkName:
        :return: 成功则 True， 否则 False
        """
        try:
            self.dev.app_clear(pkName)
            return True
        except Exception as e:
            print("appClear ERROR: ", str(e))
            return False

    def appStopAll(self, excludesList=None):
        """
        停止所有 app，包括系统应用， 除了 excludesList
        :param excludesList:
        :return: 成功 True， 否则 False
        """
        if excludesList is None:
            excludesList = []
        try:
            res = self.dev.app_stop_all(excludes=excludesList)
            if len(res) > 0:
                return True
            else:
                return False
        except Exception as e:
            print("appStopAll ERROR: ", str(e))
            return False

# 模拟触控操作：用于模拟用户对手机的点击或滑动等操作 -----------------------------------------------

    def click(self, x, y):
        """
        单击, 长按
        :return: 成功 True，否则 False
        """
        try:
            self.dev.click(x=x, y=y)
            return True
        except Exception as e:
            print("click ERROR : ", str(e))
            return False

    def doubleClick(self, x, y, useTime : float = 0.1):
        """
        双击
        :return: 成功 True，否则 False
        """
        try:
            self.dev.double_click(x=x, y=y, duration=useTime)
            return True
        except Exception as e:
            print("doubleClick ERROR : ", str(e))
            return False

    def longClick(self, x, y, useTime : float = 0.5):
        """
        长按
        :return: 成功 True，否则 False
        """
        try:
            self.dev.long_click(x=x, y=y, duration=useTime)
            return True
        except Exception as e:
            print("longClick ERROR : ", str(e))
            return False

    def swipe(self, x1, y1, x2, y2, useTime: float = None, steps: int = None):
        """
        划动，(x1, y1) 划动到 (x2, y2)
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :param useTime: 用时，建议小于 1，  数值太大会会拖动拖动控件
        :param steps: 划动次数，该值被设置时，duration则无用， 每一个 steps 用时 5 ms
        :return: 成功 True，否则 False
        """
        if useTime > 1:
            useTime = 0.5
        try:
            self.dev.swipe(fx=x1, fy=y1, tx=x2, ty=y2, duration=useTime, steps=steps)
            return True
        except Exception as e:
            print("swipe ERROR : ", str(e))
            return False

    def swipeExt(self, direction: str, scale: float = 0.9):
        """
        划动， 上， 下， 左， 右 划动
        :param direction: right: 右滑，从左往右
        :param scale: 滑动距离为屏幕宽度的 90%
        :return: 成功 True，否则 False
        """
        try:
            self.dev.swipe_ext(direction, scale=scale)
            return True
        except Exception as e:
            print("swipeExt ERROR : ", str(e))
            return False

    def swipePoints(self, pointsList: list, useTime: float = 0.5):
        """
        划动， 路径 划动，多用于图案解锁
        useTime 每步耗时
        :return: 成功 True，否则 False
        """
        try:
            res = self.dev.swipe_points(pointsList, duration=useTime)
            return res
        except Exception as e:
            print("swipePoints ERROR : ", str(e))
            return False

    def drag(self, x1, y1, x2, y2, useTime : float = 0.5):
        """
        拖拽， (x1, y1) 拖拽到 (x2, y2)
        :return: 成功 True，否则 False
        """
        try:
            res = self.dev.drag(sx=x1, sy=y1, ex=x2, ey=y2, duration=useTime)
            return res
        except Exception as e:
            print("swipePoints ERROR : ", str(e))
            return False

    def pressKey(self, keyName):
        """
        按键
        :return: 成功 True，否则 False
        """
        try:
            res = self.dev.press(key=keyName)
            return res
        except Exception as e:
            print("pressKey ERROR : ", str(e))
            return False

    def inputAndSearch(self, text):
        """
        输入
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.set_fastinput_ime(True)  # 切换成FastInputIME输入法
            self.dev.clear_text()  # 清除输入框所有内容
            time.sleep(0.5)

            res = self.dev.send_keys(text)  # adb广播输入
            time.sleep(0.5)

            flag = False
            if res:
                self.dev.send_action("search")  # 模拟输入法的搜索
                flag = True
            self.dev.set_fastinput_ime(False)  # 切换成正常的输入法
            return flag
        except Exception as e:
            print("inputAndSearch ERROR :", str(e))
            return False

    def doShell(self, cmdStr, timeout=3):
        """
        执行 adb shell 命令
        :param cmdStr:
        :param timeout:
        :return: 请求正常 exit_code=0， 否则为其他
        """
        output, exit_code = self.dev.shell(cmdStr, timeout=timeout)
        return {"exit_code" : exit_code, "output" : output}

    def getIp(self, cmdStr, timeout=3):
        """
        获取 设备 的 ip
        :param cmdStr:
        :param timeout:
        :return:
        """
        count = 0
        while True:
            if count == 3:
                print("获取设备IP失败")
                return False

            try:
                output, exit_code = self.dev.shell(cmdStr, timeout=timeout)
                ip = output.replace('\n\n', '\n').strip()
                ip = ip.split("\n")[-1]
                if ip is None or len(ip) == 0:
                    time.sleep(2)
                    count += 1
                    continue
                else:
                    return ip
            except Exception as e:
                print("获取设备IP异常: ", str(e))

    def screen(self, action: bool):
        """
        亮屏， 熄屏
        :param action:
        :return:
        """
        if action is True:
            return self.dev.screen_on()
        else:
            return self.dev.screen_off()

    def unlock(self):
        """
        解锁
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.unlock()
            return True
        except Exception as e:
            print("unlock ERROR:", str(e))

# 监控 守护进程 -------------------------------------------------------------------------
    """ 与 session 无关 """
    def watcherNew(self, watcherName, keyWord):
        """
        添加 守护， 用于处理非预期的弹出框，如崩溃窗口，一些确定或取消弹出框。
        监控弹窗(在线程中监控)
        - 注册名为ANR的监控，当出现 ANR 和 Force Close时，点击 Force Close
            d.watcher("ANR").when(xpath="ANR").when("Force Close").click()
        :param watcherName: 该守护进程 名称
        :param keyWord: 关键字
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.watcher(watcherName).when(keyWord).click()
            return True
        except Exception as e:
            print("watcherNew ERROR:", str(e))

    def watcherDel(self, watcherName):
        """
        移除 守护
        :param watcherName: 守护进程 名称
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.watcher.remove(watcherName)
            return True
        except Exception as e:
            print("watcherDel ERROR:", str(e))

    def watcherStart(self, timeout: float = 2.0):
        """
        开启 守护
        :return: <Thread(watcher, started daemon 33500)>
        """
        try:
            res = self.dev.watcher.start(interval=timeout)
            return res
        except Exception as e:
            print("watcherStart ERROR:", str(e))

    def watcherStop(self):
        """
        停止 守护
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.watcher.stop()
            return True
        except Exception as e:
            print("watcherStop ERROR:", str(e))

    def watcherReset(self):
        """
        停止并移除所有的监控，常用于初始化
        :return: 成功 True， 否则 False
        """
        try:
            self.dev.watcher.stop()
            return True
        except Exception as e:
            print("watcherStop ERROR:", str(e))

# 使用 session 操作app,  元素定位 与 操作 --------------------------------------------------------------
    """
    Session represent an app lifecycle. Can be used to start app, detect app crash.
    Session操作: 一般用于测试某个特定的APP，
        首先将某个APP设定为一个Session，所有的操作都基于此Session，
        当Session退出时，代表APP退出
        session的用途是操作的同时监控应用是否闪退，当闪退时操作，会抛出SessionBrokenError
    """

    def getAppSess(self, pkName, attach=False, strict=False, timeout=None):
        """
        启动 app，并监控该 app 的生命周期
        会阻塞，直到 app 启动成功
        返回的是 当前连接的 dev对象， 所以一次只能监控 1 个app
        :param pkName:
        :param attach: True : 已启动则跳过启动 ,  False : 重新启动
        :param strict: True : 没有启动成功 则抛异常
        :param timeout: 启动时间 秒
        :return: <uiautomator2.Device object at 0x000001BED12C4D48> 其实就是 self.dev
        """
        try:
            newSess = self.dev.session(package_name=pkName, attach=attach, strict=strict, launch_timeout=timeout)
            return newSess
        except Exception as e:
            print("getAppSess ERROR : ", str(e))
            return False

    def sessHandler(self):
        pkName1 = "cc.quanben.novel"
        pkName2 = "com.android.settings"

        print(">>>> 0 ", self.dev.implicitly_wait())  # 查找元素的等待时间， 默认 20s

        sess1 = self.dev.session(package_name=pkName1, attach=True)
        print("sess1 >>> ", sess1)

        print(sess1(text="榜单").__len__())
        if sess1(text="榜单"):  # 会调用 __len__() 方法， 会等待 默认时间
            print("111")
        # sess1(text="榜单").click()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # def pinchIn(self, percent: int = 100, steps: int = 50):
    #     """
    #     缩放
    #     :return: 成功 True，否则 False
    #     """
    #     try:
    #         res = self.dev(resourceId="android:id/content").pinch_in(percent=percent, steps=steps)
    #         return res
    #     except Exception as e:
    #         print("pinchIn ERROR : ", str(e))
    #         return False
    #
    # def pinchOut(self):
    #     """
    #     放大
    #     :return:
    #     """
    #     try:
    #         self.dev(resourceId="android:id/content").pinch_out()
    #         return True
    #     except Exception as e:
    #         print("pinchOut ERROR : ", str(e))
    #         return False


