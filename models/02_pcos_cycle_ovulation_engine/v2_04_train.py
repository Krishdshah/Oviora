
"""
v2_04_train.py

Training script for HybridCycleModel.
"""

from pathlib import Path
import json
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from torch.cuda.amp import GradScaler, autocast
import warnings
warnings.filterwarnings("ignore")

from config import *
from utils import set_seed, regression_metrics, save_checkpoint
from v2_02_dataset import get_dataloaders
from v2_03_model import HybridCycleModel

def train():
    set_seed(SEED)

    meta = json.loads((PROCESSED_DIR / "metadata.json").read_text())
    NUM_DYNAMIC = len(meta["dynamic_features"])
    NUM_STATIC = len(meta["static_features"])

    criterion = nn.SmoothL1Loss(beta=1.0)

    all_metrics = []

    for fold in range(1, 6):

        print(f"\n{'='*60}")
        print(f"Fold {fold}")
        print(f"{'='*60}")

        train_loader, valid_loader = get_dataloaders(
            fold=fold,
            batch_size=BATCH_SIZE
        )

        model = HybridCycleModel(
            dynamic_features=NUM_DYNAMIC,
            static_features=NUM_STATIC
        ).to(DEVICE)

        optimizer = AdamW(
            model.parameters(),
            lr=LEARNING_RATE,
            weight_decay=WEIGHT_DECAY
        )

        scheduler = CosineAnnealingWarmRestarts(
            optimizer,
            T_0=10,
            T_mult=2
        )

        scaler = GradScaler(enabled=USE_AMP)

        best_loss = float("inf")
        patience = 0

        best_path = MODEL_DIR / f"fold_{fold}_best.pt"

        for epoch in range(EPOCHS):

            model.train()
            train_loss = 0

            for batch in train_loader:

                dyn = batch["dynamic"].to(DEVICE)
                sta = batch["static"].to(DEVICE)
                y = batch["target"].to(DEVICE)

                optimizer.zero_grad()

                with autocast(enabled=USE_AMP):

                    pred = model(dyn, sta)

                    loss = criterion(pred, y)

                scaler.scale(loss).backward()

                scaler.unscale_(optimizer)

                torch.nn.utils.clip_grad_norm_(
                    model.parameters(),
                    1.0
                )

                scaler.step(optimizer)
                scaler.update()

                train_loss += loss.item()

            scheduler.step(epoch)

            train_loss /= len(train_loader)

            model.eval()

            valid_loss = 0

            preds = []
            truth = []

            with torch.no_grad():

                for batch in valid_loader:

                    dyn = batch["dynamic"].to(DEVICE)
                    sta = batch["static"].to(DEVICE)
                    y = batch["target"].to(DEVICE)

                    pred = model(dyn, sta)

                    valid_loss += criterion(pred, y).item()

                    preds.extend(pred.cpu().numpy())
                    truth.extend(y.cpu().numpy())

            valid_loss /= len(valid_loader)

            metrics = regression_metrics(
                np.array(truth),
                np.array(preds)
            )

            print(
                f"Epoch {epoch+1:03d} "
                f"Train={train_loss:.4f} "
                f"Val={valid_loss:.4f} "
                f"MAE={metrics['MAE']:.3f} "
                f"R2={metrics['R2']:.3f}"
            )

            if valid_loss < best_loss:

                best_loss = valid_loss
                patience = 0

                save_checkpoint(
                    model,
                    optimizer,
                    epoch,
                    best_path
                )

            else:

                patience += 1

            if patience >= EARLY_STOPPING:

                print("Early stopping.")
                break

        print("\nBest Fold Metrics")
        print(metrics)

        all_metrics.append(metrics)

    print("\n" + "="*60)
    print("Cross Validation Results")
    print("="*60)

    for key in ["MAE", "RMSE", "R2"]:
        vals = [m[key] for m in all_metrics]
        print(
            f"{key}: "
            f"{np.mean(vals):.4f} ± {np.std(vals):.4f}"
        )

if __name__ == "__main__":
    train()
