# JK's Python 솔루션 구조 분석툴 (Package)

Python 솔루션 내에 여러 프로젝트들을 빠르게 분석하는데, 도움을 제공하기 위한 툴들을 개발하여 제공한다.

`PyFileViewer`툴이 존재하지만, 그 기능들은 `PyProjectViewer` 툴에도 내장되어 있기에 제외시켰다.


## 변경 이력
* [PyFolderViewer](PyFolderViewer/README.md#변경-이력)
* [PyProjectViewer](PyProjectViewer/README.md#변경-이력)


## 개발 목적

아래의 [솔루션 파일 구성](#솔루션-파일-구성) 항목과 같이,
  * PyFolderViewer 툴로, `솔루션(프로젝트들)`의 파일 구성과 설명을 추출하여 표출하고,

아래의 [Python 코드 분석](#python-코드-분석) 항목과 같이,
  * PyProjectViewer 툴로, py파일마다 코드를 분석하여, 그 정보들(클래스/함수/변수)을 트리 형태의 시각화로,

운영자에게는 빠른 분석 보고서 작성을, 개발자에게는 구조 분석에 편리함을 제공하기 위함이다.


### 솔루션 파일 구성
```
> python PyFolderViewer\pyfolderviewer.py . --hide-size --hide-hidden
./
├── LICENSE
├── PyFolderViewer/
│   ├── README.md # JK's 폴더의 파일구성 분석툴
│   └── pyfolderviewer.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
├── PyProjectViewer/
│   ├── README.md # JK's 프로젝트 구조 분석툴
│   └── pyprojectviewer.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
└── README.md # JK's Python 솔루션 구조 분석툴 (Package)
```

### Python 코드 분석
```
> python PyProjectViewer\pyprojectviewer.py . --hide-size --hide-hidden
./
├── LICENSE
├── PyFolderViewer/
│   ├── README.md # JK's 폴더의 파일구성 분석툴
│   └── pyfolderviewer.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
│       [I] os
│       [I] ast
│       [I] re
│       [I] argparse
│       ----------------------------------------
│       [V] gobjSavedFile = None
│       [V] gaDenyNames = None
│       [V] gaPassNames = None
│       [V] gaDenyExts = None
│       [V] gaPassExts = None
│       [V] gnMaxDepth = 3
│       [V] gbHideDesc = False
│       [V] gbHideSize = False
│       [V] gbHideHidden = False
│       ----------------------------------------
│       [F] extract_docstring(file_path) # py파일의 첫 번째 docstring을 추출하여 리턴
│       [F] extract_md_title(file_path) # md파일의 첫 번째 제목(#로 시작하는 라인)을 추출하여 리턴
│       [F] print_and_save(line) # 문장을 콘솔화면에 출력하면서, 지정한 파일에도 저장
│       [F] print_tree(root_path, prefix, depth) # [재귀호출] 지정 경로의 트리 구조를 루프하며, 분석정보 출력
│       [F] convert_str2list(comma_string)
│       [F] main() # 메인 엔트리 : 콘솔옵션 설정/파싱 > 전역변수 설정 > 경로 파일들 루프/분석/출력
├── PyProjectViewer/
│   ├── README.md # JK's 프로젝트 구조 분석툴
│   └── pyprojectviewer.py # 지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)
│       [I] os
│       [I] ast
│       [I] argparse
│       [I] re
│       ----------------------------------------
│       [V] MAX_VIEW_PARAMS = 6
│       [V] MAX_VIEW_COMMENTS = 200
│       [V] BIT_PART_IMPORT = 1
│       [V] BIT_PART_TYPE = 2
│       [V] BIT_PART_VAR = 4
│       [V] BIT_PART_CLASS = 8
│       [V] BIT_PART_FUNC = 16
│       [V] BIT_PART_DEF = ...
│       [V] BIT_PART_TV = ...
│       [V] BIT_PART_ALL = 31
│       [V] BIT_ITEM_NAME = 1
│       [V] BIT_ITEM_INHERIT = 2
│       [V] BIT_ITEM_PARAMS = 4
│       [V] BIT_ITEM_COMMENTS = 8
│       [T] BIT_ITEM_MIN = BIT_ITEM_NAME
│       [V] BIT_ITEM_DEF = ...
│       [V] BIT_ITEM_ALL = 15
│       [V] gobjSavedFile = None
│       [V] gaDenyNames = None
│       [V] gaPassNames = None
│       [V] gaDenyExts = None
│       [V] gaPassExts = None
│       [V] gnMaxDepth = 3
│       [V] gbHideDesc = False
│       [V] gbHideSize = False
│       [V] gbHideHidden = False
│       [V] gbHideCodes = False
│       [T] gnViewParts = BIT_PART_ALL
│       [T] gnViewItems = BIT_ITEM_ALL
│       [V] gaSaveLines = ...
│       ----------------------------------------
│       [F] extract_docstring(file_path) # py파일의 첫 번째 docstring을 추출하여 리턴
│       [F] extract_md_title(file_path) # md파일의 첫 번째 제목(#로 시작하는 라인)을 추출하여 리턴
│       [F] print_and_save(line) # 문장을 콘솔화면에 출력하면서, 지정한 파일에도 저장
│       [F] print_buffer(prefix, screenconn, fileconn) # 코드검출저장버퍼를 콘솔화면에 출력하면서, 지정한 파일에도 저장
│       [F] analyze_folder(root_path, prefix, depth) # [재귀호출] 지정 경로의 트리 구조를 루프하며, 분석정보 출력
│       [F] write(line) # 문자열을 코드검출저장버퍼에 추가
│       [F] print_imports(tree) # 임포트된 모듈 및 패키지 목록 출력
│       [F] get_class_bases(class_node) # 클래스의 부모클래스 명칭 목록을 문자열로 리턴
│       [F] get_function_signature(func_node, max_args) # 함수의 파라미터 목록을 문자열로 리턴 (최대 파라미터 제한)
│       [F] get_docstring(node) # 클래스/함수 노드의 docstring을 추출하여 리턴
│       [F] print_classes_funcs(node, indent) # [재귀호출] 단일 py파일의 AST구조를 루프하며, (클래스/함수) 분석정보를 버퍼에 추가
│       [F] extract_type_alias(value_node) # 사용자정의타입 표현식을 문자열로 변환
│       [F] print_global_definitions(tree) # 전역변수 및 사용자정의타입 출력
│       [F] analyze_file(file_path, prefix, connector, info, screenconn, fileconn) # 지정 py파일의 AST구조를 분석하여, 설명과 PITVCF 출력
│       [F] convert_str2list(comma_string)
│       [F] main() # 메인 엔트리 : 콘솔옵션 설정/파싱 > 전역변수 설정 > 경로 파일들 루프/분석/출력
└── README.md # JK's Python 솔루션 구조 분석툴 (Package)
```


## 프로젝트별 사용법
* [PyFolderViewer](PyFolderViewer/README.md#사용법)
* [PyProjectViewer](PyProjectViewer/README.md#사용법)
