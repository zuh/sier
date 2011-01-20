"""
 * A simple visualization of a Sierpinski triangle
 * Copyright 2011 Kalle Vahlman, <zuh@iki.fi>
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
"""

import gtk
from time import time

class Triangle:
    """ x1,y1
         /\
        /__\
    x2,y2  x3,y3
    """
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def __repr__(self):
        s = "Triangle("
        s += str(self.x1) + "," + str(self.y1) + " "
        s += str(self.x2) + "," + str(self.y2) + " "
        s += str(self.x3) + "," + str(self.y3)
        s += ")"
        return s

    def draw(self, cr):
        cr.move_to(self.x1, self.y1)
        cr.line_to(self.x2, self.y2)
        cr.line_to(self.x3, self.y3)
        cr.close_path()
        cr.fill()


class Sier(gtk.DrawingArea):
    level = 0

    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)

    """ We assume x2,y2-x3,y3 to be horizontal here
        TODO: more accurate & generic maths
    """
    def shrink(self, t):
        width = (t.x3 - t.x2)/2.0
        height = (t.y1 - t.y2)/2.0
        ts=[];
        ts.append(Triangle(t.x2 + width/2.0, t.y2 + height,
                           t.x2,             t.y2,
                           t.x2 + width,     t.y2))
        ts.append(Triangle(t.x1,             t.y1,
                           t.x2 + width/2.0, t.y2 + height,
                           t.x2 + width*1.5, t.y3 + height))
        ts.append(Triangle(t.x2 + width*1.5, t.y3 + height,
                           t.x2 + width,     t.y2,
                           t.x3,             t.y3))
        return ts

    def fractal(self, tri, level):
        start = time()
        tris = [tri]
        for i in range(0, level):
            new_tris = []
            for t in tris:
                new_tris.extend(self.shrink(t))
            tris = new_tris
        end = time()
        print "Calculated", len(tris), "triangles in", round((end-start), 4), "s"
        return tris

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()
        tri = Triangle(rect.x + rect.width/2.0, rect.y,
                       rect.x, rect.y + rect.height,
                       rect.x + rect.width, rect.y + rect.height)
        tris = self.fractal(tri, self.level)
        cr.set_source_rgb(0.0, 0.0, 0.0)
        start = time()
        for t in tris:
            t.draw(cr)
        end = time()
        print "Drew", len(tris), "triangles in", round((end-start), 4), "s"

        return False

def key_release(widget, event, sier):
    if event.keyval == 43:
        sier.level = sier.level+1
    if event.keyval == 45:
        sier.level = sier.level-1
    sier.queue_draw()
    return False

def main():
    window = gtk.Window()
    s = Sier()
    
    window.add(s)
    window.connect("destroy", gtk.main_quit)
    window.connect("key_release_event", key_release, s)
    window.show_all()
    
    window.set_size_request(200, 200)
    window.resize(200,200)
    
    gtk.main()

if __name__ == "__main__":
    main()
