import asyncio
import subprocess
import threading
import time
import winreg
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psutil
import uiautomation as auto
import win32api
import win32con
import win32gui
import win32security
from PySide6 import QtAsyncio
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QWidget
from qfluentwidgets import Action, FluentIcon, RoundMenu

import subtitle_rc  # noqa: F401
from settings import get_settings
from subtitle_ui import Ui_Form
from translator import BergamotTranslator, DeeplTranslator

CURRENT_DIR = Path(__file__).parent.resolve()


class SubtitleMainWindow(QWidget, Ui_Form):
    def __init__(self) -> None:
        super().__init__()

        # 初始化设置
        self.settings = get_settings()

        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # 初始化拖拽栏
        self.global_path = QPainterPath()
        self.global_path.addRect(self.drag_widget.rect())
        self.drag_start_pos = None

        # 设置所有文本为红色
        self.plainTextEdit.setStyleSheet("color: red;")

        # 开一个线程用来更新字幕
        self.live_caption_manager_thread = LiveCaptionManagerThread()
        self.live_caption_manager_thread.signal.connect(lambda text: asyncio.ensure_future(self.updateSubtitle(text)))
        self.live_caption_manager_thread.start()

        # 创建系统托盘
        self.create_tray_menu()

        # 设置图标
        self.setWindowIcon(QIcon(":/icons/app-icon.png"))

        # 用于字幕更新
        self.last_text = ""
        self.interval = 5
        self.count = 1
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.last_time = time.time()
        self.enable_translation = True

    def create_tray_menu(self) -> None:
        """创建系统托盘UI"""
        self.trayicon = QSystemTrayIcon(self)
        self.trayicon.setIcon(QIcon(":/icons/app-icon.png"))

        # 创建托盘的右键菜单
        self.traymenu = RoundMenu()

        self.traymenu.addActions(
            [
                Action(FluentIcon.VIEW, "隐藏", triggered=lambda: self.hide() if self.isVisible() is True else self.show()),
                Action(FluentIcon.HOME_FILL, "Live Captions", triggered=self.live_caption_manager_thread.switch_live_caption_window),
                Action(FluentIcon.CLOSE, "退出", triggered=self.close),
            ],
        )

        # 翻译开关
        checked_icon = QIcon(":/icons/checkbox-checked.png")
        unchecked_icon = QIcon(":/icons/checkbox-unchecked.png")
        checkbox_action = Action(checked_icon, "翻译")
        checkbox_action.setCheckable(True)
        checkbox_action.setChecked(True)
        checkbox_action.triggered.connect(lambda checked: checkbox_action.setIcon(checked_icon) if checked is True else checkbox_action.setIcon(unchecked_icon))
        checkbox_action.toggled.connect(lambda checked: setattr(self, "enable_translation", checked))
        self.traymenu.addAction(checkbox_action)

        # 配置菜单并显示托盘
        self.trayicon.setContextMenu(self.traymenu)
        self.trayicon.show()

    async def updateSubtitle(self, text) -> None:
        """更新字幕界面 槽函数"""
        text = text.replace("\n", "")
        if text == "":
            return

        if text.startswith(self.last_text) and len(self.last_text) <= self.interval * self.count:
            self.last_text = text
            return

        if text.startswith(self.last_text) and len(self.last_text) > self.interval * self.count:
            self.count += 1

        if not text.startswith(self.last_text):
            self.count = 1

        if self.enable_translation is True:
            loop = asyncio.get_running_loop()
            translation_task = asyncio.ensure_future(
                loop.run_in_executor(
                    self.executor,
                    lambda text: BergamotTranslator.translate(text, self.live_caption_manager_thread.get_current_language()),
                    self.last_text,
                ),
            )
            self.last_text = text
            result = await translation_task
        else:
            result = self.last_text
            self.last_text = text

        # 如果句子太长，则截断显示在界面上
        if len(result) > 50:
            result = result[len(result) - 50 :]

        # 控制界面刷新的频率
        if self.last_time is not None and time.time() - self.last_time > 0.5:
            self.last_time = time.time()
            self.plainTextEdit.setText(result)

    def paintEvent(self, event) -> None:
        """绘制关键步骤：透明背景+两个图形"""
        painter = QPainter(self)

        painter.fillPath(self.global_path, QColor(0, 0, 0, 1))

    def mousePressEvent(self, event) -> None:
        """记录拖拽起始位置"""
        if event.button() == Qt.LeftButton:
            # 获取相对窗口左上角的坐标
            self.drag_start_pos = event.position().toPoint()

    def mouseMoveEvent(self, event) -> None:
        """实时更新窗口位置"""
        if self.drag_start_pos and event.buttons() & Qt.LeftButton:
            # 计算新的全局坐标
            global_pos = event.globalPosition().toPoint()
            # 更新窗口位置（全局坐标 - 按压点的相对坐标）
            self.move(global_pos - self.drag_start_pos)

    def mouseReleaseEvent(self, event) -> None:
        """清除拖拽状态"""
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None

    def closeEvent(self, event) -> None:
        """主线程退出时的操作"""
        # 退出子线程
        self.live_caption_manager_thread.stop()


