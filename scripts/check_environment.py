"""Check the supported macOS authoring environment without changing it."""
import argparse
import importlib
import importlib.metadata
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender',type=Path,default=Path('/Applications/Blender.app/Contents/MacOS/Blender'))
    parser.add_argument('--fea',action='store_true',help='Also check optional Gmsh/Matplotlib imports')
    args=parser.parse_args();errors=[]
    if platform.system()!='Darwin':errors.append('Supported authoring baseline is macOS; report other-platform issues when encountered.')
    if sys.version_info[:2]!=(3,12):errors.append('Use Python 3.12 for the tested dependency set.')
    requirements=['requirements.txt']+(['requirements-fea.txt'] if args.fea else [])
    modules={'pillow':'PIL','cadquery':'cadquery','reportlab':'reportlab','pypdf':'pypdf',
             'ezdxf':'ezdxf','numpy':'numpy','scipy':'scipy','gmsh':'gmsh','matplotlib':'matplotlib'}
    for filename in requirements:
        for line in (ROOT/filename).read_text().splitlines():
            if '==' not in line:continue
            name,expected=line.split('==')
            try:
                found=importlib.metadata.version(name);importlib.import_module(modules[name])
                if found!=expected:errors.append(f'{name}: expected {expected}, installed {found}')
            except (ImportError,OSError) as exc:errors.append(f'{name}: {exc}')
    fonts=Path('/System/Library/Fonts/Supplemental')
    for name in ('Arial.ttf','Arial Bold.ttf'):
        if not (fonts/name).is_file():errors.append(f'Missing font: {fonts/name}')
    if args.blender.is_file():
        try:
            run=subprocess.run([str(args.blender),'--background','--factory-startup','--python-expr',
                "import bpy, numpy; print('AUTHORING_BLENDER_OK', bpy.app.version_string)"],capture_output=True,text=True,timeout=60)
            if run.returncode or 'AUTHORING_BLENDER_OK' not in run.stdout:errors.append('Blender startup/import failed: '+run.stdout+run.stderr)
        except (OSError,subprocess.TimeoutExpired) as exc:errors.append(f'Blender: {exc}')
    else:errors.append(f'Blender not found: {args.blender}')
    if not errors:
        # Exercise the export/read APIs used by the manufacturing toolchain.
        import cadquery as cq
        import ezdxf
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory(prefix='manifold-environment-') as scratch:
            folder=Path(scratch)
            cq.exporters.export(cq.Workplane('XY').box(1,2,3),str(folder/'check.step'))
            assert abs(cq.importers.importStep(str(folder/'check.step')).val().Volume()-6)<1e-7
            drawing=ezdxf.new();drawing.modelspace().add_circle((0,0),2);drawing.saveas(folder/'check.dxf')
            assert len(ezdxf.readfile(folder/'check.dxf').modelspace())==1
            pdfmetrics.registerFont(TTFont('CheckArial',str(fonts/'Arial.ttf')))
            c=Canvas(str(folder/'check.pdf'));c.setFont('CheckArial',12);c.drawString(30,30,'Manufacturing environment check');c.save()
            assert 'Manufacturing environment check' in PdfReader(folder/'check.pdf').pages[0].extract_text()
    if errors:
        print('\n'.join(errors));return 1
    print('PASS: macOS / Python 3.12, declared packages, Arial, Blender, STEP/DXF/PDF round trips.')
    if args.fea:print('Optional Python FEA imports pass. A separate CalculiX executable is needed only to solve new cases.')
    return 0


if __name__=='__main__':raise SystemExit(main())
