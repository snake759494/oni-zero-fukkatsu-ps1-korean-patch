# 오니제로 ~부활~ PS1 한글패치

PS1 일본판 **ONI零 ～復活～ (パンドラMAXシリーズ Vol.6, SLPS-03106)**용 비공식 한국어 패치입니다. **대사·나레이션·선택지·메뉴·아이템·법술·의뢰 이름 등 게임 안의 문장**을 한국어로 바꿨습니다. **지역 이름 배너·던전 지도·전투 명령 메뉴·세이브 화면·서두와 결말의 세로 시 같은 그림 글자**도 한글로 다시 그렸고, 그림 요소가 많은 타이틀 화면은 원본을 가리지 않게 영상 자막처럼 한글을 덧씌웠습니다. 현재 배포판은 **v1.0 (2026-11-06)**입니다.

[패치 다운로드](https://github.com/snake759494/oni-zero-fukkatsu-ps1-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 한글패치 **OniZero_Fukkatsu_PS1_KO_v1.0.xdelta**뿐입니다. 저장소에는 제작 소스와 한국어 번역만 공개합니다. 원본·완성 디스크 이미지, 추출한 게임 파일·그림, 일본어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『오니제로 ~부활~』은 판도라박스의 『ONI』 시리즈 PS1 RPG입니다(판도라 MAX 시리즈 제6탄). 헤이안 시대를 배경으로, 오니의 피를 이은 은인(隠忍) 일족의 소년 시로마루가 퇴마 의뢰를 받으며 요마와 싸우고 동료로 변신하는 이야기입니다.

이 패치는 **PS1 일본판 SLPS-03106의 BIN/CUE 이미지(1트랙, MODE2/2352)**에만 적용됩니다. 파일 이름보다 아래 표의 크기와 해시가 일치하는지가 중요합니다.

## 적용할 원본

| 항목 | 값 |
| --- | --- |
| 게임 ID | SLPS-03106 |
| 원본 형식 | 수정되지 않은 일본판 BIN/CUE (트랙 1개) |
| 원본 BIN 크기 | 596,149,680 바이트 |
| **원본 BIN MD5** | `cf7a2a6dd804533f96bd23630952624b` |
| 원본 BIN SHA-1 | `bd2f2cdacdc6be3b68dc81c29a0e476ee3f1c2d8` |
| 원본 BIN SHA-256 | `72bfd70113cb068da520917962342478bf0163790a98a013dbd8d506865a6c02` |
| xdelta 파일 크기 | 8,598,364 바이트 |
| xdelta SHA-256 | `be4e74d49d92fa63cf61bc60cc05a21c730c698a6916bc42dbfda9dd4280b79c` |
| 적용 결과 BIN 크기 | 600,270,384 바이트 (원본보다 4,120,704 바이트 큼) |
| 적용 결과 BIN SHA-1 | `39427af54e76a2c0281c0b44b089fe8cc51c1502` |
| 적용 결과 BIN SHA-256 | `9a4c3d67bafe9594d9490d7460c990e3b2a2c071d89cc89268b2862652e6b370` |

원본 게임 파일은 사용자가 직접 준비해야 합니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin'
```

위 표와 다르면 적용을 중단하세요. CHD, PBP, ECM, 압축 이미지에는 적용할 수 없습니다.

### xdelta UI 사용

1. 릴리즈에서 `OniZero_Fukkatsu_PS1_KO_v1.0.xdelta`를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 `.bin`을 선택합니다.
4. **Output File**에는 새 파일 이름을 지정합니다(예: `Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Korean).bin`).
5. 원본 `.cue`를 복사해 이름을 바꾸고, `FILE "..."` 줄을 결과 BIN 이름으로 고칩니다.

```
FILE "Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Korean).bin" BINARY
  TRACK 01 MODE2/2352
    INDEX 01 00:00:00
```

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다. xdelta 자체는 [공식 프로젝트](https://github.com/jmacd/xdelta)를 참고하세요.

### 명령줄 사용

```powershell
.\xdelta3.exe -d -s '.\Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin' '.\OniZero_Fukkatsu_PS1_KO_v1.0.xdelta' '.\Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Korean).bin'
```

해시를 자동으로 검사하고 CUE까지 만들어 주는 도구도 있습니다. Python 3과 xdelta3가 필요하며, 같은 이름의 출력 파일이 이미 있으면 덮어쓰지 않습니다.

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source '.\Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin' --patch '.\OniZero_Fukkatsu_PS1_KO_v1.0.xdelta' --output '.\Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Korean).bin'
```

