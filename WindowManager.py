import win32gui


class WindowManager:
    def __init__(self):
        pass

    def run(self, monitors):
        active_windows = {}
        win32gui.EnumWindows(self.win_enum_handler, active_windows)
        print(active_windows)

        for monitor in monitors:
            for window in monitor.windows:
                if window.process_name in active_windows:
                    print(f"Moving {window.process_name}")
                    win32gui.MoveWindow(active_windows[window.process_name],
                                        window.absolute_x,
                                        window.absolute_y,
                                        window.absolute_w,
                                        window.absolute_h,
                                        True)

    def win_enum_handler(self, hwnd, results):
        #if 1 or win32gui.IsWindowVisible(hwnd):
        window_text = win32gui.GetWindowText(hwnd).strip()
        if window_text:
            results[window_text] = hwnd
            #print(f"Window:[{window_text}]")
        """
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        """

    def list_windows(self):
        windows = {}
        win32gui.EnumWindows(self.win_enum_handler, windows)
        return windows

