FROM python:3.12-slim

# お好みで好きなパッケージを追加
RUN apt update && apt install -y \
build-essential \
git \
curl \
sudo \
libgtk-3-dev \
libgstreamer1.0-dev \
libgstreamer-plugins-base1.0-dev \
libmpv-dev \
mpv \
&& apt clean \
&& rm -rf /var/lib/apt/lists/*


RUN git config --global --add safe.directory /app

RUN ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/x86_64-linux-gnu/libmpv.so.1
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH


# ユーザーIDとグループIDをビルド時の引数として受け取る
ARG USER_ID=1000
ARG GROUP_ID=1000

# ユーザーとグループを作成
RUN groupadd -g ${GROUP_ID} appgroup && \
useradd -m -d /home/appuser -s /bin/bash -u ${USER_ID} -g appgroup appuser && \
echo 'appuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

ENV HOME=/home/appuser
USER appuser


WORKDIR /app

# poetryのインストール
RUN pip install --upgrade pip && pip install poetry 
ENV PATH="/home/appuser/.local/bin:$PATH"

# アプリケーションコードをコピー
COPY --chown=appuser:appgroup . /app