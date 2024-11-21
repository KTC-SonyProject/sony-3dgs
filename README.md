# Spadge

## 1. Introduction

このアプリケーションはSonyのSRD(Spatial Reality Display)を用いて立体的な映像を表示させるのを容易にするアプリケーションです。
主に次のような機能を提案します。
- 3DGSの理論を用いて動画から高精度な3D空間を作成、Unityのアプリケーションに送信します。
- 表示させている映像についての説明を生成AIを使用して音声会話で説明します。
- 表示している映像の操作などもAgent技術を用いて音声でできるようにします。

## 2. Requirement

### application

完全なアプリケーションはDockerでWEBアプリとして構築します。

- Docker compose
- Nvidia GPU
- CUDA Toolkit
- Visual Studio 2022

詳細な要件は[NerfStudio](https://docs.nerf.studio/quickstart/installation.html#use-docker-image)の公式ドキュメントを参照してください。

以下の条件に当てはまる場合は環境ごとのデスクトップアプリとして提供します。

- すでに学習済みの3DGSデータ(PLYファイル)がある
- 複数のユーザーからのアクセスがなくデスクトップアプリのみで充分である


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
