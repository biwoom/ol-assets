import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Add current script directory to sys.path to import sibling modules
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

try:
    from format_footnotes import format_file
    from lint_glossary import lint_file
    from validate_translation import validate_file
except ImportError as e:
    print(f"Error importing helper modules: {e}")
    sys.exit(1)

LOG_DIR_PATH = Path("BuddhaStory/log")

def is_empty_or_bypass_file(file_path):
    path = Path(file_path)
    if not path.exists():
        return False
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split("## 본문")
    if len(parts) < 2:
        body_part = content
    else:
        body_part = parts[1].split("## 각주")[0]
        
    body_text = body_part.strip()
    
    if not body_text:
        return True
        
    clean_lines = [line.strip() for line in body_text.split('\n') if line.strip()]
    if len(clean_lines) == 1:
        line = clean_lines[0]
        if line.startswith('[For the Anudīpanī') and line.endswith(']'):
            return True
            
    if re.match(r'^\[For the Anudīpanī[\s\S]*?\]$', body_text):
        return True
        
    return False

def generate_bypass_log(file_path):
    path = Path(file_path)
    root = Path.cwd()
    sub_folder = "draft-1"
    log_dir = root / LOG_DIR_PATH / sub_folder
    if not log_dir.exists():
        alternative = Path(__file__).resolve().parents[3] / LOG_DIR_PATH / sub_folder
        if alternative.exists():
            log_dir = alternative
        else:
            log_dir.mkdir(parents=True, exist_ok=True)
            
    log_filename = f"{path.stem}-log.md"
    log_file_path = log_dir / log_filename
    
    log_content = f"""# 1차 원고 자가 검증 로그 - {path.name}

## 1. 사전 계획(Plan) 수행 상태 (Bypass)

| 단계 | 계획 내용 | 수행 상태 | 비고 / 세부 조치 |
|---|---|---|---|
| Step 1 | {path.name} 입력 구조 및 용어 매핑 분석 | **Bypass** | 본문 내용이 없는 빈 문서로 판정되어 분석 생략 |
| Step 2 | YAML Frontmatter 및 tagAliases 작성 | **Bypass** | 본문이 없어 Frontmatter 작성 생략 |
| Step 3 | 1차 번역 본문 수행 및 문단별 1:1 [KO] 적용 | **Bypass** | 본문 내용이 없어 번역 및 문단 매핑 생략 |
| Step 4 | 하단 각주 통합 [KO] 래핑 및 각주 정의 간 단일 빈 줄 적용 | **Bypass** | 각주 내용이 없어 처리 생략 |
| Step 5 | AI 모델 자체검증 체크리스트 수행 및 로그 생성 | **Bypass** | 빈 문서 예외 규칙에 따라 자가 검증 우회 및 바이패스 로그 자동 생성 |

---

## 2. 예외 처리 상세
- **사유**: 본문 텍스트가 존재하지 않는 빈 문서 (참조 지시문만 있거나 내용 없음)
- **대상 파일**: {path.name}
- **조치**: 번역 및 헬퍼 스크립트 실행을 우회(Bypass)하고, 자가 검증 로그를 즉각 생성하여 예외 기록을 보존함.
"""
    with open(log_file_path, 'w', encoding='utf-8') as lf:
        lf.write(log_content)
        
    print(f"Bypass detected. Validation log generated successfully for empty file: {log_file_path.name}")

def init_draft2(file_path):
    src_path = Path(file_path)
    if not src_path.exists():
        print(f"Error: 1st draft file not found at: {file_path}")
        sys.exit(1)
        
    # Determine destination draft-2 path
    parts = list(src_path.parts)
    if "draft-1" in parts:
        idx = parts.index("draft-1")
        parts[idx] = "draft-2"
    dest_path = Path(*parts)
    
    # Copy manuscript file
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    print(f"Copied manuscript to draft-2: {dest_path.name}")
    
    # Process corresponding term file
    # Edit /draft-1/ filename maps to term/ filename-term.md
    term_dir = src_path.parents[3] / "term"
    term_file = term_dir / f"{src_path.stem}-term.md"
    
    if term_file.exists():
        with open(term_file, 'r', encoding='utf-8') as tf:
            term_content = tf.read()
            
        if "2차 :" not in term_content:
            lines = term_content.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if (line.strip().startswith('*') or line.strip().startswith('-')) and ':' in line:
                    new_lines.append("  * 2차 : ")
            
            with open(term_file, 'w', encoding='utf-8') as tf:
                tf.write('\n'.join(new_lines))
            print(f"Polished term glossary with 2nd-draft recommendation templates: {term_file.name}")
        else:
            print(f"Term glossary already polished: {term_file.name}")
    else:
        term_dir.mkdir(parents=True, exist_ok=True)
        with open(term_file, 'w', encoding='utf-8') as tf:
            tf.write(f"# 신규 용어 후보 - {src_path.name}\n\n* (신규 추출된 용어가 없습니다. 필요 시 용어를 작성해 주세요)\n  * 2차 : \n")
        print(f"Created template term glossary at: {term_file.name}")
