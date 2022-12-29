import enum


# Colour: Object for colours
class Colour():
    def __init__(self, name: str, hex: int):
        self.name = name
        self.hex = hex


# ColourList: Enumeration of colours
class ColourList(enum.Enum):
    Red = Colour("red", "FF0000");
    DarkRed = Colour("dark-red", "8B0000")
    LightRed = Colour("light-red", "F08080")
    Orange = Colour("orange", "FFC000")
    DarkOrange = Colour("dark-orange", "FF8C00")
    LightOrange = Colour("light-orange", "FFD966")
    Yellow = Colour("yellow", "FFFF00")
    LightYellow = Colour("light-yellow", "FFFFE0")
    DarkYellow = Colour("dark-yellow", "CC9900")
    Green = Colour("green", "008000")
    DarkGreen = Colour("dark-green", "00B050")
    LightGreen = Colour("light-green", "A9D08E")
    Blue = Colour("blue", "00B0F0")
    LightBlue = Colour("light-blue", "BDD7EE")
    DarkBlue = Colour("dark-blue", "4472C4")
    Purple = Colour("purple", "FF3399")
    DarkPurple = Colour("dark-purple", "8B008B")
    LightPurple = Colour("light-purple", "FF99FF")
    Grey = Colour("grey", "808080")
    DarkGrey = Colour("dark-grey", "A9A9A9")
    LightGrey = Colour("light-grey", "D3D3D3")
    Brown = Colour("brown", "A52A2A")
    DarkBrown = Colour("dark-brown", "800000")
    LightBrown = Colour("light-brown", "CC6600")
    RedOrange = Colour("red-orange", "FF6600")
    DarkRedOrange = Colour("dark-red-orange", "B34700")
    LightRedOrange = Colour("light-red-orange", "FFB380")
    YellowOrange = Colour("yellow-orange", "FFCC00")
    DarkYellowOrange = Colour("dark-yellow-orange", "CCA300")
    LightYellowOrange = Colour("light-yellow-orange", "FFE066")
    Lime = Colour("lime", "CCFF33")
    DarkLime = Colour("dark-lime", "66CC00")
    LightLime = Colour("light-lime", "BFFF80")
    Turquoise = Colour("turquoise", "40E0D0")
    DarkTurquoise = Colour("dark-turquoise", "00CED1")
    LightTurquoise = Colour("light-turquoise", "AFEEEE")
    BluePurple = Colour("blue-purple", "6666FF")
    DarkBluePurple = Colour("dark-blue-purple", "7300E6")
    LightBluePurple = Colour("light-blue-purple", "D9B3FF")
    Pink = Colour("pink", "F8CBAD")
    DarkPink = Colour("dark-pink", "FF1493")
    LightPink = Colour("light-pink", "FFB6C1")
    White = Colour("white", "FFFFFF")
    Black = Colour("black", "000000")
