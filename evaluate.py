"""Evaluate a TorchScript CropSentinel checkpoint on an ImageFolder test split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate CropSentinel checkpoint")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--model", type=Path, default=Path("models/efficientnet_ip102.pt"))
    parser.add_argument("--output", type=Path, default=Path("reports/evaluation.json"))
    args = parser.parse_args()
    try:
        import torch
        from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
        from torch.utils.data import DataLoader
        from torchvision import datasets, transforms
    except ImportError as error:
        raise SystemExit("Install ML extras: python -m pip install -r requirements-ml.txt") from error
    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    dataset = datasets.ImageFolder(args.data_dir / "test", transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), normalize]))
    loader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=0)
    model = torch.jit.load(str(args.model), map_location="cpu").eval()
    actual, predicted = [], []
    with torch.inference_mode():
        for images, labels in loader:
            predicted.extend(model(images).argmax(1).tolist())
            actual.extend(labels.tolist())
    report = {"samples": len(actual), "classes": dataset.classes, "accuracy": accuracy_score(actual, predicted), "macro_f1": f1_score(actual, predicted, average="macro", zero_division=0), "classification_report": classification_report(actual, predicted, target_names=dataset.classes, output_dict=True, zero_division=0), "confusion_matrix": confusion_matrix(actual, predicted).tolist()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"accuracy={report['accuracy']:.4f} macro_f1={report['macro_f1']:.4f} samples={report['samples']}")


if __name__ == "__main__":
    main()