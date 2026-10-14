import fitz
import re

doc = fitz.open(r"D:\ITA\report\CropSentinel_Mini_Project_Report.pdf")
print("total physical pages:", len(doc))

# Determine printed page label per physical page by reading bottom-of-page text
page_labels = []
for i, page in enumerate(doc):
    h = page.rect.height
    w = page.rect.width
    bottom = page.get_text("text", clip=fitz.Rect(0, h - 60, w, h))
    label = bottom.strip().splitlines()
    label = label[-1].strip() if label else "?"
    page_labels.append(label)
    print(i, repr(label))
