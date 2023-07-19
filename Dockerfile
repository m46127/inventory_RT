# Python環境をセットアップします
FROM python:3.8

# ワーキングディレクトリを作成します
WORKDIR /app

# 必要なパッケージをインストールします
RUN apt-get update \
    && apt-get install -y gcc g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 依存関係をコピーしてインストールします
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y openjdk-11-jre-headless
RUN apt-get update && apt-get install -y openjdk-11-jdk
RUN pip install -r requirements.txt

# Streamlitの設定
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'
RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > /root/.streamlit/config.toml'

# アプリケーションをコピーします
COPY . .

# コマンドを指定します
EXPOSE 8501
CMD streamlit run your_file.py
