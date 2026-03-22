# pyprojectviewer.py
# Copyright (c) 2025 Choi Joonkyu
"""지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)"""
# ------------------------------------------------------------------------------
# 구현 정보
# ------------------------------------------------------------------------------
# - 역할
#   지정 경로(하위 폴더 포함)의 모든 파일들을 트리 형태로 시각화하고,
#   소스코드 파일은 내부의 클래스/함수/변수를 추출하여, 콘솔화면이나 파일에 출력한다.
# ------------------------------------------------------------------------------
# [IMPORT]
# ------------------------------------------------------------------------------
# [외부] 모듈
# --------------------------------------
import os         # 운영체제 (파일/폴더/경로 제어용)
import ast        # 추상구문트리 (py파일 분석용)

import argparse   # 콘솔옵션 파서
import re         # 정규표현식 (md파일 분석용)
# ------------------------------------------------------------------------------
# [DEFINES]
# ------------------------------------------------------------------------------
# [TYPES]
# --------------------------------------

# --------------------------------------
# [CONSTANTS]
# --------------------------------------
# 임계값 속성
# ------------------
MAX_VIEW_PARAMS   = 6   # 함수파라미터 최대 출력수
MAX_VIEW_COMMENTS = 200 # 주석 최대 출력수
# ------------------
# 비트 속성
# ------------------
# 출력 부분
# --------
BIT_PART_IMPORT   = 0x01  # 임포트모듈
BIT_PART_TYPE     = 0x02  # 사용자정의타입
BIT_PART_VAR      = 0x04  # 전역변수
BIT_PART_CLASS    = 0x08  # 클래스
BIT_PART_FUNC     = 0x10  # 함수
# 조합
BIT_PART_DEF      = (BIT_PART_CLASS | BIT_PART_FUNC)  # 기본값
BIT_PART_TV       = (BIT_PART_TYPE | BIT_PART_VAR)    # 타입/변수
BIT_PART_ALL      = 0x1F  # 전체
# --------
# 출력 항목
# --------
BIT_ITEM_NAME     = 0x01  # 명칭
BIT_ITEM_INHERIT  = 0x02  # 클래스상속
BIT_ITEM_PARAMS   = 0x04  # 함수파라미터
BIT_ITEM_COMMENTS = 0x08  # 주석
# 조합
BIT_ITEM_MIN      = BIT_ITEM_NAME  # 최소값 (명칭만)
BIT_ITEM_DEF      = (BIT_ITEM_NAME | BIT_ITEM_INHERIT | BIT_ITEM_PARAMS)  # 기본값
BIT_ITEM_ALL      = 0x0F  # 전체
# ------------------------------------------------------------------------------
# [VARIABLES]
# ------------------------------------------------------------------------------
# 파일검출
# ------------------
gobjSavedFile = None    # 저장파일 객체
# [JKC:20251019-0810] 기능 추가
gaDenyNames   = None    # 거부파일명칭목록
gaPassNames   = None    # 허용파일명칭목록
gaDenyExts    = None    # 거부확장자목록
gaPassExts    = None    # 허용확장자목록
# [JKC:20260322-1820] 기능 추가
gaDenyDirs    = None    # 거부폴더명칭목록
gaPassDirs    = None    # 허용폴더명칭목록

gnMaxDepth    = 3       # 최대 깊이
gbHideDesc    = False   # 파일설명 숨김
gbHideSize    = False   # 파일사이즈 숨김
gbHideHidden  = False   # 숨김파일/폴더 숨김
# ------------------
# 코드검출
# ------------------
gbHideCodes   = False   # 코드분석 숨김
gnViewParts   = BIT_PART_ALL  # 출력 부분
gnViewItems   = BIT_ITEM_ALL  # 출력 항목

gaSaveLines   = []            # 코드검출저장 버퍼
# ------------------------------------------------------------------------------
# [FUNCTIONS]
# ------------------------------------------------------------------------------
# ==============================================================================================================================================================
# [파일검출] 관련
# ==============================================================================================================================================================
# 해당 py파일의 첫 번째 docstring을 추출하여 리턴한다.
# --------------------------------------
def extract_docstring(file_path):
  """py파일의 첫 번째 docstring을 추출하여 리턴"""
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      source = f.read()
    tree = ast.parse(source)
    docstring = ast.get_docstring(tree)
    if docstring:
      # 첫 행만 출력 (너무 길면 잘림)
      return docstring.strip().split('\n')[0]
  except Exception:
    pass
  return None
