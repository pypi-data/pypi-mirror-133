from PGUI.window import Window
import pygame as pg

class Program():
    """
    A class that stores and controls windows.

    Window navigation is designed to work like the internet, with each
    window having a unique identifier, used to get reference to it using
    the program's `get_window` function.
    """


    _windows = {}
    """
    Window registry. Each subclass of window has a unique `window_id` 
    string, used as the key to this dictionary, with the window 
    instance being the value.
    """

    def __init__(self,
            default_window = "", ## Window ID of the default window.
            fps: int = 60,       ## Frames per second to draw windows at.
        ) -> None:

        ##The number of frames per second at which to draw windows.
        self.fps = fps
        """Number of frames per second to be drawn."""
        self.default_window = default_window
        """Window ID of the window to be opened first."""

        ##Tracks if the program is running or not.
        self.running = False
    

    def window(self, window_id, popup=False) -> Window:
        """
        This wrapper function adds the window being defined to the program.
        For example::

            @my_program.window("foo_bar", popup=True)
            class FooBarWindow():
                pass

        Will add the window to the program which will not end the program 
        when it is closed. To access it again from elsewhere within the 
        program, call::

            my_program.get_window("foo_bar")

        Convention for the naming is to assume "_window" has been added to the
        end. So instead of `"login_window"` you'd use `"login"`.
        """

        def window_add(window_class: type[Window]):
            window = window_class(self)
            window.is_popup = popup
            self.add_window(window, window_id)
            return Window
        return window_add


    def add_window(self, window: Window, window_id: str) -> None:
        """
        Adds a window to the program, sets itself as the parent and applies 
        variables such as fps. This function can take a window subclass or an
        instance of a window class. The window ID can be used to get access to 
        the window after the fact.

        Note: If the window's id is `_load_`, it will be run as soon as
        the program starts, before the default window.
        """
        if isinstance(window, type):
            window = window(self)
        
        ##Set window attributes
        window.parent = self
        window.window_id = window_id
        window.fps = self.fps

        ##Add window to windows dictionary.
        self._windows[window_id] = window

        if window_id == "_load_":
            window.run()


    def run(self) -> None:
        """Start running the program's default window."""
        self.running = True

        pg.init()

        ##If loading window exists, run it first.
        if "_load_" in self._windows.keys():
            self.get_window("_load_").run()

        ##Run default window.
        self.get_window(self.default_window).run()

        ##End the program when all windows have ended.
        self.end()


    def end(self) -> None:
        """Quit the program."""
        self.running = False
        pg.quit()
        print("\nProgram ended.")


    def get_window(self, window_id: str) -> Window:
        "Return a window from it's window_id."
        return self._windows[window_id]


    def set_fps(self, fps: int) -> None:
        """Set the framerate of the program."""
        self.fps = int(fps)