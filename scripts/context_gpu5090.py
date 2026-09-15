"""Dimensioned Alphacool 5100182 / RTX 5090 FE context, in millimetres.

Pure coordinates are shared by the rod solver and Blender builder. Unpublished
PCB, connector and bracket detail remains an explicit visual approximation.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GPU = json.loads((ROOT / 'cad/context/gpu-5090fe.json').read_text())
D = GPU['published']
P = GPU['placement']
TOP = P['port_midpoint_Z_above_gpu_datum_mm'] + D['upper_port_below_top_mm'] + D['port_pitch_mm'] / 2
BOTTOM = TOP - D['active_backplate_length_height_thickness_mm'][1]
PORT_Z = (TOP - D['upper_port_below_top_mm'] - D['port_pitch_mm'], TOP - D['upper_port_below_top_mm'])


def build_gpu(index, x, z0, box, cyl, hose, materials):
    """Build an unmarked, layered reference assembly with PCB on positive X."""
    import bpy
    from mathutils import Vector
    chrome, carbon, pcb, black, steel, gold = materials
    prefix = f'GPU {index+1}'
    front = P['port_face_Y_mm']
    length, height, thick = D['main_cooler_length_height_thickness_mm']
    bx = P['main_block_outer_X_relative_to_port_mm']

    def shape(name, x0, x1, yz, material, bevel=.45):
        verts = [(x + xx, front + yy, z0 + zz) for xx in (x0, x1) for yy, zz in yz]
        n = len(yz)
        faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
        faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(verts, [], faces); mesh.update()
        obj = bpy.data.objects.new(prefix+' '+name, mesh); bpy.context.scene.collection.objects.link(obj)
        # Correct winding independently of profile order for signed surface checks.
        import bmesh
        bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
        mesh.materials.append(material)
        if bevel:
            mod=obj.modifiers.new('Small edge radii','BEVEL');mod.width=bevel;mod.segments=3
            obj.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
        return obj

    # The drawing's notched top clears the angled power connector near the port end.
    outline=[(0,BOTTOM),(length,BOTTOM),(length,TOP-1.5),(53,TOP-1.5),
             (47,TOP-7.5),(42,TOP-13.5),(35,TOP-6.5),(29,TOP-1.5),(0,TOP-1.5)]
    shape('main chrome cooling block',bx+1,bx+thick,outline,chrome)
    # Carbon cap is part of (not additional to) the published thickness envelope.
    shape('main carbon cover',bx,bx+1.0,outline,carbon,.35)
    bl,bh,bt=D['active_backplate_length_height_thickness_mm']
    bf=P['backplate_front_offset_from_port_face_mm'];outer=D['port_axis_to_backplate_outer_face_mm']
    back=[(bf,BOTTOM),(bf+bl,BOTTOM),(bf+bl,TOP),(53,TOP),
          (47,TOP-6),(42,TOP-12),(35,TOP-5),(29,TOP),(bf,TOP)]
    shape('active chrome backplate',outer-bt,outer-1,back,chrome)
    shape('active carbon back cover',outer-1,outer,back,carbon,.35)
    px=P['PCB_X_relative_to_port_mm'];pt=P['PCB_thickness_mm'];pl,ph=P['main_PCB_length_height_mm']
    pf=P['main_PCB_front_offset_from_port_face_mm'];pb=P['main_PCB_bottom_above_gpu_datum_mm']
    # The FE has separate processor, PCIe edge and display boards, not a full-length PCB.
    processor=[(pf,pb+3),(pf+6,pb),(pf+pl*.39,pb),(pf+pl*.43,pb+3),
               (pf+pl*.63,pb+3),(pf+pl*.67,pb),(pf+pl-5,pb),(pf+pl,pb+4),
               (pf+pl,pb+ph),(53,pb+ph),
               (45,pb+ph-9),(36,pb+ph),(pf,pb+ph)]
    shape('processor PCB',px-pt/2,px+pt/2,processor,pcb,.15)
    box(prefix+' PCIe daughter PCB',(x+px,front+136,z0+BOTTOM+2),(pt,112,13),pcb)
    box(prefix+' PCIe gold edge',(x+px,front+136,z0+BOTTOM-3),(pt,89,5),gold)
    box(prefix+' PCIe riser',(x+px,front+136,z0+P['riser_centre_Z_above_gpu_datum_mm']),(18,112,12),black)
    # Populate only representative hidden components; no invented external PCB dimensions.
    for yy in (pf+12,pf+pl-12):
        for zz in range(78,160,14):box(prefix+' VRM package',(x+px-1.5,front+yy,z0+zz),(1.2,8,7),black)
    # Front terminal incorporates the two threaded ports on a 34 mm vertical pitch.
    low,high=PORT_Z
    box(prefix+' black terminal',(x,front+4.5,z0+(low+high)/2),(17,9,high-low+18),black)
    cyl(prefix+' coolant fitting lower',(x,front-11,z0+low),8,22,steel)
    cyl(prefix+' coolant fitting upper',(x,front-11,z0+high),8,22,steel)
    for zz in (low,high):
        cyl(prefix+' terminal brass insert',(x,front+.5,z0+zz),8,1.5,steel)
    # Visible side screws are illustrative; do not engrave part names or port labels.
    for xx in (bx-.15,outer+.15):
        for yy in (18,65,140,205):
            for zz in (BOTTOM+6,TOP-8):
                if yy==18 and xx>0:continue
                cyl(prefix+' cover screw',(x+xx,front+yy,z0+zz),2.4,.6,steel,'X')

    # A 42.07 mm aggregate envelope is not the width of the single bracket plate.
    # Model its narrower, offset sheet at the rear, beyond the adjacent cooling bodies.
    rear=front+D['assembled_length_to_bracket_datum_mm'];left=P['bracket_outer_X_min_relative_to_port_mm']
    bw=P['bracket_width_mm'];sheet=P['bracket_sheet_mm']
    bracket_bottom=TOP-D['assembled_overall_height_including_bracket_mm']
    centre_x=x+left+bw/2
    # Rails and rungs surround four actual openings (three DP and one HDMI).
    zbottom=z0+bracket_bottom;ztop=z0+TOP
    for xx in (centre_x-bw/2+2,centre_x+bw/2-2):
        box(prefix+' IO bracket side',(xx,rear,(zbottom+ztop)/2),(4,sheet,ztop-zbottom),steel)
    ports=[z0+BOTTOM+20+22*j for j in range(4)]
    for zz in [zbottom+5]+[p-8 for p in ports]+[ztop-5]:
        box(prefix+' IO bracket bridge',(centre_x,rear,zz),(bw,sheet,5),steel)
    box(prefix+' IO bracket top flange',(centre_x,(rear+front+D['assembled_overall_length_mm'])/2,ztop-.5),
        (bw,D['assembled_overall_length_mm']-D['assembled_length_to_bracket_datum_mm'],sheet),steel)
    box(prefix+' display daughter PCB',(x+7,rear-5,z0+BOTTOM+53),(1.6,11,105),pcb)
    for j,zz in enumerate(ports):
        box(prefix+(' HDMI socket' if j==0 else ' DisplayPort socket'),(centre_x,rear+1.5,zz),(15,7,9),steel)
        box(prefix+' display socket opening',(centre_x,rear+5.05,zz),(12,.3,5),black)
    # Short internal flexible interconnects between the three FE boards.
    hose(prefix+' internal display flex',[(x+px,front+135,z0+110),(x+px+1,front+183,z0+109),(x+7,rear-8,z0+110)],black,1.2)

    sx,sy,sz=P['power_socket_position_relative_to_port_and_gpu_datum_mm']
    angle=math.radians(P['power_exit_angle_from_vertical_degrees'])
    axis=Vector((0,-math.sin(angle),math.cos(angle)));position=Vector((x+sx,sy,z0+sz))
    # The six-contact row lies in the PCB plane, across local Y; X is the
    # shallow two-row dimension. Dimensions follow Molex 2191140161 drawing A.
    power=GPU['power_housing_reference'];width=power['flange_width_mm']
    across=Vector((0,math.cos(angle),math.sin(angle)))
    def power_point(xx,yy,zz):return position+Vector((xx,0,0))+across*yy+axis*zz
    def power_box(name,xx,yy,zz,size):
        obj=box(prefix+' '+name,power_point(xx,yy,zz),size,black)
        obj.rotation_euler.x=angle
        mod=obj.modifiers.new('Moulded edge radius','BEVEL');mod.width=.16;mod.segments=3
        obj.modifiers.new('Moulded face normals','WEIGHTED_NORMAL')
        return obj
    # Separate right-angle PCB header: 18.85 across, 6.86 main shroud,
    # 9.91 axial depth. Back wall, shroud and stepped signal pod are distinct.
    power_box('12V-2x6 socket',0,0,-4.255,(6.86,18.85,1.4))
    for xx in (-3.16,3.16):
        power_box('header shroud wall',xx,0,0,(.54,18.85,9.91))
    for yy in (-9.155,9.155):
        power_box('header shroud side',0,yy,0,(6.86,.54,9.91))
    power_box('header signal pod',4.185,0,-.5,(1.51,9.4,8.91))
    power_box('header latch ramp',-4.13,0,3.2,(1.4,1.4,2.95))
    # Drawing's mated axial envelope is 17.66: 14 mm cable housing
    # overlaps the 9.91 mm header by 6.25 mm. Towers are the mating end;
    # the broad flange is at the wire end, not at the insertion tip.
    nose=-1.295;wire_end=nose+14
    plug=power_box('12V-2x6 plug housing',0,0,wire_end-4,(7.55,18.85,8))
    plug['reference_flange_width_mm']=width;plug['reference_main_height_mm']=7.55
    plug['reference_axial_length_mm']=14.0
    power_box('power housing flange',0,0,wire_end-.5,(7.55,width,1))
    power_box('power signal ledge',4.4,0,wire_end-4.5,(1.3,9.2,9))
    for row,xx in enumerate((-1.5,1.5)):
        for col in range(6):
            yy=(col-2.5)*3
            power_box(f'power mating tower {row+1}-{col+1}',xx,yy,nose+3,(2.4,2.4,6))
            hose(prefix+f' power conductor {row+1}-{col+1}',
                 [power_point(xx,yy,wire_end-.2),power_point(xx,yy,wire_end+15),
                  power_point(xx*.85,yy*.65,wire_end+31),
                  power_point(xx*.8,yy*.3,wire_end+46)],black,1.05)
    for j in range(4):
        hose(prefix+f' sense conductor {j+1}',
             [power_point(4.4,(j-1.5)*2,wire_end-.2),power_point(4.4,(j-1.5)*2,wire_end+15),
              power_point(3.5,(j-1.5),wire_end+31),power_point(2.8,(j-1.5)*.8,wire_end+46)],black,.38)
    power_box('power latch root',-4.15,0,wire_end-6,(1.1,3.85,2))
    power_box('power latch arm',-5.0,0,wire_end-7,(.9,3.85,9))
    power_box('power latch release',-5.78,0,wire_end-2.5,(1.6,3.85,2.2))
    power_box('power latch hook',-4.9,0,wire_end-10.5,(1.6,3.85,1.2))
    exit_=power_point(0,0,wire_end+42);lead=power_point(0,0,wire_end+59)
    hose(prefix+' auxiliary power',[exit_,lead,(x+sx,95+index*9,z0+252),
          (186+index*2,95+index*9,z0+252),(195,100+index*3,z0+43)],black,4.5)
    hose(prefix+' riser data',[(x+px,front+155,z0+52),(x+px,300,z0+30),
          (117+index*13,360,z0+10),(117+index*13,337,z0+20)],materials[-3],3)
    return dict(port_centres=[[x,front,z0+zz] for zz in PORT_Z],
                pcb_X=x+px,main_block_X_bounds=[x+bx,x+bx+thick],
                backplate_X_bounds=[x+outer-bt,x+outer],body_gap_at_40mm_pitch=40-D['assembled_body_thickness_mm'],
                bracket_sheet_width_mm=bw,bracket_edge_gap_mm=40-bw,
                overall_envelope_mm=[42.07,245.83,150.60])
