import sys
import re
from pathlib import Path

def format_file(file_path):
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. 본문 내 각주 기호 변환 (예: [1] -> [^1], **[1]** -> [^1])
    # 단, [KO] 블록 내부나 이미 [^1] 형식인 것은 제외
    # 복잡하게 치환하기보다 본문의 텍스트에서 각주 기호를 찾아 [^번호]로 정형화
    
    # 2. 레거시 위키 주석 변환 (예: [*Note on chapter title] -> [^note1] 등으로 유연하게 교체할 수 있도록 유도하거나 표준화)
    # 여기서는 주로 숫자로 된 각주 기호를 타겟으로 함.
    def replace_body_notes(match):
        num = match.group(1)
        return f"[^{num}]"
        
    # 본문 영역과 각주 영역 분리
    parts = content.split("## 각주")
    body = parts[0]
    footnote_section = parts[1] if len(parts) > 1 else ""
    
    # 본문 내 [1] 이나 **[1]** 매칭하여 [^1] 로 변경
    # 단, 이미 [^1] 로 되어 있는 것 제외
    body = re.sub(r'(?<!\^)(?<!\[)\*\*\[(\d+)\]\*\*(?!\])', r'[^\1]', body)
    body = re.sub(r'(?<!\^)(?<!\[)\[(\d+)\](?!\])', r'[^\1]', body)
    parts[0] = body
    
    # 3. 각주 섹션 정형화
    if footnote_section:
        # 각주 번호 정의 줄 파싱
        # 예: **[1]** 내용 -> [^1]: 내용
        # 혹은 [1] 내용 -> [^1]: 내용
        # 혹은 [^1]: 내용 -> [^1]: 내용
        
        # 영어 각주와 [KO] 각주 영역 분리
        ko_match = re.search(r'\[KO\]\s*([\s\S]*?)\s*\[/KO\]', footnote_section)
        
        en_section = footnote_section
        ko_section = ""
        if ko_match:
            ko_section = ko_match.group(1)
            en_section = footnote_section.replace(ko_match.group(0), "")
            
        # 영어 각주 파싱
        en_notes = {}
        # 각주 정의들을 파인드
        # 패턴: **[1]** 또는 [1] 또는 [^1]: 으로 시작하여 다음 각주 정의 전까지
        pattern = r'(?:^\*\*\[(\d+)\]\*\*|^\[(\d+)\]|^\[\^(\d+)\]:)\s*(.*?)(?=\n\*\*\[\d+\]\*\*|\n\[\d+\]|\n\[\^\d+\]:|\Z)'
        matches = re.finditer(pattern, en_section, re.MULTILINE | re.DOTALL)
        for m in matches:
            num = m.group(1) or m.group(2) or m.group(3)
            content_text = m.group(4).strip()
            en_notes[num] = content_text
            
        # 한국어 각주 파싱
        ko_notes = {}
        if ko_section:
            ko_matches = re.finditer(pattern, ko_section, re.MULTILINE | re.DOTALL)
            for m in ko_matches:
                num = m.group(1) or m.group(2) or m.group(3)
                content_text = m.group(4).strip()
                ko_notes[num] = content_text
                
        # 재정렬 및 정형화
        new_footnote_section = "\n\n"
        
        # 번호별 정렬
        sorted_keys = sorted(en_notes.keys(), key=lambda x: int(x) if x.isdigit() else 999)
        
        # 영어 각주 출력
        for key in sorted_keys:
            new_footnote_section += f"[^{key}]: {en_notes[key]}\n"
            
        # 한국어 각주 출력 (통합 [KO] 블록)
        if ko_notes or ko_section:
            new_footnote_section += "\n[KO]\n"
            for key in sorted_keys:
                ko_text = ko_notes.get(key, "")
                if ko_text:
                    new_footnote_section += f"[^{key}]: {ko_text}\n\n"
            # 끝에 있는 개행들 정리 후 [/KO] 닫기
            new_footnote_section = new_footnote_section.rstrip() + "\n[/KO]\n"
            
        parts[1] = new_footnote_section
        
    new_content = "## 각주".join(parts)
    
    # 변경 사항 저장
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Footnotes formatted successfully for: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 format_footnotes.py <file_path>")
        sys.exit(1)
    format_file(sys.argv[1])
