"""Generate PhysicsMate.pptx from scratch (OOXML zipped with the stdlib).
No python-pptx / LibreOffice needed. 16:9, editable in PowerPoint/Keynote/Slides."""
import pathlib
import zipfile
from xml.sax.saxutils import escape

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "PhysicsMate.pptx"
EMU = 914400  # per inch
TEAL = "14A8A0"; DARK = "1F2A28"; GREY = "5A6A66"; DEEP = "0D5750"

# ---- slide content: (title, subtitle_or_None, [bullet lines]) ----
BASE = [
    ("PhysicsMate", "Curriculum-Grounded Bengali Physics QA with Small Language Models",
     ["NCTB Grade 9-10  ·  Rashid Azraf & Saadman Sajid", "Final Project Presentation — August 29, 2026"]),
    ("The Problem", None,
     ["Bengali ~230M speakers, tiny presence in educational NLP",
      "No curriculum-specific Bengali physics QA resource",
      "Target users (BD classrooms) often have no reliable internet / weak hardware",
      "So the real constraint is: offline, on cheap hardware"]),
    ("Research Question", None,
     ["Can a small, curriculum-grounded dataset teach a SMALL model enough",
      "   Bengali physics to be useful OFFLINE — and how does the benefit scale with size?",
      "",
      "Two outputs:  a reusable benchmark  +  a deployable model"]),
    ("Data Pipeline", None,
     ["NCTB book scans  →  vision OCR  →  clean Markdown",
      "811 text chunks across 13 chapters",
      "Knowledge graph: 1,760 nodes / 2,600 edges (10 node types)",
      "1,834 QA pairs, each grounded on a graph node",
      "Split 1374 / 185 / 275  (seed 42, stratified, held-out test)"]),
    ("Method", None,
     ["LoRA fine-tuning of 4-bit Qwen3 at 0.6B / 1.7B / 4B",
      "Closed-book: no retrieval — isolates what the DATASET teaches",
      "Only small adapters trained → feasible on one consumer machine"]),
    ("Headline Result", "Fine-tuning wins at every size — and the gain grows with size",
     ["Qwen3-0.6B :   0.0%  →   5.5%   accuracy   (+5.5 pp)",
      "Qwen3-1.7B :  10.5%  →  25.5%   accuracy   (+15.0 pp)",
      "Qwen3-4B   :  27.6%  →  50.9%   accuracy   (+23.3 pp)",
      "",
      "Same dataset, bigger model, bigger payoff  (n = 275 held-out)"]),
    ("Honest & Reproducible", None,
     ["Token-F1 + BERTScore are deterministic — verify.py re-derives & asserts them",
      "Accuracy = LLM-as-a-judge (MT-Bench protocol), to corroborate",
      "n = 275, one fixed judge prompt across all 6 model variants",
      "One command reproduces every deterministic number"]),
    ("Deployment  (live demo)", None,
     ["Each model → Q4_K_M GGUF (0.4 / 1.1 / 2.5 GB) → Ollama, fully offline",
      "Local web app: switch 0.6B / 1.7B / 4B, streaming, Bangla + English",
      "DEMO: ask one question, switch sizes, watch quality climb"]),
    ("Also Built: Hybrid RAG", None,
     ["BM25 + dense (BGE-M3) + graph → RRF fusion",
      "Optimised pipeline: dedup, boundary stitching, verifier, refusal gate",
      "Fine-tuned 4B reaches PARITY with RAG on a leakage-free subset",
      "→ adaptation can reduce dependence on retrieval at inference"]),
    ("Takeaways & Future", None,
     ["A reusable Bengali curriculum QA benchmark (1,834 QA, KG-grounded)",
      "Fine-tuning helps at every size; payoff scales with capacity",
      "Offline, 2.5 GB deployment for real classrooms",
      "Next: HSC (11-12) via the KG bridge; human-rated test set",
      "", "Thank you — questions?"]),
]

# optional slides that get added in later presentation versions
FAILURE_SLIDE = ("What Went Wrong (and the Redo)", None,
    ["1st system was REJECTED in review — rebuilt from scratch:",
     "   Tesseract OCR (garbled Bangla)   →   vision-model OCR, page by page",
     "   33-node 'chapter graph'          →   1,760-node concept graph",
     "   3,502 noisy chunks / scraped QA  →   811 clean chunks / 1,834 grounded QA",
     "Fine-tuning failures: ~20 Kaggle GPU crashes; early LoRA lost to baseline",
     "   (catastrophic forgetting); a broken eval run (nan scores) — discarded",
     "Fix: clean closed-book retrain at 3 sizes, measured vs a frozen baseline"])

VERSION_SLIDE = ("Data & Model Journey: v1 → v2 → v3", None,
    ["v1  (rejected):  Tesseract OCR · 3,502 noisy chunks · 33-node chapter",
     "     graph · QA scraped from question banks · agentic-RAG prototype",
     "v2  (rebuilt):   vision OCR page-by-page · 811 clean chunks ·",
     "     1,760-node concept graph · 1,834 QA grounded on graph nodes",
     "v3  (shipped):   closed-book LoRA retrain at 0.6B / 1.7B / 4B →",
     "     the deployed offline GGUF models",
     "Each version fixed the previous one's rejected weakness."])


