# ファイル内容検索ツール (File Content Searcher)

複雑なAND/OR/NOTの論理条件、正規表現、ファイル種別のフィルタリングをサポートし、ファイルの内容に基づいて検索を行うコマンドラインツールです。
プレーンテキストファイルおよびMicrosoft Excel (.xlsx) ファイル内の検索に対応しています。

## 使い方

```bash
python3 search.py [検索ディレクトリ] [オプション]
```

## オプション

| フラグ | 引数 | 説明 |
|---|---|---|
| `directory` | (必須) | 検索対象のディレクトリパス。 |
| `--and` | PATTERN | ファイルに**必ず**含まれなければならないパターン。複数指定可能です。 |
| `--or` | PATTERN | **いずれか**が含まれていれば良いパターン。複数指定可能です。 |
| `--not` | PATTERN | ファイルに**含まれてはならない**パターン。複数指定可能です。 |
| `-i`, `--ignore-case` | | 大文字と小文字を区別せずに検索を実行します。 |
| `-r`, `--regex` | | すべてのパターン (`--and`, `--or`, `--not`) を正規表現として扱います。 |
| `--include` | GLOB | 検索対象に**含める**ファイル名のパターンをカンマ区切りで指定します (例: `*.py,*.md`)。 |
| `--exclude` | GLOB | 検索対象から**除外する**ファイル名のパターンをカンマ区切りで指定します (例: `*.log,*.tmp`)。 |

**注意:** 検索を実行するには、`--and` または `--or` のいずれかを少なくとも1つ指定する必要があります。

## 実行例

### 基本的な検索

*   **1つの単語を検索:**
    ```bash
    python3 search.py . --and "error"
    ```

*   **"error" と "critical" の両方を含むファイルを検索 (AND検索):**
    ```bash
    python3 search.py . --and "error" --and "critical"
    ```

*   **"warning" または "notice" のいずれかを含むファイルを検索 (OR検索):**
    ```bash
    python3 search.py . --or "warning" --or "notice"
    ```

### 応用的な検索

*   **"error" を含むが "debug" は含まないファイルを検索:**
    ```bash
    python3 search.py . --and "error" --not "debug"
    ```

*   **Pythonファイル内で、"FIXME" または "TODO" を含み(大文字小文字問わず)、かつ "DONE" は含まないファイルを検索:**
    ```bash
    python3 search.py src/ --or "FIXME" --or "TODO" --not "DONE" -i --include "*.py"
    ```

*   **テキストファイル内で正規表現パターンに一致するものを検索:**
    ```bash
    python3 search.py logs/ --and "user_[0-9]+" -r --include "*.log"
    ```