# --------------------------------------
# 해당 md파일의 첫 번째 제목(#로 시작하는 라인)을 추출하여 리턴한다.
# --------------------------------------
def extract_md_title(file_path):
  """md파일의 첫 번째 제목(#로 시작하는 라인)을 추출하여 리턴"""
  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      for line in f:
        match = re.match(r'^\s*#{1,6}\s+(.*)', line)
        if match:
          return match.group(1).strip()
  except Exception:
    pass
  return None
# --------------------------------------
# 해당 문장을 콘솔화면에 출력하면서, 지정한 파일에도 저장한다.
# --------------------------------------
def print_and_save(line):
  """문장을 콘솔화면에 출력하면서, 지정한 파일에도 저장"""
  print(line)
  if gobjSavedFile:
    try:
      gobjSavedFile.write(line + '\n')
    except Exception:
      pass
# --------------------------------------
# 해당 코드검출저장버퍼를 콘솔화면에 출력하면서, 지정한 파일에도 저장한다.
# --------------------------------------
def print_buffer(prefix='', screenconn='', fileconn=''):
  """코드검출저장버퍼를 콘솔화면에 출력하면서, 지정한 파일에도 저장"""
  if len(gaSaveLines) > 0:
    # ------------------
    # 콘솔 출력
    # ------------------
    for line in gaSaveLines:
      print(f"{prefix}{screenconn}{line}")
    # ------------------
    # 파일 저장
    # ------------------
    if gobjSavedFile:
      try:
        for line in gaSaveLines:
          gobjSavedFile.write(f"{prefix}{fileconn}{line}\n")
      except Exception:
        pass
    # ------------------
    # 버퍼 초기화
    # ------------------
    gaSaveLines.clear()
# --------------------------------------
# [재귀호출] 해당 경로의 트리 구조를 루프하며, 분석정보 출력한다.
# --------------------------------------
def analyze_folder(root_path, prefix='', depth=0):
  """[재귀호출] 지정 경로의 트리 구조를 루프하며, 분석정보 출력"""
  # 최대깊이 제한 체크
  if depth > gnMaxDepth:
    return
  # 디렉토리 내 요소들 추출
  try:
    entries = sorted(os.listdir(root_path))
  except Exception:
    return
  # 숨김파일/폴더 제외 (윈도우는 숨김속성 체크가 복잡하여, 이름이 '.'로 시작하는 파일만 제외)
  if gbHideHidden:
      entries = [e for e in entries if not e.startswith('.')]
  entries_count = len(entries)
  # ------------------
  # 각 요소별 처리
  # ------------------
  for i, entry in enumerate(entries):
    full_path = os.path.join(root_path, entry)
    if i == entries_count - 1:
      # 파일검출 출력용
      connector = '└── '
      # 코드검출 출력용
      screenconn= '    '
      fileconn  = '       '
    else:
      # 파일검출 출력용
      connector = '├── '
      # 코드검출 출력용
      screenconn= '│   '
      fileconn  = '│     '
    # --------------------------------------
    # 파일
    # --------------------------------------
    if os.path.isfile(full_path):
      # [JKC:20251019-0810] 기능 추가
      name, ext = os.path.splitext(entry)
      name = name.lower()
      ext  = ext[1:].lower()
      # ------------------
      # 파일명칭 필터링
      # ------------------
      # [JKC:20260322-1840] 버그 패치
      # gaPassNames 배열의 요소가 name에 포함되지 않으면 continue
      if gaPassNames and not any(pass_name in name for pass_name in gaPassNames):
        continue
      # gaDenyNames 배열의 요소가 name에 포함되어 있다면 continue
      if gaDenyNames and any(deny_name in name for deny_name in gaDenyNames):
        continue
      # ------------------
      # 확장자 필터링
      # ------------------
      if gaPassExts and ext not in gaPassExts:
        continue
      # [JKC:20251019-0810] 코드 변경 (허용되었더라도 거부를 체크하도록 처리)
      if gaDenyExts and ext in gaDenyExts:
        continue
      # ------------------
      # 파일사이즈 추출
      # ------------------
      if not gbHideSize:
        size = os.path.getsize(full_path)
        info = f"{entry} ({size})"
      else:
        info = f"{entry}"
      # ------------------
      # 파일별 내용 추출/출력
      # ------------------
      # py파일이면, 상세 분석/출력
      if entry.endswith('.py'):
        analyze_file(full_path, prefix, connector, info, screenconn, fileconn)
      # 타이틀 출력
      elif not gbHideDesc:
        # md파일이면, 타이틀 추출/출력
        if entry.endswith('.md'):
          # 첫 번째 title 추출
          title = extract_md_title(full_path)
          if title:
            info += f' # {title}'
          print_and_save(f"{prefix}{connector}{info}")
        # 기타
        else:
          print_and_save(f"{prefix}{connector}{info}")
      # 타이틀 없이 출력
      else:
        print_and_save(f"{prefix}{connector}{info}")
    # --------------------------------------
    # 폴더
    # --------------------------------------
    elif os.path.isdir(full_path):
      # ------------------
      # [JKC:20260322-1820] 폴더명칭 필터링
      # ------------------
      low_path = full_path.lower()
      # gaPassDirs 배열의 요소가 dir에 포함되지 않으면 continue
      if gaPassDirs and not any(pass_dir in low_path for pass_dir in gaPassDirs):
        continue
      # gaDenyDirs 배열의 요소가 dir에 포함되어 있다면 continue
      if gaDenyDirs and any(deny_dir in low_path for deny_dir in gaDenyDirs):
        continue
      # ------------------
      print_and_save(f"{prefix}{connector}{entry}/")
      extension = '    ' if i == entries_count - 1 else '│   '
      analyze_folder(full_path, prefix + extension, depth + 1)