### 실행

에뮬레이터에서 결과 `.cue`를 여세요. 원본판의 세이브 스테이트는 불러오지 마세요(실행파일과 데이터가 다릅니다). 메모리 카드 세이브는 원본판과 같은 형식입니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 대사 | 스크립트 대사·나레이션·선택지 17,615줄 |
| 기타 문자열 | 메뉴·아이템·장비·법술 설명·의뢰 이름·상점·전투 메시지·데이터 변환 안내 등 2,066개 |
| 글꼴 | 게임 글꼴의 한자 영역에 한글 음절을 넣음(나눔스퀘어 네오, 원본과 같은 테두리 글리프) |
| 이름 | 동료·적 이름 표, 주인공 기본 이름(시로마루), 이름 입력판 가나 표 → 한글 음절표 |
| 그림 글자 | 206항목: 타이틀 메뉴(자막식), 지역 이름 배너, 던전 지도 제목·범례, 전투 명령 메뉴(공격/방어/법술/신강림/변신/도구/도주 등), 세이브·로드·데이터 변환 화면, 예/아니오, 서두·결말 세로 시, 정반 도박 글자 등 |

### 번역 원칙

- 기계 번역 없이 문맥을 보고 직접 번역했습니다(`docs/TRANSLATION_GUIDE.md`).
- 인물·지명은 일본어 발음을 따르되 불교 용어 등은 한국 한자음을 썼습니다(예: 시로마루, 헤이안쿄, 보현보살).
- 주인공 이름 뒤 조사는 기본 이름 「시로마루」(받침 없음)에 맞추거나 조사가 필요 없게 문장을 다듬었습니다.

### 번역하지 않은 것

- 전투 상태창의 「体力」「神力」 라벨(압축된 데이터 안에 있어 찾지 못함)
- 오프닝 등 동영상(STR) 안의 글자
- 덤 메뉴 일부(다른 게임 예고 그림, 일부 메뉴 글자)
- 디버그용 문자열, 음성

## 알려진 한계

- 모든 화면을 직접 확인하지는 못했습니다. 타이틀·데이터 로드/변환·이름 입력·초반 대화·필드 이동·첫 전투는 에뮬레이터로 확인했지만, 이후 장면·결말과 수정한 전투 명령 메뉴는 게임 화면으로 끝까지 보지 못했습니다.
- 칸 길이가 정해진 일부 의뢰 제목은 자리가 모자라 끝이 잘릴 수 있습니다.
- 인게임 확인은 DuckStation으로 했습니다. 실기에서의 동작은 확인하지 못했습니다. 칸을 넘치거나 어긋난 문구가 있으면 이슈로 알려 주세요.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `build.py` | 전체 빌드(대사 교체·재배치, 기타 문자열, 글꼴, 이름, 그림, 디스크 기록) |
| `tools/prepare.py` | 빌드 준비(디스크 추출, 참조표, 원문 목록, 해시표, 그림 목록) |
| `tools/` | `strings.py` 대사 위치, `refs.py` 파일 참조, `misc_scan.py` 기타 문자열, `font.py`·`kglyph.py` 글꼴, `gfx.py`·`tim.py` 그림 글자, `iso.py`·`disc.py`·`cdsec.py` 디스크, `apply_release.py` 해시 검사 후 적용, `check.py` 번역 검사, `emu.py`·`srv.py`·`c.py` DuckStation 테스트 조작, 기타 분석 도구 |
| `text/ko/dNN.tsv`, `mNN.tsv` | 번역. `번호<TAB>한국어` (번호는 빌드 준비 때 만드는 원문 목록과 짝) |
| `text/ko/fix.tsv` | 수동 교정. `원문 SHA-1 앞 16자리<TAB>한국어` |
| `text/gfx_spec.py` | 그림별 지우기·그리기 명령 |
| `fonts/` | (저장소에 없음) 갈무리 글꼴을 두는 곳 |
| `docs/` | 기술 설명, 재빌드 방법, 글꼴 출처, 번역 지침 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
