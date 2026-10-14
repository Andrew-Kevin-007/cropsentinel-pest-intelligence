# CropSentinel: Field Intelligence

CropSentinel is a deployable pest-intelligence dashboard for image-based insect identification and responsible control guidance. It supports transparent demo mode and a TorchScript EfficientNet checkpoint trained from IP102.

## Product surfaces

- **Identify:** upload a field image, view the top matches, confidence, and recommended action ladder.
- **Action ladder:** review preventive, organic/biological, and chemical-control guidance.
- **History export:** review observations in the current session and export them as JSON.
- **Model status:** see whether the EfficientNet checkpoint can actually load.

## Run the demo

```powershell
cd d:\ITA
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

The app runs immediately  in **demo mode** when no checkpoint is available. Demo predictions use a transparent image heuristic and are labelled in the interface. To run with the local ML environment and checkpoint, use `\.venv\Scripts\python.exe -m streamlit run app.py`.

## Production container

```powershell
docker build -t cropsentinel .
docker run --rm -p 8501:8501 cropsentinel
```

Open `http://localhost:8501` after the container starts.

## Connect a trained EfficientNet model

Place these files in `models/`:

- `efficientnet_ip102.pt`: TorchScript model returning classification logits.
- `class_names.json`: JSON object mapping class indexes to IP102 class names.

Example:

```json
{"0": "000_rice_leaf_roller", "1": "001_rice_leaf_caterpillar"}
```

The training notebook or script should  use the same resize and normalization pipeline as inference.

Prepare the official IP102 classification archive first:

```powershell
py -m pip install -r requirements-ml.txt
py prepare_ip102.py --archive data\raw\ip102\Classification\ip102_v1.1.tar --classes data\raw\ip102\Classification\classes.txt --output-dir data\processed\ip102
py train.py --data-dir data\processed\ip102 --epochs 12 --output-dir models
py evaluate.py --data-dir data\processed\ip102 --model models\efficientnet_ip102.pt
```

The preparation script extracts the official archive, maps its split files into ImageFolder directories, and preserves the 102-class label mapping. The verified local preparation contains 45,095 training images, 7,508 validation images, and 22,619 test images. Training saves the best TorchScript checkpoint and `class_names.json`; evaluation writes `reports/evaluation.json` with accuracy, macro F1, per-class metrics, and a confusion matrix.

For a fast architecture smoke test without downloading pretrained weights:

```powershell
\.venv\Scripts\python.exe train.py --data-dir data\processed\ip102 --epochs 1 --batch-size 16 --limit-per-class 2 --limit-val 128 --no-pretrained --output-dir models
\.venv\Scripts\python.exe evaluate.py --data-dir data\processed\ip102 --model models\efficientnet_ip102.pt --limit 256 --output reports\smoke-evaluation.json
```

The verified smoke run produced validation accuracy `0.867` and held-out smoke accuracy/macro F1 of `1.000` on 256 samples. These are pipeline checks only, not production performance claims.

## Project structure

```text
app.py
train.py
prepare_ip102.py
evaluate.py
data/recommendations.json
models/                 # optional trained checkpoint
requirements.txt
requirements-ml.txt
Dockerfile
.streamlit/config.toml
README.md
```

## Verification status

- Streamlit health endpoint: `HTTP 200`.
- Browser flow: upload image, run inference, render confidence, show action ladder, update history, and expose JSON export.
- Real checkpoint flow: EfficientNet checkpoint loaded and an IP102 test image returned a low-confidence result with the correct safety fallback.
- Focused automated tests: `2 passed`.

## Deployment checklist

1. Verify the IP102 license and record the dataset version used. IP102 is free for academic use; contact the authors for other purposes.
2. Run full-data pretrained training on a GPU and evaluate on the untouched test split.
3. Copy the checkpoint and matching `class_names.json` into `models/`.
4. Review every recommendation against local agricultural guidance.
5. Limit uploaded image size at the reverse proxy.
6. Keep logs free of personal data.

## Important limitation

The recommendation panel is educational guidance, not a pesticide prescription. Chemical products, doses, application intervals, and local approval must come from an authoritative local source and the product label. The repository contains a smoke checkpoint locally, but model binaries are excluded from Git; production deployment must supply a reviewed full-data checkpoint.
