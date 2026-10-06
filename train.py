"""Train an EfficientNet classifier on an ImageFolder-compatible IP102 export."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CropSentinel EfficientNet classifier")
    parser.add_argument("--data-dir", type=Path, required=True, help="Folder containing train/ and val/ ImageFolder directories")
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--output-dir", type=Path, default=Path("models"))
    args = parser.parse_args()

    try:
        import torch
        from torch import nn
        from torch.utils.data import DataLoader
        from torchvision import datasets, models, transforms
    except ImportError as error:
        raise SystemExit("Install the ML extras first: python -m pip install -r requirements-ml.txt") from error

    train_dir = args.data_dir / "train"
    val_dir = args.data_dir / "val"
    if not train_dir.exists() or not val_dir.exists():
        raise SystemExit("Expected ImageFolder directories: <data-dir>/train and <data-dir>/val")

    normalize = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    train_data = datasets.ImageFolder(train_dir, transforms.Compose([transforms.Resize((224, 224)), transforms.RandomHorizontalFlip(), transforms.RandomRotation(10), transforms.ToTensor(), normalize]))
    val_data = datasets.ImageFolder(val_dir, transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), normalize]))
    train_loader = DataLoader(train_data, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_data, batch_size=args.batch_size, shuffle=False, num_workers=0)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weights = models.EfficientNet_B0_Weights.DEFAULT
    model = models.efficientnet_b0(weights=weights)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(train_data.classes))
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
    best_accuracy = 0.0

    for epoch in range(args.epochs):
        model.train()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
        model.eval()
        correct = total = 0
        with torch.inference_mode():
            for images, labels in val_loader:
                outputs = model(images.to(device))
                correct += (outputs.argmax(1).cpu() == labels).sum().item()
                total += labels.numel()
        accuracy = correct / max(total, 1)
        print(f"epoch {epoch + 1}/{args.epochs} · validation accuracy {accuracy:.3f}")
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            args.output_dir.mkdir(parents=True, exist_ok=True)
            scripted = torch.jit.script(model.cpu())
            scripted.save(str(args.output_dir / "efficientnet_ip102.pt"))
            (args.output_dir / "class_names.json").write_text(json.dumps({str(index): name for index, name in enumerate(train_data.classes)}, indent=2), encoding="utf-8")
            model.to(device)

    print(f"saved best checkpoint with validation accuracy {best_accuracy:.3f}")


if __name__ == "__main__":
    main()