def copy_to_draft3(file_path):
    src_path = Path(file_path)
    if not src_path.exists():
        print(f"Error: 2nd draft file not found for copying: {file_path}")
        return
        
    parts = list(src_path.parts)
    if "draft-2" in parts:
        idx = parts.index("draft-2")
        parts[idx] = "draft-3"
    dest_path = Path(*parts)
    
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    print(f"[Success] Copied 2nd-draft manuscript to draft-3: {dest_path.name}")

def upgrade_workflow(log_file_path):
    log_path = Path(log_file_path)
    if not log_path.exists():
        print(f"Error: Log file not found: {log_file_path}")
        sys.exit(1)
        
    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
        
    # Extract ## 8. 워크플로우 개선 및 시스템 자가 업그레이드 사항 section
    pattern = r'## 8\. 워크플로우 개선 및 시스템 자가 업그레이드 사항.*?$(.*?)(\n##|\Z)'
    match = re.search(pattern, log_content, re.MULTILINE | re.DOTALL)
    if not match:
        print("No upgrade section found in log file.")
        return
        
    section_text = match.group(1).strip()
    upgrade_lines = [line.strip() for line in section_text.split('\n') if line.strip()]
    
    rule_updates = []
    script_updates = []
    
    for line in upgrade_lines:
        if "[룰문서]" in line:
            content = line.split("[룰문서]")[1].strip(" )]}-*•")
            if content and "이곳에 예시 규정" not in content:
                rule_updates.append(content)
        elif "[스크립트]" in line:
            content = line.split("[스크립트]")[1].strip(" )]}-*•")
            if content:
                script_updates.append(content)
                
    if not rule_updates and not script_updates:
        print("No valid upgrade feedback lines found in the log.")
        return
        
    current_date = datetime.now().strftime("%Y-%m-%d")
    root = Path.cwd()
    
    # Path mappings to rules files
    manual_path = root / "BuddhaStory/translation-agent-manual.md"
    gemini_path = root / "BuddhaStory/GEMINI.md"
    skill_path = root / "BuddhaStory/skills/buddha-translation-helper/SKILL.md"
    
    # Fallback to parents logic if not running at root
    if not manual_path.exists():
        manual_path = Path(__file__).resolve().parents[3] / "translation-agent-manual.md"
        gemini_path = Path(__file__).resolve().parents[3] / "GEMINI.md"
        skill_path = Path(__file__).resolve().parents[2] / "SKILL.md"
        
    targets = [manual_path, gemini_path, skill_path]
    history_header = "\n\n## 🔄 워크플로우 자가 개정 이력 (Self-Upgrade History)\n"
    
    if rule_updates:
        new_history_entry = f"\n- **[{current_date}]** (from `{log_path.name}`):\n"
        for rule in rule_updates:
            new_history_entry += f"  - {rule}\n"
            
        for target in targets:
            if target.exists():
                with open(target, 'r', encoding='utf-8') as tf:
                    doc_content = tf.read()
                    
                if "워크플로우 자가 개정 이력" in doc_content:
                    doc_content = doc_content.rstrip() + f"\n{new_history_entry}"
                else:
                    doc_content = doc_content.rstrip() + f"{history_header}{new_history_entry}"
                    
                with open(target, 'w', encoding='utf-8') as tf:
                    tf.write(doc_content)
                print(f"Successfully appended rule patch to: {target.name}")
            else:
                print(f"Target rule file not found for patching: {target}")
                
    if script_updates:
        print("\n[Alert] Script update feedback detected:")
        for script_fb in script_updates:
            print(f"  - {script_fb}")
        print("Please verify the helper scripts and apply physical code adjustments if needed.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 run_pipeline.py <mode> <file_path>")
        print("Modes:")
        print("  --preprocess        : Format footnotes and clean markup (1st draft)")
        print("  --validate          : Run glossary linting & validation for 1st draft")
        print("  --init-draft2       : Setup draft-2 manuscript & recommendation term templates")
        print("  --validate-draft2   : Run glossary linting & validation for 2nd draft")
        print("  --upgrade-workflow  : Parse draft-2 log and self-patch rule manuals")
        sys.exit(1)
        
    mode = sys.argv[1]
    file_path = sys.argv[2]
    
    if mode == "--upgrade-workflow":
        upgrade_workflow(file_path)
        sys.exit(0)
        
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    # Automatic bypass logic for empty files (applicable to validation and formatting modes)
    if is_empty_or_bypass_file(file_path):
        generate_bypass_log(file_path)
        sys.exit(0)
        
    if mode == "--preprocess":
        print(f"Running preprocessing on: {file_path}")
        format_file(file_path)
    elif mode == "--validate":
        print(f"Running validation on: {file_path}")
        lint_file(file_path)
        validate_file(file_path, is_draft2=False)
    elif mode == "--init-draft2":
        print(f"Initializing draft-2 environment for: {file_path}")
        init_draft2(file_path)
    elif mode == "--validate-draft2":
        print(f"Running 2nd draft validation on: {file_path}")
        lint_file(file_path)
        validate_file(file_path, is_draft2=True)
        copy_to_draft3(file_path)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
