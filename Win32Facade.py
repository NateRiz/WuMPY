import win32gui
import win32api
import subprocess


class Win32Facade:
    def __init__(self):
        pass

    def get_monitors(self):
        monitors = win32api.EnumDisplayMonitors()
        return [win32api.GetMonitorInfo(m[0])["Monitor"] for m in monitors]

    def run(self, monitors):
        """
        Run the main program. Gui is used mostly for tests.
        :param monitors: [Monitors] in the current workspace
        :return: None
        """
        active_windows = {}
        win32gui.EnumWindows(self.win_enum_handler, active_windows)

        for monitor in monitors:
            for window in monitor.windows:
                if window.process_name in active_windows:
                    if window.is_pixel_precision_enabled:
                        self.move_window_absolute(active_windows[window.process_name], window)
                    else:
                        self.move_window_relative(active_windows[window.process_name], window)
                else:
                    try:
                        subprocess.Popen(window.target)
                    except Exception as e:
                        print(e)

    def win_enum_handler(self, hwnd, results):
        window_text = win32gui.GetWindowText(hwnd).strip()
        if window_text:
            results[window_text] = hwnd

    def list_windows(self):
        windows = {}
        win32gui.EnumWindows(self.win_enum_handler, windows)
        return windows

    def move_window_absolute(self, hwnd, window):
        win32gui.MoveWindow(hwnd,
                            window.win_x,
                            window.win_y,
                            window.win_w,
                            window.win_h,
                            True)

    def move_window_relative(self, hwnd, window):
        monitor_index = window.parent().index
        monitors = self.get_monitors()
        monitor = monitors[monitor_index]
        mx, my = monitor[0], monitor[1]
        mw = monitor[2] - mx
        mh = monitor[3] - my
        x = int(mx + (mw * (window.win_x / 100)))
        y = int(my + (mh * (window.win_y / 100)))
        w = int((window.win_w / 100) * mw)
        h = int((window.win_h / 100) * mh)
        win32gui.MoveWindow(hwnd, x, y, w, h, True)

    def move_window_to_monitor(self, hwnd, monitor_index):
        monitors = self.get_monitors()
        monitor = monitors[monitor_index]
        mx, my = monitor[0], monitor[1]
        mw = monitor[2] - mx
        mh = monitor[3] - my
        x = mx + int(mw / 2) - 500
        y = my + int(mh / 2) - 400
        win32gui.MoveWindow(hwnd, x, y, 1000, 800, True)
