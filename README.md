# CropSentinel: Field Intelligence

CropSentinel is a deployable pest-intelligence dashboard for image-based insect identification and responsible control guidance. It supports a transparent demo mode immediately and an EfficientNet checkpoint when IP102 training is complete.

## Product surfaces

- **Identify:** upload a field image, view the top matches, confidence, and recommended action ladder.
- **Pest library:** search verified pest profiles and field clues.
- **History:** review observations in the current session and export them as JSON.
- **Model readiness:** see whether the production checkpoint and class mapping are installed.

## Run the demo

```powershell
cd d:\ITA
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

The app runs immediately in **demo mode**. Demo predictions use a transparent image heuristic and are labelled in the interface. This makes the dashboard usable for a presentation before the IP102 model has finished training.

## Production container

```powershell
docker build -t cropsentinel .
docker run --rm -p 8501:8501 cropsentinel
```

Open `http://localhost:8501` after the container starts.

## Connect a trained EfficientNet model

Place these files in `models/`:

- `efficientnet_ip102.pt`: TorchScript model returning classification logits.
- `class_names.json`: JSON object mapping class indexes to recommendation keys.

Example:

```json
{"0": "aphids", "1": "fall armyworm", "2": "beet armyworm"}
```

The training notebook or script should use the same resize and normalization pipeline as inference.

To train from an ImageFolder-compatible IP102 export:

```powershell
py -m pip install -r requirements-ml.txt
py train.py --data-dir path\to\IP102 --epochs 12 --output-dir models
```

The dataset folder must contain `train/` and `val/` directories. The script saves the best TorchScript checkpoint and `class_names.json` under `models/`.

## Project structure

```text
app.py
train.py
data/recommendations.json
models/                 # optional trained checkpoint
requirements.txt
requirements-ml.txt
Dockerfile
.streamlit/config.toml
README.md
```

## Deployment checklist

1. Verify the IP102 license and record the dataset version used.
2. Train and evaluate the model on a held-out test set.
3. Copy the checkpoint and `class_names.json` into `models/`.
4. Review every recommendation against local agricultural guidance.
5. Limit uploaded image size at the reverse proxy.
6. Keep logs free of personal data.

## Important limitation

The recommendation panel is educational guidance, not a pesticide prescription. Chemical products, doses, application intervals, and local approval must come from an authoritative local source and the product label.