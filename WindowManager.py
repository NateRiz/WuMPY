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
                print("?", window.process_name)
                if window.process_name in active_windows:
                    print("yes")
                    win32gui.MoveWindow(active_windows[window.process_name],
                                        window.absolute_x,
                                        window.absolute_y,
                                        window.absolute_w,
                                        window.absolute_h,
                                        True)

    def win_enum_handler(self, hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd).strip()
            if window_text:
                results[window_text] = hwnd
                print(f"Window:[{window_text}]")

            """
            x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
            w = x1 - x0
            h = y1 - y0
            print(x0, x1, y0, y1, w, h)
            win32gui.MoveWindow(hwnd, x0, y0, w + 500, h + 500, True)
            """
