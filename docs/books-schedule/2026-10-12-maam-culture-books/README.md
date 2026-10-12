# MaAM Culture & Books · 2026년 10–12월

배너와 실제 월간 달력으로 구성한 카카오톡 공유용 PNG 3장입니다.

| 월 | 캐릭터 | 명언 출처 |
|---|---|---|
| 10월 | BFR-N · 벤저민 프랭클린봇 | 프랭클린, 『부에 이르는 길』 |
| 11월 | GTH-N · 괴테봇 | 괴테, 『파우스트』 |
| 12월 | 찰스 디킨스봇 | 디킨스, 『크리스마스 캐럴』 |

실제 일정이 없는 발제독서모임은 모두 제외했습니다. 이번 변경은 캐릭터와 명언 교체이며, 기존 일정의 신규 전수 조사는 수행하지 않았습니다. 일정 확인 기준일과 각 항목의 출처·확정 여부는 `data/`에 있습니다. 명언 원문·번역·작품 맥락은 [출처 노트](quote-sources.md)에 기록했습니다.

## 다시 렌더링

이 디렉터리에서 실행합니다. Node.js와 Playwright, Chrome, Noto Sans KR이 필요합니다.

```powershell
node scripts/render-monthly.cjs --skill-root . --input data/culture-10.json --output MaAM-2026-10-Culture-and-Books.png --modules NODE_MODULES --chrome CHROME_PATH --font FONT_PATH
```

11월·12월은 입력과 출력 파일의 월을 바꾸면 됩니다. 배너·캐릭터·데이터를 함께 보존했습니다. 한국어 일정과 명언은 실제 폰트로 조판합니다. 디킨스봇은 built-in image_gen으로 생성한 투명 PNG이며, 프롬프트는 `assets/dickens-bot-prompt.txt`에 있습니다.

검증 결과: 월별 날짜 수 31·30·31, 캐릭터 각각 하나, 글자 잘림 및 제목·말풍선 겹침 없음. `qa/`에 검사 결과를 보관했습니다.