# ==============================================================================================================================================================
# [코드검출] 관련
# ==============================================================================================================================================================
# 해당 문자열을 코드검출저장버퍼(gaSaveLines)에 추가한다.
# --------------------------------------
def write(line=""):
  """문자열을 코드검출저장버퍼에 추가"""
  gaSaveLines.append(line)
# --------------------------------------
# 임포트된 모듈 및 패키지 목록을 리턴한다.
# --------------------------------------
def print_imports(tree):
  """임포트된 모듈 및 패키지 목록 출력"""
  if (gnViewParts & BIT_PART_IMPORT) == 0:
    return
  count = 0
  for node in tree.body:
    if isinstance(node, ast.Import):
      for alias in node.names:
        name    = alias.name
        write(f"[I] {name}")
        count += 1
    elif isinstance(node, ast.ImportFrom):
      package = node.module or ""
      for alias in node.names:
        name    = alias.name
        write(f"[P] {package} [I] {name}")
        count += 1
  if count > 0:
    write("----------------------------------------")
# --------------------------------------
# 해당 클래스의 부모클래스 목록을 문자열로 제작하여 리턴한다.
# --------------------------------------
def get_class_bases(class_node):
  """클래스의 부모클래스 명칭 목록을 문자열로 리턴"""
  bases = []
  for base in class_node.bases:
    if isinstance(base, ast.Name):
      bases.append(base.id)
    elif isinstance(base, ast.Attribute):
      # 예: module.BaseClass
      value = base.value.id if isinstance(base.value, ast.Name) else "?"
      bases.append(f"{value}.{base.attr}")
    else:
      bases.append("?")
  return ", ".join(bases) if bases else "object"
# --------------------------------------
# 해당 함수의 파라미터목록 문자열을 제작하여 리턴한다.
# --------------------------------------
def get_function_signature(func_node, max_args=MAX_VIEW_PARAMS):
  """함수의 파라미터 목록을 문자열로 리턴 (최대 파라미터 제한)"""
  args = []
  # 위치 인자들 (추가)
  for arg in func_node.args.args:
    args.append(arg.arg)
  # 키워드 인자들 (추가)
  for kwarg in func_node.args.kwonlyargs:
    args.append(f"{kwarg.arg}=")
  # *args, **kwargs (추가)
  if func_node.args.vararg:
    args.append(f"*{func_node.args.vararg.arg}")
  if func_node.args.kwarg:
    args.append(f"**{func_node.args.kwarg.arg}")
  # 초과 시, 생략 처리
  if len(args) > max_args:
    args = args[:max_args] + ["..."]
  return ", ".join(args)
