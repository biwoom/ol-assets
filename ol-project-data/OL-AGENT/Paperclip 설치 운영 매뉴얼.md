# Paperclip 설치 운영 매뉴얼

## 1.1 Quickstart 설치

```bash
npx paperclipai onboard --yes
```

Quickstart 문서는 이 명령으로 기본 설정을 만들고, embedded PostgreSQL과 로컬 파일 저장소를 설정하며, Paperclip 서버를 시작하는 흐름을 안내한다.[^paperclip-quickstart]

브라우저 접속:

```text
http://localhost:3100
```

## 1.2 저장소 직접 설치

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

## 1.3 기본 점검

```bash
curl http://localhost:3100/api/health
```

문제가 생기면:

```bash
paperclipai doctor
```

---
