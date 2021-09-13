import win32gui
import subprocess


class WindowManager:
    def __init__(self):
        pass

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
                    win32gui.MoveWindow(active_windows[window.process_name],
                                        window.absolute_x,
                                        window.absolute_y,
                                        window.absolute_w,
                                        window.absolute_h,
                                        True)
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

