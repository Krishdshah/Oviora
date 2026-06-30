
"""
v2_03_model.py

Hybrid Static + Temporal Model
"""

import torch
import torch.nn as nn

from config import (
    STATIC_HIDDEN,
    LSTM_HIDDEN,
    LSTM_LAYERS,
    TRANSFORMER_LAYERS,
    NUM_HEADS,
    DROPOUT,
)


class ResidualMLP(nn.Module):
    def __init__(self, in_features, hidden=STATIC_HIDDEN):
        super().__init__()

        self.fc1 = nn.Linear(in_features, hidden)
        self.bn1 = nn.LayerNorm(hidden)

        self.fc2 = nn.Linear(hidden, hidden)
        self.bn2 = nn.LayerNorm(hidden)

        self.shortcut = (
            nn.Linear(in_features, hidden)
            if in_features != hidden
            else nn.Identity()
        )

        self.drop = nn.Dropout(DROPOUT)

    def forward(self, x):
        identity = self.shortcut(x)

        out = self.fc1(x)
        out = self.bn1(out)
        out = torch.relu(out)

        out = self.drop(out)

        out = self.fc2(out)
        out = self.bn2(out)

        out = out + identity
        out = torch.relu(out)

        return out


class TemporalEncoder(nn.Module):
    def __init__(self, input_dim):

        super().__init__()

        self.embedding = nn.Linear(
            input_dim,
            LSTM_HIDDEN
        )

        self.lstm = nn.LSTM(
            LSTM_HIDDEN,
            LSTM_HIDDEN,
            num_layers=LSTM_LAYERS,
            batch_first=True,
            bidirectional=True,
            dropout=DROPOUT
        )

        encoder = nn.TransformerEncoderLayer(
            d_model=LSTM_HIDDEN * 2,
            nhead=NUM_HEADS,
            dim_feedforward=512,
            dropout=DROPOUT,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder,
            num_layers=TRANSFORMER_LAYERS
        )

        self.attention = nn.Sequential(
            nn.Linear(LSTM_HIDDEN * 2, 64),
            nn.Tanh(),
            nn.Linear(64, 1)
        )

    def forward(self, x):

        x = self.embedding(x)

        x, _ = self.lstm(x)

        x = self.transformer(x)

        weights = torch.softmax(
            self.attention(x),
            dim=1
        )

        pooled = torch.sum(
            weights * x,
            dim=1
        )

        return pooled


class HybridCycleModel(nn.Module):

    def __init__(
        self,
        dynamic_features,
        static_features
    ):

        super().__init__()

        self.temporal = TemporalEncoder(
            dynamic_features
        )

        self.static = ResidualMLP(
            static_features
        )

        fusion_dim = (LSTM_HIDDEN * 2) + STATIC_HIDDEN

        self.fusion = nn.Sequential(

            nn.Linear(fusion_dim, 256),

            nn.LayerNorm(256),

            nn.ReLU(),

            nn.Dropout(DROPOUT),

            nn.Linear(256, 128),

            nn.ReLU(),

            nn.Dropout(DROPOUT)

        )

        self.regressor = nn.Linear(
            128,
            1
        )

    def forward(
        self,
        dynamic,
        static
    ):

        temporal = self.temporal(dynamic)

        static = self.static(static)

        fused = torch.cat(
            [
                temporal,
                static
            ],
            dim=1
        )

        fused = self.fusion(fused)

        pred = self.regressor(fused)

        return pred.squeeze(1)


if __name__ == "__main__":

    model = HybridCycleModel(
        dynamic_features=28,
        static_features=3
    )

    x_dyn = torch.randn(
        8,
        6,
        28
    )

    x_sta = torch.randn(
        8,
        3
    )

    out = model(
        x_dyn,
        x_sta
    )

    print(model)

    print(out.shape)
