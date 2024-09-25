FROM public.ecr.aws/lambda/python:3.11

# requirements.txtを使用して関数の依存関係をインストールする。
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# AWS ベースイメージには、環境変数「LAMBDA_TASK_ROOT=/var/task」が含まれています。
COPY app.py .env ${LAMBDA_TASK_ROOT}

# Dockerイメージ内の実行時のデフォルトコマンドを設定します。
CMD [ "app.handler" ]
