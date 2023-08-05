"""Adds a window, innit?"""

from typing import Callable
import pygame as pg
from PGUI.uielement import UIElement

class Window:
    """Creates a window using pygame.
    - UIElements can be added to the window, and their update() and draw()
      methods will be called every frame.
    """
    height = None
    width = None
    title = None

    def __init__(self, parent) -> None:

        self.window_id = ""
        self.is_popup = False
        self.loaded = False

        ##Display stuff.
        self.screen_size: tuple = (self.width, self.height)
        """The width and height of the screen in pixels."""
        self.title: str = self.title
        """The title to be displayed at the top of the window."""
        self.parent = parent
        """Window's parent program."""
        self.colours = self.parent.colours
        """List of colours used by the window."""

        ##Pygame stuff.
        self.running: bool = False
        self.fps: int = self.parent.fps
        """Number of frames per second to draw the window at."""
        self.clock = pg.time.Clock()
        """Pygame clock to control FPS."""
        self.mouse = pg.mouse
        """Reference to the pygame mouse."""
        self.events = []
        """List of pygame events, updated every frame."""

        ##Font.
        pg.font.init()
        self.font: str = "Consolas"
        """The text font to be used throughout the window."""

        ##List of UI elements.
        self.ui_elements: list[UIElement] = []
        """List of UI elements that the window draws and updates every 
        frame."""


    def __str__(self) -> str:
        screen_size = f"(X){self.width}px (Y){self.height}px"
        return (f"Window '{self.window_id}': title = {self.title},"
                f" size = {screen_size}")


    ##A little shorthand for getting width and height.
    @property
    def width(self) -> int:
        """The width of the windw in pixels."""
        return self.screen_size[0]

    @property
    def height(self) -> int:
        """The height of the windw in pixels."""
        return self.screen_size[1]


    def start(self):
        """
        Overwrite this function to add code that runs when the window starts.
        This is a good place to put UI elements and instance variables.
        
        No need to worry about calling::

            super().start()

        Because it doesn't do anything by default.
        """
        pass


    def add_ui_element(self, ui_element: UIElement) -> None:
        """Adds a UI element to the window."""
        self.ui_elements.append(ui_element)
        ui_element.window = self


    def add_ui_elements(self, ui_elements: list) -> None:
        """Adds multiple UI elements to the window."""
        for ui_element in ui_elements:
            self.ui_elements.append(ui_element)
            ui_element.window = self


    def remove_ui_element(self, ui_element: UIElement) -> None:
        """Removes a UI element from the window."""
        self.ui_elements.remove(ui_element)


    def update(self):
        """
        Overwrite this function to add code that runs every frame.
        This is a good place to update variables and perform any calculations
        necessary before drawing.
        
        No need to worry about calling::

            super().update()

        Because it doesn't do anything by default.
        """
        pass


    def _update(self) -> None:
        """Called every frame"""
        ##Get events. 
        ##In try except because program crashes on close otherwise.
        try:
            self.events = pg.event.get()
        except pg.error:
            self._end()

        ##Close window if close button clicked or parent stops running.
        if (
            any(event.type == pg.QUIT for event in self.events) 
            or not self.parent.running
           ):
            self._end()
            return
        
        ##Update the window's UI elements.
        for ui_element in self.ui_elements:
            ui_element.update()

        ##Call user defined update.
        self.update()


    def draw(self):
        """
        Overwrite this function to add code that runs every frame.
        This is where any drawing code goes.
        
        No need to worry about calling::

            super().draw()

        Because it doesn't do anything by default.
        """
        pass
    

    def _draw(self) -> None:
        """Called every frame and draws the window."""
        if not self.parent.running:
            return

        ##Fills the screen. Drawing code run before this will not display.
        self.screen.fill(self.colours[0])

        ##Draws each of the UI elements in the window.
        for ui_element in self.ui_elements:
            ui_element.draw()

        ##Call user defined draw function.
        self.draw()

        ##Displays what's been drawn.
        pg.display.flip()


    def run(self) -> None:
        """
        Starts the window running. This is called once when the window is
        first opened."""
        self.running = True
        self.setup()

        ##User defined start function.
        if not self.loaded:
            self.loaded = True
            self.start()

        while self.running:
            self._run()
            self.clock.tick(self.parent.fps)


    def setup(self) -> None:
        """
        Sets the window up. If this isn't called before the window is
        opened it will retain the old window's size and title."""
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption(self.title)
        

    def _run(self) -> None:
        """
        Runs the window. This function contains anything that needs to
        happen every frame."""     
        self._update()
        self._draw()


    def _end(self) -> None:
        """
        Closes the window. Any code that needs to happen before the window
        closes goes here."""
        if self.is_popup:
            self.parent.end()
        
        self.running = False


    def open_window(self, window_id):
        """
        Opens another window and then runs own setup method. This prevents
        window A from retaining window B's size when B is closed."""
        window = self.parent.get_window(window_id)
        window.run()
        self.setup()


    def update_colours(self, colours: list):
        self.colours = colours
        for element in self.ui_elements:
            element.update_colours()