# --------------------------------------
# 해당 [클래스/함수]의 docstring을 추출하여 리턴한다.
# --------------------------------------
def get_docstring(node):
  """클래스/함수 노드의 docstring을 추출하여 리턴"""
  doc = ast.get_docstring(node)
  if doc:
  # doc = doc.strip().replace("\n", " ")
    doc = doc.strip().splitlines()[0]
    if len(doc) > MAX_VIEW_COMMENTS:
        doc = doc[:(MAX_VIEW_COMMENTS-3)] + "..."
  else:
    doc = ""
  return doc
# --------------------------------------
# [재귀호출] 해당 py파일 AST노드를 루프하며, [CF] 들여쓰기 분석정보를 버퍼에 추가한다.
# --------------------------------------
def print_classes_funcs(node, indent=0):
  """[재귀호출] 단일 py파일의 AST구조를 루프하며, (클래스/함수) 분석정보를 버퍼에 추가"""
  # ------------------
  # [들여쓰기] 문자열 제작
  # ------------------
  prefix = "  " * indent
# prefix = "│   " * indent + "├── "
  # ------------------
  # [클래스/함수] 내용 출력
  # ------------------
  # 클래스
  # --------
  if (gnViewParts & BIT_PART_CLASS) and isinstance(node, ast.ClassDef):
    docstring = get_docstring(node) if (gnViewItems & BIT_ITEM_COMMENTS) else ""
    # 상속 출력
    if gnViewItems & BIT_ITEM_INHERIT:
      base_names = get_class_bases(node)        # 해당 클래스의 부모클래스 목록을 문자열로 제작하여 리턴한다.
      if base_names == "object":
        base_names = ""
      if len(docstring) > 1:
        write(f"{prefix}[C] {node.name}({base_names}) # {docstring}")
      else:
        write(f"{prefix}[C] {node.name}({base_names})")
    # 명칭만 출력
    elif gnViewItems == BIT_ITEM_NAME:
      if len(docstring) > 1:
        write(f"{prefix}[C] {node.name} # {docstring}")
      else:
        write(f"{prefix}[C] {node.name}")
    # 기본 출력
    else:
      if len(docstring) > 1:
        write(f"{prefix}[C] {node.name}() # {docstring}")
      else:
        write(f"{prefix}[C] {node.name}()")
  # --------
  # 함수
  # --------
  elif (gnViewParts & BIT_PART_FUNC) and isinstance(node, ast.FunctionDef):
    docstring = get_docstring(node) if (gnViewItems & BIT_ITEM_COMMENTS) else ""
    # 명칭만 출력
    if gnViewItems == BIT_ITEM_NAME:
      if len(docstring) > 1:
        write(f"{prefix}[F] {node.name} # {docstring}")
      else:
        write(f"{prefix}[F] {node.name}")
    # 파라미터 생략 출력
    elif (gnViewItems & BIT_ITEM_PARAMS == 0):
      if len(docstring) > 1:
        write(f"{prefix}[F] {node.name}() # {docstring}")
      else:
        write(f"{prefix}[F] {node.name}()")
    # 파라미터 포함 출력
    else:
      signature = get_function_signature(node)  # 해당 함수의 파라미터목록 문자열을 제작하여 리턴한다.
      if len(docstring) > 1:
        write(f"{prefix}[F] {node.name}({signature}) # {docstring}")
      else:
        write(f"{prefix}[F] {node.name}({signature})")
  # ------------------
  # [재귀호출] 다음 요소, 들여쓰기 적용시켜 호출
  # ------------------
  for child in ast.iter_child_nodes(node):
    # 클래스 내부 함수만, 들여쓰기 증가
    if isinstance(node, ast.ClassDef) and isinstance(child, ast.FunctionDef):
      if gnViewParts & BIT_PART_CLASS:
        print_classes_funcs(child, indent + 1)
    # 전역 함수
    elif isinstance(child, (ast.ClassDef, ast.FunctionDef)):
      print_classes_funcs(child, indent)
