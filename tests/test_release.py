"""Exercise revision isolation, review freshness and actual ZIP/PDF handling."""
from datetime import date
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from reportlab.pdfgen.canvas import Canvas

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import release


def put(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')


def drawing(path,part):
    path.parent.mkdir(parents=True,exist_ok=True)
    c=Canvas(str(path));c.drawString(20,50,part);c.drawString(20,30,'TEST FIXTURE ONLY');c.save()


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        rows=[]
        for role,part in [('body','RM10-Q-M04-BODY'),('faceplate','RM10-Q-M03-FACEPLATE'),('radiator','SN1260-R7-M01-PLATE')]:
            manufacturing_revision=part.split('-',1)[1].rsplit('-',1)[0]
            row=dict(part=part,manufacturing_revision=manufacturing_revision,source=f'cad/manufacturing/{manufacturing_revision}.json',
                     step=f'output/manufacturing/{manufacturing_revision}/{part}.step',drawing=f'output/pdf/{part}.pdf',
                     dxf=None if role=='body' else f'output/manufacturing/{manufacturing_revision}/{part}.dxf',
                     pdf_sheets=1,quantity=1,jlc=dict(category='CNC machining' if role=='body' else 'Sheet Metal',
                     material='POM' if role=='body' else '304',finish='Raw',remarks='Test fixture',threads=role=='body'))
            put(self.root/row['source'],dict(manufacturing_revision=manufacturing_revision,part_number=part,geometry_revision='Q'))
            step=self.root/row['step'];step.parent.mkdir(parents=True,exist_ok=True);step.write_text('ISO-10303-21;\nTEST FIXTURE ONLY\n')
            drawing(self.root/row['drawing'],part)
            if row['dxf']:(self.root/row['dxf']).write_text('TEST FIXTURE ONLY')
            bundle=self.root/f'output/submission/{part}.zip';bundle.parent.mkdir(parents=True,exist_ok=True)
            with zipfile.ZipFile(bundle,'w') as z:
                for key in ('step','drawing','dxf'):
                    if row[key]:z.write(self.root/row[key],Path(row[key]).name)
            row.update(manufacturing_revision_bundle=str(bundle.relative_to(self.root)),sha256=release.sha(bundle));rows.append(row)
        put(self.root/'cad/current-release.json',dict(parts=rows))
        self.original={str(p.relative_to(self.root)):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_new_selection_uses_explicit_schema_two_revision(self):
        manifest=release.initialise(self.root,'new-study',{'body':'Q-M05'})
        data=json.loads(manifest.read_text())
        self.assertEqual(data['schema_version'],2)
        self.assertEqual(data['parts'][0]['manufacturing_revision'],'Q-M05')
        config=json.loads((self.root/data['parts'][0]['source']).read_text())
        self.assertEqual(config['source_manufacturing_revision'],'Q-M04')

    def candidate(self):
        manifest=release.initialise(self.root,'study',{'body':'Q-M05'})
        data=release.read(manifest);part=data['parts'][0];part['jlc']['remarks']='New test fixture';part['review_images']=['output/study/review.png']
        step=self.root/part['step'];step.parent.mkdir(parents=True,exist_ok=True);step.write_text('ISO-10303-21;\nNEW TEST FIXTURE\n')
        drawing(self.root/part['drawing'],part['part'])
        image=self.root/part['review_images'][0];image.parent.mkdir(parents=True,exist_ok=True)
        from PIL import Image
        Image.new('RGB',(8,8),'white').save(image)
        put(self.root/part['verification'],dict(manufacturing_revision=part['manufacturing_revision'],checks='PASS',
            source_sha256={part['source']:release.sha(self.root/part['source'])}))
        put(manifest,data);return manifest

    def reviewed(self,manifest):
        path=release.snapshot(self.root,manifest);r=release.read(path)
        r.update(status='reviewed',reviewer='Automated test fixture, not product approval',reviewed_on=date.today().isoformat())
        put(path,r)

    def test_package_preserves_originals_and_unchanged_zip_bytes(self):
        manifest=self.candidate();self.reviewed(manifest);out=release.package(self.root,manifest)
        for path,content in self.original.items():self.assertEqual((self.root/path).read_bytes(),content,path)
        report=release.read(out/'release.json');self.assertFalse(report['supplier_submission_performed'])
        self.assertEqual(len(report['parts']),3)
        originals=release.canonical(self.root)
        for role in ('faceplate','radiator'):
            p=originals[role];self.assertEqual((out/(p['part']+'.zip')).read_bytes(),(self.root/p['manufacturing_revision_bundle']).read_bytes())
        with zipfile.ZipFile(out/'RM10-Q-M05-BODY.zip') as z:
            self.assertEqual(set(z.namelist()),{'RM10-Q-M05-BODY.step','RM10-Q-M05-BODY.pdf'})
        with self.assertRaises(FileExistsError):release.package(self.root,manifest)

    def test_existing_manufacturing_revision_and_duplicate_destinations_refused_without_writes(self):
        with self.assertRaises(ValueError):release.initialise(self.root,'bad',{'body':'Q-M04'})
        with self.assertRaises(ValueError):release.initialise(self.root,'bad',{'body':'Q-M05','faceplate':'Q-M05'})
        self.assertFalse((self.root/'cad/manufacturing/Q-M05.json').exists())

    def test_pending_review_refused(self):
        m=self.candidate();release.snapshot(self.root,m)
        with self.assertRaises(ValueError):release.package(self.root,m)
        self.assertFalse((self.root/'output/submission/releases/study').exists())

    def test_changed_step_or_view_invalidates_review(self):
        m=self.candidate();self.reviewed(m)
        part=release.read(m)['parts'][0]
        for target in (part['step'],part['review_images'][0]):
            with self.subTest(target=target):
                p=self.root/target;original=p.read_bytes();p.write_bytes(original+b'changed')
                with self.assertRaisesRegex(ValueError,'since the review'):release.package(self.root,m)
                p.write_bytes(original)

    def test_stale_geometry_check_and_wrong_pdf_manufacturing_revision_rejected(self):
        m=self.candidate();part=release.read(m)['parts'][0]
        config=self.root/part['source'];before=config.read_bytes();config.write_text(config.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'Stale geometry'):release.inputs(self.root,m)
        config.write_bytes(before);drawing(self.root/part['drawing'],'RM10-Q-M04-BODY')
        with self.assertRaisesRegex(ValueError,'Drawing must identify'):release.inputs(self.root,m)

    def test_carried_part_cannot_be_silently_changed(self):
        m=self.candidate();p=self.root/release.read(m)['parts'][1]['step'];p.write_text('ISO-10303-21; MODIFIED')
        with self.assertRaisesRegex(ValueError,'no longer matches'):release.inputs(self.root,m)

    def test_path_escape_and_canonical_input_reuse_rejected(self):
        with self.assertRaises(ValueError):release.file(self.root,'../elsewhere')
        m=self.candidate();data=release.read(m)
        data['parts'][0]['source']='cad/manufacturing/Q-M04.json';put(m,data)
        with self.assertRaisesRegex(ValueError,'Cannot reuse delivered'):release.inputs(self.root,m)


if __name__=='__main__':unittest.main()
