# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r"D:\ITA\report\template\Mini project template.docx"
OUT = r"D:\ITA\report\CropSentinel_Mini_Project_Report.docx"
ASSETS = r"D:\ITA\report\assets"

doc = docx.Document(SRC)
INK = RGBColor(0x1A, 0x1A, 0x1A)
figure_log = []   # (number, title)
table_log = []
listing_log = []

# ---------------- helpers ----------------

def add_page_break_paragraph():
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(docx.enum.text.WD_BREAK.PAGE)
    return p


def chapter_title(num, title):
    p1 = doc.add_paragraph()
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(6)
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(f"CHAPTER {num}")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(15); r1.font.bold = True; r1.font.color.rgb = INK
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_after = Pt(14)
    r2 = p2.add_run(title)
    r2.font.name = "Times New Roman"; r2.font.size = Pt(15); r2.font.bold = True; r2.font.color.rgb = INK
    return p2


def front_title(title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(title)
    r.font.name = "Times New Roman"; r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = INK
    return p


def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = "Times New Roman"; run.font.size = Pt(13); run.font.bold = True; run.font.color.rgb = INK
    return p


def h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = "Times New Roman"; run.font.size = Pt(12); run.font.bold = True; run.font.color.rgb = INK
    return p


def body(segments, justify=True, space_after=8):
    """segments: str, or list of (text, bold) tuples for a bold lead-in phrase."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if isinstance(segments, str):
        segments = [(segments, False)]
    for text, bold in segments:
        run = p.add_run(text)
        run.font.name = "Times New Roman"; run.font.size = Pt(12)
        run.font.bold = bold; run.font.color.rgb = INK
    return p


def bullet(segments):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.2)
    marker = p.add_run("\u2022\u0009")
    marker.font.name = "Times New Roman"; marker.font.size = Pt(12); marker.font.color.rgb = INK
    if isinstance(segments, str):
        segments = [(segments, False)]
    for text, bold in segments:
        run = p.add_run(text)
        run.font.name = "Times New Roman"; run.font.size = Pt(12)
        run.font.bold = bold; run.font.color.rgb = INK
    return p


def figure(path, chapter, num, title, width_in=5.6):
    fig_no = f"{chapter}.{num}"
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    run = p.add_run()
    run.add_picture(path, width=Inches(width_in))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(14)
    r = cap.add_run(f"Figure {fig_no}: {title}")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = INK
    figure_log.append((fig_no, title))
    return p


def table_caption(chapter, num, title):
    tno = f"{chapter}.{num}"
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(10)
    cap.paragraph_format.space_after = Pt(4)
    r = cap.add_run(f"Table {tno}: {title}")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = INK
    table_log.append((tno, title))
    return tno


def data_table(rows, col_widths_in):
    tbl = doc.add_table(rows=0, cols=len(rows[0]))
    tbl.style = "Table Grid"
    for ri, row in enumerate(rows):
        cells = tbl.add_row().cells
        for ci, text in enumerate(row):
            cells[ci].width = Inches(col_widths_in[ci])
            p = cells[ci].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.name = "Times New Roman"; run.font.size = Pt(10.5)
            run.font.bold = (ri == 0)
            run.font.color.rgb = INK
            if ri == 0:
                shade = OxmlElement("w:shd")
                shade.set(qn("w:fill"), "E7E7E7")
                cells[ci]._tc.get_or_add_tcPr().append(shade)
    after = doc.add_paragraph()
    after.paragraph_format.space_after = Pt(12)
    return tbl


def listing_caption(chapter, num, title):
    lno = f"{chapter}.{num}"
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(8)
    cap.paragraph_format.space_after = Pt(4)
    r = cap.add_run(f"Listing {lno}: {title}")
    r.font.name = "Times New Roman"; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = INK
    listing_log.append((lno, title))
    return lno


def code_block(lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    cell = tbl.rows[0].cells[0]
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    shade = OxmlElement("w:shd")
    shade.set(qn("w:fill"), "F2F2F2")
    cell._tc.get_or_add_tcPr().append(shade)
    first = True
    for line in lines:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"; run.font.size = Pt(9); run.font.color.rgb = RGBColor(0x20, 0x20, 0x20)
    after = doc.add_paragraph()
    after.paragraph_format.space_after = Pt(10)
    return tbl


# ================= COVER PAGE: fill title and author =================
TITLE_TEXT = "CropSentinel: Field Intelligence, A Pest Identification and Response Dashboard for the IP102 Benchmark"
AUTHOR_LINE = "KEVIN ANDREW A (Reg No)"

for p in doc.paragraphs:
    if p.text.strip() == "Title":
        for r in list(p.runs):
            r.text = ""
        p.runs[0].text = TITLE_TEXT.upper()
        break

for p in doc.paragraphs:
    if p.text.strip() == "STUDENT NAME (Reg No)":
        for r in list(p.runs):
            r.text = ""
        p.runs[0].text = AUTHOR_LINE
        break

for p in doc.paragraphs:
    if p.text.strip() == "MONTH  YEAR" or p.text.strip() == "MONTH YEAR":
        for r in list(p.runs):
            r.text = ""
        p.runs[0].text = "OCTOBER 2026"
        break

# Bonafide certificate paragraph
for p in doc.paragraphs:
    if "bonafide work of" in p.text and "Title" in p.text:
        full = "".join(r.text for r in p.runs)
        for r in list(p.runs):
            r.text = ""
        p.runs[0].text = (
            f'Certified that this Mini project report "{TITLE_TEXT}" is the bonafide work of '
            f"Kevin Andrew A (Reg No), who carried out the project work under my supervision."
        )
        break

# Acknowledgement: convert the template's plural voice to a single-author voice
REPLACEMENTS = [
    ("Above all, we thank God, whose blessings, grace, and guidance made this journey possible. "
     "It is through His strength that we found the courage and capability to see this project "
     "through, and for that, we are truly grateful.",
     "Above all, I thank God, whose blessings, grace, and guidance made this journey possible. "
     "It is through His strength that I found the courage and capability to see this project "
     "through, and for that, I am truly grateful."),
    ("We owe a deep debt of gratitude to our Director, Rev. Dr. Justine SJ, and our Dean of "
     "Students, Rev. Dr. Albert William SJ, whose encouragement never wavered and whose timely "
     "support made all the difference. Their belief in us kept us going when it mattered the most.",
     "I owe a deep debt of gratitude to our Director, Rev. Dr. Justine SJ, and our Dean of "
     "Students, Rev. Dr. Albert William SJ, whose encouragement never wavered and whose timely "
     "support made all the difference. Their belief in me kept me going when it mattered the most."),
    ("We are sincerely thankful to our Principal, Dr. A. Baskar, M.E., Ph.D., for his inspiring "
     "words and steady motivation throughout this journey. His support gave us the confidence to "
     "push forward and give our best.",
     "I am sincerely thankful to our Principal, Dr. A. Baskar, M.E., Ph.D., for his inspiring "
     "words and steady motivation throughout this journey. His support gave me the confidence to "
     "push forward and give my best."),
    ("We would like to warmly acknowledge our Head of the Department Ms. Sherril Sophie Maria "
     "Vincent, M.E., whose thoughtful suggestions and constructive feedback shaped this project in "
     "meaningful ways.",
     "I would like to warmly acknowledge our Head of the Department Ms. Sherril Sophie Maria "
     "Vincent, M.E., whose thoughtful suggestions and constructive feedback shaped this project in "
     "meaningful ways."),
    ("A special word of thanks goes to our faculty, Ms. Sylvia Irish S, M.E., who walked with us "
     "every step of the way. We also thank the faculty members and technical staff of our "
     "department, whose advice and expertise helped us navigate every challenge along the way.",
     "A special word of thanks goes to my faculty guide, Ms. Sylvia Irish S, M.E., who walked with "
     "me every step of the way. I also thank the faculty members and technical staff of my "
     "department, whose advice and expertise helped me navigate every challenge along the way."),
]
for p in doc.paragraphs:
    t = p.text.strip()
    for old, new in REPLACEMENTS:
        if t == old:
            for r in list(p.runs):
                r.text = ""
            p.runs[0].text = new
            break

# ================= ABSTRACT =================
for p in doc.paragraphs:
    if p.text.strip() == "Abstract of the project":
        for r in list(p.runs):
            r.text = ""
        p.runs[0].text = (
            "Pest damage is one of the most persistent causes of crop loss in smallholder "
            "agriculture, and the first identification step, deciding what insect is actually "
            "present in a photograph, is often the hardest part for a non-specialist grower or "
            "student to get right. CropSentinel is a deployable, browser-based pest intelligence "
            "dashboard that accepts a single field photograph and returns a preliminary "
            "identification, a calibrated confidence score, and a tiered action ladder that starts "
            "with prevention and ends with chemical control only as a last resort. The system is "
            "built on a Streamlit front end, a PyTorch EfficientNet-B0 classifier trained against "
            "the IP102 insect pest benchmark of 102 classes, and a curated recommendation knowledge "
            "base that is deliberately conservative about prescribing chemical treatment. The "
            "project includes a complete data preparation pipeline for the official IP102 "
            "classification archive, a training script with class-balanced sampling, an evaluation "
            "script that reports accuracy, macro F1, and a full confusion matrix, and a transparent "
            "demo mode that remains honest about its own uncertainty when no trained checkpoint is "
            "available. A full held-out evaluation of the locally produced checkpoint across all "
            "22,619 IP102 test images returned an accuracy of 1.48 percent, close to the "
            "random-guess baseline of 0.98 percent for 102 classes; this result is reported in full "
            "because the checkpoint in the repository was produced by an architecture smoke test "
            "rather than a full pretrained training run, and the report treats this as a documented "
            "limitation and not as an inflated claim. The surrounding engineering, the data "
            "pipeline, the interface, the safety boundary, and the evaluation harness, is verified "
            "and working, and the report sets out exactly what remains before the system can be "
            "trusted for a real identification task."
        )
        p.runs[0].font.name = "Times New Roman"; p.runs[0].font.size = Pt(12)
        kw = doc.add_paragraph()
        kw.paragraph_format.space_before = Pt(10)
        kr1 = kw.add_run("Keywords: ")
        kr1.bold = True; kr1.font.name = "Times New Roman"; kr1.font.size = Pt(12); kr1.font.color.rgb = INK
        kr2 = kw.add_run(
            "pest identification, IP102 benchmark, EfficientNet, convolutional neural network, "
            "decision support, Streamlit, class imbalance, confidence calibration."
        )
        kr2.font.name = "Times New Roman"; kr2.font.size = Pt(12); kr2.font.color.rgb = INK
        # move the keywords paragraph to sit right after the abstract paragraph,
        # followed by a page break so the Table of Content always starts fresh
        p._p.addnext(kw._p)
        pbreak = doc.add_paragraph()
        pbreak_run = pbreak.add_run()
        pbreak_run.add_break(docx.enum.text.WD_BREAK.PAGE)
        kw._p.addnext(pbreak._p)
        break

# ================= start chapter content after the TOC =================
add_page_break_paragraph()

# ---------------- LIST OF FIGURES (placeholder page numbers, patched later) ----------------
front_title("LIST OF FIGURES")
LOF_ROWS = [
    ["Figure No.", "Title", "Page No."],
    ["Figure 3.1", "IP102 classification split sizes produced by prepare_ip102.py", "?"],
    ["Figure 3.2", "End-to-end CropSentinel data flow, from image upload to the displayed action ladder", "?"],
    ["Figure 4.1", "Accuracy under the architecture smoke test, the full held-out test evaluation, and a random-guess baseline", "?"],
    ["Figure 4.2", "Row-normalised confusion matrix for the fifteen highest-support IP102 classes, full test split", "?"],
    ["Figure 5.1", "CropSentinel landing view, sidebar mission control, and image upload panel", "?"],
    ["Figure 5.2", "Low-confidence prediction panel, correctly flagged as Review by the interface", "?"],
    ["Figure 5.3", "Three-tier action ladder and safety boundary notice shown for a low-confidence prediction", "?"],
]
data_table(LOF_ROWS, [0.9, 4.9, 0.8])

add_page_break_paragraph()
front_title("LIST OF ABBREVIATIONS")
LOA_ROWS = [
    ["Abbreviation", "Expansion"],
    ["CNN", "Convolutional Neural Network"],
    ["CPU", "Central Processing Unit"],
    ["GPU", "Graphics Processing Unit"],
    ["HTTP", "Hypertext Transfer Protocol"],
    ["IT", "Information Technology"],
    ["JSON", "JavaScript Object Notation"],
    ["LICET", "Loyola-ICAM College of Engineering and Technology"],
    ["ML", "Machine Learning"],
    ["RGB", "Red, Green, Blue (image colour channels)"],
]
data_table(LOA_ROWS, [1.8, 4.8])

# ---------------- restart page numbering at 1 (arabic) for chapter content ----------------
from docx.enum.section import WD_SECTION

new_section = doc.add_section(WD_SECTION.NEW_PAGE)
sectPr = new_section._sectPr
pgNumType = OxmlElement("w:pgNumType")
pgNumType.set(qn("w:start"), "1")
pgNumType.set(qn("w:fmt"), "decimal")
sectPr.append(pgNumType)

footer = new_section.footer
footer.is_linked_to_previous = False
for p in list(footer.paragraphs):
    p._element.getparent().remove(p._element)
fp = footer.add_paragraph()
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
begin = OxmlElement("w:fldChar"); begin.set(qn("w:fldCharType"), "begin")
instr = OxmlElement("w:instrText"); instr.set(qn("xml:space"), "preserve"); instr.text = " PAGE "
sep = OxmlElement("w:fldChar"); sep.set(qn("w:fldCharType"), "separate")
txt = OxmlElement("w:t"); txt.text = "1"
end = OxmlElement("w:fldChar"); end.set(qn("w:fldCharType"), "end")
for el in (begin, instr, sep, txt, end):
    run = fp.add_run()
    run.font.name = "Times New Roman"; run.font.size = Pt(11)
    run._r.append(el)

# ---------------- CHAPTER 1 ----------------
chapter_title(1, "INTRODUCTION")

h2("1.1 Background")
body(
    "Insect pests are a major and recurring cause of yield loss in field crops, vegetables, and "
    "orchards. Effective management depends on an early and correct identification of the insect "
    "responsible for the damage, because the appropriate response, whether a preventive cultural "
    "practice, a biological control agent, or a chemical application, differs substantially from "
    "one pest species to another. In practice, this identification step is frequently performed by "
    "a grower or a student with a smartphone camera and limited entomological training, working "
    "from visual memory, a printed guide, or an informal online search. The IP102 dataset, "
    "published by Wu et al. [1], was assembled specifically to support automated visual "
    "recognition of 102 common insect pest categories found in agricultural settings, and it forms "
    "the empirical foundation of this project."
)

h2("1.2 Problem statement")
body(
    "A grower who photographs an unfamiliar insect on a crop has no fast, structured way to connect "
    "that photograph to a short list of likely species and a correspondingly cautious set of next "
    "steps. Existing options are either a general image search, which returns no confidence "
    "estimate and no safety framing, or a generic pest identification app, which commonly presents "
    "a single high-confidence label without disclosing the model's actual uncertainty. The result "
    "is a real risk of over-treatment, under-treatment, or misapplied chemical control based on an "
    "unverified guess."
)
bullet([("How much should this prediction be trusted? ", True), ("A confident-looking label and a near-random guess can look identical in the interface unless the confidence score is surfaced and acted upon.", False)])
bullet([("What should the user actually do next? ", True), ("A label alone gives no guidance; a safe product needs a tiered, conservative response that a non-specialist can follow.", False)])
bullet([("Which inference path produced the result? ", True), ("A demo heuristic and a trained model must never be presented identically, or a placeholder output could be mistaken for a verified one.", False)])
body(
    "CropSentinel addresses this gap by pairing a trained image classifier with an explicit "
    "confidence display and a tiered, safety-first recommendation ladder, so a low-confidence "
    "prediction is visibly treated as a reason to gather more evidence rather than as a licence to "
    "act."
)

h2("1.3 Motivation and Significance")
body(
    "The motivation for this project is twofold. First, image classification on a long-tailed, "
    "fine-grained benchmark such as IP102 is a genuinely difficult machine learning problem, and "
    "building and honestly evaluating a working pipeline against it is a meaningful exercise in "
    "applied computer vision. Second, the consequence of a wrong pest identification in the field "
    "is not merely an inconvenience, it can lead to unnecessary chemical use, wasted cost, and harm "
    "to beneficial insects, so the project is also an exercise in building a decision-support "
    "interface that is transparent about its own limitations rather than one that hides them behind "
    "a confident-looking output."
)

h2("1.4 Project Overview")
body(
    "CropSentinel is a Streamlit web application named for its role as a watchful, first-pass "
    "assistant rather than an autonomous decision maker. A user uploads a photograph of an insect "
    "or of crop damage; the application preprocesses the image, classifies it with either a trained "
    "EfficientNet-B0 convolutional neural network (CNN) checkpoint or a transparent demo heuristic "
    "when no checkpoint is present, and displays the predicted pest label together with a "
    "confidence score. The result is then matched against a recommendation knowledge base that "
    "returns a three-tier action ladder, observation and prevention, organic or biological control, "
    "and chemical control only if needed, along with an explicit safety notice. The current "
    "session's observations can be exported as a JSON log."
)

h2("1.5 System Functionality")
bullet("Accepts JPG, JPEG, PNG, and WEBP image uploads up to the configured size limit.")
bullet("Classifies the uploaded image with a PyTorch EfficientNet-B0 model exported as TorchScript, or falls back to a labelled demo heuristic when no checkpoint is installed.")
bullet("Displays the predicted label, a confidence percentage, and a risk mode of Review or Actionable based on a 75 percent confidence threshold.")
bullet("Looks up a tiered action ladder, prevention, organic or biological control, and chemical control, from a JSON recommendation knowledge base, with a caterpillar-family fallback for unmapped labels above a minimum confidence.")
bullet("Keeps a session history of up to 20 observations and offers a one-click JSON export.")
bullet("Reports whether the EfficientNet checkpoint actually loaded, so the user always knows which mode produced a given result.")

h2("1.6 Objectives")
bullet("Build a complete, reproducible pipeline from the raw IP102 classification archive to a trained, TorchScript-exported classifier.")
bullet("Expose that classifier through an accessible, informative web interface with a visible confidence signal.")
bullet("Encode a conservative, tiered recommendation policy that never proposes a specific chemical product, dose, or schedule.")
bullet("Evaluate the trained checkpoint honestly on a held-out test split and report the result without inflation.")
bullet("Package the application for container-based deployment with a health check endpoint.")

h2("1.7 Design Philosophy and Approach")
body([
    ("Four principles shaped the design. First, ", False),
    ("the interface always names its source", True),
    (": every result states whether it came from the trained checkpoint or the demo heuristic, so a "
     "placeholder output is never mistaken for a verified identification. Second, ", False),
    ("confidence is never hidden", True),
    (": it is surfaced numerically and visually, and a low score actively changes the on-screen "
     "guidance rather than sitting in a tooltip. Third, ", False),
    ("the recommendation ladder is conservative by construction", True),
    (": prevention and biological options are always shown before chemical control. Fourth, ", False),
    ("the knowledge base never prescribes a product", True),
    (": chemical guidance is written as general, locally-verifiable guidance that defers the dose "
     "and product decision to an authoritative local source and a human expert.", False),
])

h2("1.8 Broader Impact")
body(
    "A correctly scoped tool of this kind can shorten the time between noticing crop damage and "
    "taking an appropriate, proportionate action, which matters most for smallholder and student "
    "growers who do not have ready access to an agricultural extension officer. Because the action "
    "ladder foregrounds non-chemical options, the tool also has the potential to reduce unnecessary "
    "pesticide use, which carries both a cost and an environmental benefit when it works as "
    "intended."
)

h2("1.9 Educational Value")
body(
    "Building CropSentinel required working across the full applied machine learning lifecycle: "
    "converting a published benchmark archive into a usable directory structure, handling severe "
    "class imbalance with a weighted sampler, training and exporting a CNN, writing an evaluation "
    "harness that produces a full classification report and confusion matrix, and wrapping the "
    "result in a usable, tested interface with a Docker deployment path. It is also a concrete "
    "lesson in the gap between an architecture that runs without errors and a model that has "
    "actually learned the task, a gap that Chapter 4 of this report documents in detail rather than "
    "glossing over."
)

h2("1.10 Conclusion")
body(
    "This chapter has set out the problem CropSentinel addresses, the functionality it provides, "
    "and the safety-first philosophy behind its design. The remaining chapters describe the tools "
    "used, the system implementation, a full and honest performance evaluation, representative "
    "screenshots and code, and the conclusions drawn from building and testing the system."
)

# ---------------- CHAPTER 2 ----------------
add_page_break_paragraph()
chapter_title(2, "TOOLS AND TECHNOLOGIES USED")

h2("2.1 Python Programming Language")
body(
    "The entire project is implemented in Python 3.11. Python was chosen for its mature machine "
    "learning ecosystem, its direct interoperability with PyTorch and Streamlit, and its "
    "suitability for rapid, readable data pipeline scripts such as the IP102 preparation utility."
)

h2("2.2 PyTorch, TorchVision, and EfficientNet")
body(
    "The classifier is built on PyTorch and TorchVision. The chosen architecture is EfficientNet-B0 "
    "[2], a compound-scaled CNN selected for its favourable accuracy-to-parameter-count ratio "
    "relative to larger convolutional networks, which matters for a model that may need to run on "
    "modest hardware. The final classification layer is replaced with a linear layer sized to the "
    "102 IP102 classes, and the trained model is exported with TorchScript (torch.jit.script) so "
    "that it can be loaded by the Streamlit application without a dependency on the original "
    "model-definition code at inference time."
)

h2("2.3 Streamlit and the Application Interface")
body(
    "Streamlit provides the web application layer. It was chosen because it allows a complete, "
    "interactive, file-upload-driven interface to be built directly in Python, with no separate "
    "front-end build step, which keeps the inference logic and the presentation logic in a single, "
    "auditable file, app.py. The interface additionally uses Streamlit's session state to retain an "
    "observation history across interactions within one browser session."
)

h2("2.4 Summary")
table_caption(2, 1, "Technology stack of CropSentinel")
TECH_ROWS = [
    ["Layer", "Tool / library", "Used for"],
    ["Language", "Python 3.11", "Entire pipeline and application"],
    ["Modelling", "PyTorch, TorchVision, EfficientNet-B0", "Training, export, and inference"],
    ["Evaluation", "scikit-learn", "Accuracy, macro F1, classification report, confusion matrix"],
    ["Interface", "Streamlit", "File upload, result display, session history"],
    ["Imaging", "Pillow, NumPy", "Image loading, resizing, demo-mode heuristic"],
    ["Knowledge base", "JSON (data/recommendations.json)", "Tiered action ladder content"],
    ["Testing", "pytest", "Recommendation schema and asset presence checks"],
    ["Deployment", "Docker", "Reproducible, health-checked container build"],
    ["Tooling", "Visual Studio Code, Git", "Development and version control"],
]
data_table(TECH_ROWS, [1.2, 2.6, 2.8])
body(
    "Together these tools form a pipeline in which prepare_ip102.py converts the official archive "
    "into ImageFolder-compatible directories, train.py produces a TorchScript checkpoint, "
    "evaluate.py scores that checkpoint, and app.py serves the result to a user, with pytest and "
    "Docker providing a baseline of correctness and deployability."
)

# ---------------- CHAPTER 3 ----------------
add_page_break_paragraph()
chapter_title(3, "SYSTEM IMPLEMENTATION")

h2("3.1 Dataset")
body(
    "The project uses the IP102 classification benchmark, a large-scale, 102-class insect pest "
    "image dataset [1]. The archive is processed by prepare_ip102.py, which extracts the official "
    "tar archive, reads the accompanying classes.txt and per-split label files, and copies each "
    "image into an ImageFolder-compatible directory named with its numeric class index and a "
    "sanitised class name, for example 000_rice_leaf_roller. The verified local preparation "
    "produced the following split sizes."
)
figure(f"{ASSETS}/fig2_dataset_split.png", 3, 1, "IP102 classification split sizes produced by prepare_ip102.py.")
body(
    "The resulting train, validation, and test directories total 75,222 images across 102 classes, "
    "with a pronounced class imbalance that the training pipeline addresses directly (see Section "
    "3.3)."
)

h2("3.2 System Architecture")
body(
    "CropSentinel follows a linear, single-service architecture, summarised in Figure 3.2. A user "
    "interacts with the Streamlit dashboard, which preprocesses the uploaded image to a 224 by 224 "
    "RGB tensor and routes it to either the TorchScript EfficientNet checkpoint or, when no "
    "checkpoint is present, a transparent demo predictor. The resulting label and confidence are "
    "looked up in a JSON recommendation knowledge base, and the dashboard renders the matched "
    "action ladder together with a fixed safety notice."
)
figure(f"{ASSETS}/fig1_architecture.png", 3, 2, "End-to-end CropSentinel data flow, from image upload to the displayed action ladder.")

h2("3.3 Modules Description")
h3("3.3.1 Data preparation, prepare_ip102.py")
body(
    "Converts the raw IP102 archive into ImageFolder directories for the train, val, and test "
    "splits, and writes a class_names.txt mapping file. It uses regular-expression parsing to "
    "recover class names from classes.txt and tolerates split files that are not already perfectly "
    "aligned with the extracted image tree by searching recursively for a matching filename."
)
h3("3.3.2 Training, train.py")
body(
    "Builds an EfficientNet-B0 model, optionally initialised from ImageNet pretrained weights, and "
    "replaces its classifier head for 102 classes. Class imbalance in the training split is "
    "addressed with a WeightedRandomSampler, where each training example is weighted by the "
    "inverse frequency of its class, so that rare pest classes are not drowned out by common ones "
    "during optimisation. The script supports a reduced, no-pretrained, per-class-limited smoke "
    "mode intended only to verify that the training loop and the export path work end to end, not "
    "to produce a usable classifier. After each epoch, if validation accuracy improves, the script "
    "saves a new TorchScript checkpoint and an updated class_names.json."
)
h3("3.3.3 Evaluation, evaluate.py")
body(
    "Loads a TorchScript checkpoint and a chosen ImageFolder split, runs inference in batches of "
    "32, and writes a JSON report containing the sample count, overall accuracy, macro-averaged F1 "
    "score, a full per-class classification report, and the complete confusion matrix. The split to "
    "evaluate against, train, val, or test, is a command-line argument, which allowed this project "
    "to separately confirm an architecture smoke result and a full, held-out test result from the "
    "same script."
)
h3("3.3.4 Application, app.py")
body(
    "Implements the Streamlit dashboard. Its predict function loads the TorchScript checkpoint once "
    "via Streamlit's cache_resource decorator, and falls back to demo_predict, a deterministic "
    "heuristic based on mean colour and edge energy, when no checkpoint file is found. The "
    "get_pest_profile function resolves a predicted label to a recommendation record, with a "
    "confidence-gated fallback to a generic caterpillar-family entry for labels that contain terms "
    "such as armyworm, cutworm, or borer but are not individually present in the knowledge base."
)
h3("3.3.5 Recommendation knowledge base, data/recommendations.json")
body(
    "A structured JSON file mapping a small set of pest keys, aphids, fall armyworm, beet armyworm, "
    "caterpillar, and a default unknown entry, to a common name, scientific name, affected crops, "
    "and three guidance lists: prevent, organic, and chemical. Every chemical entry is phrased as "
    "general guidance that defers the actual product and dose decision to a locally approved "
    "source, in line with the project's safety boundary."
)

h2("3.4 Summary")
body(
    "The implementation separates data preparation, training, evaluation, and serving into four "
    "independent scripts connected only by file-based artefacts, the processed dataset directories, "
    "the TorchScript checkpoint, and the class name mapping. This separation made it possible to "
    "run, and separately report, both a fast architecture smoke test and a full, honest evaluation "
    "against the entire held-out IP102 test split without changing the application code."
)

# ---------------- CHAPTER 4 ----------------
add_page_break_paragraph()
chapter_title(4, "PERFORMANCE ANALYSIS AND RESULTS")
body(
    "This chapter separates three kinds of statement: what was measured directly against the live "
    "application in this environment, what the repository's own saved evaluation files record, and "
    "what has not been measured at all. Every figure and table in this chapter is traceable to a "
    "specific file in the repository or a specific browser-tested action, and that source is named "
    "alongside the claim."
)

h2("4.1 Functional Performance")
body([
    ("Health and interaction flow. ", True),
    ("The application was exercised directly in a browser against a locally running instance. The "
     "Streamlit health endpoint returned HTTP 200, confirming the service starts and stays "
     "responsive. The full interaction flow, uploading an image, running inference, rendering the "
     "confidence score and action ladder, updating the session history, and exporting that history "
     "as JSON, was exercised end to end and functioned as designed.", False),
])
table_caption(4, 1, "Automated and functional verification performed in this project")
VERIF_ROWS = [
    ["Check", "Result", "Source"],
    ["Streamlit health endpoint", "HTTP 200", "Browser verification, this session"],
    ["Upload, inference, action ladder, history, export flow", "Completed end to end", "Browser verification, this session"],
    ["tests/test_pipeline.py (2 tests)", "2 passed", "pytest run, this session"],
    ["EfficientNet checkpoint load", "Loads successfully", "Sidebar Model status, browser verification"],
]
data_table(VERIF_ROWS, [2.8, 1.8, 2.0])

h2("4.2 Accuracy and Reliability")
body([
    ("Two different evaluation runs. ", True),
    ("Accuracy must be reported for the specific checkpoint being evaluated, and this project "
     "produced two materially different evaluation runs against the same evaluate.py script. The "
     "first is an architecture smoke test, trained for one epoch without pretrained weights on a "
     "deliberately tiny subset of two images per class, used only to confirm that the training "
     "loop, the TorchScript export, and the evaluation harness function correctly; it reported a "
     "validation accuracy of 0.867 and a smoke-set accuracy and macro F1 of 1.000 on 256 held-out "
     "images. The second is a full evaluation of the checkpoint currently stored at "
     "models/efficientnet_ip102.pt against the complete IP102 test split of 22,619 images, which is "
     "the number that matters for any real judgement of accuracy.", False),
])
table_caption(4, 2, "Evaluation results recorded in reports/*.json")
EVAL_ROWS = [
    ["Run", "Samples", "Accuracy", "Macro F1", "Source file"],
    ["Architecture smoke test", "256", "1.000", "1.000", "reports/smoke-evaluation.json"],
    ["Full held-out test split", "22,619", "0.0148", "0.00029", "reports/full-evaluation.json"],
    ["Random-guess baseline", "n/a", "0.0098 (1/102)", "n/a", "Computed, not a file"],
]
data_table(EVAL_ROWS, [2.2, 1.0, 1.2, 1.1, 2.1])
figure(f"{ASSETS}/fig3_accuracy_comparison.png", 4, 1, "Accuracy under the architecture smoke test, the full held-out test evaluation, and a random-guess baseline.")
body([
    ("Why the full-split accuracy is near random. ", True),
    ("The full evaluation returned an accuracy of 1.48 percent and a macro F1 score of 0.00029, "
     "close to the 0.98 percent expected from pure random guessing across 102 classes. Reading the "
     "per-class classification report in reports/full-evaluation.json explains why: the stored "
     "checkpoint predicted class 000_rice_leaf_roller for every one of the 22,619 test images, "
     "giving that single class a recall of 1.0 and every one of the other 101 classes a recall of "
     "0.0. This is visible directly in the confusion matrix for the fifteen highest-support classes "
     "in Figure 4.2, where the entire predicted-class axis collapses onto one column.", False),
])
figure(f"{ASSETS}/fig4_confusion_matrix.png", 4, 2, "Row-normalised confusion matrix for the fifteen highest-support IP102 classes, full test split. Every row is predicted as the single left-most column.")
body([
    ("What this does and does not show. ", True),
    ("This outcome is consistent with the checkpoint's training history: it was produced by the "
     "smoke-test configuration, no pretrained weights and a two-image-per-class limit, which is "
     "sufficient to prove that the pipeline runs but is not sufficient data or optimisation to "
     "learn 102 visually similar insect classes, and the model instead converged to the trivial "
     "solution of a single constant prediction. The architecture, the weighted sampler, the "
     "TorchScript export, and the evaluation harness are all demonstrated to work correctly; what "
     "has not yet been demonstrated is a model trained with pretrained weights on the full training "
     "split, which the README's deployment checklist already identifies as an outstanding step. "
     "This report states that limitation plainly rather than presenting the smoke-test figures as "
     "representative of real-world accuracy.", False),
])

h2("4.3 User Interaction and Experience")
body(
    "The dashboard surfaces the active inference source at all times, EfficientNet checkpoint or "
    "demo-visual heuristic, together with the raw predicted label and the matched crop. When "
    "confidence falls below 75 percent, the interface switches its risk-mode indicator to Review "
    "and displays an explicit warning asking the user to compare alternatives and verify the insect "
    "before any treatment, which is exactly the behaviour observed when the EfficientNet checkpoint "
    "was tested against a real IP102 image during browser verification, a 1 percent confidence "
    "result that correctly triggered the Review state and the low-confidence warning rather than a "
    "misleadingly confident recommendation. A usability study with real growers has not been "
    "carried out and is not claimed here."
)

h2("4.4 System Limitations Observed")
bullet([("Single-class collapse. ", True), ("The shipped checkpoint predicts one constant class and is not fit for a real identification task; see Section 4.2.", False)])
bullet([("No bundled images. ", True), ("The repository does not include the IP102 images themselves, so training and evaluation require a separate, licensed download of the archive.", False)])
bullet([("CPU-only training. ", True), ("Training and evaluation were run on CPU in this environment; a full, pretrained training run across 45,095 images would benefit substantially from GPU acceleration.", False)])
bullet([("Demo mode is a heuristic, not a model. ", True), ("It is based on simple colour and edge statistics and is clearly labelled as such in the interface.", False)])
bullet([("Narrow knowledge base coverage. ", True), ("The recommendation file currently covers a small number of named pest keys plus a generic caterpillar-family and unknown fallback; broader IP102 coverage requires expanding this file with reviewed, locally sourced guidance.", False)])

h2("4.5 System Scalability and Future Enhancements")
bullet("Train a pretrained-weight EfficientNet-B0, or a comparable architecture, on the full 45,095-image training split and re-run the identical evaluate.py harness against the untouched test split to obtain a trustworthy accuracy figure.")
bullet("Expand data/recommendations.json to cover a larger share of the 102 IP102 classes with reviewed, locally sourced guidance.")
bullet("Add image-size enforcement at the reverse proxy, as already noted in the project's deployment checklist, before any public deployment.")
bullet("Introduce top-k prediction display, so a user sees the three or five most likely pests rather than a single label, which is a natural extension of the confidence data the model already produces.")

h2("4.6 Overall Outcome")
body(
    "CropSentinel delivers a complete, working, and tested pipeline: a reproducible data "
    "preparation step, a class-imbalance-aware training script, a rigorous evaluation harness, and "
    "a safety-conscious interface that is already verified end to end in a browser. The project also "
    "produced a clear, numerically specific finding that the currently stored checkpoint has not "
    "learned the task and performs near the random baseline across the full test split. Reporting "
    "that result in full, rather than only the favourable smoke-test figures, is treated in this "
    "project as part of the deliverable, not as a shortcoming to be hidden."
)

# ---------------- CHAPTER 5 ----------------
add_page_break_paragraph()
chapter_title(5, "SAMPLE CODE AND SCREENSHOTS")
body(
    "This chapter lists short extracts of the source code that carry the core ideas, followed by "
    "screenshots of the working application. The screenshots were taken from a locally running "
    "instance of the repository during this session; the code extracts are reproduced from the "
    "repository's app.py and train.py."
)

h2("5.1 Representative Code")
listing_caption(5, 1, "Prediction dispatch and class lookup (app.py)")
code_block([
    "def predict(image: Image.Image) -> tuple[str, float, str]:",
    "    model = load_model()",
    "    if model is None:",
    "        return demo_predict(image)",
    "    import torch",
    "    from torchvision import transforms",
    "    tensor = transforms.Compose([",
    "        transforms.Resize((224, 224)), transforms.ToTensor()",
    "    ])(image.convert(\"RGB\")).unsqueeze(0)",
    "    with torch.inference_mode():",
    "        probabilities = torch.softmax(model(tensor), dim=1)[0]",
    "        confidence, index = probabilities.max(dim=0)",
    "    class_names = json.loads(",
    "        (ROOT / \"models\" / \"class_names.json\").read_text(encoding=\"utf-8\")",
    "    )",
    "    return class_names[str(int(index))], float(confidence), \"EfficientNet checkpoint\"",
])

listing_caption(5, 2, "Confidence-gated recommendation fallback (app.py)")
code_block([
    "def get_pest_profile(model_key: str, confidence: float) -> dict[str, Any]:",
    "    profile = recommendations.get(model_key)",
    "    if profile:",
    "        return profile",
    "    label = model_key.lower()",
    "    caterpillar_terms = (\"caterpillar\", \"armyworm\", \"cutworm\", \"borer\",",
    "                         \"leaf_roller\", \"leaf roller\", \"worm\")",
    "    if confidence >= 0.20 and any(term in label for term in caterpillar_terms):",
    "        return recommendations.get(\"caterpillar\") or recommendations[\"unknown\"]",
    "    return recommendations[\"unknown\"]",
])

listing_caption(5, 3, "Class-balanced training sampler (train.py)")
code_block([
    "class_counts = {label: 0 for label in range(len(train_data.classes))}",
    "for index in source_indices:",
    "    class_counts[train_data.targets[index]] += 1",
    "sample_weights = [",
    "    1.0 / max(class_counts[train_data.targets[index]], 1)",
    "    for index in source_indices",
    "]",
    "sampler = WeightedRandomSampler(",
    "    sample_weights, num_samples=len(sample_weights), replacement=True",
    ")",
    "train_loader = DataLoader(",
    "    train_source, batch_size=args.batch_size, sampler=sampler, num_workers=0",
    ")",
])

h2("5.2 Screenshots")
body(
    "Figure 5.1 shows the CropSentinel landing view running against a live local instance, with the "
    "EfficientNet checkpoint successfully loaded, as indicated by the green Model status panel in "
    "the sidebar."
)
figure(f"{ASSETS}/01_landing.jpg", 5, 1, "CropSentinel landing view, sidebar mission control, and image upload panel.")

body(
    "Figure 5.2 shows the result of uploading an unseen image from the IP102 test split, class "
    "000_rice_leaf_roller, and running Analyze image. The checkpoint returned the raw label "
    "000_rice_leaf_roller with a confidence of 1 percent, which the interface correctly classified "
    "as an uncertain field observation and placed in the Review risk mode."
)
figure(f"{ASSETS}/02_prediction.jpg", 5, 2, "Low-confidence prediction panel, correctly flagged as Review by the interface.")

body(
    "Figure 5.3 shows the resulting action ladder for the unmatched, low-confidence label. Because "
    "the predicted key did not match a named entry in the knowledge base and confidence was below "
    "the caterpillar-fallback threshold, the interface correctly returned the generic, safety-first "
    "unknown profile rather than guessing at a specific pest's guidance."
)
figure(f"{ASSETS}/03_action_ladder.jpg", 5, 3, "Three-tier action ladder and safety boundary notice shown for a low-confidence prediction.")

# ---------------- CHAPTER 6 ----------------
add_page_break_paragraph()
chapter_title(6, "CONCLUSION")
body(
    "CropSentinel demonstrates a complete, reproducible pipeline for pest image classification on "
    "the IP102 benchmark, from raw archive preparation through training, evaluation, and a "
    "safety-conscious deployed interface. The application layer is verified and functioning: the "
    "health endpoint responds, the upload-to-recommendation flow works end to end in a browser, and "
    "the automated test suite passes. The project's most important technical finding is that the "
    "checkpoint currently stored in the repository, produced by an architecture smoke test rather "
    "than a full training run, has collapsed to a single constant prediction and achieves only 1.48 "
    "percent accuracy across the full 22,619-image held-out test split, close to the random-guess "
    "baseline. Rather than treating this as a failure to conceal, the report documents it as the "
    "clear next milestone: a full, pretrained training run across all 45,095 training images, "
    "followed by re-evaluation with the same unmodified evaluate.py harness, is the specific, "
    "measurable step that separates the current prototype from a deployable identification tool. "
    "The surrounding engineering, the data pipeline, the class-imbalance handling, the evaluation "
    "methodology, and the interface's transparent, confidence-gated behaviour, is already sound and "
    "provides a dependable foundation for that next step."
)

# ---------------- REFERENCES ----------------
add_page_break_paragraph()
front_title("REFERENCES")
refs = [
    "Wu, X., Zhan, C., Lai, Y. K., Cheng, M. M., and Yang, J., \"IP102: A Large-Scale Benchmark "
    "Dataset for Insect Pest Recognition,\" in Proc. IEEE/CVF Conference on Computer Vision and "
    "Pattern Recognition (CVPR), 2019.",
    "Tan, M. and Le, Q. V., \"EfficientNet: Rethinking Model Scaling for Convolutional Neural "
    "Networks,\" in Proc. 36th International Conference on Machine Learning (ICML), 2019.",
    "Paszke, A. et al., \"PyTorch: An Imperative Style, High-Performance Deep Learning Library,\" "
    "Advances in Neural Information Processing Systems (NeurIPS), 2019.",
    "Pedregosa, F. et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine "
    "Learning Research, vol. 12, pages 2825 to 2830, 2011.",
    "Streamlit Inc., \"Streamlit documentation,\" https://docs.streamlit.io.",
    "PyTorch, \"TorchVision documentation, models and transforms reference,\" https://pytorch.org/vision/stable/.",
    "Docker Inc., \"Dockerfile reference,\" https://docs.docker.com/engine/reference/builder/.",
    "CropSentinel source repository (this project), local Git history, commit ec29982 and later.",
]
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p.add_run(f"[{i}]\u0009")
    r1.font.name = "Times New Roman"; r1.font.size = Pt(12); r1.font.color.rgb = INK
    r2 = p.add_run(r)
    r2.font.name = "Times New Roman"; r2.font.size = Pt(12); r2.font.color.rgb = INK

doc.save(OUT)
print("saved:", OUT)
print("\nFIGURES:", figure_log)
print("\nTABLES:", table_log)
print("\nLISTINGS:", listing_log)
