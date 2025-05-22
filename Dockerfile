FROM python:3.12-slim

# 필수 도구 설치 + oh-my-zsh + agnoster 테마 설정
RUN apt-get update && apt-get install -y \
    docker.io \
    git \
    curl \
    zsh \
    fonts-powerline \
    && rm -rf /var/lib/apt/lists/* \
    && sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && chsh -s $(which zsh) \
    && echo 'ZSH_THEME="agnoster"' >> ~/.zshrc

# docker compose CLI 플러그인 설치 (v2)
RUN mkdir -p ~/.docker/cli-plugins && \
    curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 \
      -o ~/.docker/cli-plugins/docker-compose && \
    chmod +x ~/.docker/cli-plugins/docker-compose

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic alembic
COPY ./app ./app
COPY .env .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
