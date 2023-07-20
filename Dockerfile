# Python 3.9イメージをベースとする
FROM python:3.11

# Javaをインストール
RUN apt-get clean && \
    apt-get update -y --fix-missing || true && \
    apt-get install -y openjdk-11-jre-headless || true && \
    apt-get clean;


# requirements.txtをコピー
COPY requirements.txt ./requirements.txt

# Pythonの依存関係をインストール
RUN pip install -r requirements.txt

# Streamlitスクリプトをコピー
COPY app.py ./app.py

# Streamlitのポートを開放
EXPOSE 8501

# Streamlitを実行
CMD streamlit run app.py
