# 재빌드

## 준비물

빌드 스크립트는 저장소 폴더를 작업 폴더로 쓰고, **그 상위 폴더**에서 원본 디스크와 큰 글꼴을 찾습니다.

```
<상위 폴더>/
  Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin   ← README의 해시와 일치해야 함
  NanumSquareNeo-cBd.ttf  NanumSquareNeo-eHv.ttf
  SeoulHangangB.ttf  SeoulHangangEB.ttf
  <이 저장소>/
    fonts/Galmuri11.ttf
```

- Python 3.13, `numpy`, `Pillow` (`capstone`은 분석 도구 `tools/mdis.py`·`xref.py`에만 필요)
- 글꼴 출처는 `docs/FONT_CREDITS.md`
- xdelta3 (배포 파일을 만들 때만)

## 빌드

저장소 폴더에서 실행합니다.

```powershell
python tools/prepare.py
python build.py
```

`prepare.py`는 다음을 차례로 합니다(결과물은 모두 배포하지 않는 원본 유래 파일). 원본 BIN이 다른 곳에 있으면 첫 인자로 경로를 주세요.

1. `tools/extract.py`: 디스크 파일(STR 영상 제외) → `orig/`
2. `tools/refs.py`: `DATA00.DAT` 안 파일들의 섹터 참조표 → `refs.pkl`
3. 대사 원문 목록 → `text/ja_all.json`, `text/src/dNN.tsv` (번역 파일의 `d00000` 번호와 짝)
4. `tools/misc_scan.py`: 대사 밖의 문자열 → `text/misc_raw.json`, `text/src/mNN.tsv`
5. 원문 SHA-1 해시표 → `text/hash_ja.json` (`text/ko/fix.tsv` 수동 교정의 짝)
6. CLUT 없는 그림 목록 → `gfx/nc.pkl`

결과는 상위 폴더의 `Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan) [KR].bin`입니다. 출력 경로는 `python build.py <출력.bin>`으로 바꿀 수 있습니다. 결과 BIN의 SHA-256이 `release_manifest.json`의 `output_bin_sha256`과 같아야 합니다. 경고(번역 없음, 칸 초과 등)는 `build.log`에 남습니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s "Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan).bin" "Pandora Max Series Vol. 6 - Oni Zero - Fukkatsu (Japan) [KR].bin" OniZero_Fukkatsu_PS1_KO_v1.0.xdelta
```

## 번역 수정

`docs/TRANSLATION_GUIDE.md`를 참고하세요. `text/ko/dNN.tsv`·`mNN.tsv`는 `번호<TAB>한국어`, `text/ko/fix.tsv`는 `원문 SHA-1 앞 16자리<TAB>한국어`입니다. 원문과 똑같이 둘 줄(디버그 문자열 등)은 번역 파일에서 뺐습니다. `python tools/check.py`가 줄 길이·제어 코드를 검사합니다.

그림 글자는 `text/gfx_spec.py`에 그림별로 지우기·그리기 명령을 적어 두었고, `python tools/gfxprev.py`로 미리보기를 만들 수 있습니다.