# --------------------------------------
# 사용자정의타입 표현식을 문자열로 변환하여 리턴한다.
# --------------------------------------
def extract_type_alias(value_node):
  """사용자정의타입 표현식을 문자열로 변환"""
  if isinstance(value_node, ast.Name):
    return value_node.id
  elif isinstance(value_node, ast.Subscript):
    root = extract_type_alias(value_node.value)
    sub  = extract_type_alias(value_node.slice)
    return f"{root}[{sub}]"
  elif isinstance(value_node, ast.Tuple):
    return ", ".join(extract_type_alias(elt) for elt in value_node.elts)
  elif isinstance(value_node, ast.Attribute):
    return f"{extract_type_alias(value_node.value)}.{value_node.attr}"
  elif isinstance(value_node, ast.Constant):
    return repr(value_node.value)
  # TypeVar(...) 함수호출 형태가 출력되도록...
  elif isinstance(value_node, ast.Call):
    func_name = extract_type_alias(value_node.func)
    args      =[extract_type_alias(arg) for arg in value_node.args]
    keywords  = [f"{kw.arg}={extract_type_alias(kw.value)}" for kw in value_node.keywords]
    all_args  = args + keywords
    return f"{func_name}({', '.join(all_args)})"
  else:
    return "..."
# --------------------------------------
# 전역변수 및 사용자정의타입 출력
# --------------------------------------
def print_global_definitions(tree):
  """전역변수 및 사용자정의타입 출력"""
  if (gnViewParts & BIT_PART_TV) == 0:
    return
  count = 0
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name):
          var_name  = target.id
          value     = node.value
          # [JKC:20251016-0530] 버그 해결 : 출력거부 체크하여, 카운팅 하도록 처리
          denied    = False
          # ------------------
          # 1. [V] 상수 출력
          if (gnViewParts & BIT_PART_VAR) and isinstance(value, ast.Constant):
            write(f"[V] {var_name} = {repr(value.value)}")
          # 2. [V] 튜플 처리
          elif (gnViewParts & BIT_PART_VAR) and isinstance(value, ast.Tuple):
            # 복잡 튜플 생략 : 요소가 많거나, 상수가 아닌 요소가 포함된 경우
            if len(value.elts) > MAX_VIEW_PARAMS or any(not isinstance(elt, ast.Constant) for elt in value.elts):
              write(f"[V] {var_name} = ...")
            # 간단 튜플 출력 : 적당한 요소 수량에, 모두 상수인 경우
            else:
              values = ", ".join(repr(elt.value) for elt in value.elts)
            # values = ", ".join(repr(elt.value) for elt in value.elts if isinstance(elt, ast.Constant))
              write(f"[V] {var_name} = ({values})")
          # 3. [V] 실수 출력
          elif (gnViewParts & BIT_PART_VAR) and isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub) and isinstance(value.operand, ast.Constant):
            write(f"[V] {var_name} = -{repr(value.operand.value)}")
          # 4. [T] 사용자정의타입 추정
          # [JKC:20251016-0530] 버그 해결 : 타입의 출력 여부는 내부에서 처리하도록 변경
          elif isinstance(value, (ast.Name, ast.Subscript, ast.Attribute, ast.Call)):
            if gnViewParts & BIT_PART_TYPE:
              type_str = extract_type_alias(value)
              write(f"[T] {var_name} = {type_str}")
            else:
              denied = True
          # 5. [V] 기타 생략
          elif (gnViewParts & BIT_PART_VAR):
            write(f"[V] {var_name} = ...")
          else:
            denied = True
          # ------------------
          if not denied:
            count += 1
  if count > 0:
    write("----------------------------------------")
