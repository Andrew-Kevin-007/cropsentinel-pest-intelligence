import fitz
import json

pdf = fitz.open(r"D:\ITA\report\CropSentinel_Mini_Project_Report.pdf")

page_label = []
page_text = []
for page in pdf:
    h = page.rect.height; w = page.rect.width
    bottom = page.get_text("text", clip=fitz.Rect(0, h - 60, w, h)).strip().splitlines()
    page_label.append(bottom[-1].strip() if bottom else "?")
    page_text.append(page.get_text("text"))

def find_label(snippet, start_physical=9):
    for i in range(start_physical, len(page_text)):
        if snippet in page_text[i]:
            return page_label[i]
    return None

# TOC rows: (chapter_no_cell_text, title_cell_text, search_snippet)
toc_targets = [
    ("ABSTRACT", "iii"),
    ("LIST OF FIGURES", "vii"),
    ("LIST OF ABBREVIATIONS", "viii"),
    ("1 INTRODUCTION", "1. INTRODUCTION heading"),
]

sections = [
    ("1", "INTRODUCTION", "INTRODUCTION"),
    ("1.1", "Background", "1.1 Background"),
    ("1.2", "Problem statement", "1.2 Problem statement"),
    ("1.3", "Motivation and Significance", "1.3 Motivation and Significance"),
    ("1.4", "Project Overview", "1.4 Project Overview"),
    ("1.5", "System Functionality", "1.5 System Functionality"),
    ("1.6", "Objectives", "1.6 Objectives"),
    ("1.7", "Design Philosophy and Approach", "1.7 Design Philosophy and Approach"),
    ("1.8", "Broader Impact", "1.8 Broader Impact"),
    ("1.9", "Educational Value", "1.9 Educational Value"),
    ("1.10", "Conclusion", "1.10 Conclusion"),
    ("2", "TOOLS AND TECHNOLOGIES USED", "TOOLS AND TECHNOLOGIES USED"),
    ("2.1", "Python Programming Language", "2.1 Python Programming Language"),
    ("2.2", "PyTorch, TorchVision, and EfficientNet", "2.2 PyTorch, TorchVision, and EfficientNet"),
    ("2.3", "Streamlit and the Application Interface", "2.3 Streamlit and the Application Interface"),
    ("2.4", "Summary", "2.4 Summary"),
    ("3", "SYSTEM IMPLEMENTATION", "SYSTEM IMPLEMENTATION"),
    ("3.1", "Dataset", "3.1 Dataset"),
    ("3.2", "System Architecture", "3.2 System Architecture"),
    ("3.3", "Modules Description", "3.3 Modules Description"),
    ("3.4", "Summary", "3.4 Summary"),
    ("4", "PERFORMANCE ANALYSIS AND RESULTS", "PERFORMANCE ANALYSIS AND RESULTS"),
    ("4.1", "Functional Performance", "4.1 Functional Performance"),
    ("4.2", "Accuracy and Reliability", "4.2 Accuracy and Reliability"),
    ("4.3", "User Interaction and Experience", "4.3 User Interaction and Experience"),
    ("4.4", "System Limitations Observed", "4.4 System Limitations Observed"),
    ("4.5", "System Scalability and Future Enhancements", "4.5 System Scalability and Future Enhancements"),
    ("4.6", "Overall Outcome", "4.6 Overall Outcome"),
    ("5", "SAMPLE CODE AND SCREENSHOTS", "SAMPLE CODE AND SCREENSHOTS"),
    ("6", "CONCLUSION", "CONCLUSION"),
    ("", "REFERENCES", "REFERENCES"),
]

results = {}
for num, title, snippet in sections:
    label = find_label(snippet)
    results[f"{num}|{title}"] = label
    print(f"{num:6} {title:45} -> {label}")

print("\n--- figures ---")
figures = [
    ("3.1", "IP102 classification split sizes produced by prepare_ip102.py."),
    ("3.2", "End-to-end CropSentinel data flow"),
    ("4.1", "Accuracy under the architecture smoke test"),
    ("4.2", "Row-normalised confusion matrix for the fifteen"),
    ("5.1", "CropSentinel landing view, sidebar mission control"),
    ("5.2", "Low-confidence prediction panel, correctly flagged"),
    ("5.3", "Three-tier action ladder and safety boundary notice"),
]
fig_results = {}
for num, snippet in figures:
    label = find_label(snippet)
    fig_results[num] = label
    print(f"Figure {num} -> {label}")

with open(r"D:\ITA\scratch_pages_out.json", "w", encoding="utf-8") as f:
    json.dump({"sections": results, "figures": fig_results}, f, indent=2)
print("\nwritten scratch_pages_out.json")
