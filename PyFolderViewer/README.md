# JK's 폴더의 파일구성 분석툴

지정 경로에 존재하는 모든 파일들(하위 폴더 포함)의 간략 정보를 트리 형태로, 콘솔화면이나 파일에 출력시키는 어플이다.

[패키지로 이동](../README.md#프로젝트별-사용법)<br/>


## 변경 이력
```
[20260322-20260322] : 기능 추가
                        > "--pass-dir=bin,obj" 콘솔옵션으로 특정 폴더명칭목록만 허용
                        > "--deny-dir=bin,obj" 콘솔옵션으로 특정 폴더명칭목록은 제외
                      버그 패치
                        > `파일명칭 허용 필터` 문제 해결
[20251019-20251019] : 기능 추가
                        > "--pass-name=_test,log_" 콘솔옵션으로 특정 파일명칭목록만 허용
                        > "--deny-name=_test,log_" 콘솔옵션으로 특정 파일명칭목록은 제외
                      기능 확장
                        > 파일의 명칭/확장자 필터링에, 특수문자 포함되도록 처리
                          python pyfolderviewer.py . --hide-size --hide-hidden --deny-name='_test,(test),[test]' --pass-ext=py,txt --savedfile=logs/pfv-parse-test.txt
                          python pyfolderviewer-lite.py . --hide-size --hide-hidden --deny-name='_test,(test),[test]' --pass-ext=py,txt
[20251018-20251018] : 기능 변경
                        > 파일검출의 show 옵션들을 hide 옵션으로 변경
[20251015-20251015] : 최초 개발
```

## 목차
* [개발 목적](#개발-목적)
* [파일 구성](#파일-구성)
* [사용법](#사용법)
  * [콘솔 도움말 보기](#콘솔-도움말-보기)
  * [사용 예시](#사용-예시)
    * [본 프로젝트 파일 구성 출력 > [hidden]파일 제외](#본-프로젝트-파일-구성-출력--hidden파일-제외)
    * [본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외](#본-프로젝트-파일-구성-출력--hidden-pyc-md파일-제외)
    * [본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한](#본-프로젝트-파일-구성-출력--hidden-pyc-md파일-제외--깊이-제한)
    * [본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김](#본-프로젝트-파일-구성-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김)
    * [본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김](#본-프로젝트-파일-구성-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김--설명-숨김)
    * [본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 파일 저장](#본-프로젝트-파일-구성-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김--설명-숨김--파일-저장)


## 개발 목적

아래의 [파일 구성](#파일-구성) 항목과 같이, 프로젝트의 파일 구성과 설명을 추출하여 표출함으로써,</br>
운영자에게는 빠른 분석 보고서 작성을, 개발자에게는 구조 분석에 편리함을 제공하기 위함이다.


## 파일 구성
```
> python pyfolderviewer.py . --hide-size
./
├── .gitignore
├── .hidden.txt             # 테스트용 숨김 파일
├── README.md               # JK's 폴더의 파일구성 분석툴
├── example.py              # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── pyfolderviewer-lite.py  # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
└── pyfolderviewer.py       # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
```


## 사용법

### 콘솔 도움말 보기
```
> python pyfolderviewer.py -h
usage: python pyfolderviewer.py <parsepath> [--savedfile=경로]
                        [--deny-name=n1,n2] [--pass-name=n1,n2]
                        [--deny-ext=ext1,ext2] [--pass-ext=ext1,ext2]
                        [--max-depth=N] [--hide-desc] [--hide-size] [--hide-hidden]

디렉토리 파일구성 분석툴 (파일검출: 파일명/확장자 필터링 + 깊이 제한 + 파일설명 + 파일사이즈 + 숨김파일 제어, 결과출력: 콘솔+파일)

positional arguments:
  parsepath             분석 디렉토리 경로

options:
  -h, --help            show this help message and exit
  --savedfile SAVEDFILE
                        분석결과 저장파일 경로
  --deny-name DENY_NAME
                        제외할 파일명칭 목록 (예: _test,log_)
  --pass-name PASS_NAME
                        허용할 파일명칭 목록 (예: _test,log_)
  --deny-ext DENY_EXT   제외할 파일 확장자 목록 (예: pyc,md)
  --pass-ext PASS_EXT   허용할 파일 확장자 목록 (예: py,txt)
  --max-depth MAX_DEPTH
                        출력할 최대 디렉토리 깊이 (예: 2)
  --hide-desc           파일설명 숨김
  --hide-size           파일사이즈 숨김
  --hide-hidden         숨김파일 숨김
```

### 사용 예시

#### 본 프로젝트 파일 구성 출력 > [hidden]파일 제외
```
> python pyfolderviewer.py . --hide-hidden
./
├── README.md (10537) # JK's 폴더의 파일구성 분석툴
├── example.py (9989) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── logs/
│   └── output-ptree.txt (616)
├── pyfolderviewer-lite.py (9143) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
└── pyfolderviewer.py (10520) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
```

#### 본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외
```
> python pyfolderviewer.py . --hide-hidden --deny-ext=pyc,md
./
├── example.py (9989) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── logs/
│   └── output-ptree.txt (616)
├── pyfolderviewer-lite.py (9143) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
└── pyfolderviewer.py (10520) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
```

#### 본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한
```
> python pyfolderviewer.py . --hide-hidden --deny-ext=pyc,md --max-depth=0
./
├── example.py (9989) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── logs/
├── pyfolderviewer-lite.py (9143) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
└── pyfolderviewer.py (10520) # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
```

#### 본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김
```
> python pyfolderviewer.py . --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size
./
├── example.py # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── logs/
├── pyfolderviewer-lite.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
└── pyfolderviewer.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
```

#### 본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김
```
> python pyfolderviewer.py . --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size --hide-desc
./
├── example.py
├── logs/
├── pyfolderviewer-lite.py
└── pyfolderviewer.py
```

#### 본 프로젝트 파일 구성 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 파일 저장
```
> python pyfolderviewer.py . --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size --hide-desc --savedfile=./output-ptree.txt
  콘솔화면과 저장파일내용 동일한지 확인
```


[패키지로 이동](../README.md#프로젝트별-사용법)<br/>
