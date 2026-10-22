"""Extract resume text in memory; invoked in a timeout-bounded subprocess."""
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

MAX_BYTES = 5 * 1024 * 1024
MAX_TEXT = 10000

def extract_resume(data: bytes, filename: str) -> dict:
    if not data or len(data) > MAX_BYTES:
        raise ValueError('Choose a nonempty file smaller than 5 MB.')
    ext = Path(filename).suffix.lower()
    if ext == '.txt':
        try:
            text = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            raise ValueError('Save your text file as UTF-8, or upload PDF or DOCX.') from None
    elif ext == '.docx':
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                infos = archive.infolist()
                if len(infos) > 2000 or sum(x.file_size for x in infos) > 12 * 1024 * 1024:
                    raise ValueError('This Word file is too complex. Export a simpler PDF or TXT version.')
                names = ['word/document.xml'] + sorted(n for n in archive.namelist() if re.fullmatch(r'word/(header|footer)\d+\.xml', n))
                paragraphs = []
                for name in names:
                    xml = archive.read(name)
                    if b'<!DOCTYPE' in xml.upper() or b'<!ENTITY' in xml.upper():
                        raise ValueError('This Word file contains unsupported XML declarations.')
                    root = ElementTree.fromstring(xml)
                    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
                    for p in root.iter(ns + 'p'):
                        paragraphs.append(''.join(n.text or '' for n in p.iter(ns + 't')))
                text = '\n'.join(paragraphs)
        except (zipfile.BadZipFile, KeyError, ElementTree.ParseError, RuntimeError):
            raise ValueError('Could not read this DOCX. Export it again or paste your experience.') from None
    elif ext == '.pdf':
        from pypdf import PdfReader
        try:
            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted:
                raise ValueError('Password-protected PDFs are not supported. Upload an unlocked copy.')
            if len(reader.pages) > 15:
                raise ValueError('Please upload a resume with 15 pages or fewer.')
            parts = []
            for page in reader.pages:
                parts.append(page.extract_text() or '')
            text = '\n'.join(parts)
        except ValueError:
            raise
        except Exception:
            raise ValueError('Could not read this PDF. Try DOCX or paste your experience.') from None
    else:
        raise ValueError('Choose a PDF, DOCX, or UTF-8 TXT file. Legacy .doc files are not supported.')
    text = ''.join(c for c in text if c in '\n\t' or ord(c) >= 32).strip()
    if not text:
        raise ValueError('No readable text found. Scanned/image resumes need OCR first, or you can paste your experience.')
    truncated = len(text) > MAX_TEXT
    return {'text': text[:MAX_TEXT], 'truncated': truncated,
            'notice': ('Only the first 10,000 characters were imported. ' if truncated else '') + 'Review the reading order and remove contact details you do not want to share.'}

if __name__ == '__main__':
    try:
        result = extract_resume(sys.stdin.buffer.read(MAX_BYTES + 1), sys.argv[1])
    except Exception as exc:
        result = {'error': str(exc) if isinstance(exc, ValueError) else 'Could not extract this file. Try a different format.'}
    print(json.dumps(result))
