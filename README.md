# OrderLab Python CI/CD 실습

주문 금액 계산부터 CSV 매출 집계, 주문 API, 자동 테스트,
GitHub Actions 검사와 GitHub Pages 배포까지 구현한 프로젝트입니다.

## 링크

- 저장소: https://github.com/eunlovelee77-hub/orderlab-project
- 매출 보고서: https://eunlovelee77-hub.github.io/orderlab-project/
- 자동 검사 기록: https://github.com/eunlovelee77-hub/orderlab-project/actions
- PR 실습: https://github.com/eunlovelee77-hub/orderlab-project/pull/1

## 구현 기능

1. 상품 가격과 수량으로 주문 금액 계산
2. 할인율 검증 및 할인 후 금액에 따른 배송비 계산
3. CSV 주문 파일의 총매출 집계
4. FastAPI 주문 생성 및 조회
5. CSV 매출을 HTML 보고서로 생성하고 GitHub Pages에 배포

API의 주문 데이터는 메모리에 저장되므로 앱을 새로 만들면 초기화됩니다.
GitHub Pages에는 HTML 매출 보고서를 배포하며, API 서버는 배포하지 않습니다.

## 실행 환경 준비

Python 3.14와 Windows PowerShell 기준입니다.
프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## 코드 검사와 테스트

```powershell
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
```

정상·예외·경계값 및 API 동작을 검사하는 테스트 20개를 작성했습니다.

커버리지 확인:

```powershell
python -m pytest --cov=orderlab --cov-report=term-missing
```

## 보고서 생성

```powershell
python generate_report.py
```

`data/sample_orders.csv`를 읽어 `site/index.html`을 생성합니다.
샘플 데이터의 총매출은 35,000원입니다.
이 집계는 할인과 배송비 없이 상품 가격 × 수량을 합산합니다.

## CI/CD 동작

- Push와 Pull Request에서 Ruff 검사와 pytest를 실행합니다.
- 테스트는 Ubuntu와 Windows에서 각각 실행합니다.
- 커버리지 XML 보고서를 운영체제별 artifact로 보관합니다.
- PR과 main 이외의 브랜치에서는 배포하지 않습니다.
- main Push에서는 lint와 모든 테스트가 성공한 후에만 배포합니다.

## 실패 재현과 복구

### PR 자동 검사 확인

1. feature/report-check 브랜치를 만들었습니다.
2. 정상 계산의 기댓값을 20,000에서 99,999로 변경했습니다.
3. PR에서 테스트 실패 로그의 `assert 20000 == 99999`를 확인했습니다.
4. 기댓값을 20,000으로 복구하고 같은 PR의 검사 통과를 확인했습니다.
5. PR을 main에 병합한 뒤 자동 배포를 확인했습니다.

### 테스트 실패 시 배포 차단 확인

1. main에서 테스트 기댓값을 일부러 잘못 변경했습니다.
2. GitHub Actions에서 테스트 실패와 deploy의 Skipped 상태를 확인했습니다.
3. 기댓값을 복구한 후 모든 검사와 배포가 성공하는 것을 확인했습니다.

### 실습 중 해결한 문제

- orderlab 폴더 이름의 오타를 수정하여 import 오류를 해결했습니다.
- .venv 안에 있던 테스트 파일을 프로젝트의 tests 폴더로 옮겼습니다.
- Ruff로 코드 형식을 정리했습니다.
- API 테스트 도구의 변경 안내에 따라 httpx2를 설치 목록에 반영했습니다.
- 배포 설정을 Commit과 Push한 뒤 실제 Pages 배포를 확인했습니다.

## 추가 검증

- 사용하지 않는 import os를 추가하여 Ruff의 F401 오류를 확인하고 복구했습니다.
- 보고서 생성과 예상 매출 35,000 KRW 표시를 확인하는 회귀 테스트를 추가했습니다.
