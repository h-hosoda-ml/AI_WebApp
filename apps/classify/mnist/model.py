import torch
from torch import nn
from torch.optim import RMSprop
from torchvision import datasets

from torchvision import transforms
from torch.utils.data.dataloader import DataLoader
from torch.utils.data.dataset import Subset

from pathlib import Path

dataset_path = Path(__file__).parent / "dataset"
model_path = Path(__file__).parent / "params"


# モデルの作成
class Net(nn.Module):
    def __init__(self):
        super().__init__()

        # 畳み込み層
        self.conv1 = nn.Conv2d(1, 32, 3)  # 入力チャネル, 出力チャネル, カーネルサイズ
        self.conv2 = nn.Conv2d(32, 64, 3)

        # 全結合層
        self.l1 = nn.Linear(5 * 5 * 64, 128)  # 入力次元, 出力次元
        self.l2 = nn.Linear(128, 10)

        # バッチ正規化
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)

        # 活性化関数
        self.relu = nn.ReLU(inplace=True)

        # 平坦化
        self.flatten = nn.Flatten()

        # プーリング層
        self.pool = nn.MaxPool2d(2)  # カーネルサイズ

        # ドロップアウト層
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout(0.5)

        # ソフトマックス
        self.softmax = nn.Softmax(dim=1)

        # 特徴量抽出
        self.features = nn.Sequential(
            self.conv1,
            self.bn1,
            self.relu,
            self.pool,
            self.conv2,
            self.bn2,
            self.relu,
            self.pool,
            self.dropout1,
        )

        # 分類器
        self.classifier = nn.Sequential(
            self.flatten,
            self.l1,
            self.relu,
            self.l2,
            self.dropout2,
            self.softmax,
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)

        return x


def load_MNIST(batch=128):
    """
    MNISTデータセットを訓練データと検証データに分割してDataLoaderとして返す関数
    batch: バッチサイズ
    """
    # テンソルに変換を行い、平均0.5, 標準偏差0.5にスケール変換を行う
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
    )

    train_set = datasets.MNIST(
        root=dataset_path, train=True, download=True, transform=transform
    )

    n_sample = len(train_set)  # サンプル数
    train_size = int(n_sample * 0.8)  # 8:2の割合で訓練と検証を分割

    # 分割を行うインデックスを指定
    subset1_indices = list(range(0, train_size))
    subset2_indices = list(range(train_size, n_sample))

    # Subsetを用いて指定インデックスに分割する
    train_dataset = Subset(train_set, subset1_indices)
    val_dataset = Subset(train_set, subset2_indices)

    # 訓練データと検証データをバッチサイズを指定してDataLoaderインスタンス化
    train_loader = DataLoader(train_dataset, batch_size=batch, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch, shuffle=True)

    return {"train": train_loader, "val": val_loader}


def main():
    """
    学習と検証データに対するスコアの計算。ベストモデルの保存を行う。
    """
    # データのロード
    data_loader = load_MNIST(batch=128)

    # エポック
    epochs = 50

    # 検証データの最高スコアを格納する変数
    val_best = 0.0

    # デバイスの指定 (M1 or M2 Mac環境の想定)
    device = torch.device("mps")

    # モデルのインスタンス化
    net = Net().to(device)

    # オプティマイザ
    optimizer = RMSprop(net.parameters(), lr=0.001)

    # 損失関数
    criterion = nn.CrossEntropyLoss()

    # 学習の開始
    for epoch in range(epochs):
        """学習"""
        # 学習モード
        net.train()

        # 訓練データの損失値を格納
        train_loss = 0.0

        for i, (data, label) in enumerate(data_loader["train"]):
            # 指定のデバイスへ移動
            data = data.to(device)
            label = label.to(device)

            # 勾配の初期化
            optimizer.zero_grad()

            # forward関数の計算
            output = net(data)

            # lossの計算
            loss = criterion(output, label)

            train_loss += loss.item()

            # 勾配の計算
            loss.backward()

            # パラメータの更新
            optimizer.step()

        train_loss /= len(data_loader["train"])  # 1エポックごとの訓練データのlossの平均

        print("-" * 10 + f"{epoch + 1}epoch(s)" + "-" * 10)
        print(f"Training loss: {train_loss:.5f}")

        """検証"""
        # 評価モード
        net.eval()

        val_loss = 0.0  # 検証データの損失を格納
        val_acc = 0.0  # 検証データに対する精度を格納

        with torch.no_grad():
            for data, label in data_loader["val"]:
                # 指定のデバイスに移動
                data = data.to(device)
                label = label.to(device)

                # forward関数の計算
                output = net(data)
                # 損失の計算
                loss = criterion(output, label)
                val_loss += loss.item()

                # 検証データの予測
                predict = output.argmax(dim=1, keepdim=True)
                # 検証データの精度
                val_acc += predict.eq(label.view_as(predict)).sum().item()

        val_loss /= len(data_loader["val"].dataset)  # 検証データの損失
        val_acc /= len(data_loader["val"].dataset)  # 検証データの精度

        print(f"val_loss: {val_loss:.5f}")
        print(f"val_acc: {val_acc:.5f}", end="\n\n")

        # 検証データのスコアが最高値を上回ったときに保存
        if val_acc > val_best:
            # モデルの更新
            torch.save(net.state_dict(), model_path / f"CNN_Model_{str(epoch)}.pth")
            # 最高精度の更新
            val_best = val_acc


# コマンドラインから呼び出されたときにメイン関数を実行する
if __name__ == "__main__":
    main()
