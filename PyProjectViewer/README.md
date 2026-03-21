# JK's 프로젝트 구조 분석툴

지정 경로(하위 폴더 포함)의 모든 파일들을 트리 형태로 시각화하고, 소스코드 파일은 내부의 클래스/함수/변수를 추출하여, 콘솔화면이나 파일에 출력시키는 어플이다.

[패키지로 이동](../README.md#프로젝트별-사용법)<br/>


## 변경 이력
```
[20251019-20251019] : 기능 추가
                      - 파일검출
                        > "--pass-name=_test,log_" 콘솔옵션으로 특정 파일명칭목록만 허용
                        > "--deny-name=_test,log_" 콘솔옵션으로 특정 파일명칭목록은 제외
                      기능 확장
                      - 파일검출
                        > 파일의 명칭/확장자 필터링에, 특수문자 포함되도록 처리
                          python pyprojectviewer.py . --hide-size --hide-hidden --deny-name='_test,(test),[test]' --pass-ext=py,txt --hide-codes --savedfile=logs/ppv-parse-test.txt
[20251017-20251018] : 최초 개발
                        > PyFolderViewer, PyFilesViewer-Pro 기능을 통합하여 개발
                        > 파일검출의 show 옵션들을 hide 옵션으로 변경
```

## 목차
* [개발 목적](#개발-목적)
* [파일 구성](#파일-구성)
* [설계](#설계)
* [사용법](#사용법)
  * [콘솔 도움말 보기](#콘솔-도움말-보기)
  * [사용 예시](#사용-예시)
    * [테스팅 프로젝트 구조 출력 > [hidden]파일 제외](#테스팅-프로젝트-구조-출력--hidden파일-제외)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외--깊이-제한)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김--설명-숨김)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 코드분석 제외](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김--설명-숨김--코드분석-제외)
    * [테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 파일 저장](#테스팅-프로젝트-구조-출력--hidden-pyc-md파일-제외--깊이-제한--파일사이즈-숨김--설명-숨김--파일-저장)


## 개발 목적

운영자에게는 빠른 분석 보고서 작성을, 개발자에게는 구조 분석에 편리함을 제공하기 위함이다.


## 파일 구성
```
> python pyprojectviewer.py . --hide-size --hide-codes
./
├── .gitignore
├── README.md                 # JK's 프로젝트 구조 분석툴
├── example.py                # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
├── pyprojectviewer-lite.py   # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면에 출력하는 어플 (기능 제한 배포용)
├── pyprojectviewer.py        # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
└── testing/                  # 본 프로젝트 테스트용
    ├── .hidden.txt
    ├── example.py # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
    ├── logs/
    │   ├── example.py # PyProjectViewer 테스트용
    │   └── output-ppv.txt
    ├── output-allfiles.txt
    ├── output-gen.html
    ├── output-gen.json
    ├── output-gen.md # 분석 정보
    ├── output-onefile.txt
    └── pyfileviewer-s.py # 하나의 py파일을 분석하여, 포함된 클래스/함수/변수 목록을 콘솔화면에 출력하는 어플
```

## 설계
```
- 정리
  > 조건
    - PyFolderViewer를 메인으로 하고, PyFilesViewer-Pro의 기능을 추가시켜 구현한다.
    - 파일의 코드분석을 수행할지 여부에 대한, 콘솔옵션(--hide-codes)과 기능을 추가한다.
  > 작업 사항
    - PyFolderViewer의 코드를 정리하여, PyProjectViewer/example.py에 복사한다.
    - 우선, example.py 파일에 구현한다.
      > PyFilesViewer-Pro 전용 콘솔옵션들을 example에 추가시킨다.
        [--viewparts=16진수] [--viewitems=16진수]
      > py파일인 경우, [PITVCF]를 분석하여, 출력시킨다.
      > 콘솔옵션(--hide-codes) 기능 추가
    - example.py 파일로, pyprojectviewer.py 파일을 제작한다.
    x example.py 파일의 기능을 제한하여, pyprojectviewer-lite.py 파일을 제작한다.
  
- [PyFolderViewer] 분석
  1. 사용법
    > python ../PyFolderViewer/pyfolderviewer.py -h
    ...
  2. 코드 분석
    > python ../PyFileViewer/pyfileviewer-s.py ../PyFolderViewer/pyfolderviewer.py
    ...

- [PyFilesViewer-Pro] 분석
  1. 사용법
    > python ../PyFileViewer/pyfilesviewer-pro.py -h
    ...
  2. 코드 분석
    > python ../PyFileViewer/pyfileviewer-s.py ../PyFileViewer/pyfilesviewer-pro.py
    ...
```


## 사용법

### 콘솔 도움말 보기
```
> python pyprojectviewer.py -h
usage: python pyprojectviewer.py <parsepath> [--savedfile=경로]
                        [--deny-name=n1,n2] [--pass-name=n1,n2]
                        [--deny-ext=ext1,ext2] [--pass-ext=ext1,ext2]
                        [--max-depth=N] [--hide-desc] [--hide-size] [--hide-hidden]
                        [--hide-codes] [--viewparts=16진수] [--viewitems=16진수]

프로젝트 구조 분석툴 (파일검출: 파일명/확장자 필터링 + 깊이 제한 + 파일설명 + 파일사이즈 + 숨김파일 + 코드분석 제어, 코드검출: 출력부분 + 출력항목 비트제어, 결과출력: 콘솔+파일)

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
  --hide-codes          코드분석 숨김
  --viewparts VIEWPARTS
                        출력부분 : 16진수 비트조합 (예: 0x1F)
                          0x01  # 임포트모듈
                          0x02  # 사용자정의타입
                          0x04  # 전역변수
                          0x08  # 클래스
                          0x10  # 함수
  --viewitems VIEWITEMS
                        출력항목 : 16진수 비트조합 (예: 0x0F)
                          0x01  # 명칭
                          0x02  # 클래스상속
                          0x04  # 함수파라미터
                          0x08  # 주석
```

### 사용 예시

#### 테스팅 프로젝트 구조 출력 > [hidden]파일 제외
```
> python pyprojectviewer.py testing --hide-hidden
testing/
├── example.py (15421) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
│     [I] ast
│     [I] os
│     [I] argparse
│     [I] json
│     ----------------------------------------
│     [V] gstrParsePath = ''
│     [V] gaSavedBlocks = ...
│     ----------------------------------------
│     [F] add_block(file_path, imports, classes, functions, globals)
│     [F] get_function_signature(func_node, max_args)
│     [F] get_class_bases(class_node)
│     [F] extract_type_alias(value_node)
│     [F] analyze_file(file_path)
│     [F] analyze_directory(directory_path)
│     [F] save_output(output_path, format)
│     [F] main()
├── logs/
│   ├── example.py (3810) # PyProjectViewer 테스트용
│   │     [I] os
│   │     [I] enum
│   │     ----------------------------------------
│   │     [V] gstrParsePath = ''
│   │     [V] gaSavedBlocks = ...
│   │     ----------------------------------------
│   │     [C] eTestStyles(enum.Enum) # 테스트용 나열형 클래스
│   │     [C] CSumClass() # 테스트용 일반 클래스
│   │       [F] __init__(self) # 생성자
│   │       [F] __call__(self, *args, **kwds) # 호출자
│   │       [F] __setvalues__(self, a, b) # 값 설정
│   │       [F] __getvalues__(self) # 값 리턴
│   │       [F] __sum__(self) # 덧셈
│   │     [F] add_block(file_path, imports, classes, functions, globals)
│   │     [F] get_function_signature(func_node, max_args)
│   │     [F] analyze_file(file_path)
│   │     [F] analyze_directory(directory_path)
│   └── output-ppv.txt (15512)
├── output-allfiles.txt (9260)
├── output-gen.html (17682)
├── output-gen.json (24238)
├── output-gen.md (12378) # 분석 정보
├── output-onefile.txt (1281)
└── pyfileviewer-s.py (19055) # 하나의 py파일을 분석하여, 포함된 클래스/함수/변수 목록을 콘솔화면에 출력하는 어플
       [I] ast
       [I] os
       [I] enum
       [I] argparse
       ----------------------------------------
       [V] MAX_VIEW_PARAMS = 6
       [V] MAX_VIEW_COMMENTS = 200
       [V] BIT_PART_IMPORT = 1
       [V] BIT_PART_TYPE = 2
       [V] BIT_PART_VAR = 4
       [V] BIT_PART_CLASS = 8
       [V] BIT_PART_FUNC = 16
       [V] BIT_PART_DEF = ...
       [V] BIT_PART_TV = ...
       [V] BIT_PART_ALL = 31
       [V] BIT_ITEM_NAME = 1
       [V] BIT_ITEM_INHERIT = 2
       [V] BIT_ITEM_PARAMS = 4
       [V] BIT_ITEM_COMMENTS = 8
       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
       [V] BIT_ITEM_DEF = ...
       [V] BIT_ITEM_ALL = 15
       [T] gnViewParts = BIT_PART_ALL
       [T] gnViewItems = BIT_ITEM_ALL
       ----------------------------------------
       [C] eViewStyles(enum.Enum) # 테스트용 나열형 클래스
       [C] CTestClass() # 테스트용 일반 클래스
         [F] __init__(self) # 생성자
         [F] __call__(self, *args, **kwds) # 호출자
         [F] __setvalues__(self, a, b) # 값 설정
         [F] __getvalues__(self) # 값 리턴
         [F] __sum__(self) # 덧셈
       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 반환
       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 반환 (최대 파라미터 제한)
       [F] get_function_signature_old(func_node) # 함수의 파라미터 목록을 문자열로 반환
       [F] get_docstring(node)
       [F] print_classes_funcs(node, indent)
       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
       [F] analyze_file(file_path) # py파일의 [PITVCF]를 분석하여, 콘솔화면에 출력
       [F] main()
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md
testing/
├── example.py (15421) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
│     [I] ast
│     [I] os
│     [I] argparse
│     [I] json
│     ----------------------------------------
│     [V] gstrParsePath = ''
│     [V] gaSavedBlocks = ...
│     ----------------------------------------
│     [F] add_block(file_path, imports, classes, functions, globals)
│     [F] get_function_signature(func_node, max_args)
│     [F] get_class_bases(class_node)
│     [F] extract_type_alias(value_node)
│     [F] analyze_file(file_path)
│     [F] analyze_directory(directory_path)
│     [F] save_output(output_path, format)
│     [F] main()
├── logs/
│   ├── example.py (3810) # PyProjectViewer 테스트용
│   │     [I] os
│   │     [I] enum
│   │     ----------------------------------------
│   │     [V] gstrParsePath = ''
│   │     [V] gaSavedBlocks = ...
│   │     ----------------------------------------
│   │     [C] eTestStyles(enum.Enum) # 테스트용 나열형 클래스
│   │     [C] CSumClass() # 테스트용 일반 클래스
│   │       [F] __init__(self) # 생성자
│   │       [F] __call__(self, *args, **kwds) # 호출자
│   │       [F] __setvalues__(self, a, b) # 값 설정
│   │       [F] __getvalues__(self) # 값 리턴
│   │       [F] __sum__(self) # 덧셈
│   │     [F] add_block(file_path, imports, classes, functions, globals)
│   │     [F] get_function_signature(func_node, max_args)
│   │     [F] analyze_file(file_path)
│   │     [F] analyze_directory(directory_path)
│   └── output-ppv.txt (15512)
├── output-allfiles.txt (9260)
├── output-gen.html (17682)
├── output-gen.json (24238)
├── output-onefile.txt (1281)
└── pyfileviewer-s.py (19055) # 하나의 py파일을 분석하여, 포함된 클래스/함수/변수 목록을 콘솔화면에 출력하는 어플
       [I] ast
       [I] os
       [I] enum
       [I] argparse
       ----------------------------------------
       [V] MAX_VIEW_PARAMS = 6
       [V] MAX_VIEW_COMMENTS = 200
       [V] BIT_PART_IMPORT = 1
       [V] BIT_PART_TYPE = 2
       [V] BIT_PART_VAR = 4
       [V] BIT_PART_CLASS = 8
       [V] BIT_PART_FUNC = 16
       [V] BIT_PART_DEF = ...
       [V] BIT_PART_TV = ...
       [V] BIT_PART_ALL = 31
       [V] BIT_ITEM_NAME = 1
       [V] BIT_ITEM_INHERIT = 2
       [V] BIT_ITEM_PARAMS = 4
       [V] BIT_ITEM_COMMENTS = 8
       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
       [V] BIT_ITEM_DEF = ...
       [V] BIT_ITEM_ALL = 15
       [T] gnViewParts = BIT_PART_ALL
       [T] gnViewItems = BIT_ITEM_ALL
       ----------------------------------------
       [C] eViewStyles(enum.Enum) # 테스트용 나열형 클래스
       [C] CTestClass() # 테스트용 일반 클래스
         [F] __init__(self) # 생성자
         [F] __call__(self, *args, **kwds) # 호출자
         [F] __setvalues__(self, a, b) # 값 설정
         [F] __getvalues__(self) # 값 리턴
         [F] __sum__(self) # 덧셈
       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 반환
       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 반환 (최대 파라미터 제한)
       [F] get_function_signature_old(func_node) # 함수의 파라미터 목록을 문자열로 반환
       [F] get_docstring(node)
       [F] print_classes_funcs(node, indent)
       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
       [F] analyze_file(file_path) # py파일의 [PITVCF]를 분석하여, 콘솔화면에 출력
       [F] main()
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md --max-depth=0
testing/
├── example.py (15421) # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
│     [I] ast
│     [I] os
│     [I] argparse
│     [I] json
│     ----------------------------------------
│     [V] gstrParsePath = ''
│     [V] gaSavedBlocks = ...
│     ----------------------------------------
│     [F] add_block(file_path, imports, classes, functions, globals)
│     [F] get_function_signature(func_node, max_args)
│     [F] get_class_bases(class_node)
│     [F] extract_type_alias(value_node)
│     [F] analyze_file(file_path)
│     [F] analyze_directory(directory_path)
│     [F] save_output(output_path, format)
│     [F] main()
├── logs/
├── output-allfiles.txt (9260)
├── output-gen.html (17682)
├── output-gen.json (24238)
├── output-onefile.txt (1281)
└── pyfileviewer-s.py (19055) # 하나의 py파일을 분석하여, 포함된 클래스/함수/변수 목록을 콘솔화면에 출력하는 어플
       [I] ast
       [I] os
       [I] enum
       [I] argparse
       ----------------------------------------
       [V] MAX_VIEW_PARAMS = 6
       [V] MAX_VIEW_COMMENTS = 200
       [V] BIT_PART_IMPORT = 1
       [V] BIT_PART_TYPE = 2
       [V] BIT_PART_VAR = 4
       [V] BIT_PART_CLASS = 8
       [V] BIT_PART_FUNC = 16
       [V] BIT_PART_DEF = ...
       [V] BIT_PART_TV = ...
       [V] BIT_PART_ALL = 31
       [V] BIT_ITEM_NAME = 1
       [V] BIT_ITEM_INHERIT = 2
       [V] BIT_ITEM_PARAMS = 4
       [V] BIT_ITEM_COMMENTS = 8
       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
       [V] BIT_ITEM_DEF = ...
       [V] BIT_ITEM_ALL = 15
       [T] gnViewParts = BIT_PART_ALL
       [T] gnViewItems = BIT_ITEM_ALL
       ----------------------------------------
       [C] eViewStyles(enum.Enum) # 테스트용 나열형 클래스
       [C] CTestClass() # 테스트용 일반 클래스
         [F] __init__(self) # 생성자
         [F] __call__(self, *args, **kwds) # 호출자
         [F] __setvalues__(self, a, b) # 값 설정
         [F] __getvalues__(self) # 값 리턴
         [F] __sum__(self) # 덧셈
       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 반환
       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 반환 (최대 파라미터 제한)
       [F] get_function_signature_old(func_node) # 함수의 파라미터 목록을 문자열로 반환
       [F] get_docstring(node)
       [F] print_classes_funcs(node, indent)
       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
       [F] analyze_file(file_path) # py파일의 [PITVCF]를 분석하여, 콘솔화면에 출력
       [F] main()
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size
testing/
├── example.py # 정식 프로그램을 제작하기 전에, 여러가지 실험적인 코드를 연습하기 위한, 테스트용 어플
│     [I] ast
│     [I] os
│     [I] argparse
│     [I] json
│     ----------------------------------------
│     [V] gstrParsePath = ''
│     [V] gaSavedBlocks = ...
│     ----------------------------------------
│     [F] add_block(file_path, imports, classes, functions, globals)
│     [F] get_function_signature(func_node, max_args)
│     [F] get_class_bases(class_node)
│     [F] extract_type_alias(value_node)
│     [F] analyze_file(file_path)
│     [F] analyze_directory(directory_path)
│     [F] save_output(output_path, format)
│     [F] main()
├── logs/
├── output-allfiles.txt
├── output-gen.html
├── output-gen.json
├── output-onefile.txt
└── pyfileviewer-s.py # 하나의 py파일을 분석하여, 포함된 클래스/함수/변수 목록을 콘솔화면에 출력하는 어플
       [I] ast
       [I] os
       [I] enum
       [I] argparse
       ----------------------------------------
       [V] MAX_VIEW_PARAMS = 6
       [V] MAX_VIEW_COMMENTS = 200
       [V] BIT_PART_IMPORT = 1
       [V] BIT_PART_TYPE = 2
       [V] BIT_PART_VAR = 4
       [V] BIT_PART_CLASS = 8
       [V] BIT_PART_FUNC = 16
       [V] BIT_PART_DEF = ...
       [V] BIT_PART_TV = ...
       [V] BIT_PART_ALL = 31
       [V] BIT_ITEM_NAME = 1
       [V] BIT_ITEM_INHERIT = 2
       [V] BIT_ITEM_PARAMS = 4
       [V] BIT_ITEM_COMMENTS = 8
       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
       [V] BIT_ITEM_DEF = ...
       [V] BIT_ITEM_ALL = 15
       [T] gnViewParts = BIT_PART_ALL
       [T] gnViewItems = BIT_ITEM_ALL
       ----------------------------------------
       [C] eViewStyles(enum.Enum) # 테스트용 나열형 클래스
       [C] CTestClass() # 테스트용 일반 클래스
         [F] __init__(self) # 생성자
         [F] __call__(self, *args, **kwds) # 호출자
         [F] __setvalues__(self, a, b) # 값 설정
         [F] __getvalues__(self) # 값 리턴
         [F] __sum__(self) # 덧셈
       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 반환
       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 반환 (최대 파라미터 제한)
       [F] get_function_signature_old(func_node) # 함수의 파라미터 목록을 문자열로 반환
       [F] get_docstring(node)
       [F] print_classes_funcs(node, indent)
       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
       [F] analyze_file(file_path) # py파일의 [PITVCF]를 분석하여, 콘솔화면에 출력
       [F] main()
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size --hide-desc
testing/
├── example.py
│     [I] ast
│     [I] os
│     [I] argparse
│     [I] json
│     ----------------------------------------
│     [V] gstrParsePath = ''
│     [V] gaSavedBlocks = ...
│     ----------------------------------------
│     [F] add_block(file_path, imports, classes, functions, globals)
│     [F] get_function_signature(func_node, max_args)
│     [F] get_class_bases(class_node)
│     [F] extract_type_alias(value_node)
│     [F] analyze_file(file_path)
│     [F] analyze_directory(directory_path)
│     [F] save_output(output_path, format)
│     [F] main()
├── logs/
├── output-allfiles.txt
├── output-gen.html
├── output-gen.json
├── output-onefile.txt
└── pyfileviewer-s.py
       [I] ast
       [I] os
       [I] enum
       [I] argparse
       ----------------------------------------
       [V] MAX_VIEW_PARAMS = 6
       [V] MAX_VIEW_COMMENTS = 200
       [V] BIT_PART_IMPORT = 1
       [V] BIT_PART_TYPE = 2
       [V] BIT_PART_VAR = 4
       [V] BIT_PART_CLASS = 8
       [V] BIT_PART_FUNC = 16
       [V] BIT_PART_DEF = ...
       [V] BIT_PART_TV = ...
       [V] BIT_PART_ALL = 31
       [V] BIT_ITEM_NAME = 1
       [V] BIT_ITEM_INHERIT = 2
       [V] BIT_ITEM_PARAMS = 4
       [V] BIT_ITEM_COMMENTS = 8
       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
       [V] BIT_ITEM_DEF = ...
       [V] BIT_ITEM_ALL = 15
       [T] gnViewParts = BIT_PART_ALL
       [T] gnViewItems = BIT_ITEM_ALL
       ----------------------------------------
       [C] eViewStyles(enum.Enum) # 테스트용 나열형 클래스
       [C] CTestClass() # 테스트용 일반 클래스
         [F] __init__(self) # 생성자
         [F] __call__(self, *args, **kwds) # 호출자
         [F] __setvalues__(self, a, b) # 값 설정
         [F] __getvalues__(self) # 값 리턴
         [F] __sum__(self) # 덧셈
       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 반환
       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 반환 (최대 파라미터 제한)
       [F] get_function_signature_old(func_node) # 함수의 파라미터 목록을 문자열로 반환
       [F] get_docstring(node)
       [F] print_classes_funcs(node, indent)
       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
       [F] analyze_file(file_path) # py파일의 [PITVCF]를 분석하여, 콘솔화면에 출력
       [F] main()
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 코드분석 제외
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size --hide-desc --hide-codes
testing/
├── example.py
├── logs/
├── output-allfiles.txt
├── output-gen.html
├── output-gen.json
├── output-onefile.txt
└── pyfileviewer-s.py
```

#### 테스팅 프로젝트 구조 출력 > [hidden, pyc, md]파일 제외 + 깊이 제한 + 파일사이즈 숨김 + 설명 숨김 + 파일 저장
```
> python pyprojectviewer.py testing --hide-hidden --deny-ext=pyc,md --max-depth=0 --hide-size --hide-desc --savedfile=logs/output-ppv.txt
  콘솔화면과 저장파일내용 동일한지 확인
```


[패키지로 이동](../README.md#프로젝트별-사용법)<br/>
