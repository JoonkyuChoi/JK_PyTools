# pyfolderviewer.py
# Copyright (c) 2025 Choi Joonkyu
"""지정 경로에 존재하는 모든 파일들의 정보를 트리 형태로, 콘솔화면이나 파일에 출력하는 어플 (풀 기능 배포용)"""
# ------------------------------------------------------------------------------
# 구현 정보
# ------------------------------------------------------------------------------
# - 역할
#   지정 경로에 존재하는 모든 파일들(하위 폴더 포함)의 간략 정보를 트리 형태로,
#   콘솔화면이나 파일에 출력한다.
# ------------------------------------------------------------------------------
# [IMPORT]
# ------------------------------------------------------------------------------
# [외부] 모듈
# --------------------------------------
import os         # 운영체제 (파일/폴더/경로 제어용)
import ast        # 추상구문트리 (py파일 분석용)
import re         # 정규표현식 (md파일 분석용)
import argparse   # 콘솔옵션 파서
# ------------------------------------------------------------------------------
# [DEFINES]
# ------------------------------------------------------------------------------
# [TYPES]
# --------------------------------------

# --------------------------------------
# [CONSTANTS]
# --------------------------------------

# ------------------------------------------------------------------------------
# [VARIABLES]
# ------------------------------------------------------------------------------
gobjSavedFile = None    # 저장파일 객체
# [JKC:20251019-0810] 기능 추가
gaDenyNames   = None    # 거부파일명칭목록
gaPassNames   = None    # 허용파일명칭목록
gaDenyExts    = None    # 거부확장자목록
gaPassExts    = None    # 허용확장자목록

gnMaxDepth    = 3       # 최대 깊이
gbHideDesc    = False   # 파일설명 숨김
gbHideSize    = False   # 파일사이즈 숨김
gbHideHidden  = False   # 숨김파일 숨김
# ------------------------------------------------------------------------------
# [FUNCTIONS]
# ------------------------------------------------------------------------------
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
      # 첫 줄만 출력 (너무 길면 잘림)
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
# [재귀호출] 해당 경로의 트리 구조를 루프하며, 분석정보 출력한다.
# --------------------------------------
def print_tree(root_path, prefix='', depth=0):
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
  # 각 요소별 처리
  for i, entry in enumerate(entries):
    full_path = os.path.join(root_path, entry)
    connector = '└── ' if i == entries_count - 1 else '├── '
    # 파일
    if os.path.isfile(full_path):
      # [JKC:20251019-0810] 기능 추가
      name, ext = os.path.splitext(entry)
      name = name.lower()
      ext  = ext[1:].lower()
      # ------------------
      # 파일명칭 필터링
      # ------------------
      # gaPassNames 배열의 요소가 name에 포함되어 있다면 continue
      if gaPassNames and any(pass_name in name for pass_name in gaPassNames):
          continue
      # gaDenyNames 배열의 요소가 name과 정확히 일치하면 continue
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
      # 파일설명 추출
      if not gbHideDesc:
        # py파일인 경우, 첫 번째 docstring 추출
        if entry.endswith('.py'):
          doc = extract_docstring(full_path)
          if doc:
            info += f" # {doc}"
        # md파일인 경우, 첫 번째 title 추출
        elif entry.endswith('.md'):
          title = extract_md_title(full_path)
          if title:
            info += f' # {title}'
      print_and_save(f"{prefix}{connector}{info}")
    # 폴더
    elif os.path.isdir(full_path):
      print_and_save(f"{prefix}{connector}{entry}/")
      extension = '    ' if i == entries_count - 1 else '│   '
      print_tree(full_path, prefix + extension, depth + 1)
# --------------------------------------
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
  # 전역변수 사용 선언
  global gobjSavedFile, gaDenyNames, gaPassNames, gaDenyExts, gaPassExts, gnMaxDepth, gbHideDesc, gbHideSize, gbHideHidden
  # 콘솔옵션/사용법 설정
  parser = argparse.ArgumentParser(
    description="디렉토리 파일구성 분석툴 (파일검출: 파일명/확장자 필터링 + 깊이 제한 + 파일설명 + 파일사이즈 + 숨김파일 제어, 결과출력: 콘솔+파일)",
    usage=("python pyfolderviewer.py <parsepath> [--savedfile=경로]\n"
           "                        [--deny-name=n1,n2] [--pass-name=n1,n2]\n"
           "                        [--deny-ext=ext1,ext2] [--pass-ext=ext1,ext2]\n"
           "                        [--max-depth=N] [--hide-desc] [--hide-size] [--hide-hidden]")
  )
  parser.add_argument("parsepath"     , help="분석 디렉토리 경로")
  parser.add_argument("--savedfile"   , help="분석결과 저장파일 경로", default="")
  # [JKC:20251019-0810] 기능 추가
  parser.add_argument("--deny-name"   , help="제외할 파일명칭 목록 (예: _test,log_)", default="")
  parser.add_argument("--pass-name"   , help="허용할 파일명칭 목록 (예: _test,log_)", default="")

  parser.add_argument("--deny-ext"    , help="제외할 파일 확장자 목록 (예: pyc,md)", default="")
  parser.add_argument("--pass-ext"    , help="허용할 파일 확장자 목록 (예: py,txt)", default="")
  parser.add_argument("--max-depth"   , help="출력할 최대 디렉토리 깊이 (예: 2)", type=int, default=None)
  parser.add_argument("--hide-desc"   , help="파일설명 숨김", action="store_true")
  parser.add_argument("--hide-size"   , help="파일사이즈 숨김", action="store_true")
  parser.add_argument("--hide-hidden" , help="숨김파일 숨김", action="store_true")
  # 콘솔옵션 파싱
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
  gbHideDesc = args.hide_desc
  # 파일사이즈 숨김
  gbHideSize = args.hide_size
  # 숨김파일 숨김
  gbHideHidden = args.hide_hidden
  # ------------------
  # 분석/출력+저장
  # ------------------
  print_and_save(f"{args.parsepath}/")
  print_tree(args.parsepath, depth=0)
# ------------------------------------------------------------------------------
# [EXECUTE-CODES] 직접 실행 시, 수행 코드
# ------------------------------------------------------------------------------
# > python pyfolderviewer.py -h
#   python pyfolderviewer.py .
#   python pyfolderviewer.py . --savedfile=logs/output-ptree.txt
#   python pyfolderviewer.py . --hide-size --hide-hidden --hide-desc
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --max-depth=1
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --deny-ext=pyc
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --pass-ext=py,md,txt
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --pass-ext=py,md,txt --max-depth=1
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2/examples/gemma --savedfile=logs/output-ptree.txt
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2 --max-depth=0
#   python pyfolderviewer.py /mnt/d/E/Study/Rust/repos/AI/AI3/Google-CPP-LLM/Flax2 --max-depth=0 --hide-hidden
# --------------------------------------
if __name__ == "__main__":
  main()
# ------------------------------------------------------------------------------
