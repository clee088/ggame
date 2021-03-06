"""
# ggame
The simple cross-platform sprite and game platform for Brython Server (Pygame, Tkinter to follow?).

Ggame stands for a couple of things: "good game" (of course!) and also "git game" or "github game" 
because it is designed to operate with [Brython Server](http://runpython.com) in concert with
Github as a backend file store.

Ggame is **not** intended to be a full-featured gaming API, with every bell and whistle. Ggame is
designed primarily as a tool for teaching computer programming, recognizing that the ability
to create engaging and interactive games is a powerful motivator for many progamming students.
Accordingly, any functional or performance enhancements that *can* be reasonably implemented 
by the user are left as an exercise. 

## Functionality Goals

The ggame library is intended to be trivially easy to use. For example:

    from ggame import App, ImageAsset, Sprite
  
    # Create a displayed object at 100,100 using an image asset
    Sprite(ImageAsset("ggame/bunny.png"), (100,100))
    # Create the app, with a 500x500 pixel stage
    app = App(500,500)  
    # Run the app
    app.run()
    
## Extensions

The `ggame` library has been extended with [ggmath](/ggame/ggmath.html) for geometry
exploration in a manner reminiscent of Geogebra, and [ggrocket](/ggame/ggrocket.html)
for tools and classes to use with rocket and orbital simulations.

## Overview

There are three major components to the `ggame` system: Assets, Sprites and the App.

### Assets

Asset objects (i.e. `ggame.ImageAsset`, etc.) typically represent separate files that
are provided by the "art department". These might be background images, user interface
images, or images that represent objects in the game. In addition, `ggame.SoundAsset` 
is used to represent sound files (`.wav` or `.mp3` format) that can be played in the 
game.

Ggame also extends the asset concept to include graphics that are generated dynamically
at run-time, such as geometrical objects, e.g. rectangles, lines, etc.

### Sprites

All of the visual aspects of the game are represented by instances of `ggame.Sprite` or
subclasses of it. 

### App

Every ggame application must create a single instance of the `ggame.App` class (or 
a sub-class of it). Creating an instance of the `ggame.App` class will initiate 
creation of a pop-up window on your browser. Executing the app's `run` method will
begin the process of refreshing the visual assets on the screen. 

### Events

No game is complete without a player and players produce events. Your code handles user
input by registering to receive keyboard and mouse events using `ggame.App.listenKeyEvent` and
`ggame.App.listenMouseEvent` methods.

## Execution Environment

Ggame is designed to be executed in a web browser using [Brython](http://brython.info/),
[Pixi.js](http://www.pixijs.com/) and [Buzz](http://buzz.jaysalvat.com/). The easiest
way to do this is by executing from [runpython](http://runpython.com), with source
code residing on [github](http://github.com).

To use Ggame in your own application, you may create a folder called
`ggame` in your project. Within `ggame`, copy the `ggame.py`, `sysdeps.py` and 
`__init__.py` files from the [ggame project](https://github.com/BrythonServer/ggame).

When using `ggame` from within [runpython](http://runpython.com), the Github
`ggame` repository is automatically placed on the import search path.

## Geometry

When referring to screen coordinates, note that the x-axis of the computer screen
is *horizontal* with the zero position on the left hand side of the screen. The 
y-axis is *vertical* with the zero position at the **top** of the screen.

Increasing positive y-coordinates correspond to the downward direction on the 
computer screen. Note that this is **different** from the way you may have learned
about x and y coordinates in math class!

"""

import math

try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

