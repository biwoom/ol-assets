# OL홈페이지 개발 체크리스트


## 핵심 레퍼런스
https://basecoatui.com/
https://ui.shadcn.com/

---

- [x] 로컬 개발 환경구축
- [x] 깃헙배포
- [x] 온톨로지 기반 설계
- [x] 홈페이지 샘플코드 기반 디자인 적용
- [x] WORKS 메뉴 신설. basecoat 스타일 3단 칼럼의 문서 전용 레이아웃 적용. 
      - 참고: https://basecoatui.com/
      - 왼쪽사이드바: 폴더구조(buddha-story/1.birth/birth.md)를 그룹방식 문서구조로 변환: buddha-story > 1.birth > birth.
- [x] BLOG 첫화면 신규글 자동반영: src/content/blog 에 새 md 파일 추가하면 자동으로  BLOG 첫화면에서 최신글 리스트로 반영되는 기능이 추가되어 있는지 확인하고 없다면 최신글 반영 기능 업데이트하기.
- [x] WORKS  페이지 오른쪽 사이드 목차 생성 추가. 왼쪽 사이드바 숨기고 보이는 토글 추가. 
- [x] Book 완료 html파일 저장방식 변경: 파일 하나만 저장. 그리고 메타데이터도 htmlPath 하나로 통일. book 페이지에서 a 태그 속성으로 download 추가해서 웹에서 읽기와 내려받기를 분리: **A. 현재 제안**파일 1개, `download` 속성가장 단순iOS Safari 미지원. 모바일 iOS Safari 미지원 대응:  iOS Safari에서 클릭시 경고창 표시하기. `book` collection 스키마와 `book/index.astro`의 버튼 코드만 수정
- [x] 검색기능 추가, 헤더에 검색폼 추가.

- [ ] blog페이지 .ol-chips 카테고리 클릭시 필터링 기능 추가.
- [ ] book페이지 .ol-chips 카테고리 별 필터링 기능 추가.
- [ ] atlas페이지 .ol-section-tight 섹션 미리보기창 수정 - 현재 atlas 모습으로 변경. 사이드바 탭에 편집뷰와 독서뷰 버튼 추가. 각 탭 클릭시 편집뷰나 독서뷰 렌더링.
- [ ] works페이지에 샘플 md 데이터 추가하여 테스트 해보기.
- [ ] design페이지 어떻게 이미지 파일 등을 추가할 지 결정. book 처럼 파일 저장경로와 실제 src/contents/design 에는 디자인_메타.md 만 추가할 지 등등.
- [ ] home 
- [ ] 모바일 버전 css 수정
- [ ] 블로그 이미지 첨부시 이미지 저장위치?
- [ ] atlas페이지 툴 미리보기 섹션 탭 전환 구조로 교체


---
