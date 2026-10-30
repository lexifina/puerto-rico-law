# Puerto Rico: law history in git

The Constitution and core statutes of the Commonwealth of Puerto Rico as a git repository: one file per section or article, and the publisher as the commit's author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `pr/`.

**Language:** Spanish, the official language of this text. There is no English text from the same publisher.

**What is in it now**

| Folder | Law | Versions | History |
| --- | --- | ---: | --- |
| `constitucion/` | Constitución del Estado Libre Asociado de Puerto Rico | 1 | Oldest version available: the copy revised 15 April 2024 |
| `codigo-penal/` | Código Penal de Puerto Rico (Ley 146-2012, según enmendada) | 1 | Oldest version available: the OGP compilation revised 5 August 2026 |
| `codigo-civil/` | Código Civil de Puerto Rico de 2020 (Ley 55-2020, según enmendada) | 1 | Oldest version available: the OGP compilation revised 21 August 2026 |
| `ley-transacciones-comerciales/` | Ley de Transacciones Comerciales (Ley 208-1995, según enmendada) | 1 | Oldest version available: the OGP compilation revised 23 June 2025 |
| `reglas-procedimiento-criminal/` | Reglas de Procedimiento Criminal de 1963 (según enmendadas) | 1 | Oldest version available: the OGP compilation revised 15 June 2026 |
| `reglas-evidencia/` | Reglas de Evidencia de Puerto Rico de 2009 (según enmendadas) | 1 | Oldest version available: the OGP compilation revised 15 April 2024 |
| `ley-80-1976-despidos/` | Ley sobre Despidos Injustificados (Ley 80-1976, según enmendada) | 1 | Oldest version available: the OGP compilation revised 15 April 2024 |
| `ley-379-1948-jornada/` | Ley para Establecer la Jornada de Trabajo en Puerto Rico (Ley 379-1948, según enmendada) | 1 | Oldest version available: the OGP compilation revised 15 April 2024 |
| `ley-4-2017-flexibilidad-laboral/` | Ley de Transformación y Flexibilidad Laboral (Ley 4-2017, según enmendada) | 1 | Oldest version available: the OGP compilation revised 15 April 2024 |
| `ley-general-corporaciones/` | Ley General de Corporaciones (Ley 164-2009, según enmendada) | 1 | Oldest version available: the OGP compilation revised 31 July 2025 |

This is a first build, not a complete record. Each statute is one version, dated by the revision date of the OGP compilation it comes from, and credited to the publisher, not to the amending laws; the OGP says its compilations are not official and may contain inadvertent errors. Chapter and title headings, the OGP's bracketed amendment notes and the L.P.R.A. citations are left out; repealed articles are kept as a heading. The Constitution took effect on 25 July 1952 and has been amended since; no official dated earlier texts are online, so the single version is dated by the source's own revision date and credited to the publisher, not to an amending law. The other statutes of Puerto Rico (Leyes de Puerto Rico, the L.P.R.A.) are not included: the annotated code is a commercial publication and the government's free consolidations keep no past versions.

**Sources:** Oficina de Gerencia y Presupuesto (OGP), Biblioteca Virtual (bvirtualogp.pr.gov): "Constitución del Estado Libre Asociado de Puerto Rico", Rev. 15 de abril de 2024; "Código Penal de Puerto Rico" (Ley 146-2012, según enmendada), Rev. 5 de agosto de 2026; "Código Civil de Puerto Rico" de 2020 (Ley 55-2020, según enmendada), Rev. 21 de agosto de 2026; "Ley de Transacciones Comerciales" (Ley 208-1995, según enmendada), Rev. 23 de junio de 2025; "Reglas de Procedimiento Criminal" de 1963, Rev. 15 de junio de 2026; "Reglas de Evidencia de Puerto Rico" de 2009, Rev. 15 de abril de 2024; Ley 80-1976, Ley 379-1948 and Ley 4-2017, each Rev. 15 de abril de 2024 (compiled without the amendments of Ley 41-2022, which the Title III court annulled on 3 March 2023); "Ley General de Corporaciones" (Ley 164-2009, según enmendada), Rev. 31 de julio de 2025. The Código de Comercio de 1932 is not included: the OGP does not publish a text-layer copy of it, and the Ley de Transacciones Comerciales, which repealed its Articles 353 to 548, is the nearest equivalent. Rule files are named `regla-0131-1.md` for Rule 131.1; `art-0004-01.md` is Article 4.01. Text-layer PDF, converted to text; page headers and footers removed and wrapped lines joined. No other change was made to the words.

File names: `ley-transacciones-comerciales/sec-03-104.md` is Section 3-104; `codigo-penal/art-0025-a.md` is Article 25A of the Penal Code; `art-02-sec-07.md` is Article II, Section 7; `art-02-titulo.md` is the Article heading; `preambulo.md` is the Preamble.

How this repository was made is in [REPRODUCE.md](REPRODUCE.md). This repository is not legal advice; for anything that matters, read the original.
