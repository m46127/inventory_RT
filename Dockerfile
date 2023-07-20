# Python 3.11イメージをベースとする
FROM python:3.11

# Javaと必要なシステムパッケージをインストール
RUN apt-get clean && \
    apt-get update -y --fix-missing && \
    apt-get install -y openjdk-11-jre-headless libpoppler-cpp-dev ghostscript && \
    apt-get clean;

# requirements.txtをコピー
COPY requirements.txt ./requirements.txt

# Pythonの依存関係をインストール
RUN pip install -r requirements.txt

# camelotをインストール
RUN pip install camelot-py[cv]

# Streamlitスクリプトをコピー
COPY app.py ./app.py

# Streamlitのポートを開放
EXPOSE 8501

# Streamlitを実行
CMD streamlit run app.py