def run(text, sz, color, bold=True):
    b = ' b="1"' if bold else ''
    return (f'<a:r><a:rPr lang="en-US" sz="{sz}"{b} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr>'
            f'<a:t>{escape(text)}</a:t></a:r>')


def para(text, sz, color, bold=False, bullet=False, align=None):
    algn = f' algn="{align}"' if align else ''
    if bullet and text.strip():
        pPr = f'<a:pPr marL="285750" indent="-285750"{algn}><a:buFont typeface="Arial"/><a:buChar char="&#8226;"/></a:pPr>'
    else:
        pPr = f'<a:pPr{algn}><a:buNone/></a:pPr>'
    if not text.strip():
        return f'<a:p>{pPr}</a:p>'
    return f'<a:p>{pPr}{run(text, sz, color, bold)}</a:p>'


def textbox(sid, name, x, y, cx, cy, paras):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square"><a:normAutofit/></a:bodyPr><a:lstStyle/>'
            f'{"".join(paras)}</p:txBody></p:sp>')


def slide_xml(idx, title, subtitle, bullets):
    in_ = lambda v: int(v * EMU)
    shapes = []
    if idx == 0:  # title slide, centered
        shapes.append(textbox(2, "Title", in_(1), in_(2.4), in_(11.33), in_(1.6),
                              [para(title, 5400, TEAL, True, align="ctr")]))
        subs = [para(subtitle, 2000, DEEP, False, align="ctr")] if subtitle else []
        subs += [para(b, 1500, GREY, False, align="ctr") for b in bullets]
        shapes.append(textbox(3, "Sub", in_(1), in_(4.1), in_(11.33), in_(2.2), subs))
    else:
        shapes.append(textbox(2, "Title", in_(0.6), in_(0.35), in_(12.1), in_(1.0),
                              [para(title, 3600, TEAL, True)]))
        body = []
        if subtitle:
            body.append(para(subtitle, 2000, DEEP, True))
            body.append(para("", 1200, GREY))
        body += [para(b, 1800, DARK, False, bullet=bool(b.strip()) and not b.startswith("   ")) for b in bullets]
        shapes.append(textbox(3, "Body", in_(0.7), in_(1.7), in_(11.9), in_(5.3), body))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:cSld><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{"".join(shapes)}'
            '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')


# ---- static parts ----
THEME = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office">
<a:themeElements><a:clrScheme name="Office">
<a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1><a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>
<a:dk2><a:srgbClr val="0D5750"/></a:dk2><a:lt2><a:srgbClr val="E7F1EF"/></a:lt2>
<a:accent1><a:srgbClr val="14A8A0"/></a:accent1><a:accent2><a:srgbClr val="4FC0B5"/></a:accent2>
<a:accent3><a:srgbClr val="0A6F6B"/></a:accent3><a:accent4><a:srgbClr val="6FE0D5"/></a:accent4>
<a:accent5><a:srgbClr val="2BB3AA"/></a:accent5><a:accent6><a:srgbClr val="0D857F"/></a:accent6>
<a:hlink><a:srgbClr val="14A8A0"/></a:hlink><a:folHlink><a:srgbClr val="0A6F6B"/></a:folHlink></a:clrScheme>
<a:fontScheme name="Office"><a:majorFont><a:latin typeface="Helvetica Neue"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
<a:minorFont><a:latin typeface="Helvetica Neue"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme>
<a:fmtScheme name="Office"><a:fillStyleLst>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle>
<a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
</a:themeElements></a:theme>'''

LAYOUT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
<p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'''

MASTER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>
<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
</p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>'''


def build(out_path, slides):
    global OUT
    OUT = out_path
    SLIDES = slides
    n = len(SLIDES)
    sldIds = "".join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(n))
    presentation = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{sldIds}</p:sldIdLst>'
        '<p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>'
        '<p:notesSz cx="6858000" cy="9144000"/></p:presentation>')

    pres_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    for i in range(n):
        pres_rels.append(f'<Relationship Id="rId{i+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')
    pres_rels.append(f'<Relationship Id="rId{n+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>')
    pres_rels.append('</Relationships>')

    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>']
    for i in range(n):
        ct.append(f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
    ct.append('</Types>')

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
        '</Relationships>')

    master_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        '</Relationships>')
    layout_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
        '</Relationships>')

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", "".join(pres_rels))
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
        for i, (title, sub, bullets) in enumerate(SLIDES):
            z.writestr(f"ppt/slides/slide{i+1}.xml", slide_xml(i, title, sub, bullets))
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                '</Relationships>')
    print(f"wrote {OUT}  ({len(SLIDES)} slides)")


if __name__ == "__main__":
    # v1: the original result-focused deck
    v1 = list(BASE)
    # v2: + the "What Went Wrong (and the Redo)" slide, after the Headline Result
    v2 = BASE[:6] + [FAILURE_SLIDE] + BASE[6:]
    # v3: + an explicit v1->v2->v3 journey slide (after Data Pipeline) as well
    v3 = BASE[:4] + [VERSION_SLIDE] + BASE[4:6] + [FAILURE_SLIDE] + BASE[6:]

    build(HERE / "Presentation1.pptx", v1)
    build(HERE / "Presentation2.pptx", v2)
    build(HERE / "Presentation3.pptx", v3)
    print(f"v1={len(v1)} slides, v2={len(v2)} slides, v3={len(v3)} slides")