# --------------------------------------
# 해당 py파일의 AST구조를 분석하여, 설명과 PITVCF를 출력한다.
# --------------------------------------
def analyze_file(file_path, prefix='', connector='', info='', screenconn='', fileconn=''):
  """지정 py파일의 AST구조를 분석하여, 설명과 PITVCF 출력"""
  # [JKC:20260322-1740] 파일데이터 인코딩 능동 대처
  # 파일 열기/로드
  source    = None
  encodings = ['utf-8', 'cp949', 'euc-kr']  # 인코딩 목록 (가장 범용적인 순서)
  for enc in encodings:
    try:
      with open(file_path, 'r', encoding=enc) as f:
        source = f.read()
      # 성공적으로 로드하여 루프 탈출
      break
    except UnicodeDecodeError:
      continue
  # 모든 인코딩이 실패했을 경우의 최후 수단 (오류 무시하고 로드)
  if source is None:
    try:
      with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        source = f.read()
      print(f"[wrn] 파일데이터 인코딩 문제로 손실 발생: {file_path}")
    except Exception as e:
      print(f"[err] 파일데이터 로드 오류: {e}")
      return
  # 코드 분석/보관
  try:
    # ------------------
    # 파일내용 AST구조로 변환
    # ------------------
    codestree = ast.parse(source)
    # ------------------
    # 파일 설명 (바로 출력)
    # ------------------
    if not gbHideDesc:
      # 첫 번째 docstring 추출
      docstring = ast.get_docstring(codestree)
      if docstring:
        # 첫 행만 출력 (너무 길면 잘림)
        docstring = docstring.strip().split('\n')[0]
        info += f" # {docstring}"
    print_and_save(f"{prefix}{connector}{info}")
    # ------------------
    # 코드 분석 (보관/출력)
    # ------------------
    if not gbHideCodes:
      # ------------------
      # 코드 분석 (보관)
      # ------------------
      print_imports(codestree)             # PI (패키지/모듈 임포트)
      print_global_definitions(codestree)  # TV (타입/전역변수)
      print_classes_funcs(codestree)       # CF (클래스/함수)
      # ------------------
      # 분석 결과 (출력/저장)
      # ------------------
      print_buffer(prefix, screenconn, fileconn)
  except SyntaxError as e:
    print(f"[err] 구문 오류 발생: {e}")
  except Exception as e:
    print(f"[err] 예외 발생: {e}")
# ==============================================================================================================================================================
# [메인실행] 관련
# ==============================================================================================================================================================
# 해당 목록 문자열을 배열로 전환하여 리턴한다.(유효하지 않으면 None 리턴)
# --------------------------------------
# [JKC:20251019-1030] 파일명칭 특수문자 허용
def convert_str2list(comma_string):
  if not comma_string:
    return []
  result = [cur.strip().lower() for cur in comma_string.split(',') if cur.strip()]
  for cur in result:
    # 허용 문자: 영문 소문자, 숫자, -, _, ., (, ), [, ], ~
    if not re.match(r'^[a-z0-9.()\-\_\[\]~]+$', cur):
      return None
  return result
