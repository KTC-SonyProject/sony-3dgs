# SRD ＆ 3DGS application

## 1. Introduction

このアプリケーションはSony SRD(Spatial Reality Display)と3DGS(3D Gaussian Splatting)を用いたアプリケーションです。

## 2. Requirement

### application
- Python 3.12
- Poetry

### Unity

## 3. Installation

1. Unity Hubを起動し、Unity 2020.3.14f1をインストールします。

## 4. Usage

1. Unity Hubを起動し、プロジェクトを開きます。

## 5. Development

このプロジェクトではpoetryを使用しています。poetryを使用していない場合はrequirements.txtを参照してください。

### Docker環境がある場合

> Devcontainer(Docker)を使用できる環境の場合、Devcontainerを使用することをお勧めします。

1. このリポジトリをクローンします。
2. Devcontainerでこのリポジトリを開きます。
3. `flet run app`でアプリケーションを起動します。(Linuxアプリとして起動します。Webブラウザでも表示することができるのでそちらも活用してください。`--web`)
> ※ WSLの場合、WSLのGUIを有効にする必要がある場合があります。トラブルシューティングは[公式サイト](https://flet.dev/docs/getting-started/)を参照してください。

### Docker環境がない場合

1. このリポジトリをクローンします。
2. `poetry install` or `pip install -r requirements.txt`で必要なライブラリをインストールします。
3. `flet run app`でアプリケーションを起動します。