class Frame(object):
    """
    Frame is a utility class for expressing the idea of a rectangular region.
    """
    
    def __init__(self, x, y, w, h):
        """
        Initialization for the `ggame.Frame` objects.

        `x` and `y` are coordinates of the upper left hand corner of the frame.
 
        `w` and `h` are the width and height of the frame rectangle.
        """

        self.GFX = GFX_Rectangle(x,y,w,h)
        """
        `GFX` is a reference to the underlying object provided by the system.
        """
        self.x = x
        """
        X-coordinate of the upper left hand corner of this `ggame.Frame`.
        """
        self.y = y
        """
        Y-coordinate of the upper left hand corner of this `ggame.Frame`.
        """
        self.w = w
        """
        Width of the `ggame.Frame`.
        """
        self.h = h
        """
        Height of the `ggame.Frame`.
        """
    
    @property
    def x(self):
        return self.GFX.x
    
    @x.setter
    def x(self, value):
        self.GFX.x = value
        
    @property
    def y(self):
        return self.GFX.y
    
    @y.setter
    def y(self, value):
        self.GFX.y = value
    
    @property
    def w(self):
        return self.GFX.width
    
    @w.setter
    def w(self, value):
        self.GFX.width = value
        
    @property
    def h(self):
        return self.GFX.height
        
    @h.setter
    def h(self, value):
        self.GFX.height = value
    
    @property
    def center(self):
        """
        `center` property computes a coordinate pair (tuple) for the 
        center of the frame.

        The `center` property, when set, redefines the `x` and `y` properties
        of the frame in order to make the center agree with the coordinates
        (tuple) assigned to it.
        """

        return (self.x + self.w//2, self.y + self.h//2)
    
    @center.setter
    def center(self, value):
        c = self.center
        self.x += value[0] - c[0]
        self.y += value[1] - c[1]

class _Asset(object):
    """
    Base class for all game asset objects.
    
    The `ggame.Asset` class is set up to understand the concept
    of multiple instances of an asset. This is currently only used for image-based
    assets.
    """

    def __init__(self):
        self.GFXlist = [None,]
        """A list of the underlying system objects used to represent this asset."""

    @property
    def GFX(self):
        """
        `GFX` property represents the underlying system object used to represent
        this asset. If this asset is composed of multiple assets, then the **first**
        asset is referenced by `GFX`.
        """
        return self.GFXlist[0]
        
    @GFX.setter
    def GFX(self, value):
        self.GFXlist[0] = value
        
    def __len__(self):
        return len(self.GFXlist)
        
    def __getitem__(self, key):
        return self.GFXlist[key]
        
    def __setitem__(self, key, value):
        self.GFXlist[key] = value
        
    def __iter__(self):
        class Iter():
            def __init__(self, image):
                self.obj = image
                self.n = len(image.GFXlist)
                self.i = 0
                
            def __iter__(self):
                return self
                
            def __next__(self):
                if self.i ==self.n:
                    raise StopIteration
                self.i += 1
                return self.obj.GFXlist[self.i]
        return Iter(self)

    def destroy(self):
        if hasattr(self, 'GFX'):
            try:
                for gfx in self.GFXlist:
                    try:
                        gfx.destroy(True)
                    except:
                        pass
            except:
                pass
        
        
class ImageAsset(_Asset):
    """
    The `ImageAsset` class connects ggame to a specific image **file**.
    """

    def __init__(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        All `ggame.ImageAsset` instances must specify a file name or url with
        the `url` parameter.

        If the desired sprite image exists in only a smaller sub-section of the 
        original image, then the are can be specified by providing the
        `frame` parameter, which must be a valid `ggame.Frame` object.

        If image file actually is a *collection* of images, such as a so-called
        *sprite sheet*, then the `ImageAsset` class supports defining a list
        of images, provided they exist in the original image as a **row**
        of evenly spaced images or a **column** of images. To specify this,
        provide the `qty` (quantity) of images in the row or column, the
        `direction` of the list ('horizontal' or 'vertical' are supported),
        and an optional `margin`, if there is a gap between successive 
        images. When used in this way, the `frame` parameter must define the
        area of the **first** image in the collection; all subsequent images
        in the list are assumed to be the same size.
        """
        super().__init__()
        self.url = url
        """
        A string that represents the path or url of the original file.
        """
        del self.GFXlist[0]
        self.width = self.height = 0
        self.append(url, frame, qty, direction, margin)

    def _subframe(self, texture, frame):
        return GFX_Texture(texture, frame.GFX)
        
    def append(self, url, frame=None, qty=1, direction='horizontal', margin=0):
        """
        Append a texture asset from a new image file (or url). This method
        allows you to build a collection of images into an asset (such as you
        might need for an animated sprite), but without using a single 
        sprite sheet image.

        The parameters for the `append` method are identical to those 
        supplied to the `ggame.ImageAsset` initialization method. 

        This method allows you to build up an asset that consists of 
        multiple rows or columns of images in a sprite sheet or sheets.
        """
        GFX = GFX_Texture_fromImage(url, False)
        dx = 0
        dy = 0
        for i in range(qty):
            if not frame is None:
                self.width = frame.w
                self.height = frame.h
                if direction == 'horizontal':
                    dx = frame.w + margin
                elif direction == 'vertical':
                    dy = frame.h + margin
                f = Frame(frame.x + dx * i, frame.y + dy * i, frame.w, frame.h)
                GFX = self._subframe(GFX, f)
            else:
                self.width = GFX.width
                self.height = GFX.height
            self.GFXlist.append(GFX)


class Color(object):
    """
    The `ggame.Color` class is used to represent colors and/or colors with
    transparency.
    """

    def __init__(self, color, alpha):
        """
        A `ggame.Color` instance must specify both a `color` as an integer
        in the conventional format (usually as a hexadecimal literal, e.g.
        0xffbb33 that represents the three color components, red, green 
        and blue), and a transparency value, or `alpha` as a floating
        point number in the range of 0.0 to 1.0 where 0.0 represents 
        completely transparent and 1.0 represents completely solid.

        Example: `red = Color(0xff0000, 1.0)`

        """
        self.color = color
        self.alpha = alpha
        
    def __eq__(self, other):
        return type(self) is type(other) and self.color == other.color and self.alpha == other.alpha
        
black = Color(0, 1.0)
"""
Default black color
"""
white = Color(0xffffff, 1.0)
"""
Default white color
"""

class LineStyle(object):
    """
    The `ggame.LineStyle` class is used to represent line style when
    drawing geometrical objects such as rectangles, ellipses, etc.
    """
    
    def __init__(self, width, color):
        """
        When creating a `ggame.LineStyle` instances you must specify 
        the `width` of the line in pixels and the `color` as a valid
        `ggame.Color` instance.

        Example: `line = LineStyle(3, Color(0x00ff00, 1.0))` will define
        a 3 pixel wide green line.
        """
        self.width = width
        self.color = color

    def __eq__(self, other):
        return type(self) is type(other) and self.width == other.width and self.color == other.color

blackline = LineStyle(1, black)
"""
Default thin black line
"""
whiteline = LineStyle(1, white)
"""
Default thin white line
"""

class _GraphicsAsset(_Asset):
    
    def __init__(self):
        super().__init__()
        GFX_Graphics.clear()
        

class _CurveAsset(_GraphicsAsset):

    def __init__(self, line):
        super().__init__()
        GFX_Graphics.lineStyle(line.width, line.color.color, line.color.alpha)

class _ShapeAsset(_CurveAsset):

    def __init__(self, line, fill):
        super().__init__(line)
        GFX_Graphics.beginFill(fill.color, fill.alpha)
    

class RectangleAsset(_ShapeAsset):
    """
    The `ggame.RectangleAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    """

    def __init__(self, width, height, line=blackline, fill=black):
        """
        Creation of a `ggame.RectangleAsset` requires specification of the 
        rectangle `width` and `height` in pixels, the `line` (as a proper
        `ggame.LineStyle` instance) and fill properties (as a `ggame.Color`
        instance).
        """
        super().__init__(line, fill)
        self.width = width
        self.height = height
        self.GFX = GFX_Graphics.drawRect(0, 0, self.width, self.height).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        

class CircleAsset(_ShapeAsset):
    """
    The `ggame.CircleAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    """    

    def __init__(self, radius, line=blackline, fill=black):
        """
        Creation of a `ggame.CircleAsset` requires specification of the circle
        `radius` in pixels, the `line` (as a proper `ggame.LineStyle` instance)
        and fill properties (as a `ggame.Color` instance).
        """
        super().__init__(line, fill)
        self.radius = radius
        self.GFX = GFX_Graphics.drawCircle(0, 0, self.radius).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class EllipseAsset(_ShapeAsset):
    """
    The `ggame.EllipseAsset` is a "virtual" asset that is created on the 
    fly without requiring creation of an image file.
    """

    def __init__(self, halfw, halfh, line=blackline, fill=black):
        """
        Creation of a `ggame.EllipseAsset` requires specification of the ellipse
        `halfw`, or semi-axis length in the horizontal direction (half of the
        ellipse width) and the `halfh`, or semi-axis length in the vertical direction.
        `line` (as `ggame.LineStyle` instance) and `fill` (as `ggame.Color` instance)
        must also be provided.
        """
        super().__init__(line, fill)
        self.halfw = halfw
        self.halfh = halfh
        self.GFX = GFX_Graphics.drawEllipse(0, 0, self.halfw, self.halfh).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
        
class PolygonAsset(_ShapeAsset):
    """
    The `ggame.PolygonAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file.
    """

    def __init__(self, path, line=blackline, fill=black):
        """
        Creation of a `ggame.PolygonAsset` requires specification of a 
        `path` consisting of a list of coordinate tuples. `line` and 
        `fill` arguments (instances of `ggame.LineStyle` and `ggame.Color`,
        respectively) must also be supplied. The final coordinate in the 
        list must be the same as the first.

        Example: `poly = PolygonAsset([(0,0), (50,50), (50,100), (0,0)], linesty, fcolor)`
        """
        super().__init__(line, fill)
        self.path = path
        jpath = []
        for point in self.path:
            jpath.extend(point)
        self.GFX = GFX_Graphics.drawPolygon(jpath).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False
    

class LineAsset(_CurveAsset):
    """
    The `ggame.LineAsset` is a "virtual" asset that is created on the
    fly without requiring creation of an image file. A `LineAsset` instance
    represents a single line segment.
    """

    def __init__(self, x, y, line=blackline):
        """
        Creation of a `ggame.LineAsset` requires specification of an `x` and
        `y` coordinate for the endpoint of the line. The starting point of the
        line is implied as coordinates (0,0). Note that when this asset is 
        used in a `ggame.Sprite` class, the sprite's `x` and `y` coordinates
        will control the location of the line segment on the screen.

        As the `ggame.LineAsset` does not cover a region, only a `ggame.LineStyle` 
        argument must be supplied (`line`).
        """
        super().__init__(line)
        self.deltaX = x
        """This attribute represents the `x` parameter supplied during instantiation."""
        self.deltaY = y
        """This attribute represents the `y` parameter supplied during instantiation."""
        GFX_Graphics.moveTo(0, 0)
        self.GFX = GFX_Graphics.lineTo(self.deltaX, self.deltaY).clone()
        """The `GFX` property represents the underlying system object."""
        self.GFX.visible = False

class TextAsset(_GraphicsAsset):
    """
    The `ggame.TextAsset` is a "virtual" asset that is created on the fly
    without requiring creation of an image file. A `TextAsset` instance
    represents a block of text, together with its styling (font, color, etc.).
    """
 
    def __init__(self, text, **kwargs):
        """
        The `ggame.TextAsset` must be created with a string as the `text` parameter.
        
        The remaining optional arguments must be supplied as keyword parameters. These
        parameters are described under the class attributes, below:
        """
        super().__init__()
        self.text = text
        self.style = kwargs.get('style', '20px Arial')
        """A string that specifies style, size and typeface (e.g. `'italic 20pt Helvetica'` or `'20px Arial'`)"""
        width = kwargs.get('width', 100)
        """Width of the text block on the screen, in pixels."""
        self.fill = kwargs.get('fill', Color(0, 1))
        """A valid `ggame.Color` instance that specifies the color and transparency of the text."""
        self.align = kwargs.get('align', 'left')
        """The alignment style of the text. One of: `'left'`, `'center'`, or `'right'`."""
        self.GFX = GFX_Text(self.text, 
            {'font': self.style,
                'fill' : self.fill.color,
                'align' : self.align,
                'wordWrap' : True,
                'wordWrapWidth' : width,
                })
        """The `GFX` property represents the underlying system object."""
        self.GFX.alpha = self.fill.alpha
        self.GFX.visible = False
        
    def _clone(self):
        return type(self)(self.text,
            style = self.style,
            width = self.width,
            fill = self.fill,
            align = self.align)
    
    @property
    def width(self):
        return self.GFX.width
        
    @property
    def height(self):
        return self.GFX.height


class Sprite(object):
    """
    The `ggame.Sprite` class combines the idea of a visual/graphical asset, a
    position on the screen, and *behavior*. Although the `ggame.Sprite` can be
    used as-is, it is generally subclassed to give it the desired behavior.

    When subclassing the `ggame.Sprite` class, you may customize the initialization
    code to use a specific asset. A 'step' or 'poll' method may be added
    for handling per-frame actions (e.g. checking for collisions). Step or poll
    functions are not automatically called by the `ggame.App` class, but you
    may subclass the `ggame.App` class in order to do this.

    Furthermore, you may wish to define event callback methods in your customized
    sprite class. With customized creation, event handling, and periodic processing
    you can achieve fully autonomous behavior for your class. 
    """
 
    _rectCollision = "rect"
    _circCollision = "circ"
    
    def __init__(self, asset, pos=(0,0), edgedef=None):
        """
        The `ggame.Sprite` must be created with an existing graphical `asset`.
        
        An optional `pos` or position may be provided, which specifies the 
        starting (x,y) coordinates of the sprite on the screen. By default,
        the position of a sprite defines the location of its upper-left hand
        corner. This behavior can be modified by customizing the `center` of
        the sprite.
        
        An optional `edgedef` or edge definition may be provided, which
        specifies an asset that will be used to define the boundaries of
        the sprite for the purpose of collision detection. If no `edgedef` 
        asset is given, the Sprite asset is used, which will be a rectangular
        asset in the case of an image texture. This option is typically used
        to define a visible image outline for a texture-based sprite that has
        a transparent texture image background.
        
        Example: player = Sprite(ImageAsset("player.png", (100,100), CircleAsset(50))
        
        This creates a sprite using the `player.png` image, positioned with its
        upper left corner at coordinates (100,100) and with a 50 pixel radius 
        circular collision border. 
        """
        self._index = 0
        if type(asset) == ImageAsset:
            self.asset = asset
            try:
                #self.GFX = GFX_Sprite()
                self.GFX = GFX_Sprite(asset.GFX) # GFX is PIXI Sprite
            except:
                self.GFX = None
        elif type(asset) in [RectangleAsset, 
            CircleAsset, 
            EllipseAsset, 
            PolygonAsset,
            LineAsset,
            ]:
            self.asset = asset
            self.GFX = GFX_Sprite(asset.GFX.generateTexture())
            #self.GFX = asset.GFX.clone() # GFX is PIXI Graphics (from Sprite)
            #self.GFX.visible = True
        elif type(asset) in [TextAsset]:
            self.asset = asset._clone()
            self.GFX = self.asset.GFX # GFX is PIXI Text (from Sprite)
            self.GFX.visible = True
        if not edgedef:
            self.edgedef = asset
        else:
            self.edgedef = edgedef
        self.xmin = self.xmax = self.ymin = self.ymax = 0
        self.position = pos
        """Tuple indicates the position of the sprite on the screen."""
        self._extentsdirty = True
        """Boolean indicates if extents must be calculated before collision test"""
        self._createBaseVertices()
        self._setExtents()
        """Initialize the extents (xmax, xmin, etc.) for collision detection"""
        App._add(self)
        
    def _createBaseVertices(self):
        """
        Create sprite-relative list of vertex coordinates for boundary
        """
        self._basevertices = []
        assettype = type(self.edgedef)
        if assettype in [RectangleAsset, ImageAsset, TextAsset]:
            self._basevertices = [(0,0), 
                (0,self.edgedef.height), 
                (self.edgedef.width,self.edgedef.height),
                (self.edgedef.width,0)]
        elif assettype is PolygonAsset:
            self._basevertices = self.edgedef.path[:-1]
        elif assettype is LineAsset:
            self._basevertices = [(0,0), 
                (self.edgedef.deltaX, self.edgedef.deltaY)]
        elif assettype is EllipseAsset:
            w = self.edgedef.halfw * 2
            h = self.edgedef.halfh * 2
            self._basevertices = [(0,0), (0,h), (w,h), (w,0)]

    def _xformVertices(self):
        """
        Create window-relative list of vertex coordinates for boundary
        """
        # find center as sprite-relative points (note sprite may be scaled)
        x = self.width * self.fxcenter / self.scale
        y = self.height * self.fycenter / self.scale
        if self.scale != 1.0:
            sc = self.scale
            # center-relative, scaled coordinates
            crsc = [((xp-x)*sc,(yp-y)*sc) for xp,yp in self._basevertices]
        else:
            crsc = [(xp-x,yp-y) for xp,yp in self._basevertices]
            
        # absolute, rotated coordinates
        c = math.cos(self.rotation)
        s = math.sin(self.rotation)
        self._absolutevertices = [(self.x + x*c + y*s, self.y + -x*s + y*c) 
                                    for x,y in crsc]


    def _setExtents(self):
        """
        update min/max x and y based on position, center, width, height
        """
        if self._extentsdirty:
            if type(self.asset) is CircleAsset:
                th = math.atan2(
                    self.fycenter - 0.5, 0.5 - self.fxcenter) + self.rotation
                D = self.width
                L = math.sqrt(math.pow(self.fxcenter - 0.5, 2) + 
                    math.pow(self.fycenter - 0.5, 2)) * D
                self.xmin = self.x + int(L*math.cos(th)) - D//2
                self.ymin = self.y - int(L*math.sin(th)) - D//2
                self.xmax = self.xmin + D
                self.ymax = self.ymin + D
            else:
                # Build vertex list
                self._xformVertices()
                x, y = zip(*self._absolutevertices)
                self.xmin = min(x)
                self.xmax = max(x)
                self.ymin = min(y)
                self.ymax = max(y)
            self._extentsdirty = False

    def firstImage(self):
        """
        Select and display the *first* image used by this sprite.
        """
        self.GFX.texture = self.asset[0]
    
    def lastImage(self):
        """
        Select and display the *last* image used by this sprite.
        """
        self.GFX.texture = self.asset[-1]
    
    def nextImage(self, wrap = False):
        """
        Select and display the *next* image used by this sprite.
        If the current image is already the *last* image, then
        the image is not advanced.

        If the optional `wrap` parameter is set to `True`, then calling
        `ggame.Sprite.nextImage` on the last image will cause the *first*
        image to be loaded.
        """
        self._index += 1
        if self._index >= len(self.asset):
            if wrap:
                self._index = 0
            else:
                self._index = len(self.asset)-1
        self.GFX.texture = self.asset[self._index]
    
    def prevImage(self, wrap = False):
        """
        Select and display the *previous* image used by this sprite.
        If the current image is already the *first* image, then
        the image is not changed.

        If the optional `wrap` parameter is set to `True`, then calling
        `ggame.Sprite.prevImage` on the first image will cause the *last*
        image to be loaded.
        """
        self._index -= 1
        if self._index < 0:
            if wrap:
                self._index = len(self.asset)-1
            else:
                self._index = 0
        self.GFX.texture = self.asset[self._index]
    
    def setImage(self, index=0):
        """
        Select the image to display by giving its `index`, where an index
        of zero represents the *first* image in the asset.

        This is equivalent to setting the `ggame.Sprite.index` property
        directly.
        """
        self.index = index

    def rectangularCollisionModel(self):
        """
        Obsolete. No op.
        """
        pass
    
    def circularCollisionModel(self):
        """
        Obsolete. No op.
        """
        pass
    
    

    @property
    def index(self):
        """This is an integer index in to the list of images available for this sprite."""
        return self._index
        
    @index.setter
    def index(self, value):
        self._index = value
        try:
            self.GFX.texture = self.asset[self._index]
        except:
            self._index = 0
            self.GFX.texture = self.asset[self._index]

    @property
    def width(self):
        """
        This is an integer representing the display width of the sprite.
        Assigning a value to the width will scale the image horizontally.
        """
        return self.GFX.width
        
    @width.setter
    def width(self, value):
        self.GFX.width = value
        self._extentsdirty = True
    
    @property
    def height(self):
        """
        This is an integer representing the display height of the sprite.
        Assigning a value to the height will scale the image vertically.
        """
        return self.GFX.height
    
    @height.setter
    def height(self, value):
        self.GFX.height = value
        self._extentsdirty = True
        
    @property
    def x(self):
        """
        This represents the x-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite horizontally.
        """
        return self.GFX.position.x
        
    @x.setter
    def x(self, value):
        deltax = value - self.GFX.position.x
        self.xmax += deltax
        self.xmin += deltax
        """Adjust extents directly with low overhead"""
        self.GFX.position.x = value

    @property
    def y(self):
        """
        This represents the y-coordinate of the sprite on the screen. Assigning
        a value to this attribute will move the sprite vertically.
        """
        return self.GFX.position.y
        
    @y.setter
    def y(self, value):
        deltay = value - self.GFX.position.y
        self.ymax += deltay
        self.ymin += deltay
        """Adjust extents directly with low overhead"""
        self.GFX.position.y = value

    @property
    def position(self):
        """
        This represents the (x,y) coordinates of the sprite on the screen. Assigning
        a value to this attribute will move the sprite to the new coordinates.
        """
        return (self.GFX.position.x, self.GFX.position.y)
        
    @position.setter
    def position(self, value):
        self.x, self.y = value

    @property
    def fxcenter(self):
        """
        This represents the horizontal position of the sprite "center", as a floating
        point number between 0.0 and 1.0. A value of 0.0 means that the x-coordinate
        of the sprite refers to its left hand edge. A value of 1.0 refers to its 
        right hand edge. Any value in between may be specified. Values may be assigned
        to this attribute. 
        """
        try:
            return self.GFX.anchor.x
            self._extentsdirty = True
        except:
            return 0.0
        
    @fxcenter.setter
    def fxcenter(self, value):
        """
        Float: 0-1
        """
        try:
            self.GFX.anchor.x = value
            self._extentsdirty = True
        except:
            pass
        
    @property
    def fycenter(self):
        """
        This represents the vertical position of the sprite "center", as a floating
        point number between 0.0 and 1.0. A value of 0.0 means that the x-coordinate
        of the sprite refers to its top edge. A value of 1.0 refers to its 
        bottom edge. Any value in between may be specified. Values may be assigned
        to this attribute. 
        """
        try:
            return self.GFX.anchor.y
        except:
            return 0.0
        
    @fycenter.setter
    def fycenter(self, value):
        """
        Float: 0-1
        """
        try:
            self.GFX.anchor.y = value
            self._extentsdirty = True
        except:
            pass
    
    @property
    def center(self):
        """
        This attribute represents the horizontal and vertical position of the 
        sprite "center" as a tuple of floating point numbers. See the 
        descriptions for `ggame.Sprite.fxcenter` and `ggame.Sprite.fycenter` for 
        more details.
        """
        try:
            return (self.GFX.anchor.x, self.GFX.anchor.y)
        except:
            return (0.0, 0.0)
        
    @center.setter
    def center(self, value):
        try:
            self.GFX.anchor.x = value[0]
            self.GFX.anchor.y = value[1]
            self._extentsdirty = True
        except:
            pass
    
    @property
    def visible(self):
        """
        This boolean attribute may be used to change the visibility of the sprite. Setting
        `ggame.Sprite.visible` to `False` will prevent the sprite from rendering on the 
        screen.
        """
        return self.GFX.visible
    
    @visible.setter
    def visible(self, value):
        self.GFX.visible = value

    @property
    def scale(self):
        """
        This attribute may be used to change the size of the sprite ('scale' it) on the 
        screen. Value may be a floating point number. A value of 1.0 means that the sprite
        image will keep its original size. A value of 2.0 would double it, etc.
        """
        try:
            return self.GFX.scale.x
        except AttributeError:
            return 1.0
        
    @scale.setter
    def scale(self, value):
        self.GFX.scale.x = value
        self.GFX.scale.y = value
        self._extentsdirty = True

    @property
    def rotation(self):
        """
        This attribute may be used to change the rotation of the sprite on the screen.
        Value may be a floating point number. A value of 0.0 means no rotation. A value 
        of 1.0 means  a rotation of 1 radian in a counter-clockwise direction. One radian
        is 180/pi or approximately 57.3 degrees.
        """
        try:
            return -self.GFX.rotation
        except AttributeError:
            return 0.0
        
    @rotation.setter
    def rotation(self, value):
        self.GFX.rotation = -value
        if value:
            self._extentsdirty = True

    @classmethod
    def collidingCircleWithPoly(cls, circ, poly):
        return True
    
    def collidingPolyWithPoly(self, obj):
        return True

    def collidingWith(self, obj):
        """
        Return a boolean True if this sprite is currently overlapping the sprite 
        referenced by `obj`. Returns False if checking for collision with 
        itself. Returns False if extents of object make it impossible for
        collision to occur. Returns True if sprite's `edgedef` parameter overlaps
        with other sprite's `edgedef` parameter, taking into consideration both
        sprites' center, rotation and scale settings.
        """
        if self is obj:
            return False
        else:
            self._setExtents()
            obj._setExtents()
            # Gross check for overlap will usually rule out a collision
            if (self.xmin > obj.xmax
                or self.xmax < obj.xmin
                or self.ymin > obj.ymax
                or self.ymax < obj.ymin):
                return False
            # Otherwise, perform a careful overlap determination
            elif type(self.asset) is CircleAsset:
                if type(obj.asset) is CircleAsset:
                    # two circles .. check distance between
                    sx = (self.xmin + self.xmax) / 2
                    sy = (self.ymin + self.ymax) / 2
                    ox = (obj.xmin + obj.xmax) / 2
                    oy = (obj.ymin + obj.ymax) / 2
                    d = math.sqrt((sx-ox)**2 + (sy-oy)**2)
                    return d <= self.width/2 + obj.width/2
                else:
                    return self.collidingCircleWithPoly(self, obj)
            else:
                if type(obj.asset) is CircleAsset:
                    return self.collidingCircleWithPoly(obj, self)
                else:
                    return self.collidingPolyWithPoly(obj)
                
                

    def collidingWithSprites(self, sclass = None):
        """
        Return a list of sprite objects identified by the `sclass` parameter
        that are currently colliding with (that is, with which the `ggame.Sprite.collidingWith`
        method returns True) this sprite. If `sclass` is set to `None` (default), then
        all other sprites are checked for collision, otherwise, only sprites whose
        class matches `sclass` are checked.
        """
        if sclass is None:
            slist = App.spritelist
        else:
            slist = App.getSpritesbyClass(sclass)
        return list(filter(self.collidingWith, slist))

    def destroy(self):
        """
        Call the `ggame.Sprite.destroy` method to prevent the sprite from being displayed,
        or checked in collision detection. If you only want to prevent a sprite from being
        displayed, set the `ggame.Sprite.visible` attribute to `False`.
        """
        App._remove(self)
        self.GFX.destroy()


class SoundAsset(object):
    """
    Class representing a single sound asset (sound file, such as .mp3 or .wav).
    """    
    def __init__(self, url):
        """
        Create a `ggame.SoundAsset` instance by passing in the URL or file name
        of the desired sound. Sound file formats may include `.wav` or `.mp3`, subject
        to browser compatibility. 
        """
        self.url = url
        """
        A string containing the url or name of the asset file.
        """

        
class Sound(object):
    """
    The `ggame.Sound` class represents a sound, with methods for controlling
    when and how the sound is played in the application.
    """

    def __init__(self, asset):
        """
        Pass a valid `ggame.SoundAsset` instance when creating a `ggame.Sound` object.
        """
        self.asset = asset
        """
        A reference to the `ggame.SoundAsset` instance.
        """
        self.SND = SND_Sound(self.asset.url)
        """
        A reference to the underlying sound object provided by the system.
        """
        self.SND.load()
        
    def play(self):
        """
        Play the sound once.
        """
        self.stop()
        self.SND.play()

    def loop(self):
        """
        Play the sound continuously, looping forever.
        """
        self.stop()
        self.SND.loop()
        self.SND.play()
        
    def stop(self):
        """
        Stop playing the sound.
        """
        self.SND.stop()
        
    @property
    def volume(self):
        """
        The `ggame.Sound.volume` property is a number ranging from 0-100, that 
        represents the volume or intensity of the sound when it is playing.
        """
        return self.SND.getVolume()
        
    @volume.setter
    def volume(self, value):
        self.SND.setVolume(value)
    

class _Event(object):

    def __init__(self, hwevent):
        self.hwevent = hwevent
        """The underlying system event object."""
        self.type = hwevent.type
        """String representing the type of received event."""
        self.consumed = False
        """
        Set the `consumed` member of the event to prevent the event
        from being received by any more handler methods.
        """
        
class MouseEvent(_Event):
    """
    The `ggame.MouseEvent` class encapsulates information regarding a user mouse
    action that is being reported by the system.
    """    

    mousemove = "mousemove"
    """Constant identifying a `mousemove` event."""
    mousedown = "mousedown"
    """Constant identifying a `mousedown` event."""
    mouseup = "mouseup"
    """Constant identifying a `mouseup` event."""
    click = "click"
    """Constant identifying a button `click` event."""
    dblclick = "dblclick"
    """Constant identifying a button `dblclick` event."""
    mousewheel = "wheel"
    """Constant identifying a mouse `wheel` scroll event."""
    
    def __init__(self, hwevent):
        """
        The event is initialized by the system, with a `hwevent` input parameter.
        """
        super().__init__(hwevent)
        self.wheelDelta = 0
        """Integer representing up/down motion of the scroll wheel."""
        if self.type == self.mousewheel:
            self.wheelDelta = hwevent.deltaY
        else:
            self.wheelDelta = 0
        rect = App._win._renderer.view.getBoundingClientRect()
        xscale = App._win.width/rect.width
        yscale = App._win.height/rect.height
        self.x = (hwevent.clientX - rect.left) * xscale
        """The window x-coordinate of the mouse pointer when the event occurred."""
        self.y = (hwevent.clientY - rect.top) * yscale
        """The window y-coordinate of the mouse pointer when the event occurred."""


class KeyEvent(_Event):
    """
    The `ggame.KeyEvent` class encapsulates information regarding a user keyboard
    action that is being reported by the system.
    """    

    no_location = 0
    """Constant indicating no specific location for the key event."""
    right_location = 2
    """Constant indicating the key event was on the right hand side of the keyboard."""
    left_location = 1
    """Constant indicating the key event was on the left hand side of the keyboard."""
    keydown = "keydown"
    """Constant indicating the key was pressed down."""
    keyup = "keyup"
    """Constant indicating the key was released."""
    keypress = "keypress"
    """Constant indicating the combination of keydown, followed by keyup."""
    keys = {8: 'backspace',
        9: 'tab',
        13: 'enter',
        16: 'shift',
        17: 'ctrl',
        18: 'alt',
        19: 'pause/break',
        20: 'caps lock',
        27: 'escape',
        32: 'space',
        33: 'page up',
        34: 'page down',
        35: 'end',
        36: 'home',
        37: 'left arrow',
        38: 'up arrow',
        39: 'right arrow',
        40: 'down arrow',
        45: 'insert',
        46: 'delete',
        48: '0',
        49: '1',
        50: '2',
        51: '3',
        52: '4',
        53: '5',
        54: '6',
        55: '7',
        56: '8',
        57: '9',
        65: 'a',
        66: 'b',
        67: 'c',
        68: 'd',
        69: 'e',
        70: 'f',
        71: 'g',
        72: 'h',
        73: 'i',
        74: 'j',
        75: 'k',
        76: 'l',
        77: 'm',
        78: 'n',
        79: 'o',
        80: 'p',
        81: 'q',
        82: 'r',
        83: 's',
        84: 't',
        85: 'u',
        86: 'v',
        87: 'w',
        88: 'x',
        89: 'y',
        90: 'z',
        91: 'left window key',
        92: 'right window key',
        93: 'select key',
        96: 'numpad 0',
        97: 'numpad 1',
        98: 'numpad 2',
        99: 'numpad 3',
        100: 'numpad 4',
        101: 'numpad 5',
        102: 'numpad 6',
        103: 'numpad 7',
        104: 'numpad 8',
        105: 'numpad 9',
        106: 'multiply',
        107: 'add',
        109: 'subtract',
        110: 'decimal point',
        111: 'divide',
        112: 'f1',
        113: 'f2',
        114: 'f3',
        115: 'f4',
        116: 'f5',
        117: 'f6',
        118: 'f7',
        119: 'f8',
        120: 'f9',
        121: 'f10',
        122: 'f11',
        123: 'f12',
        144: 'num lock',
        145: 'scroll lock',
        186: 'semicolon',
        187: 'equal sign',
        188: 'comma',
        189: 'dash',
        190: 'period',
        191: 'forward slash',
        192: 'grave accent',
        219: 'open bracket',
        220: 'back slash',
        221: 'close bracket',
        222: 'single quote'}    
    """Dictionary mapping key code integers to textual key description."""
    
    def __init__(self, hwevent):
        """
        The event is initialized by the system, with a `hwevent` input parameter.
        """
        super().__init__(hwevent)
        self.keynum = hwevent.keyCode
        """The `keynum` attribute identifies a keycode (number)."""
        self.key = self.keys[hwevent.keyCode]
        """The `key` attribute identifes the key in text form (e.g. 'back slash')."""



class App(object):
    """
    The `ggame.App` class is a (typically subclassed) class that encapsulates
    handling of the display system, and processing user events. The `ggame.App` 
    class also manages lists of all `ggame.Sprite` instances in the application.

    When subclassing `ggame.App` you may elect to instantiate most of your
    sprite objects in the initialization section.

    Processing that must occur on a per-frame basis may be included by overriding
    the `ggame.App.step` method. This is also an appropriate location to call
    similar 'step' methods for your various customized sprite classes.

    Once your application class has been instantiated, begin the frame drawing
    process by calling its `ggame.App.run` method.

    NOTE: Only **one** instance of an `ggame.App` class or subclass may be 
    instantiated at a time.
    """
    spritelist = []
    """List of all sprites currently active in the application."""
    _eventdict = {}
    _spritesdict = {}
    _spritesadded = False
    _win = None

    def __init__(self, *args):
        """
        The `ggame.App` class is called either by specifying the desired app window size
        in pixels, as two parameters (e.g. `myapp = App(640,480)`), or by providing
        no size parameters at all (e.g. `myapp = App()`), in which case, the full browser
        window size is used.
        """
        if App._win == None and (len(args) == 0 or len(args) == 2):
            x = y = 0
            if len(args) == 2:
                x = args[0]
                y = args[1]
            App._win = GFX_Window(x, y, type(self)._destroy)
            self.width = App._win.width
            self.height = App._win.height
            # Add existing sprites to the window
            if not App._spritesadded and len(App.spritelist) > 0:
                App._spritesadded = True
                for sprite in App.spritelist:
                    App._win.add(sprite.GFX)
            App._win.bind(KeyEvent.keydown, self._keyEvent)
            App._win.bind(KeyEvent.keyup, self._keyEvent)
            App._win.bind(KeyEvent.keypress, self._keyEvent)
            App._win.bind(MouseEvent.mousewheel, self._mouseEvent)
            App._win.bind(MouseEvent.mousemove, self._mouseEvent)
            App._win.bind(MouseEvent.mousedown, self._mouseEvent)
            App._win.bind(MouseEvent.mouseup, self._mouseEvent)
            App._win.bind(MouseEvent.click, self._mouseEvent)
            App._win.bind(MouseEvent.dblclick, self._mouseEvent)

        
    def _routeEvent(self, event, evtlist):
        for callback in reversed(evtlist):
            if not event.consumed:
                callback(event)
        
    def _keyEvent(self, hwevent):
        evtlist = App._eventdict.get(
            (hwevent.type, KeyEvent.keys.get(hwevent.keyCode,0)), [])
        evtlist.extend(App._eventdict.get((hwevent.type, '*'), []))
        if len(evtlist) > 0:
            evt = KeyEvent(hwevent)
            self._routeEvent(evt, evtlist)
        return False

    def _mouseEvent(self, hwevent):
        evtlist = App._eventdict.get(hwevent.type, [])
        if len(evtlist) > 0:
            evt = MouseEvent(hwevent)
            self._routeEvent(evt, evtlist)
        return False

    @classmethod
    def _add(cls, obj):
        if App._win != None:
            App._win.add(obj.GFX)
        App.spritelist.append(obj)
        if type(obj) not in App._spritesdict:
            App._spritesdict[type(obj)] = []
        App._spritesdict[type(obj)].append(obj)

    @classmethod
    def _remove(cls, obj):
        if App._win != None:
            App._win.remove(obj.GFX)
        App.spritelist.remove(obj)
        App._spritesdict[type(obj)].remove(obj)
        
    def _animate(self, dummy):
        if self.userfunc:
            self.userfunc()
        else:
            self.step()
        App._win.animate(self._animate)

    @classmethod
    def _destroy(cls, *args):
        """
        This will close the display window/tab, remove all references to 
        sprites and place the `App` class in a state in which a new 
        application could be instantiated.
        """ 
        if App._win:
            App._win.unbind(KeyEvent.keydown)
            App._win.unbind(KeyEvent.keyup)
            App._win.unbind(KeyEvent.keypress)
            App._win.unbind(MouseEvent.mousewheel)
            App._win.unbind(MouseEvent.mousemove)
            App._win.unbind(MouseEvent.mousedown)
            App._win.unbind(MouseEvent.mouseup)
            App._win.unbind(MouseEvent.click)
            App._win.unbind(MouseEvent.dblclick)
            App._win.destroy()
        App._win = None
        for s in list(App.spritelist):
            s.destroy()
        App.spritelist = []
        App._spritesdict = {}
        App._eventdict = {}
        App._spritesadded = False

    @classmethod
    def listenKeyEvent(cls, eventtype, key, callback):
        """
        Register to receive keyboard events. The `eventtype` parameter is a 
        string that indicates what type of key event to receive (value is one
        of: `'keydown'`, `'keyup'` or `'keypress'`). The `key` parameter is a 
        string indicating which key (e.g. `'space'`, `'left arrow'`, etc.) to 
        receive events for. The `callback` parameter is a reference to a 
        function or method that will be called with the `ggame.KeyEvent` object
        when the event occurs.

        See the source for `ggame.KeyEvent.keys` for a list of key names
        to use with the `key` paramter.
        """
        evtlist = App._eventdict.get((eventtype, key), [])
        if not callback in evtlist:
            evtlist.append(callback)
        App._eventdict[(eventtype, key)] = evtlist

    @classmethod
    def listenMouseEvent(cls, eventtype, callback):
        """
        Register to receive mouse events. The `eventtype` parameter is
        a string that indicates what type of mouse event to receive (
        value is one of: `'mousemove'`, `'mousedown'`, `'mouseup'`, `'click'`, 
        `'dblclick'` or `'mousewheel'`). The `callback` parameter is a 
        reference to a function or method that will be called with the 
        `ggame.MouseEvent` object when the event occurs.
        """
        evtlist = App._eventdict.get(eventtype, [])
        if not callback in evtlist:
            evtlist.append(callback)
        App._eventdict[eventtype] = evtlist

    @classmethod
    def unlistenKeyEvent(cls, eventtype, key, callback):
        """
        Use this method to remove a registration to receive a particular
        keyboard event. Arguments must exactly match those used when
        registering for the event.
        """
        App._eventdict[(eventtype,key)].remove(callback)

    @classmethod
    def unlistenMouseEvent(cls, eventtype, callback):
        """
        Use this method to remove a registration to receive a particular
        mouse event. Arguments must exactly match those used when
        registering for the event.
        """
        App._eventdict[eventtype].remove(callback)

    @classmethod
    def getSpritesbyClass(cls, sclass):
        """
        Returns a list of all active sprites of a given class.
        """
        return App._spritesdict.get(sclass, [])
    
    def step(self):
        """
        The `ggame.App.step` method is called once per animation frame. Override
        this method in your own subclass of `ggame.App` to perform periodic 
        calculations, such as checking for sprite collisions, or calling
        'step' functions in your own customized sprite classes.

        The base class `ggame.App.step` method is empty and is intended to be overriden.
        """
        pass
    
    def run(self, userfunc = None):
        """
        Calling the `ggame.App.run` method begins the animation process whereby the 
        `ggame.App.step` method is called once per animation frame. Set `userfunc`
        to any function which shall be called once per animation frame.
        """
        self.userfunc = userfunc
        App._win.animate(self._animate)


        
if __name__ == '__main__':
    

    def test(event):
        print("BOOM")
        x = input("Enter something")
        print(x)

    def testm(event):
        print('squeek!')

    xcenter = 0.0
    xstep = 0.01
    scale = 0.5
    red = Color(0xff0000, 1.0)
    blue = Color(0x0000ff, 1.0)
    line = LineStyle(0, red)
    poly = PolygonAsset([(0,0),(50,75),(100,60),(90,150),(45,100),(0,0)], line, red)
    circ = CircleAsset(75, line, red)
    circ2 = CircleAsset(55, line, blue)
    bun = ImageAsset('bunny.png')
    bun.center = (0.5,0.5)
    rect = RectangleAsset(30,150)
    ell = EllipseAsset(10,3)
    spr = Sprite(bun, (200,300))
    spr2 = Sprite(poly, (375, 255))
    # TRYING to get the extents to initialize!!
    spr2._extentsdirty = True
    spr2._setExtents()
    spr2.rotation = 0.000
    # /\ this does it
    h1 = Sprite(LineAsset(500,0))
    h2 = Sprite(LineAsset(500,0))
    v1 = Sprite(LineAsset(0,500))
    v2 = Sprite(LineAsset(0,500))
    hh1 = Sprite(LineAsset(500,0))
    hh2 = Sprite(LineAsset(500,0))
    vv1 = Sprite(LineAsset(0,500))
    vv2 = Sprite(LineAsset(0,500))

    def step():
        global spr
        global spr2
        global xcenter
        global xstep
        global h1
        global h2
        global v1
        global v2
        global hh1
        global hh2
        global vv1
        global vv2
        global scale
        

        scale = scale + xstep
        spr.fxcenter = xcenter
        spr.fycenter = xcenter
        xcenter = xcenter + xstep
        if xcenter >= 1.0 or xcenter <= 0.0:
            xstep = xstep * -1
        spr.rotation = spr.rotation + 10*xstep
        spr.scale = scale
        spr.x += 1
        spr._setExtents()
        h1.y = spr.ymin
        h2.y = spr.ymax
        v1.x = spr.xmin
        v2.x = spr.xmax
        spr2._setExtents()
        hh1.y = spr2.ymin
        hh2.y = spr2.ymax
        vv1.x = spr2.xmin
        vv2.x = spr2.xmax
        if spr.collidingWith(spr2):
            print("BANG")

    app = App()

    app.listenKeyEvent('keydown', 'e', test)
    app.listenMouseEvent('mousedown', testm)
    app.run(step)


