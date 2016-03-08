from pyx import *

# Helper method to convert quadratic bezier curve to equivalent cubix bezier
# curve
def quadToCub(x0,y0,x1,y1,x2,y2):
    new_x1 = x0 + (2./3.) * (x1 - x0)
    new_y1 = y0 + (2./3.) * (y1 - y0)
    new_x2 = x2 + (2./3.) * (x1 - x2)
    new_y2 = y2 + (2./3.) * (y1 - y2)

    x3 = x2
    y3 = y2
    x1 = new_x1
    y1 = new_y1
    x2 = new_x2
    y2 = new_y2

    return {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,'x2': x2, 'y2': y2,'x3': x3, 'y3': y3}

# Predefined quadratic bezier curve
class qbcurve(path.curve_pt):

    """bezier curve with control points (x0, y1),..., (x2, y2)"""

    def __init__(self, x0, y0, x1, y1, x2, y2):

        a = quadToCub(x0, y0, x1, y1, x2, y2)
        path.curve_pt.__init__(self, unit.topt(a['x0']), unit.topt(a['y0']),
                                unit.topt(a['x1']), unit.topt(a['y1']),
                                unit.topt(a['x2']), unit.topt(a['y2']),
                                unit.topt(a['x3']), unit.topt(a['y3']))

path.qbcurve =  qbcurve

# Create new quadratic bezier path that can be appending to existing path
class qbcurveto(path.curveto_pt):

    """Append curveto"""

    __slots__ = "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"
    def __init__(self, x1, y1, x2, y2):
        # Incorrect values for first 2 x/y pairs used, which will subsequently be corrected
        # in append method
        path.curveto_pt.__init__(self,
                            unit.topt(x1), unit.topt(y1),
                            unit.topt(0), unit.topt(0),
                            unit.topt(x2), unit.topt(y2))

path.qbcurveto = qbcurveto

# Override append method so that incorrect points specified in qbcurve_to can
# be corrected. Implemented in this way as the append method is the simplest
# way to gain visibility of the start points which are required quadToCUb to
# calculate the new control points.

def append(self, apathitem):
    """append a path item"""
    assert isinstance(apathitem, path.pathitem), "only pathitem instance allowed"
    # find end  of current path before appending
    x =  unit.topt(self.normpath().atend()[0])
    y =  unit.topt(self.normpath().atend()[1])

    # if apathiem is a qbcurveto then correct its definition
    if isinstance(apathitem, path.qbcurveto):
        a = quadToCub(x,y,apathitem.x1_pt,apathitem.y1_pt,apathitem.y2_pt,apathitem.x2_pt)
        apathitem.x1_pt = a['x1']
        apathitem.y1_pt = a['y1']
        apathitem.x2_pt = a['x2']
        apathitem.y2_pt = a['y2']
    self.pathitems.append(apathitem)
    self._normpath = None

path.path.append = append

# Sample execution
# import gkpyx
# gkpyx.unit.set(uscale=None, vscale=None, wscale=None, xscale=None, defaultunit='pt')
# print gkpyx.qbcurve(1,2,3,4,5,6)
