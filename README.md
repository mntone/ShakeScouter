[English](//github.com/mntone/ShakeScouter/blob/main/README-en.md) | 日本語

# ShakeScouter

ShakeScouterは「サーモンランNEXT WAVE」の映像を解析し、テレメトリーデータを生成するために設計されたPythonプログラムです。このツールは、Nintendo Switchで人気のゲーム「スプラトゥーン3」にあるサーモンランの映像を解析するために設計されています。

## 目次

* [特徴](#特徴)
* [インストール](#インストール)
* [使用方法](#使用方法)
* [貢献について](#貢献について)
* [ライセンス](#ライセンス)
* [謝辞](#謝辞)
* [著者](#著者)
* [関連プロジェクト](#関連プロジェクト)

## 特徴

- **画像解析**: ShakeScouterは高度な画像処理技術を使用して、サーモンランNEXT WAVEの映像を解析します。
- **テレメトリー生成**: このプログラムは、解析結果に基づいてテレメトリーデータを生成し、ゲームプレイの統計に関する貴重な洞察を提供します。

## インストール

1. リポジトリーをクローン: `git clone https://github.com/mntone/ShakeScouter.git`
2. プロジェクト ディレクトリーに移動: `cd ShakeScouter`
3. Pythonをインストール
    - Windows: https://www.microsoft.com/store/productId/9NCVDN91XZQP
    - macOS: `brew install python@3.12`
4. 依存関係をインストール: `pip install -r requirements.txt`
5. PyTorchをインストール: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu`

将来的に、Windows上でCUDAを使用した解析プログラムを採用する可能性があります。

## 使用方法

```sh
py shakescout.py [options]
```

### オプション

- `--development`: 開発モードで起動します。
- `-d`, `--device`: PyTorchで使用するデバイスを指定します。選択可能なデバイスは、`auto`、`cpu`、`cuda` です。
- `-o`, `--outputs`: 出力方式を選択します。選択可能な出力方式は、`console`、`json`、`websocket` です。
- `-i`, `--input`: OpenCV入力のカメラ入力デバイスIDを指定します。
- `--width`: OpenCV入力のカメラ入力の幅を指定します。
- `--hight`: OpenCV入力のカメラ入力の高さを指定します。
- `-t`, `--timestamp`: JSONファイル名に日時を使用します。
- `-H`, `--host`: WebSocket接続で使用するホスト名を指定します。
- `-p`, `--port`: WebSocket接続で使用するポート番号を指定します。

## 貢献について

あなたの貢献に感謝します! リポジトリーをフォークして、改善点を含めたプルリクエストを提出してください。

## ライセンス

このプロジェクトは GPLv3 ライセンスの下で認可されています。詳細については [LICENSE](//github.com/mntone/ShakeScouter/blob/main/LICENSE) ファイルを参照してください。

## 連絡先

質問やサポートが必要な場合は、私に連絡してください。

- Mastodon: https://mstdn.jp/@mntone

## 謝辞

- まず、スプラトゥーン3のクリエイターの方々に心から感謝します。
- [erudot](https://x.com/erudot)氏に感謝します。彼は私にサーモンランNEXT WAVEをプレイする機会を与えてくれ、でんせつ 999に到達するきっかけとなりました。
- また、このソフトウェアの開発において、ChatGPTのサポートに心から感謝いたします。

## 著者

- mntone - このプロジェクトの作成者

## 関連プロジェクト

- [Shake StreamKit](//github.com/mntone/shake-streamkit): サーモンランNEXT WAVEのオーバーレイツール
