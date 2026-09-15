"""Manufacturer-informed StarTech 4POSTRACK25U reference; dimensions in mm.
See docs/references/startech-25u/sources.json for explicit vs inferred dimensions.
"""
import math

U=44.45
RAIL_DEPTH=558.8
RACK_U_DATUM=142.255
CASTER_HEIGHT=72.94
HEIGHT=1288.34

def build_rack(box,cyl,black,metal,rubber):
    # The manufacturer drawing's three depth datums differ by 33 and 70mm.
    # Symmetric datum registration is an integration inference, not a tolerance.
    for rear,y in ((False,0),(True,RAIL_DEPTH)):
        inward=-1 if rear else 1
        outer=y-inward*16.5
        for sign in (-1,1):
            xc=sign*232.5
            # 75mm wide L-profile flange, with 9.8mm square cage-nut apertures.
            box('StarTech rail inner flange',(sign*226.3,y+inward*1.25,697.945),(2.6,2.5,1113.9),black)
            box('StarTech rail outer flange',(sign*268.7,y+inward*1.25,680.7),(62.6,2.5,1211.4),black)
            box('StarTech outer return',(sign*298.75,outer+inward*25.75,680.7),(2.5,51.5,1211.4),black)
            zs=[RACK_U_DATUM+u*U+d for u in range(25) for d in (6.35,22.225,38.1)]
            last=140.995
            for z in zs+[1254.895+4.9]:
                length=z-4.9-last
                if length>0:box('StarTech square-hole web',(xc,y+inward*1.25,last+length/2),(9.8,2.5,length),black)
                last=z+4.9
        # Folded full-width base and top brackets, not generic solid beams.
        box('StarTech base web',(0,outer,106.25),(600,2.5,62.5),black)
        box('StarTech base foot flange',(0,outer,73.94),(600,70,2),black)
        box('StarTech base upper lip',(0,outer+inward*8.75,138.75),(593,20,2.5),black)
        box('StarTech top web',(0,outer,1272.64),(600,2.5,31.4),black)
        box('StarTech top flange',(0,outer+inward*17.5,1287.29),(600,35,2.1),black)
        for x in (-260,260):
            box('StarTech caster mount',(x,outer,71),(42,55,4),metal)
            cyl('StarTech swivel bearing',(x,outer,64),16,10,metal,'Z')
            for dx in (-17,17):box('StarTech caster fork',(x+dx,outer+8,45),(3,30,40),metal)
            cyl('StarTech caster wheel',(x,outer+8,25),25,29,rubber,'X')
            cyl('StarTech caster axle',(x,outer+8,25),4,39,metal,'X')
        for x in (-196,196):
            cyl('StarTech leveller spindle',(x,outer,48),4,50,metal,'Z')
            cyl('StarTech leveller foot',(x,outer,20),13,7,rubber,'Z')
        for x in (-287,287):
            for z in (92,123,1272):cyl('StarTech M8 assembly head',(x,outer-3*inward,z),6.5,5,metal)
    for sign in (-1,1):
        x=sign*296
        # Three nested pieces are visible at the minimum 0/0 extension setting.
        for z in (105,1258):
            box('StarTech centre depth channel',(x,RAIL_DEPTH/2,z),(3,RAIL_DEPTH,40),black)
            for yc in (120,RAIL_DEPTH-120):
                box('StarTech corner depth channel',(x-sign*3,yc,z),(3,273,48),black)
                for yy in (yc-90,yc-64.6,yc+64.6,yc+90):
                    for zz in (z-12,z+12):cyl('StarTech depth-lock bolt',(x-sign*7,yy,zz),5,5,metal,'X')
            box('StarTech depth channel lip',(sign*280,RAIL_DEPTH/2,z+23),(35,RAIL_DEPTH,2),black)
        # Optional rear cable-management rings occupy the side away from tubing.
        for z in (380,691,1002):
            box('StarTech rear cable hook stem',(sign*313,RAIL_DEPTH-5,z),(26,4,4),black)
            box('StarTech rear cable hook outer',(sign*326,RAIL_DEPTH+10,z),(4,34,4),black)
            box('StarTech rear cable hook return',(sign*317,RAIL_DEPTH+27,z),(18,4,4),black)
