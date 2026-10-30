# How this repository was made (Puerto Rico)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| OGP Biblioteca Virtual: Constitución del Estado Libre Asociado de Puerto Rico | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Derechos%20Civiles/CONST/CONST.pdf> | 2026-10-29 | none stated |
| OGP Biblioteca Virtual: Código Penal de Puerto Rico (Ley 146-2012, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Justicia/146-2012/146-2012.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Código Civil de Puerto Rico de 2020 (Ley 55-2020, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/55-2020.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Ley de Transacciones Comerciales (Ley 208-1995, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Transacciones/208-1995/208-1995.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Reglas de Procedimiento Criminal de 1963 (según enmendadas) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Justicia/RPC/RPC.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Reglas de Evidencia de Puerto Rico de 2009 (según enmendadas) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Justicia/REVI/REVI.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Ley sobre Despidos Injustificados (Ley 80 de 30 de mayo de 1976, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Trabajo/80-1976/80-1976.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Ley para Establecer la Jornada de Trabajo en Puerto Rico (Ley 379 de 15 de mayo de 1948, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Trabajo/379-1948.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Ley de Transformación y Flexibilidad Laboral (Ley 4-2017, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Trabajo/4-2017.pdf> | 2026-10-30 | none stated |
| OGP Biblioteca Virtual: Ley General de Corporaciones (Ley 164-2009, según enmendada) | <https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Corporaciones%20Privadas/164-2009/164-2009.pdf> | 2026-10-30 | none stated |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitucion` | Constitución del Estado Libre Asociado de Puerto Rico | 1 | 2024-04-15 to 2024-04-15 |
| `codigo-penal` | Código Penal de Puerto Rico (Ley 146-2012, según enmendada) | 1 | 2026-08-05 to 2026-08-05 |
| `codigo-civil` | Código Civil de Puerto Rico de 2020 (Ley 55-2020, según enmendada) | 1 | 2026-08-21 to 2026-08-21 |
| `ley-transacciones-comerciales` | Ley de Transacciones Comerciales (Ley 208-1995, según enmendada) | 1 | 2025-06-23 to 2025-06-23 |
| `reglas-procedimiento-criminal` | Reglas de Procedimiento Criminal de 1963 (según enmendadas) | 1 | 2026-06-15 to 2026-06-15 |
| `reglas-evidencia` | Reglas de Evidencia de Puerto Rico de 2009 (según enmendadas) | 1 | 2024-04-15 to 2024-04-15 |
| `ley-80-1976-despidos` | Ley sobre Despidos Injustificados (Ley 80 de 30 de mayo de 1976, según enmendada) | 1 | 2024-04-15 to 2024-04-15 |
| `ley-379-1948-jornada` | Ley para Establecer la Jornada de Trabajo en Puerto Rico (Ley 379 de 15 de mayo de 1948, según enmendada) | 1 | 2024-04-15 to 2024-04-15 |
| `ley-4-2017-flexibilidad-laboral` | Ley de Transformación y Flexibilidad Laboral (Ley 4-2017, según enmendada) | 1 | 2024-04-15 to 2024-04-15 |
| `ley-general-corporaciones` | Ley General de Corporaciones (Ley 164-2009, según enmendada) | 1 | 2025-07-31 to 2025-07-31 |

The build made 10 commits:

| Commits | Kind |
| ---: | --- |
| 10 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futuro`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 10 tags.

## Dates

Each commit is dated at noon (America/Puerto_Rico) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: The source gives only the revision date of its own copy (Rev. 15 de abril de 2024); the version is dated by that day. https://bvirtualogp.pr.gov/ogp/Bvirtual/leyesreferencia/PDF/Derechos%20Civiles/CONST/CONST.pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `8b94877b2638b5f3b86bfc840822e388a1d85075c056b58609a7c200cee43d8a` (3412860 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

10 versions of 10 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 10 history commits and 10 tags (history tip `8f71f4279fb3bff31f6af33252048fd2291e8dad`).

## Decisions made by hand

- One version only: the OGP copy dated by its own revision date (15 April 2024); history before that is not reconstructed.
- Page headers and footers of the PDF were removed; wrapped lines were joined into paragraphs; a paragraph split by a page break was rejoined.
- Language: Spanish, the official language of this text; no English official text was used.
- One version only for codigo-penal: the OGP compilation dated by its own revision date (2026-08-05); history before that is not reconstructed. Chapter and title headings and the OGP amendment notes in brackets are left out; only the articles are kept.
- One version only for codigo-civil: the OGP compilation dated by its own revision date (2026-08-21); history before that is not reconstructed. Chapter and title headings and the OGP amendment notes in brackets are left out; only the articles are kept.
- One version only for ley-transacciones-comerciales: the OGP compilation dated by its own revision date (2025-06-23); history before that is not reconstructed. Chapter and title headings and the OGP amendment notes in brackets are left out; only the articles are kept.
- One version only for reglas-procedimiento-criminal: the OGP compilation dated by its own revision date (2026-06-15); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered rules are kept.
- One version only for reglas-evidencia: the OGP compilation dated by its own revision date (2024-04-15); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered rules are kept.
- One version only for ley-80-1976-despidos: the OGP compilation dated by its own revision date (2024-04-15); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered articles are kept.
- One version only for ley-379-1948-jornada: the OGP compilation dated by its own revision date (2024-04-15); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered articles are kept.
- One version only for ley-4-2017-flexibilidad-laboral: the OGP compilation dated by its own revision date (2024-04-15); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered articles are kept.
- One version only for ley-general-corporaciones: the OGP compilation dated by its own revision date (2025-07-31); history before that is not reconstructed. Front matter, chapter and title headings and the OGP amendment notes in brackets are left out; only the numbered articles are kept.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code wrote the parser; it did not write or alter any legal text.
- none
- none
- none
- none
- none
- none
