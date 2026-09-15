"""Exact rounded cable-notch outline shared by CAD, DXF and drawing generators."""
import math

def outline(p):
    w,h,r=p['width'],p['height'],p['outer_radius'];q=math.tan(math.pi/8)
    l,rt=-w/2,w/2
    pts=[(l+r,0,0),(rt-r,0,q),(rt,r,0),(rt,h-r,q),(rt-r,h,0)]
    if p.get('cable_notch'):
        n=p['cable_notch'];a=n['mouth_width']/2;d=n['depth'];u=n['mouth_radius'];b=n['bottom_radius']
        wall=a-u
        assert d>=u+b and wall>=b
        pts += [(a,h,q),(wall,h-u,0),(wall,h-d+b,-q),
                (wall-b,h-d,0),(-wall+b,h-d,-q),(-wall,h-d+b,0),
                (-wall,h-u,q),(-a,h,0)]
    pts += [(l+r,h,q),(l,h-r,0),(l,r,q)]
    return pts

def arc_mid(a,b,bulge):
    return ((a[0]+b[0])/2+bulge*(b[1]-a[1])/2,
            (a[1]+b[1])/2-bulge*(b[0]-a[0])/2)

def notch_area(p):
    n=p.get('cable_notch')
    if not n:return 0
    u,b=n['mouth_radius'],n['bottom_radius']
    return (n['mouth_width']-2*u)*n['depth']+2*(u*u-b*b)*(1-math.pi/4)