class LiveCaptionManagerThread(QThread):
    """LiveCaptions.exe 管理线程(获取字幕)"""

    signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        self.start_live_caption()

        self.live_caption_window = auto.WindowControl(searchDepth=1, ClassName="LiveCaptionsDesktopWindow")
        self.hwnd = self.live_caption_window.NativeWindowHandle
        self.style_ex = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        rect_ex = win32gui.GetWindowRect(self.hwnd)
        self.x_ex = rect_ex[0] if rect_ex[0] > 0 else 500
        self.y_ex = rect_ex[1] if rect_ex[1] > 0 else 1000
        self.width_ex = rect_ex[2] - rect_ex[0]
        self.height_ex = rect_ex[3] - rect_ex[1]

        # 找到字幕文字所在的控件
        self.live_caption_text_control = None

        # LiveCaptions.exe窗口目前可见性
        self.visible = True
        self.switch_live_caption_window()

        # 线程退出标志
        self.stop_event = threading.Event()

    @property
    def text(self) -> str:
        """获取LiveCaptions.exe 字幕"""
        if self.live_caption_text_control is None or self.live_caption_text_control.Name == "":
            for wnd in self.live_caption_window.GetChildren():
                if wnd.ClassName == "Windows.UI.Composition.DesktopWindowContentBridge":
                    self.live_caption_text_control = wnd.GetFirstChildControl().TextControl()
                    break

        return self.live_caption_text_control.Name

    def stop(self) -> None:
        """退出线程"""
        # 退出LiveCaptions.exe
        for proc in psutil.process_iter(["name", "pid"]):
            if proc.info["name"] == "LiveCaptions.exe":
                psutil.Process(proc.info["pid"]).kill()
                break

        # 设置退出标志
        self.stop_event.set()

    def run(self) -> None:
        """线程主函数"""
        # 每一轮的结果
        subtitle = ""

        # 记录上一轮字幕
        last_text = self.text

        # 记录上一轮遍历的位置
        last_index = len(last_text) - 1

        # 当前轮遍历的位置
        cur_index = last_index

        start_time = None

        while True:
            if self.stop_event.is_set():
                return

            time.sleep(0.01)
            text = self.text
            length = len(text)

            # 由于windows LiveCaptions.exe的字幕虽然是不断累加的
            # 但是有长度限制，到一定长度就会删除字符串开头的字符串导致长度发生变化
            # 所以当长度发生变化时需要特殊处理
            if last_text[:10] != text[:10]:
                offset = last_text.find(text[:10])
                last_index -= offset

            cur_index = last_index
            last_text = text

            # 记录轮次开始时间
            if subtitle == "":
                start_time = time.time()

            while True:
                # 每隔0.1s如果语句还没结束（没遇到。、）则更新部分语句到界面
                if time.time() - start_time > 0.05:
                    self.emit(subtitle)
                    start_time = time.time()
                    continue

                # LiveCaptions.exe字幕没有更新 则进行下一轮
                if cur_index >= length:
                    last_index = length
                    break

                # 如果是。或、则这一轮停止并更新界面，不是则累加
                if text[cur_index] != "。" and text[cur_index] != "、" and text[cur_index] != ".":
                    # and text[cur_index] != "、"
                    subtitle += text[cur_index]
                    cur_index += 1
                else:
                    last_index = cur_index + 1

                    self.emit(subtitle)
                    subtitle = ""
                    break

    def get_current_language(self) -> str:
        """获取LiveCaptions.exe现在识别的语言

        Returns:
            str: 语言代码(ja, em, zh等)
        """
        # 获取用户sid
        username = win32api.GetUserName()
        domain = win32api.GetComputerName()
        pysid = win32security.LookupAccountName(domain, username)[0]
        sid = win32security.ConvertSidToStringSid(pysid)

        # 获取现在LiveCaptions.exe识别的语言
        with winreg.OpenKey(
            winreg.HKEY_USERS,
            f"{sid}\\Software\\Microsoft\\LiveCaptions\\UI",
            0,
            winreg.KEY_READ,
        ) as key:
            value, _ = winreg.QueryValueEx(key, "CaptionLanguage")
            return value.lower()

    def emit(self, text) -> None:
        """字幕更新事件"""
        if text == "":
            return

        self.signal.emit(text)

    def start_live_caption(self) -> None:
        """打开Windows LiveCaptions.exe"""
        proc = subprocess.Popen(
            ["LiveCaptions.exe"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def switch_live_caption_window(self) -> None:
        """改变LiveCaptions.exe窗口是否可见"""
        if self.visible is True:
            self.hide_live_caption_window()
            self.visible = False
        else:
            self.show_live_caption_window()
            self.visible = True

    def hide_live_caption_window(self) -> None:
        """隐藏windows LiveCaptions.exe窗口"""
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOPMOST,
            -10000,
            -10000,
            0,
            0,
            win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
        )

        win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_EXSTYLE,
            self.style_ex | win32con.WS_EX_TOOLWINDOW,
        )

    def show_live_caption_window(self) -> None:
        """打开windows LiveCaptions.exe窗口"""
        win32gui.SetWindowPos(
            self.hwnd,
            win32con.HWND_TOP,
            self.x_ex,
            self.y_ex,
            self.width_ex,
            self.height_ex,
            win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
        )

        win32gui.SetWindowLong(
            self.hwnd,
            win32con.GWL_EXSTYLE,
            self.style_ex,
        )


def main() -> None:
    """程序主入口"""

    app = QApplication([])
    subtitle_main_window = SubtitleMainWindow()

    subtitle_main_window.show()
    # app.exec()
    QtAsyncio.run()


if __name__ == "__main__":
    main()
