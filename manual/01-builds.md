<!-- manual: kind=reference status=draft -->
# 1 Client generations and builds

This part names every client build the notes cover. Every other part keys its version columns off the build names in §1.1 and the schemes defined in → §0.9.

## 1.1 Build catalogue

### 1.1.1 Delphi and Java clients, 1998 to 2001

One row per executable, sorted by link date. *Compiled* is the resource-directory timestamp in local time; *Gen* is the encryption generation (→ §1.4); *Levels and saves* lists the level, map and save magics the loader compares against (→ §1.5). Default hosts and list names are in → §6.

| Archive | Release | Compiled | FileVersion | MD5 | Size | Token | Gen | Levels and saves | Source |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| zeldaonline2 | Zelda Online (Java applet) | 1997–98 | – | – | – | none | 1998 relay (→ §2.3.1) | `Z3-V1.02`/`1.03` | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 1stgraal-1 | first Delphi beta | 1998-09-06 23:54 | – | 07452f8941fdfcdce878b035156e701c | 654336 | none | 1 | Z3-V1.03/1.04 only; Graalsav1 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 2ndgraal | beta | 1998-09-16 01:33 | – | f74b35fc7975a4873087f7fd2aa1d79b | 777216 | none | 1 | + GR-V1.00–1.01; Graalsav1 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 3rdgraal | beta | 1998-09-30 01:47 | – | fc78fbc96bdbc6ca22ae56d3ed8635ab | 665600 | none | 1 | GR-V1.00–1.01; Graalsav1 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 4thgraal | beta | 1998-10-05 01:33 | – | e040af2e19912419ab80aa6dd202b4ea | 666112 | none | 1 | GR-V1.00–1.01; Graalsav1 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 4thgraalalpha | beta (alpha) | 1998-10-12 22:54 | – | 8cae23a58e1b1b10f3149bdbe53d0431 | 711680 | none | 1 | GR-V1.00–1.01; Graalsav2 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 5thgraal | beta | 1998-10-19 02:27 | – | 0e7c3573f0a916f8b2376060e768fe96 | 723968 | none | 1 | GR-V1.00–1.02; Graalsav2 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 5thgraalalpha | beta (alpha) | 1998-10-29 02:21 | – | e54397e7d4f59d30b77d5cf0475335a1 | 739840 | none | 1 | GR-V1.00–1.02; Graalsav2 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 6thgraal | beta5 | 1998-11-09 02:08 | – | 53c3caf3d930534db3f44f346f5d651a | 750080 | none | 1 | GR-V1.00–1.02; Graalsav3 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 7thgraal | beta7 | 1998-12-04 00:28 | – | deb40c31268e499fc4436b8d0687f05d | 766976 | none | 1 | GR-V1.00–1.03; Graalsav4 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 8thgraal | beta8 | 1998-12-08 01:13 | – | a49aa1b773e41741f211867fd5ea55d7 | 775680 | none | 1 | GR-V1.00–1.03; Graalsav4 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 9thgraalalpha | beta9 (alpha) | 1998-12-16 02:36 | – | e226e1b83fd437b0aede968fb395b911 | 788992 | none | 1 | GR-V1.00–1.03; Graalsav5 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 9thgraal | beta9 | 1998-12-18 01:53 | – | f0185ff8525a13f2f4e5997f649bc250 | 793088 | none | 1 | GR-V1.00–1.03; Graalsav5 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 10thgraal | V1.0 | 1998-12-22 03:24 | – | f1f34b4479a8ad7614bd8f7ce56112c6 | 795648 | none | 1 | GR-V1.00–1.03; Graalsav5 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 11thgraal | V1.0 | 1998-12-23 01:00 | – | a255212621907affc94a4483c6dfc8e3 | 795648 | none | 1 | GR-V1.00–1.03; Graalsav5 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 12thgraal | V1.0 | 1999-01-05 01:04 | – | 788ae59e9419806024d14d3e5b611971 | 794624 | none | 1 | GR-V1.00–1.03; Graalsav5 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 13thgraal | V1.1 beta1 | 1999-01-12 01:15 | – | a211a0ecf3b58daa2f46759444e18bd3 | 797184 | none | 1 | GR-V1.00–1.03; Graalsav6 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 14thgraal | V1.1 | 1999-01-15 02:20 | – | d0999d44fcd9c226f350fcf204618885 | 858112 | none | 1 | GR-V1.00–1.03; Graalsav7 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| 15thgraal | V1.1 | 1999-01-25 00:12 | – | 9a7d66dd5c8c506ad4d3e63ee4a9a1f1 | 878592 | none | 1 | GR-V1.00–1.03; Graalsav7 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal1.1.9 | V1.1.9 Gold Edition | 1999-02-11 23:50 | – | 0a6eef88acb4c0fce6e84eee3e76c04a | 882176 | none | 1 | GR-V1.00–1.03; Graalsav7/8 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal1.1 | V1.1 (readme) | 1999-02-14 23:03 | – | 1a9580655cce686c602c01daa251c453 | 882176 | none | 1 | GR-V1.00–1.03; Graalsav7/8 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal121 | V1.2.1 | 1999-05-10 18:29 | – | 8da2e8284dd8b315a28e2d4fccae79ac | 973824 | `GSERV007` | 2 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal128b2 | v1.28 beta2 | 1999-11-23 01:09 | – | 8e3c1a7233864da994a0db26f1811212 | 1196544 | `GSERV013` | 2 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal13b | v1.3 test | 1999-11-29 02:03 | – | b62aaa4d606a519e7f4689b33983429b | 1311744 | `GSERV014` | 2 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal131 | V1.31 | 1999-12-07 02:56 | – | bff87a95a34399b2d35b243f281169a7 | 1318400 | `GSERV016` | 2 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal132 | V1.32 | 2000-01-12 01:13 | – | 42b2596af4b75bcf82db03e0fc274f7d | 1328128 | `GSERV018` | 2 | GR-V1.00–1.03; reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal3d | Graal3D | 2000-02-05 01:57 | – | 305c985a020cec6ab8d81ac95d447343 | 605184 | none | own (→ §9) | none | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal133 | V1.33 | 2000-02-21 00:36 | – | a3667ce55a5c67cf025882014b9540b0 | 1350144 | `GNW20020` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal134 | V1.34 | 2000-03-23 00:38 | – | 9e403616e73a6079ac37d65d475c81cd | 1349632 | `GNW22030` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal135 | V1.35 | 2000-04-13 23:17 | – | fe9d99c4bf6e6bc9b1b127823f39646f | 1389568 | `GNW13040` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal136 | V1.36 | 2000-05-12 17:34 | – | 018f51662c7c8862cafb9bfbd14dea41 | 1399296 | `GNW10050` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal137 | V1.37 | 2000-05-23 02:40 | 1.3.7.0 | 5e966a9d1a079af6d682b2618674edb1 | 1401344 | `GNW21050` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal138 | V1.38 | 2000-06-23 22:11 | 1.3.8.0 | 4401f7d02966af709c2df662cebe34a1 | 1426432 | `GNW22060` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal139 | V1.39 | 2000-08-07 02:49 | 1.3.8.0 | 62513ab884f1802a0bcd8114abe349b9 | 1448960 | `GNW07080` | 2 | GR-V1.00–1.03; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal_gr1411 | V1.41 rev1 (<graalin-site>-patched copy) | – (resource stamp missing) | 1.4.1.1 | a97740e711ffe9b698ec03712d4c06af | 1506816 | `GNW13110` | 3 | GR-V1.00–1.03, GLEVNW01; carries Graalsav9/Graalsv10/Graalsv11 (string scan) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graalnm24 | NewMain client (1.42 notes) | 2001-01-10 19:55 | 1.4.1.1 | 229f05de7a43b98e223d8e1b58bffc63 | 1783296 | `GNW08011` | 3 | GR-V1.00–1.03, GLEVNW01 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graalnm26 | NewMain client (1.42 notes) | 2001-01-12 21:19 | 1.4.1.1 | 22a08ed154f67948e01b969b68cdb05e | 1784320 | `GNW08011` | 3 | GR-V1.00–1.03, GLEVNW01 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.0 | v2.00 | 2001-02-01 14:54 | 2.0.0.0 | c93e659e2cda36379aaea4706db20b38 | 1812480 | `GNW24011` | 3 | GR-V1.00–1.03 (no `.nw`) | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.0-rev1 | v2.00 rev1 | 2001-02-02 19:19 | 2.0.0.1 | 30bd230e578d3a347866a87060efec20 | 1812992 | `GNW24011` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.0-rev2 | v2.00 rev2 | 2001-02-05 02:32 | 2.0.0.2 | fc4bb7e3b7ca9cd8ea6693a033635534 | 1815040 | `GNW24011` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.0-rev3 | v2.00 rev3 | 2001-02-07 01:05 | 2.0.0.3 | 1ce5c1662b65246ae1c6559af5ff71f0 | 1815040 | `GNW24011` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| GraalX (`.rar`, separate upload) | 2.01-era side build | 2001-03-07 21:40 | 2.0.0.3 | d3ee52ef9d22a0d99b154b47c5f56f60 | 1821696 | `GNW23021` | 3 | GR-V1.00–1.03, **GLEVNW01** | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.01 | v2.01 | 2001-03-08 14:59 | 2.0.1.0 | 08340a8868f1d11e0285cc70e51200fe | 1815552 | `GNW23021` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.01-rev1 | v2.01 rev1 | 2001-03-15 21:10 | 2.0.1.0 | 010a32afce66729b838258809a97c0d9 | 1815552 | `GNW23021` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.02 | v2.02 | 2001-04-15 20:48 | 2.0.2.0 | 60018a19ef671c506743826728c49718 | 1808384 | `GNW15041` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.02-rev1 | v2.02 rev1 | 2001-04-15 23:16 | 2.0.2.0 | e06ff79aded885a223b933617d456577 | 1808896 | `GNW15041` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.02-rev2 | v2.02 rev2 | 2001-04-20 18:48 | 2.0.2.2 | 993a1829dbb6acaa2b46063f5efe636c | 1807872 | `GNW20041` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.03 | v2.03 | 2001-05-07 15:31 | 2.0.3.0 | 36972c74baad09ceb33dad94b0eb1e33 | 1836032 | `GNW06051` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.04 | v2.04 | 2001-06-25 07:42 | 2.0.4.0 | a40608308d4f890cb5e4efdd45b38ba4 | 1872384 | `GNW24061` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.05 | v2.05 | 2001-08-03 19:12 | 2.0.4.0 (stale) | 9abce477945a1307bb2be9ed47d2f170 | 1891328 | `GNW03081` | 3 | GR-V1.00–1.03, **GLEVNW01, GRMAP001** | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.05-rev1 | v2.05 rev1 | 2001-08-04 03:26 | 2.0.5.0 | 2780f2f370396c580e1648696698c871 | 1895936 | `GNW03081` | 3 | as above | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graalnwb1 | NewWorld beta 1 | 2001-08-06 04:13 | 2.0.5.0 | 88d1f84c96da1dcc3942b139fbd741c9 | 1820672 | `G2N15041` | 3 | as 2.05 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| Graal-v2.05-rev2 | v2.05 rev2 | 2001-08-16 17:24 | 2.0.5.2 | f3fdf54d943fa91c89acba5bb695db99 | 1891840 | `GNW03081` | 3 | as 2.05 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal21test2 | v2.1 test 2 | 2001-09-21 17:54 | 2.1.0.0 | d15d877822ad4145578107857c90fb3c | 1748480 | `GNW03081` | 3 | as 2.05 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graal21test3 | v2.1 test 3 | 2001-09-27 21:11 | 2.1.0.0 | 2116a7ba03648dcc004035534ec94de8 | 1753600 | `GNW03081` | 3 | as 2.05 | [bin][file] (client-internals/build-catalogue.md#catalogue) |
| graalnwb2 | NewWorld beta 2 | 2001-10-03 20:46 | 2.1.0.0 | af2d21066659bed6af6c77e52b2cc0e1 | 1613824 | `G2N15041` | 3 | as 2.05 | [bin][file] (client-internals/build-catalogue.md#catalogue) |

Notes on the catalogue:

- The "Nth graal" archive names are not chronological: 4thgraalalpha and 5thgraalalpha were linked after their namesakes and 9thgraalalpha before 9thgraal; graal1.1 has the same size as graal1.1.9 but was linked three days later [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).
- FileVersion exists only from 1.37 on and is sometimes stale (2.05 says 2.0.4.0; 1.39 says 1.3.8.0) [bin] (client-internals/build-catalogue.md#how-each-column-was-read).
- The only 1.41 copy (graal_gr1411) is patched by a third party: its resource timestamp is zeroed and its list host and port may not be the original values; the token and code-level facts look untouched [bin][inf] (client-internals/build-catalogue.md#patterns-worth-knowing).
- GraalX is 2.01 with the GLEVNW01 reader and writer kept in: 6350 functions identical to 2.01, 7 differing, and the same command table and packet and prop ids [bin] (client-internals/build-catalogue.md#graalx).
- graal_v2.05 rev 2 is the same file as `Graal_v2.05_rev2.exe`, the main decompile target of the notes [bin] (client-internals/build-catalogue.md#catalogue).

### 1.1.2 Compilers

| Builds | Compiler | Evidence | Source |
| --- | --- | --- | --- |
| all Delphi builds | Borland Delphi, linker 2.25, DelphiX for DirectDraw, RTL copyright "1983,97 Borland" | PE header and RTL strings | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 2nd Graal; 1.28 beta 2 and later | Delphi 4 | Delphi 3+ class-metadata layout (self pointer 76, name 44 bytes before the VMT) and `TMultiReadExclusiveWriteSynchronizer` linked | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 1st Graal; 3rd Graal to 1.1.9; 1.21 | disputed → App. E#1 | Delphi 2 class-metadata layout (64 and 32 bytes) but a 1997 RTL string | [bin][inf] (client-internals/build-catalogue.md#patterns-worth-knowing) |

### 1.1.3 Companion executables in the 1998 to 2001 archives

| Archive | File | Compiled | MD5 | Token | Port | Source |
| --- | --- | --- | --- | --- | --- | --- |
| graal1.1.9 | Gserver.exe | 1999-01-22 | 7882dba6ebb2ab1026de260c3043fa47 | none | 14802 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal121 | GServer.exe | 1999-05-09 | bfcdaae0217d953124a9b21ff7858967 | GSERV007 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal121 | remotecontrol.exe | 1999-05-10 | 5932d6baa08289a65515342dfc4b9f5a | GSERV007 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal128b2 | GServerv.exe | 1999-11-22 | 8d6bff85bda6e6c9558503afa6b7259d | accepts GSERV007–013 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal128b2 | RemoteControl1.28.exe | 1999-10-20 | d7150d1385ea11b812d10d30212f9757 | GSERV011 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal13b | GServer13.exe | 1999-11-29 | d1d0470e53a60b8f000b9ea5da9d37b6 | accepts GSERV007–014 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal13b | RemoteControl13.exe | 1999-11-29 | 1f2c19ab385c8b8af6236197f98ad735 | GSERV011 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graal3d | GServer.exe | 2000-02-05 | aab1a34a1f196d4f4fddf12112ccbf52 | none | 14901 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graalnm24/26 | RemoteControl-NewMain.exe | 2001-01-08 | bc2b8a2e80acc09a6bb418970cff5a64 | GSERV021 | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graalnwb1 | RemoteControl-NW.exe | 2001-05-22 | 6fe24bdd4e135900fc40d7fb70bdcdd2 | – | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |
| graalnwb2 | RemoteControl-NW.exe | 2001-08-27 | ce454437af8880f61ac2173b0bd11047 | – | 14804 | [bin] (client-internals/build-catalogue.md#other-executables-in-the-archives) |

The archives also hold gif2mng, GraalShop, GraalLevelGen and GraalLevelGenNW, NPCControl, LevelFiller with levelviewer, TerrainGenerator, PNGView, YoshiChess and Greaditor [file] (client-internals/build-catalogue.md#other-executables-in-the-archives). Their formats and behaviour are in → §11.

### 1.1.4 Later builds

Builds after 2001 are known from their tokens, lab runs and static reads; there is no per-build hash catalogue for them in the notes. Tokens are in → §1.2.

| Build | Token | Source |
| --- | --- | --- |
| 2.1.0.0 to 2.1.0.3 | GNW31101 | [doc] (client-internals/version-tokens.md) |
| 2.1.4.0 (first with server-list tabs) | GNW30042 | [doc] (client-internals/version-tokens.md) |
| 2.1.7.0, 2.1.7.1 (2.171, `Graal_2171.exe`) | GNW22122 | [bin][cap] (client-internals/version-tokens.md) |
| 2.1.9.0 (bz2 and new encryption) | GNW15053 | [doc] (client-internals/version-tokens.md) |
| 2.2.1.1 (extra compression byte) | GNW01113 | [doc] (client-internals/version-tokens.md) |
| 2.22 (`Graal_222.exe`) | GNW03014 | [bin][cap] (client-internals/version-tokens.md) |
| 2.3.0.0 | GNW14015 | [doc] (client-internals/version-tokens.md) |
| 2.31 (`Graal_231.exe`; editor separate, editor FileVersion 2.3.1.1) | GNW28015 | [bin][cap] (client-internals/version-tokens.md) |
| Linux 3.04 (Torque rewrite, 2.22 protocol) | G3D03014 | [bin][cap] (client-internals/version-tokens.md) |
| Mac OS X 3.153 (2.31 protocol) | G3D28015 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 4.04r2 (`GraalEngine.dll`, March 2006) | G3D17026 | [bin][cap] (client-internals/version-tokens.md) |
| Mac OS X 4.20r6 | G3D27076 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 4.20r8 (`GraalEngine.dll`) | G3D20126 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 5.00r7 (engine DLL, Jul 2007) | G3D22067 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 5.12 | G3D14097 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 6.00 beta1 | G3D03048 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 6.00 beta2, 5.24r3, 5.24r4 | G3D15010 | [bin][cap] (client-internals/version-tokens.md) |
| Windows 5.30r3, 5.31r4, 6.00r2, 6.00r4 | G3D26090 | [bin][cap] (client-internals/version-tokens.md) |
| Linux 6.01r1 | G3D0108A | [bin][cap] (client-internals/version-tokens.md) |
| Windows 6.03r7 | G3D0311C | [bin][cap] (client-internals/version-tokens.md) |
| Linux 6.03r7 | G3D0511C | [bin][cap] (client-internals/version-tokens.md) |

From 2.3 the editor and the online client are separate executables [doc] (client-internals/version-tokens.md). Graal3D (2000) is a separate client with its own server and no Graal level loaders [bin] (client-internals/build-catalogue.md#catalogue); it is described in → §9.

## 1.2 Version tokens

The version token is the eight-character string a client sends in its login (→ §2.3).

### 1.2.1 Token schemes

| Scheme | Form | Builds | Rule | Source |
| --- | --- | --- | --- | --- |
| none | — | 1998 betas to 1.1.9 | no token is sent | [bin] (client-internals/build-catalogue.md#catalogue) |
| protocol revision | `GSERV` + 3 digits | 1.21 to 1.32, RC to Jan 2001 | the number is a protocol revision: 007 (1.21), 011 (RC 1.28), 013 (1.28b2), 014 (1.3 test), 016 (1.31), 018 (1.32), 021 (RC-NewMain) | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| build date | `GNW` + DDMMY | 1.33 to 2.31 | DD day, MM month, Y last digit of the year; the date is on or a few days before the link date | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) ; [inf] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#reading-the-digits-inferred) |
| NewWorld | `G2N` + DDMMY | NewWorld betas 1 and 2 | same date form | [bin] (client-internals/build-catalogue.md#catalogue) |
| 3D era | `G3D` + date digits | 3.x to 6.x | the 3.x tokens carry the same date stamps as their 2.x protocol twins (G3D03014 and GNW03014); later suffixes include hex-like letters (G3D0311C, G3D0108A) | [bin] (client-internals/version-id-map.md#protocol-token--version); [cap] (client-internals/version-tokens.md) |

A revision that does not change the protocol keeps the previous token: 2.0 rev1 to rev3, 2.01 rev1, 2.02 rev1, 2.05 rev1 and rev2, and the 2.1 test builds, which still send the 2.05 token GNW03081 [bin] (client-internals/build-catalogue.md#patterns-worth-knowing). Among those revisions only 2.02 rev2 changes the token, and it also adds the `PLI_LANGUAGE` send after login [bin] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#what-changed-in-the-login-function-between-revisions); [bin] (client-internals/decomp-findings-2026-10-24-c/version_tokens.tsv). From 1.38 the token is built one character at a time in code rather than stored as a string literal [bin] (client-internals/build-catalogue.md#how-each-column-was-read).

A server accepts a range of tokens rather than one: GServer 1.28 accepts GSERV007 to GSERV013 and GServer13 accepts GSERV007 to GSERV014 [bin] (client-internals/build-catalogue.md#patterns-worth-knowing). A lab GServer-v2 admits a client when its token is in the allowed-versions list, which for 2.00 is a configuration entry, not a code change [lab] (client-internals/version-tokens.md). Server-side token handling is in → §5.4.

### 1.2.2 Token table

| Token | Build | Source |
| --- | --- | --- |
| `GSERV007` | 1.21 | [bin] (client-internals/build-catalogue.md); [srv] (client-internals/version-id-map.md) |
| `GSERV009` | 1.25 | [srv] (client-internals/version-id-map.md#full-gs2lib-client-token-table-2026-10) |
| `GSERV011` | 1.27; RemoteControl 1.28 and 1.3 | [srv] (client-internals/version-id-map.md); [bin] (client-internals/build-catalogue.md) |
| `GSERV013` | 1.28 beta 2 | [bin] (client-internals/build-catalogue.md) |
| `GSERV014` | 1.3 test (1.30) | [bin] (client-internals/build-catalogue.md) |
| `GSERV016` | 1.31 | [bin] (client-internals/build-catalogue.md) |
| `GSERV018` | 1.32 | [bin] (client-internals/build-catalogue.md) |
| `GSERV021` | RemoteControl-NewMain | [bin] (client-internals/build-catalogue.md) |
| `GNW20020` | 1.33 | [bin] (client-internals/build-catalogue.md) |
| `GNW22030` | 1.34 | [bin] (client-internals/build-catalogue.md) |
| `GNW13040` | 1.35 | [bin] (client-internals/build-catalogue.md) |
| `GNW10050` | 1.36 | [bin] (client-internals/build-catalogue.md) |
| `GNW21050` | 1.37 | [bin] (client-internals/build-catalogue.md) |
| `GNW22060` | 1.38 | [bin] (client-internals/build-catalogue.md); [bin] (client-internals/version-tokens.md) |
| `GNW07080` | 1.39 | [bin] (client-internals/build-catalogue.md); [bin] (client-internals/version-tokens.md) |
| `GNW12080` | 1.391 | [srv] (client-internals/version-id-map.md) |
| `GNW13110` | 1.41 rev1 | [bin] (client-internals/build-catalogue.md); [file] (client-internals/version-id-map.md) |
| `GNW08011` | NewMain client (1.42 notes) | [bin] (client-internals/build-catalogue.md) |
| `GNW24011` | 2.00, rev1 to rev3 | [bin] (client-internals/version-tokens.md) |
| `GNW23021` | 2.01, 2.01 rev1, GraalX | [bin] (client-internals/version-tokens.md); [bin] (client-internals/build-catalogue.md) |
| `GNW15041` | 2.02, 2.02 rev1 | [bin] (client-internals/version-tokens.md) |
| `GNW20041` | 2.02 rev2 | [bin] (client-internals/version-tokens.md) |
| `GNW06051` | 2.03 | [bin] (client-internals/version-tokens.md) |
| `GNW24061` | 2.04 | [bin] (client-internals/version-tokens.md) |
| `GNW03081` | 2.05, rev1, rev2; 2.1 test 2 and 3 | [bin] (client-internals/version-tokens.md) |
| `G2N15041` | NewWorld betas 1 and 2 | [bin] (client-internals/build-catalogue.md) |
| `GNW31101` | 2.1 (2.1.0.0 to 2.1.0.3) | [srv] (client-internals/version-id-map.md); [doc] (client-internals/version-tokens.md) |
| `GNW01012` | 2.12 | [srv] (client-internals/version-id-map.md) |
| `GNW23012` | 2.13 | [srv] (client-internals/version-id-map.md) |
| `GNW30042` | 2.14 (2.1.4.0) | [srv] (client-internals/version-id-map.md); [doc] (client-internals/version-tokens.md) |
| `GNW19052` | 2.15 | [srv] (client-internals/version-id-map.md) |
| `GNW20052` | 2.151 | [srv] (client-internals/version-id-map.md) |
| `GNW12102` | 2.16 | [srv] (client-internals/version-id-map.md) |
| `GNW22122` | 2.17 (2.1.7.0, 2.1.7.1) | [srv] (client-internals/version-id-map.md); [cap] (client-internals/version-tokens.md) |
| `GNW21033` | 2.18 | [srv] (client-internals/version-id-map.md) |
| `GNW15053` | 2.19 (2.1.9.0) | [srv] (client-internals/version-id-map.md); [doc] (client-internals/version-tokens.md) |
| `GNW28063` | 2.2 | [srv] (client-internals/version-id-map.md) |
| `GNW01113` | 2.21 (2.2.1.1) | [srv] (client-internals/version-id-map.md); [doc] (client-internals/version-tokens.md) |
| `GNW03014` | 2.22 (2.2.2.0) game login | [srv] (client-internals/version-id-map.md); [bin] (client-internals/version-tokens.md) |
| `GNW14015` | 2.3 (2.3.0.0) | [srv] (client-internals/version-id-map.md) |
| `GNW28015` | 2.31 (2.3.1.0) game login | [srv] (client-internals/version-id-map.md); [cap] (client-internals/version-tokens.md) |
| `GNW30123` | listserver hello of 2.22 and 2.31, sent with `newmain`; not a game build (→ §6) | [bin][lab] (client-internals/version-tokens.md) |
| `G3D16053` | 3.0 | [srv] (client-internals/version-id-map.md) |
| `G3D27063` | 3.01 | [srv] (client-internals/version-id-map.md) |
| `G3D03014` | Linux 3.04 rev 1 (3.041) | [bin] (client-internals/version-id-map.md) |
| `G3D28015` | Mac OS X 3.153 | [bin] (client-internals/version-id-map.md) |
| `G3D30123` | 3.x listserver login | [bin] (client-internals/version-id-map.md) |
| `G3D17026` | Windows 4.04r2 | [bin] (client-internals/version-id-map.md) |
| `G3D27076` | Mac OS X 4.20r6 | [bin] (client-internals/version-id-map.md) |
| `G3D20126` | Windows 4.20r8 | [bin] (client-internals/version-id-map.md) |
| `G3D22067` | Windows 5.00r7 | [bin] (client-internals/version-tokens.md) |
| `G3D14097` | Windows 5.12 | [cap] (client-internals/version-tokens.md) |
| `G3D03048` | Windows 6.00 beta1 | [cap] (client-internals/version-tokens.md) |
| `G3D15010` | Windows 6.00 beta2, 5.24r3, 5.24r4 | [cap] (client-internals/version-tokens.md) |
| `G3D26090` | Windows 5.30r3, 5.31r4, 6.00r2, 6.00r4 | [cap] (client-internals/version-tokens.md) |
| `G3D0108A` | Linux 6.01r1 | [cap] (client-internals/version-tokens.md) |
| `G3D0311C` | Windows 6.03r7 | [cap] (client-internals/version-tokens.md) |
| `G3D0511C` | Linux 6.03r7 | [cap] (client-internals/version-tokens.md) |

The older GServer-v2 version table writes the 1.33 to 1.38 tokens without the leading `G` (`NW20020` and so on) [srv] (client-internals/version-id-map.md#full-gs2lib-client-token-table-2026-10). The gs2lib table lists `G3D28095` and later for 4.x and up without per-build rows [srv] (client-internals/version-id-map.md#full-gs2lib-client-token-table-2026-10).

## 1.3 Version ids

Server code identifies a client by an internal version id; ids sort, so 2.05 rev 2 sorts below 2.1 [srv] (client-internals/version-id-map.md#protocol-token--version).

| Version id | Build | Token | Source |
| --- | --- | --- | --- |
| `CLVER_1_39` | 1.39 | `GNW07080` | [srv] (client-internals/version-id-map.md#protocol-token--version) |
| `CLVER_2_052` | 2.05 rev 2; sorts below CLVER_2_1 | `GNW03081` | [srv] (client-internals/version-id-map.md#protocol-token--version) |
| `CLVER_2_17` | 2.17 | `GNW22122` | [srv] (client-internals/version-id-map.md#protocol-token--version) |
| `CLVER_2_22` | 2.22 | `GNW03014` | [srv] (client-internals/version-id-map.md#protocol-token--version) |
| `CLVER_2_31` | 2.31 | `GNW28015` | [srv] (client-internals/version-id-map.md#protocol-token--version) |

The notes give version ids only for the builds above; ids for other builds are unmeasured [srv] (client-internals/version-id-map.md#protocol-token--version).

## 1.4 Encryption generation by build

| Gen | Builds | How it was determined | Source |
| --- | --- | --- | --- |
| 1 | 1st Graal to 1.1.9 | no zlib linked, no decompression-error option | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 2 | 1.21 to 1.39 | zlib 1.0.4 linked; the 1.2 notes say "packet compression"; `nodecompressionerror` from 1.28b2 | [bin][doc] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 3 | 1.41 rev1, NewMain 1.42, 2.00 to 2.05, 2.1 tests, NewWorld betas, 2.17 | the connection initialiser seeds the insertion LCG and draws a 7-bit key; 1.39 lacks it | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing); [bin] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| 4 | 2.19 to 2.21 and 3.0 to 3.01 (client type 4) | server source | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| 5 | 2.22 and later (client type 5); RemoteControl as type 6 | server source; 2.22 and 2.31 send type 5 | [srv][bin] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| 6 | v6 | not implemented in the server source the notes summarise | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| own | Graal3D | own protocol | [bin] (client-internals/build-catalogue.md#catalogue) |

The schemes themselves are defined in → §2.2. Generations of the 3.x to 6.x clients beyond these rows are in → §2.3.

## 1.5 Level-format generation by build

| Builds | Level and map magics read | Save magic | Source |
| --- | --- | --- | --- |
| Zelda Online (Java) | Z3-V1.02, Z3-V1.03 | n/a | [bin] (client-internals/build-catalogue.md#catalogue) |
| 1st Graal | Z3-V1.03, Z3-V1.04 | Graalsav1 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 2nd Graal to 4th Graal | + GR-V1.00, GR-V1.01 | Graalsav1 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 4thgraalalpha | GR-V1.00 to GR-V1.01 | Graalsav2 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 5th Graal, 5thgraalalpha | GR-V1.00 to GR-V1.02 | Graalsav2 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 6th Graal | GR-V1.00 to GR-V1.02 | Graalsav3 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 7th, 8th Graal | GR-V1.00 to GR-V1.03 | Graalsav4 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 9th Graal to 12th Graal (1.0) | GR-V1.00 to GR-V1.03 | Graalsav5 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 13th Graal | GR-V1.00 to GR-V1.03 | Graalsav6 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 14th, 15th Graal | GR-V1.00 to GR-V1.03 | Graalsav7 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 1.1.9, 1.1 | GR-V1.00 to GR-V1.03 | Graalsav7/8 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 1.21 to 1.39 | GR-V1.00 to GR-V1.03 | reads Graalsav9, Graalsv10, Graalsv11; writes Graalsv11 | [bin] (client-internals/build-catalogue.md#catalogue) |
| 1.41 rev1, NewMain 1.42 | GR-V1.00 to GR-V1.03, GLEVNW01 | as 1.21 (1.41 rev1); unmeasured (NewMain) | [bin] (client-internals/build-catalogue.md#catalogue) |
| 2.00 to 2.04 | GR-V1.00 to GR-V1.03 (no GLEVNW01, no GRMAP001) | unmeasured | [bin] (client-internals/build-catalogue.md#catalogue) |
| GraalX | GR-V1.00 to GR-V1.03, GLEVNW01 | unmeasured | [bin] (client-internals/build-catalogue.md#catalogue) |
| 2.05 and later 2001 builds | GR-V1.00 to GR-V1.03, GLEVNW01, GRMAP001 | unmeasured | [bin] (client-internals/build-catalogue.md#catalogue) |

GR-V1.03 is the last `.graal` revision any catalogued build reads [bin] (client-internals/build-catalogue.md#catalogue). `.nw` support is not monotonic: 1.41 rev1 and NewMain 1.42 read GLEVNW01, 2.00 to 2.04 contain neither GLEVNW01 nor GRMAP001, and both return in 2.05 [bin] (client-internals/build-catalogue.md#patterns-worth-knowing). That 2.0 branched from a pre-NewMain tree is an inference from strings [inf] (client-internals/build-catalogue.md#patterns-worth-knowing). The 2.05 string table holds exactly Z3-V1.03, Z3-V1.04, GR-V1.00 to GR-V1.03 and GLEVNW01 as level magics [2.05] (formats/level-binary.md). The save writer was traced only in 1.21 and 1.32; for 1.33 to 1.41 rev1 the save magics are inferred from the same string arrangement [bin][inf] (client-internals/build-catalogue.md#patterns-worth-knowing). The formats themselves are in → §3.1, → §3.2 and → §3.7.

## 1.6 Era timeline

The manual groups builds into thirteen eras. Inside an era the clients share their engine and wire format [bin] (version-profiles/matrix/README.md#eras). An era letter is a heading aid; facts stay attached to builds (→ §0.9).

| Era | Builds | Dates | Engine | Source |
| --- | --- | --- | --- | --- |
| Z | Zelda Online 1 and 2 (Java applets), GServ Standalone | May to Jul 1998 | Java | [bin][doc] (version-profiles/matrix/README.md#eras) |
| A | 1st Graal to 1.1.9 Gold (20 builds) | Sep 1998 to Feb 1999 | Delphi 2-level compiler (2nd Graal: Delphi 4), DelphiX | [bin][doc] (version-profiles/matrix/README.md#eras) |
| B | 1.21, 1.28 beta 2, 1.3 test, 1.31, 1.32 | May 1999 to Jan 2000 | Delphi 4 from 1.28b2, DelphiX | [bin][doc] (version-profiles/matrix/README.md#eras) |
| 3D0 | Graal3D | Feb 2000 | Delphi, DelphiX Direct3D retained mode | [bin][doc] (version-profiles/matrix/README.md#eras) |
| C | 1.33 to 1.39 | Feb to Aug 2000 | Delphi 4, DelphiX | [bin][doc] (version-profiles/matrix/README.md#eras) |
| D | 1.41 rev1 | Nov 2000 | as C | [bin][doc] (version-profiles/matrix/README.md#eras) |
| E | NewMain 1.42, 2.00 to 2.05 rev2, 2.1 tests, NewWorld betas | Jan to Oct 2001 | as C, plus DirectDraw 7 | [bin][doc] (version-profiles/matrix/README.md#eras) |
| F | 2.1 to 2.17 (only 2.17.1 survives as a binary) | Oct 2001 to 2002 | as E, BASS audio from 2.17 at the latest | [bin][doc] (version-profiles/matrix/README.md#eras) |
| G | 2.22, 2.3 (no binary), 2.31 | 2004 to 2005 | as F | [bin][doc] (version-profiles/matrix/README.md#eras) |
| H | 3.04 Linux, 3.153 Mac | 2004 to 2005 | C++ on the Torque Game Engine | [bin][doc] (version-profiles/matrix/README.md#eras) |
| I | 4.04r2, 4.20r6, 4.20r8 | 2006 to 2007 | Delphi launcher + C++ `GraalEngine.dll` (+ `Graal3DEngine.dll`) | [bin][doc] (version-profiles/matrix/README.md#eras) |
| J | 5.00r7, 5.12; then 5.24 to 5.31 | 2007 to 2011 | 5.00 and 5.12 as I; from 5.24 one MSVC executable | [bin][doc] (version-profiles/matrix/README.md#eras) |
| K | 6.00 betas to 6.03r7, 6.11 Mac | 2010 to 2014 | one native C++ program per platform, no Torque layer | [bin][doc] (version-profiles/matrix/README.md#eras) |

| Change | Between | Source |
| --- | --- | --- |
| largest single code step: about 800 more functions, partly new DirectDraw 7 and grid library code | 1.41 rev1 and NewMain 1.42 | [bin] (client-internals/cross-version-timeline.md#function-maps-onto-205-rev2) |
| NewWorld beta 1 cut from the 2.05 code base; NewWorld beta 2 cut from the 2.1 test code base | 2001 | [bin] (client-internals/cross-version-timeline.md#classes) |
| 2.1 test builds are a later branch of the 2.05 code: more functions than 2.05 but fewer unique to 2.05 rev2 | Sep 2001 | [bin][inf] (client-internals/cross-version-timeline.md#function-maps-onto-205-rev2) |

Era-by-era wire, scripting and id-set differences are tabulated in → App. C.

## 1.7 Precursors and side builds

These builds sit around the Delphi client line. The uploads hold 9 distinct items under 14 names [file] (client-internals/precursors-and-fan-builds.md#what-the-uploads-are).

| Date | Build | What it is | Source |
| --- | --- | --- | --- |
| 1998-05 | Zelda Online 1 | Java 1.0 applet, single player, no socket code; `Z3-V1.02` and `Z3-V1.03` levels, start `level1.zelda` | [bin] (client-internals/precursors-and-fan-builds.md#zelda-online-1-may-1998) |
| 1998-07 | Zelda Online 2 "local version" | Java 1.1 application with one-player and multiplayer modes, the GServ Standalone lobby on 14801 and the author's commented source; 51 `Z3-V1.03` levels | [src] (client-internals/precursors-and-fan-builds.md#zelda-online-2-local-version-july-1998) |
| 1998-07 | ZeldaEditor | Delphi 3 level editor; writes only `Z3-V1.03` | [bin] (client-internals/precursors-and-fan-builds.md#zeldaeditor-july-1998) |
| 1999-09 | Graal Game Boy Color demo | homebrew by the Graal author, built with GBDK 2.x; header title `GRAAL`, MBC1, 256 KB ROM of which banks 0 to 5 are used | [bin] (client-internals/precursors-and-fan-builds.md#graal-game-boy-color-demo-1999); [bin] (client-internals/gameboy-demo.md#header-and-bank-map) |
| 2000-07 | Java Graal | Zelda Online 2's game and client with Graal art, reading `GR-V1` levels; relay on 14802 (→ §2.3.1.3) | [bin][src] (client-internals/precursors-and-fan-builds.md#java-graal-july-2000) |
| 2001-03 | GraalX | a 2.01 pre-release that keeps the `.nw` reader and writer (→ §1.1.1) | [bin] (client-internals/precursors-and-fan-builds.md#graalx) |
| 2014-04 | 39ster client 1.00 | an offline fan remake on an SDL engine with GameMonkey script; reads `.nw` and `GR-V1.00` to `1.03`; NPC scripts are not run | [bin] (client-internals/precursors-and-fan-builds.md#39sters-graal-client-100-2014) |

| Rule | Source |
| --- | --- |
| 1st Graal grew out of ZeldaEditor: it carries the editor's sign, link, object-name and sign-code dialogs under the same class names; the baddy dialog and the main form were renamed | [bin] (client-internals/precursors-and-fan-builds.md#zeldaeditor-july-1998) |
| The Graal sign alphabet (→ §3.6) is already in Zelda Online 1 | [bin] (client-internals/precursors-and-fan-builds.md#zelda-online-1-may-1998) |
| Zelda Online 2's options hold a 10-character save code of 60 bits (position, level index, rupees, darts, power, item and story bits, a 6-bit count of set bits), XORed with a fixed mask and transposed before writing | [src] (client-internals/precursors-and-fan-builds.md#password-saves) |
| ZeldaEditor's `objects.dat` stamp list: a name line, one width byte and one height byte, then width × height 32-bit little-endian tile ids; tile 2047 is transparent; 105 stamps in 1998, and Graal 1.21 ships the same format | [bin] (client-internals/precursors-and-fan-builds.md#objectsdat-stamps) |
| The Java games read `arrays.dat` in the same header form as the Delphi clients (→ §3.5.3), in a fixed order of 14 lists | [src] (client-internals/precursors-and-fan-builds.md#shared-java-game-data) |
| Java Graal reads `GR-V1` NPC lines but shows only the image, dropping the script, and skips the chest section | [src] (client-internals/precursors-and-fan-builds.md#level-format-as-the-java-code-reads-it) |
| Zelda Online, the Java client of 1997–98, keeps text-line relay traffic on port 14801 (→ §2.3.1) | [bin] (client-internals/zelda-online-1998.md#server-protocol-text-lines-port-14801) |

### 1.7.1 Behaviour of the Java precursors

Zelda Online 2 and Java Graal share one engine, and every number below is the same in both [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal).

| What | Value | Source |
| --- | --- | --- |
| main loop | 50 ms per tick (20 Hz) | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| walk | half a tile per tick while a key is held; a quarter step sideways around a block corner | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| sword | 5 ticks, hits tested on ticks 1 to 3 | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| hurt | 40 ticks, half a heart | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| pushing a wall | push pose and ledge check from tick 18 (0.9 s); a push stone moves at tick 28 (1.4 s); the counter loops from 38 back to 18 | [src][live] (client-internals/precursor-runs-2026-10-30.md#walking-into-a-wall) |
| bush drop | one roll of 0 to 99: 25 % a green rupee, 5 % a heart, 2 % five rupees, else nothing; a lifted bush rolls the same | [src] (client-internals/precursor-runs-2026-10-30.md#bushes-stones-and-pots) |
| regrowth | none during a visit; every board change is cleared when the level loads | [src] (client-internals/precursor-runs-2026-10-30.md#bushes-stones-and-pots) |
| carrying | the player is drawn with carry sprites and the object above the head, not hidden under it | [src] (client-internals/precursor-runs-2026-10-30.md#bushes-stones-and-pots) |
| chat | bold serif black text with a one-pixel white offset, above the head, with no bubble; the nickname is drawn the same way under the feet | [src][live] (client-internals/precursor-runs-2026-10-30.md#chat) |

### 1.7.2 The Game Boy Color demo

| Rule | Source |
| --- | --- |
| No title screen and no HUD: the ROM goes from the Nintendo logo to room 0; a sign there reads as a welcome from the author | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator); [bin] (client-internals/precursors-and-fan-builds.md#graal-game-boy-color-demo-1999) |
| Seven rooms of 32 × 32 tiles in banks 4 and 5; their links use the PC level link record with a room number for the file name | [bin] (client-internals/gameboy-demo.md#room-format) |
| Select opens a carousel over a table of 31 character types, and the pick changes the player at once | [bin][live] (client-internals/precursor-runs-2026-10-30.md#game-boy-color-demo-in-an-emulator) |
| The text font runs space, A–Z, a–z, 0–9, then punctuation, from byte 32; it is not the PC sign alphabet | [bin] (client-internals/precursors-and-fan-builds.md#graal-game-boy-color-demo-1999) |
| Start mutes the game; the music format is open | [live] (client-internals/precursor-runs-2026-10-30.md#open) |