# --------------------------------------
# 메인 엔트리
# --------------------------------------
def main():
  """메인 엔트리 : 콘솔옵션 설정/파싱 > 전역변수 설정 > 경로 파일들 루프/분석/출력"""
  # ------------------
  # 전역변수 사용 선언
  # ------------------
  global gobjSavedFile, gaDenyDirs, gaPassDirs, gaDenyNames, gaPassNames, gaDenyExts, gaPassExts, gnMaxDepth, gbHideDesc, gbHideSize, gbHideHidden, gbHideCodes, gnViewParts, gnViewItems
  # ------------------
  # 콘솔옵션/사용법 설정
  # ------------------
  parser = argparse.ArgumentParser(
    description="프로젝트 구조 분석툴 (파일검출: 폴더명/파일명/확장자 필터링 + 깊이 제한 + 파일설명 + 파일사이즈 + 숨김파일 + 코드분석 제어, 코드검출: 출력부분 + 출력항목 비트제어, 결과출력: 콘솔+파일)",
    usage=("python pyprojectviewer.py <parsepath> [--savedfile=경로]\n"
           "                        [--deny-dir=d1,d2] [--pass-dir=d1,d2]\n"
           "                        [--deny-name=n1,n2] [--pass-name=n1,n2]\n"
           "                        [--deny-ext=ext1,ext2] [--pass-ext=ext1,ext2]\n"
           "                        [--max-depth=N] [--hide-desc] [--hide-size] [--hide-hidden]\n"
           "                        [--hide-codes] [--viewparts=16진수] [--viewitems=16진수]"),
    formatter_class=argparse.RawTextHelpFormatter  # 줄바꿈 유지
  )
  parser.add_argument("parsepath"     , help="분석 디렉토리 경로")
  # --------
  # 파일검출
  # --------
  parser.add_argument("--savedfile"   , help="분석결과 저장파일 경로", default="")
  # [JKC:20260322-1820] 기능 추가
  parser.add_argument("--deny-dir"    , help="제외할 폴더명칭 목록 (예: bin,obj)", default="")
  parser.add_argument("--pass-dir"    , help="허용할 폴더명칭 목록 (예: bin,obj)", default="")
  # [JKC:20251019-0810] 기능 추가
  parser.add_argument("--deny-name"   , help="제외할 파일명칭 목록 (예: _test,log_)", default="")
  parser.add_argument("--pass-name"   , help="허용할 파일명칭 목록 (예: _test,log_)", default="")
  
  parser.add_argument("--deny-ext"    , help="제외할 파일 확장자 목록 (예: pyc,md)", default="")
  parser.add_argument("--pass-ext"    , help="허용할 파일 확장자 목록 (예: py,txt)", default="")
  parser.add_argument("--max-depth"   , help="출력할 최대 디렉토리 깊이 (예: 2)", type=int, default=None)
  parser.add_argument("--hide-desc"   , help="파일설명 숨김", action="store_true")
  parser.add_argument("--hide-size"   , help="파일사이즈 숨김", action="store_true")
  parser.add_argument("--hide-hidden" , help="숨김파일 숨김", action="store_true")
  parser.add_argument("--hide-codes"  , help="코드분석 숨김", action="store_true")
  # --------
  # 코드검출
  # --------
  parser.add_argument("--viewparts"   , type=str,
                      help=(
                        "출력부분 : 16진수 비트조합 (예: 0x1F)\n"
                        "  0x01  # 임포트모듈\n"
                        "  0x02  # 사용자정의타입\n"
                        "  0x04  # 전역변수\n"
                        "  0x08  # 클래스\n"
                        "  0x10  # 함수"
                      ))
  parser.add_argument("--viewitems"   , type=str,
                      help=(
                        "출력항목 : 16진수 비트조합 (예: 0x0F)\n"
                        "  0x01  # 명칭\n"
                        "  0x02  # 클래스상속\n"
                        "  0x04  # 함수파라미터\n"
                        "  0x08  # 주석"
                      ))
  # ------------------
  # 콘솔옵션 파싱
  # ------------------
  args = parser.parse_args()
  # 탐색 경로 유효성 체크
  if not os.path.exists(args.parsepath):
    print(f"[err] 경로가 존재하지 않습니다: {args.parsepath}")
    parser.print_usage()
    return
  # 저장파일 오픈
  if args.savedfile:
    try:
      os.makedirs(os.path.dirname(args.savedfile), exist_ok=True)
      gobjSavedFile = open(args.savedfile, 'w', encoding='utf-8')
    except Exception as e:
      print(f"[err] 저장파일 열기 실패: {e}")
      return
  # [JKC:20260322-1820] 기능 추가
  # --------
  # 폴더명칭목록
  # --------
  # 문자열을 배열로 전환
  gaDenyDirs = convert_str2list(args.deny_dir)
  gaPassDirs = convert_str2list(args.pass_dir)
  # 유효성 체크
  if gaDenyDirs is None or gaPassDirs is None:
    print("[err] 폴더명칭 목록 형식이 잘못되었습니다. 쉼표로 구분된 영문 확장자만 입력하세요.")
    parser.print_usage()
    return
  # [JKC:20251019-0810] 기능 추가
  # --------
  # 파일명칭목록
  # --------
  # 문자열을 배열로 전환
  gaDenyNames = convert_str2list(args.deny_name)
  gaPassNames = convert_str2list(args.pass_name)
  # 유효성 체크
  if gaDenyNames is None or gaPassNames is None:
    print("[err] 파일명칭 목록 형식이 잘못되었습니다. 쉼표로 구분된 영문 확장자만 입력하세요.")
    parser.print_usage()
    return
  # --------
  # 확장자목록
  # --------
  # 문자열을 배열로 전환
  gaDenyExts  = convert_str2list(args.deny_ext)
  gaPassExts  = convert_str2list(args.pass_ext)
  # 유효성 체크
  if gaDenyExts is None or gaPassExts is None:
    print("[err] 확장자 목록 형식이 잘못되었습니다. 쉼표로 구분된 영문 확장자만 입력하세요.")
    parser.print_usage()
    return
  # --------
  # 최대깊이 유효성 체크
  if args.max_depth is not None:
    if args.max_depth < 0:
      print("[err] --max-depth 값은 0 이상의 정수여야 합니다.")
      parser.print_usage()
      return
    # 전역변수에 적용
    gnMaxDepth = args.max_depth
  # 파일설명 숨김
  gbHideDesc  = args.hide_desc
  # 코드분석 숨김
  gbHideCodes = args.hide_codes
  # 파일사이즈 숨김
  gbHideSize  = args.hide_size
  # 숨김파일 숨김
  gbHideHidden= args.hide_hidden
  # ------------------
  # 출력부분 설정
  # ------------------
  if args.viewparts:
    try:
      # 16진수 변환
      lnViewParts = int(args.viewparts, 16)
      if lnViewParts < 0 or lnViewParts > 0x1F:
        print(f"[err] 출력부분(--viewparts) 옵션은 0x00 ~ 0x1F 사이여야 합니다: {args.viewparts}")
        parser.print_usage()
        return
      # 전역변수에 적용
      gnViewParts = lnViewParts
    except ValueError:
      print(f"[err] 출력부분(--viewparts) 옵션은 16진수여야 합니다: {args.viewparts}")
      parser.print_usage()
      return
  # ------------------
  # 출력항목 설정
  # ------------------
  if args.viewitems:
    try:
      # 16진수 변환
      lnViewItems = int(args.viewitems, 16)
      if lnViewItems < 0 or lnViewItems > 0x0F:
        print(f"[err] 출력항목(--viewitems) 옵션은 0x00 ~ 0x0F 사이여야 합니다: {args.viewitems}")
        parser.print_usage()
        return
      # 전역변수에 적용
      gnViewItems = lnViewItems
    except ValueError:
      print(f"[err] 출력항목(--viewitems) 옵션은 16진수여야 합니다: {args.viewitems}")
      parser.print_usage()
      return
  # ------------------
  # 분석/출력+저장
  # ------------------
  print_and_save(f"{args.parsepath}/")
  analyze_folder(args.parsepath, depth=0)
