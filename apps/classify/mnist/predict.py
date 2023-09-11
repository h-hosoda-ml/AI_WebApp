import torch

import numpy as np

from .model import Net, model_path

from dataclasses import dataclass


@dataclass(frozen=True)
class MnistModelConfig:
    """変数を格納して一元管理するクラス"""

    # deviceを指定(M1 or M2 Mac環境を想定)
    device = torch.device("mps")

    # パラメータが保存されているファイルのパス
    param_path = model_path / "CNN_Model_41.pth"


def predict(x: np.ndarray):
    """
    手書き数字の予測結果を返す関数
    """
    # configのインスタンス化
    config = MnistModelConfig()
    # モデルのインスタンス化
    model = Net().to(config.device)

    # 学習したパラメータを読み出す
    model.load_state_dict(torch.load(config.param_path))

    # 評価モードへ
    model.eval()

    # テンソルへ変換
    x = x[np.newaxis, :, :]
    x = torch.tensor(x).float().to(config.device)

    # 0-1にスケーリング
    tensor_max = torch.max(x)
    tensor_min = torch.min(x)
    tensor_range = tensor_max - tensor_min

    # 標準偏差0.5, 平均0.5にする
    x = (x - tensor_min) / tensor_range
    x = (x - 0.5) / 0.5

    # テンソルの階層を3 -> 4
    x = torch.unsqueeze(x, dim=0)

    # 予測
    output: torch.Tensor = model(x)
    prediction = output.argmax(dim=1).item()  # 予測結果

    return str(prediction)
