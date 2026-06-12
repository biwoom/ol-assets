import sys
import re
import unicodedata
from pathlib import Path

# 상대 경로 기준 용어집 위치
GLOSSARY_PATH = Path("BuddhaStory/term/gcb-revised-term.md")

def normalize_text(text):
    # diacritics 제거 및 소문자화하여 유연한 매칭
    text = unicodedata.normalize('NFKC', text)
    text = "".join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text.lower().strip()

def parse_glossary():
    # 저장소의 루트를 기준으로 탐색
    root = Path.cwd()
    glossary_file = root / GLOSSARY_PATH
    if not glossary_file.exists():
        # 한 단계 상위 또는 하위에서도 탐색
        alternative = Path(__file__).resolve().parents[3] / GLOSSARY_PATH
        if alternative.exists():
            glossary_file = alternative
        else:
            print(f"Warning: Glossary file not found at {GLOSSARY_PATH}. Glossary linting skipped.")
            return {}
            
    terms = {}
    with open(glossary_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 포맷: * English: Korean(Pali) 형태 파싱
            m = re.match(r'^\*\s*(.*?)\s*:\s*(.*)', line)
            if m:
                eng_part = m.group(1).strip()
                kor_part = m.group(2).strip()
                
                # 영어 여러 개인 경우 분할 (예: Brother / Sister)
                eng_words = [w.strip() for w in re.split(r'/|,', eng_part) if w.strip()]
                
                # 한국어 부분에서 핵심 명사만 추출 (예: 아나타삔디까(Anāthapiṇḍika, 급고독장자) -> 아나타삔디까, 급고독장자)
                # 괄호 안의 동의어도 검증 단어로 수집
                kor_clean = re.sub(r'\(.*?\)', '', kor_part).strip()
                kor_words = [kor_clean]
                
                # 괄호 안 동의어 추출
                parens = re.findall(r'\((.*?)\)', kor_part)
                for p in parens:
                    sub_words = [w.strip() for w in re.split(r'/|,', p) if w.strip()]
                    kor_words.extend(sub_words)
                    
                for eng in eng_words:
                    norm_eng = normalize_text(eng)
                    if norm_eng:
                        terms[norm_eng] = {
                            "original_eng": eng,
                            "original_kor": kor_part,
                            "kor_words": [w for w in kor_words if w]
                        }
                        
    return terms

def lint_file(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    terms = parse_glossary()
    if not terms:
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 문단 블록 파싱 (영어 본문과 KO 번역 매핑 추출)
    # [KO] ... [/KO] 영역과 그 직전 영어 영역 매치
    blocks = re.findall(r'([\s\S]*?)\n\n\[KO\]\s*([\s\S]*?)\s*\[/KO\]', content)
    
    warnings = []
    
    for idx, (eng_block, kor_block) in enumerate(blocks, 1):
        norm_eng_block = normalize_text(eng_block)
        
        # 영어 블록에 용어집 영어 단어가 들어있는지 확인
        for norm_eng, term_info in terms.items():
            # 단어 경계(\b) 매칭 또는 포함관계 체크
            # diacritics가 있는 경우 \b가 작동 안 할 수 있어 정규화된 포함관계로 확인
            if norm_eng in norm_eng_block:
                # 한국어 블록에 해당 한국어 번역 단어 중 하나라도 들어있는지 검사
                matched = False
                for kor_w in term_info["kor_words"]:
                    if kor_w in kor_block:
                        matched = True
                        break
                        
                if not matched:
                    warnings.append({
                        "block_num": idx,
                        "eng_word": term_info["original_eng"],
                        "expected_kor": term_info["kor_words"][0],
                        "kor_block_preview": kor_block.replace('\n', ' ')[:60] + "..."
                    })
                    
    # 결과 보고
    print(f"\n--- Glossary Linting Results for {path.name} ---")
    if not warnings:
        print("Success: All terms are compliant with the glossary!")
    else:
        print(f"Warning: Found {len(warnings)} potential term mismatches.")
        for w in warnings:
            print(f"[Block {w['block_num']}] Expected Korean term '{w['expected_kor']}' (from English '{w['eng_word']}') was not found in translated block.")
            print(f"  Translated text preview: {w['kor_block_preview']}")
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lint_glossary.py <file_path>")
        sys.exit(1)
    lint_file(sys.argv[1])