# ------------------------------------------------------------------------------
# [EXECUTE-CODES] 직접 실행 시, 수행 코드
# ------------------------------------------------------------------------------
# linux
# ------------------
# > python pyprojectviewer.py -h
#   python pyprojectviewer.py .
#   python pyprojectviewer.py . --savedfile=./output-ppv.txt
#   python pyprojectviewer.py . --hide-codes
#   python pyprojectviewer.py . --hide-size --hide-hidden --hide-desc --hide-codes
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --max-depth=0
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --deny-ext=pyc
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --pass-ext=py,md,txt
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --pass-ext=py,md,txt --max-depth=1
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --savedfile=logs/output-ppv.txt
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --savedfile=logs/output-ppv.txt --viewparts=0x1C --viewitems=0x0D
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --savedfile=logs/output-ppv.txt --viewparts=0x1E --viewitems=0x07
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2 --max-depth=0
#   python pyprojectviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2 --max-depth=0 --hide-hidden
# ------------------
# windows
# ------------------
# > python pyprojectviewer.py -h
#   python pyprojectviewer.py .
#   python pyprojectviewer.py . --savedfile=./output-ppv.txt
#   python pyprojectviewer.py . --hide-codes
#   python pyprojectviewer.py . --hide-size --hide-hidden --hide-desc --hide-codes
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --max-depth=0
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --deny-ext=pyc
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --pass-ext=py,md,txt
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --pass-ext=py,md,txt --max-depth=1
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --savedfile=logs/output-ppv.txt
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --savedfile=logs/output-ppv.txt --viewparts=0x1C --viewitems=0x0D
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2\examples\gemma --savedfile=logs/output-ppv.txt --viewparts=0x1E --viewitems=0x07
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2 --max-depth=0
#   python pyprojectviewer.py D:\E\Study\Rust\repos\AI\AI3\Google-CPP-LLM\Flax2 --max-depth=0 --hide-hidden
# --------------------------------------
if __name__ == "__main__":
  main()
# ------------------------------------------------------------------------------
