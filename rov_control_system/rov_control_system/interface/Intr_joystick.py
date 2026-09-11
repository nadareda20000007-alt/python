from zope.interface import Interface, Attribute

class IJoystick(Interface):
    """ Interface for Joystick class. """

    def get_place(axis):
        """
        Get the value of where the joystick is located.
        :return: The position value for that axis.
        """
        pass

    def get_button(button):
        """
        Find which button is pressed.
        :return: True if the button is pressed, False otherwise.
        """
        pass