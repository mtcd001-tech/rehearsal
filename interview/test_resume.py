import io
import unittest
import zipfile
import httpx
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
from resume_import import extract_resume, MAX_BYTES
import server

def word_file():
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w') as z:
        z.writestr('word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Built Python APIs</w:t></w:r></w:p></w:body></w:document>')
    return output.getvalue()

def pdf_file(encrypted=False, blank=False):
    output=io.BytesIO(); writer=PdfWriter(); page=writer.add_blank_page(612,792)
    if not blank:
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject();stream.set_data(b'BT /F1 12 Tf 50 700 Td (Built Python APIs) Tj ET')
        page[NameObject('/Contents')]=writer._add_object(stream)
    if encrypted: writer.encrypt('password')
    writer.write(output);return output.getvalue()

class ResumeTests(unittest.TestCase):
    def test_txt_and_truncation(self):
        self.assertEqual(extract_resume(b'Python developer','resume.txt')['text'],'Python developer')
        result=extract_resume(b'a'*10001,'resume.TXT')
        self.assertTrue(result['truncated']);self.assertEqual(len(result['text']),10000)
    def test_docx(self):
        self.assertEqual(extract_resume(word_file(),'resume.docx')['text'],'Built Python APIs')
    def test_pdf(self):
        self.assertIn('Built Python APIs',extract_resume(pdf_file(),'resume.pdf')['text'])
    def test_encrypted_and_scanned_pdf(self):
        for data,pattern in [(pdf_file(encrypted=True),'Password'),(pdf_file(blank=True),'No readable text')]:
            with self.assertRaisesRegex(ValueError,pattern):extract_resume(data,'resume.pdf')
    def test_rejected_files(self):
        for data,name in [(b'x','resume.doc'),(b'','resume.txt'),(b'x'*(MAX_BYTES+1),'resume.txt'),(b'\xff','resume.txt'),(b'not zip','resume.docx')]:
            with self.assertRaises(ValueError):extract_resume(data,name)
    def test_xml_declarations_rejected(self):
        output=io.BytesIO()
        with zipfile.ZipFile(output,'w') as z:z.writestr('word/document.xml','<!DOCTYPE x><x/>')
        with self.assertRaisesRegex(ValueError,'XML'):extract_resume(output.getvalue(),'resume.docx')

class UploadTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_worker_extracts_and_rejects(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as c:
            for ext,data in [('txt',b'Built a Python API'),('docx',word_file()),('pdf',pdf_file())]:
                r=await c.post('/api/resume',params={'filename':'resume.'+ext},content=data)
                self.assertEqual(r.status_code,200,r.text);self.assertIn('Python',r.json()['text'])
                self.assertEqual(r.headers['cache-control'],'no-store')
            r=await c.post('/api/resume?filename=resume.exe',content=b'x');self.assertEqual(r.status_code,400)
            r=await c.post('/api/resume?filename=resume.txt',content=b'x'*(MAX_BYTES+1));self.assertEqual(r.status_code,413)
            r=await c.post('/api/resume?filename=resume.txt',content=b'text',headers={'Origin':'https://example.com'});self.assertEqual(r.status_code,403)

if __name__=='__main__':unittest.main()
