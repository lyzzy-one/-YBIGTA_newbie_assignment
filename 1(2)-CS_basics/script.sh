#!/bin/bash

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if ! command -v conda &> /dev/null; then
    echo "[INFO] conda가 없어 Miniconda를 설치합니다..."
    MINICONDA_DIR="$HOME/miniconda3"

    # OS / CPU 아키텍처에 맞는 설치 스크립트 선택
    if [[ "$(uname)" == "Darwin" ]]; then
        if [[ "$(uname -m)" == "arm64" ]]; then
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
        else
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
        fi
    else
        if [[ "$(uname -m)" == "aarch64" ]]; then
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh"
        else
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        fi
    fi

    curl -fsSL "$MINICONDA_URL" -o /tmp/miniconda.sh
    bash /tmp/miniconda.sh -b -p "$MINICONDA_DIR"
    rm -f /tmp/miniconda.sh
    source "$MINICONDA_DIR/etc/profile.d/conda.sh"
else
    # 이미 설치된 conda의 셸 함수를 현재 셸에 로드
    source "$(conda info --base)/etc/profile.d/conda.sh"
fi


# Conda 환셩 생성 및 활성화
## TODO
if ! conda env list | grep -qE "/envs/myenv$|^myenv\s"; then
    echo "[INFO] 가상환경 myenv 생성 중..."
    conda create -y -n myenv python=3.10
fi
conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1
fi

# 필요한 패키지 설치
## TODO
pip install --quiet mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

# 출력 디렉토리 준비
mkdir -p ../output

for file in *.py; do
    ## TODO
    # 파일명 예: 2_2164.py -> 문제번호 2164 추출
    problem=$(echo "$file" | sed -E 's/^[0-9]+_([0-9]+)\.py$/\1/')
    input_file="../input/${problem}_input"
    output_file="../output/${problem}_output"

    if [[ -f "$input_file" ]]; then
        python "$file" < "$input_file" > "$output_file"
        echo "[INFO] 실행 완료: $file -> output/${problem}_output"
    else
        echo "[WARN] 입력 파일 없음: $input_file (건너뜀)"
    fi
done

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
: > ../mypy_log.txt   # 로그 초기화
for file in *.py; do
    echo "===== mypy: $file =====" >> ../mypy_log.txt
    mypy "$file" >> ../mypy_log.txt 2>&1
    echo "" >> ../mypy_log.txt
done

# 원래 디렉토리(1(2)-CS_basics)로 복귀
cd ..

# conda.yml 파일 생성
## TODO
conda env export > conda.yml

# 가상환경 비활성화
## TODO
conda deactivate
