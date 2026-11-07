<!-- manual: kind=reference status=draft -->
# 1 Client generations and builds

This part names every client build the notes cover. Every other part keys its version columns off the build names in §1.1 and the schemes defined in → §0.9.

## 1.1 Build catalogue

### 1.1.1 Delphi and Java clients, 1998 to 2001

Most 1998 to 2001 executables come from one shared archive of 73 executables in 55 folders [file] (client-internals/drive-clients-inventory.md#versions-present); [file] (version-profiles/drive-clients-exes.tsv). *FileVersion* is read from the PE version resource, not from program logic [bin] (client-internals/version/VERSION.md#primary-method-pe-version-resource). One row per executable, sorted by link date. *Compiled* is the resource-directory timestamp in local time; *Gen* is the encryption generation (→ §1.4); *Levels and saves* lists the level, map and save magics the loader compares against (→ §1.5). Default hosts and list names are in → §6.

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

A revision that does not change the protocol keeps the previous token: 2.0 rev1 to rev3, 2.01 rev1, 2.02 rev1, 2.05 rev1 and rev2, and the 2.1 test builds, which still send the 2.05 token GNW03081 [bin] (client-internals/build-catalogue.md#patterns-worth-knowing). Among those revisions only 2.02 rev2 changes the token, and it also adds the `PLI_LANGUAGE` send after login [bin] (client-internals/decomp-findings-2026-10-24-c/02-login-token-and-version.md#what-changed-in-the-login-function-between-revisions); [bin] (client-internals/decomp-findings-2026-10-24-c/version_tokens.tsv); [bin] (version-profiles/version-tokens-by-build.tsv). From 1.38 the token is built one character at a time in code rather than stored as a string literal [bin] (client-internals/build-catalogue.md#how-each-column-was-read).

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

## 1.8 Build profiles

This section gives, generation by generation, what a client has to do to *be* a given build: how it is packaged and started, which login and license files it reads, what the player sees, and what the lab runs measured. Wire layouts are in → §2, per-build id sets in → §2.5 and → App. C, and the machine-readable profile tables in → §1.8.8.

### 1.8.1 GNW 1.33 to 1.39

The seven gen-2 GNW clients share one wire and one feature base; every shipped `Graal.exe` matched its catalogued hash [bin] (client-internals/versions-133-139.md#sources-and-method).

| Rule | Source |
| --- | --- |
| Wire: every flush is one `u16be length` + zlib stream, with no size threshold, no cipher and no key byte (gen 2, → §2.2) | [bin] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Login is message id 0 (`chr(32)`, which also marks a player client): the 8-byte token, then `chr(len+32)` + account, then `chr(len+32)` + password | [bin][cap] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| No listserver and no server list window: the connect dialog is pre-filled with `<list-host-classic>:14900` and the `guest`/`guest` account | [bin] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Levels: only `GR-V1.00` to `1.03` (and `Z3-V1` `.zelda` for the offline levels); no `.nw`, no `.gmap`. The board arrives as `RAWDATA` (100) then `BOARDPACKET` (101) in its own frame. Saves are written as `Graalsv11`; the reader also takes `Graalsav9` and `Graalsv10` (→ §3.7) | [bin][cap] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Files: asked for with `WANTFILE` (23), never `UPDATEFILE` (34), no large-file ids; the reply is `RAWDATA` then `PLO_FILE` (102) with no modtime. A server adds `.gif` to image names with no extension for clients before 2.1 | [bin][cap] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| No tampercheck (39). A peer UDP channel for "data packages" with `noudp=` and `fixedudpport=` (default 14899) (→ §2.9) | [bin] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Game modes: One Player, One Player Online, and Two, Three or Four Players on one machine; local multiplayer goes away in 2.0 | [bin] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Window 640×480 (648×508 outer); Alt+Enter toggles fullscreen. F1 options, F2/F3 load and save, F4 editor, F5 load level, F6 debugger, F7 player list; Alt+1 to Alt+7 screenshots, minimap, bytes counter, snapshot and record | [bin] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |
| Server-sent props 1–9, 11 and 13 parse in the pre-2.1 forms (sword `c(power+30)+str`, shield `c(power+10)+str`, head `c(len+100)+image`, X/Y in half-tiles; no X2/Y2). Prop 10 must be the bow form: a server that sends a gani string there is misread and the rest of that prop stream is lost | [cap][inf] (client-internals/versions-133-139.md#what-is-the-same-in-all-seven) |

Protocol steps inside the range [bin][cap] (client-internals/versions-133-139.md#protocol-changes):

| Build | Change | Source |
| --- | --- | --- |
| 1.34 | other-player prop 34 (account name); ignores are saved by account name (`ignoredaccounts.txt`) | [bin][cap] (client-internals/versions-133-139.md#protocol-changes) |
| 1.38 | C→S + 32 `ITEMTAKE` (the server now counts picked-up rupees) and 33 `WEAPONADD`; − 25; S→C + 43 `DEFAULTWEAPON`; UDP + 24. Up to 1.37 the client uploads each held weapon with id 25 (name, image and the full script); from 1.38 it sends 33 as `chr(0)` + `chr(default weapon id)` | [bin][cap] (client-internals/versions-133-139.md#protocol-changes) |
| 1.39 | profile window: C→S 80 `PROFILEGET`, 81 `PROFILESET`, S→C 75 `PROFILE`; own prop 34 `ACCOUNTNAME`, other-player prop 33 | [bin][cap] (client-internals/versions-133-139.md#protocol-changes) |

gs2lib also knows `GNW02070` (1.38 rev1) and `GNW12080` (1.39 rev1); neither build is in the archive [srv] (client-internals/versions-133-139.md#protocol-changes).

What the player sees change [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change):

| Build | HUD, tiles and windows | Controls and rules | Source |
| --- | --- | --- | --- |
| 1.33 | `state.png` 224×81 with the letters A, S, D on the item buttons; HUD digits at the bottom of `sprites.png` (128×484). Player list (F7) with GPs, Guild, Normal and Ignore; More Options has 13 checkboxes (vsync, joystick, music, sound, reverse stereo, save downloaded images, external chat, compatibility draw, hide decompression errors, fixed UDP port, no UDP, ignore mass messages, no DirectInput). The server message (41) shows as raw HTML | fixed keys: arrows or IJKL, D item, S or Space attack, A action, M map, Q item list, P pause, Tab chat | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.34 | F6 debugger rebuilt (Next, Run, Stop next call, Stop next script; this.vars, vars, flags and NPC attribute panes), offline only | hitting a mounted player costs the horse one bush, and at zero the rider is pushed off; two players share a horse offline; one sound per type per frame, eight at once; `canbepulled` separate from `canbepushed` | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.35 | a CHAT label in `state.png` marks the focused player in local multiplayer. Player list popup gains Buddy (`buddyaccounts.txt`); "Don't use HTML for PMs"; PMs render as HTML; a "(Senior GP)" tag | | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.36 | "Limit the length of nicknames to [50]"; an "(RC)" tag | server cap rises from 220 to 28000 players; scripts read `bombs[]`, `arrows[]`, `items[]`, `explos[]`, `horses[]` | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.37 | Español and Italiano added | volume falls off with distance; `showimg` on normal NPCs; `playlooped`, `stopsound`, array literals, `true`, `false`, `hasweapon()` | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.38 | button letters removed from the art (the client draws A/S/D itself); digits move into `state.png` (224×97; `sprites.png` 128×452); 81 tiles change in `pics1.png`; editor gains "Show blocking tiles"; external chat removed; Swedish added; gif2mng ships | up to three keys per action in `graalconfig.txt` (`up`, `down`, `left`, `right`, `item`, `attack`, `action`, `map`, `switchtochat`, `itemlist`, `pause`); Alt+8/Alt+9 zoom; Ctrl+letter emotion icons from `levels/emotions` (AFK, BRB and Zzz stay until the player moves); a nickname equal to the account shows as `*nick`; server-checked pickup; `npcs[]`, `hitnpc`, `setlevel2`, `changeimgpart`, `test*()`; explosions capped at 1024; PMs saved to `pms/` | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |
| 1.39 | 7 tiles change; Profile and Options buttons in the player list; a Player List Options window; a Profile window (real name, age, sex, country, ICQ, e-mail, homepage, favourite hangout, quote); "Don't connect levels", "Ignore toalls", "Don't load heads"; Français added | Ctrl+C, K and Y; 100 lines of chat history on Up and Down; weapon list clickable; dead players don't block; editor paints by dragging and turns a dropped image into an NPC | [bin][doc] (client-internals/versions-133-139.md#what-the-player-sees-change) |

| Rule | Source |
| --- | --- |
| The GS1 command table grows 88, 93, 93, 104, 106, 109, 111 over 1.33 to 1.39; `carryobject` and `throwcarry` are in the 1.34 table but announced only in the 1.37 notes, so being in the table does not prove a command works (→ §8.2) | [bin][doc] (client-internals/versions-133-139.md#script-commands) |
| A server that sends an id outside the build's known set hits the default branch and the client ignores it (seen for 47, 82, 156, 168, 190 and 194) | [cap] (client-internals/versions-133-139.md#using-the-table) |
| GServer-v2 beta4 needs `generation = classic` and the GNW tokens in `allowedversions.txt`, checks the account with a listserver although the client connects directly, and kicks 1.33 for id 25 ("Unknown Player Packet: 25"); a proxy that drops 25 lets 1.33 play. 1.39 logs in and plays | [cap] (client-internals/versions-133-139.md#server-compatibility-gserver-v2-beta4) |
| After the level loads, the first id 2 carries props 0, 11, 13, 18, 31 and 33 in both 1.33 and 1.39; id 31 `PACKETCOUNT` goes about every 10 s | [cap] (client-internals/versions-133-139.md#live-check-2026-10-30) |

### 1.8.2 2.0x steps, the 2.1 test builds, NewWorld and NewMain

What each 2.0x step adds, matched against the binary [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence):

| Step | Feature (vendor notes) | Binary evidence | Source |
| --- | --- | --- | --- |
| 2.01 | levels preloaded when walking on the map; map-reading animation; chat set with `setplayerprop #c` stays 3 s; `hitobjects` | PLI 35, 36; PLO 46, 156; UDP 25 | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |
| 2.02 | hats from five gani attributes; `#i()` images in signs; string parsing (`strlen`, `startswith`, `indexof`, `#e`, `#T`, `tokenize`); `local.` flags not sent; `issparringzone`/`nopkzone`; free-server limits | PLO 47; zlib import; the server learns the language from 2.02 rev2 (PLI 37) | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |
| 2.03 | `triggeraction`, `actionpushed`/`actionpulled`, `move dx,dy,time,options` | PLI 38; PLO 48, 165; UDP 26 | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |
| 2.04 | `replacegani`, `addtiledef`/`addtiledef2`, `removetiledefs`, `setshape`/`setshape2`, `attachplayertoobj`, showimg text, server-side showimg, `weaponscount` | PLO 166; 26 removed; one class added for object sets | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |
| 2.05 | `setmap` applied at once; window title with server name; the `.nw` text level (`GLEVNW01`) | PLO 168; one class added, `TADP`, the anti-debug component (→ §4.11.6) | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |
| 2.1 test | new tile art, start window and server list (F8), an image engine without GDI, `ascii()`, `tiles[x,y]`, predefined NPCs with `#COMMENTS`/`#EDIT`, smilies in PMs, a tabbed editor | PLO 49, 169 | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#what-each-step-adds-vendor-text--binary-evidence) |

| Rule | Source |
| --- | --- |
| 2.1 test2 and test3 keep the 2.05 token `GNW03081`, login and C→S set (39 ids); they add S→C 49 `PLAYERWARP2` and 169 `UPGRADEURL` (61 ids handled). test3 adds skip-reload checks in LEVELBOARD, LEVELNAME and PLAYERWARP; smilies come from `levels/smilies/smiliesdef.txt` (`code,filename`) | [bin][doc] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#21-test2-and-test3) |
| The 2.1 test exe is about 140 KB smaller than 2.05 rev 2 despite more functions, because of the rewritten image engine | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#21-test2-and-test3) |
| NewWorld beta1/beta2 (token `G2N15041`) branch from the 2.02 line: beta1 handles 53 S→C ids (no baddies, chests, horses or freeze), beta2 adds 49 and 169 and the 2.1 editor classes; C→S has 34 ids. New vocabulary: `nw*` time variables, `layer`, `arraysnw.dat`, `bodycolors.txt`, `bodynw.png`, `controlnpc.txt`; the classic baddy names and `arrays.dat` are dropped | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newworld-beta1--beta2) |
| NewMain 24 and 26 (token `GNW08011`) handle 51 S→C ids (0–45, 75, 100, 150, 151, 153) and the 2.00 C→S set; they carry the Delphi DDE classes and the old editor windows, and are a separate pre-2.00 branch, not a revision of 2.00 | [bin] (client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md#newmain-24--26) |
| 2.00 to 2.03 have 186 classes; 2.04 and 2.05 add one each; the 2.1 test swaps four editor classes for four tabbed ones (188); NewMain has 193 | [bin] (client-internals/decomp-findings-2026-10-24-c/09-features-classes-vocabulary.md#classes) |

### 1.8.3 2.17, 2.22, 2.3 and 2.31

| Rule | Source |
| --- | --- |
| The four Graal Reborn executables (2.05 rev 2, 2.17, 2.22, 2.31) are Delphi builds with one base socket class and game-server and listserver subclasses | [bin] (protocol/client-versions.md#client-versions-side-by-side-205-217-222-231) |
| 2.17 still uses the gen-3 cipher of 2.05; 2.22 and 2.31 are gen 5, sending the login frame in fixed mode 3 and switching to dynamic mode after the flush (→ §2.2) | [bin] (protocol/client-versions.md#game-server-login) |
| From 2.17 the account name is kept obfuscated in memory with `dec(b) = (~b − 10) & 0xFF` and decoded only to build the login line; 2.31 does the same for the password. The 2.18 note "new password encryption" is about the saved-password store | [bin][doc] (protocol/client-versions.md#game-server-login) |
| From 2.17 the listserver address comes from `arrays2.dat` (lines: host, port, site, registration URL, translation URL, two fallbacks), checked against the 128-byte `arrays2.sig`; `graal.sig` checks the executable the same way ("Graal.exe corrupted"). 2.05 has neither file (→ §6) | [bin][doc] (protocol/client-versions.md#listserver-login) |
| No 2.3 executable was uploaded; 2.3 values are inferred from 2.31, GServer-v2 and the notes. GServer-v2's default `allowedversions.txt` enables only 2.22's token | [srv][inf] (version-profiles/2.22-2.31.md#builds-in-this-range) |
| The Reborn `Graal_222.exe` is dated 2009 and `Graal_231.exe` 2007, and the 2.17 build beside them is rebranded "Eradia Online", so text and server-list edits by the community cannot be ruled out | [bin][inf] (version-profiles/2.22-2.31.md#builds-in-this-range) |
| Tampercheck (39) re-sends differ: 2.17 once at login; 2.22 at login, on each gmap edge crossing and after each client-initiated level-link request; 2.31 at login and about every 3.2 s. 2.31 also sends 24 about every 5.1 s and 46 on every level entry; 2.22 sends 24 = 9 every 5.1 s only while another player is in its level | [cap] (version-profiles/2.22-2.31.md#wire-protocol) |
| 2.22 login in the lab: 37 `English`, 39, 34 `UPDATEFILE` for the default sword, shield, body and bomb images, 23, then 2; it answers S→C 182 with 44 | [cap] (version-profiles/2.22-2.31.md#wire-protocol) |
| GServer-v2 sends a `-gr_zlib_fix` weapon to clients 2.21 to 2.31 that pads chat made of long runs of one or two characters; it works around a client compression bug, which a faithful client should keep or tolerate | [srv][inf] (version-profiles/2.22-2.31.md#wire-protocol) |
| 2.31 does not request the map file after `setmap`, so GServer-v2 pushes every BIGMAP file at login for 2.31 but not for 2.3 | [srv][inf] (version-profiles/2.22-2.31.md#wire-protocol) |

What the player sees [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees):

| | 2.22 | 2.31 | Source |
| --- | --- | --- | --- |
| Start window | Training · Options · Get an account! · Start | adds Editor (launches `GraalEditor.exe`); Training stays | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Server-list tabs | Gold · Silver · Bronze (possibly a Reborn edit) | Graal Gold · Graal 3D · Classic · Hosted; a 3D server asks for Graal3D or starts `Graal3.exe` | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| `graal://`, `graal3://` | not registered | registered; a link sends `serverstartparams` to the server's Control-NPC | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Editor | full level editor in the client (toolbar, tile and object panels, dialogs, F6 debugger); 29 forms | gone (18 forms); F4 does nothing; F1 shows four buttons instead of six | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Options → General | "Save downloaded images (to \levels\webgifs)" | "Use filename cache" (`cachefilenames`, `FILENAMECACHE.txt`) | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Classic client-side NPC mode (honours `HASNPCSERVER`) | yes | removed | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Positions | half-tile X/Y | X2/Y2/Z2 for players and NPCs | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |
| Fixes in the notes | | NPCs crossing gmap borders; float-to-string (`#v` prints integers of more than 6 digits); a new timer replaces the busy loop at 99 % CPU; a B-tree object lookup | [bin][cap][doc] (version-profiles/2.22-2.31.md#what-the-player-sees) |

| Rule | Source |
| --- | --- |
| 2.17's tabs are Graal Gold · Classic · Hosted. Only tabs that hold a server are drawn: the same lab server appears under Bronze in 2.22 and Hosted in 2.31 | [bin][cap] (version-profiles/2.22-2.31.md#start-window-and-server-list) |
| The HUD is identical in 2.22 and 2.31 (A/S/D slots, counters, spinning hearts, MP bar); 2.31 no longer references `ss_arrow.png`, `ss_bomb.png`, `graalmap.png`, `headsconfig.txt`, `loadgmaps.txt`, `recordpos.txt` or `shield1.gif`, all offline or editor files | [cap][bin] (version-profiles/2.22-2.31.md#in-game-windows-and-keys) |
| GS1 from 2.17 to 2.22 adds `gravity`, `textwidth`, `textheight`, `isthisflagset`, `isplayerflagset` (replacing `isflagset`) and a `#R` message code; 2.22 to 2.31 adds `timevar2`, `downloadsize`, `onwall2`, `onwater2`. `downloadsize` is in the 2.22 notes but only in 2.31's table, so a 2.22 profile treats it as 0 | [bin][doc][inf] (version-profiles/2.22-2.31.md#gs1-script-differences-from-the-clients-symbol-table-bin) |

### 1.8.4 Graal 3.x: Linux 3.04 and Mac OS X 3.153

| Rule | Source |
| --- | --- |
| 3.x is a C++ rewrite on the Torque Game Engine, not Delphi: menus, prefs and key binds are compiled TorqueScript (`.dso`, version 33); levels, NPCs, GS1, ganis and the Graal protocol are native code | [bin][file] (protocol/v3x-clients.md#what-these-clients-are) |
| Linux 3.04 (Jan 2004) is i386 ELF, UPX-packed and stripped, with SDL 1.2, OpenAL and fmod; Mac 3.153 (Feb 2005) is PowerPC Mach-O on Carbon. Both were built by "Linux Cyberjoueurs". Names come from RTTI and allocation-tracking source file names, not symbols | [bin][file] (protocol/v3x-clients.md#what-these-clients-are) |
| The tokens `G3D03014` (3.04, listed by servers as 3.041) and `G3D28015` (3.153) carry the 2.22 and 2.31 date stamps, and the clients speak those protocols; earlier 3.x tokens are `G3D16053` (3.0) and `G3D27063` (3.01) (→ §1.2) | [bin] (protocol/v3x-clients.md#version-tokens) |
| The listserver host is not compiled in: `license/license.graal` names it (`<list-host-3x>`, port 14922, site, signup and translate URLs, two fallbacks) and is RSA-1024 signed (PKCS#1 v1.5 over SHA-1, e = 17) in `license/sig.license`; `sig.graal` signs the packed executable; all three verify against the key embedded in the client | [bin][file] (protocol/v3x-clients.md#listserver) |
| The server name's prefix picks the tab: `P ` Graal Gold, `3 ` Graal 3D, `H ` Hosted, `U ` not listed, none Classic | [bin] (protocol/v3x-clients.md#listserver) |
| Neither build sends 39 after login, and the account and password go as plain strings, with no `~b − 10` step | [bin][cap] (protocol/v3x-clients.md#game-server-login-and-cipher) |
| The 3.151 Linux installer upload is 139 bytes short: an ASCII-mode transfer turned every CR LF into LF, so only its metadata (version 3.151, the 3.153 data layout) survives. The two Mac uploads are byte-identical (3.153), and the 3.04 installer and tgz hold the same game files | [file] (protocol/v3x-clients.md#the-uploads-for-the-record) |

Profile [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids):

| | 3.04 | 3.153 | Source |
| --- | --- | --- | --- |
| C→S sent | 0–24, 26–30, 32–38, 40, 41, 43, 80, 81 (complete) | 3.04's set plus 46, 50, 93, 96–98, 152, 154–158 (2, 3, 15, 24, 29 and 80 assumed) | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |
| S→C handled | 79 | 88 | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |
| Own props written | 0–76 except 25, 27–30, 34, 36, 50, 51 | 0–80 except 25, 27–30, 34, 36, 50, 51, 77 | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |
| Precise move | no | X2/Y2/Z2 and `MOVE2` | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |
| Start window | Nick, Language, Options, Tutorial, Account, Password, Get Account, Start; tabs Graal Gold, Classic, Graal 3D, Hosted with a direct-connect field; options Graphics, Audio, General; no editor | adds a 3D mode, snow and xmas themes, the RC file browser and script uploads, server-side class scripts (131–134); prefs ship with `noudp = 1` | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |
| GS1 | 496 names; every 2.05 command except `putobject`, `setbackpal`, `setbody`, `setbacktile`, `drawovertrees`, `setbacktile2` | not counted | [bin][file][cap] (version-profiles/3.04-3.153.md#client--server-ids) |

Lab runs: 3.04 on Linux in a loopback namespace, 3.153 on Mac OS X 10.4 in qemu [cap] (version-profiles/lab-304-linux-2026-10-30.md#setup-for-repeating-it); [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#3153).

| Rule | Source |
| --- | --- |
| The listserver login is one plain zlib frame holding id 7 (`key`, `G3D30123newmain`) and id 1 (account, password); the client accepts a gen-5 reply | [cap] (version-profiles/lab-304-linux-2026-10-30.md#startup-and-listserver) |
| The first game frame holds 5 (login), 37 `English` and 34 for `bigmap.txt` and `minimap.txt`; the first props are 0, 18, 31, 33, 52 `English`, 75 `linux` or `mac`, and 76 = 1250 | [cap] (version-profiles/lab-304-linux-2026-10-30.md#game-login); [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#game-login-captured) |
| Requests for its own images come in batches of at most five | [cap] (version-profiles/lab-304-linux-2026-10-30.md#game-login) |
| 3.04 sends nothing periodic over TCP; its 5.1 s message (UDP id 15 with the byte 9) goes to peers over UDP. 3.153 sends 24 about every 16 to 18 s and walks with props 78/79 (X2/Y2), never 15/16 | [cap] (version-profiles/lab-304-linux-2026-10-30.md#two-players-the-udp-channel); [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#other-sends) |
| 3.04 play: walk 10 tiles per second, X or Y sent every 100 ms, `idle` 0.1 to 0.15 s after release; `push` after about 0.9 s against a wall; `sword` lasts 0.25 s; a dropped item is removed by the client with 13 after 8.3 s; a thrown bush sends no 11; chat is white with a one-pixel blue shadow and no bubble, and Tab opens the chat bar | [cap] (version-profiles/lab-304-linux-2026-10-30.md#movement-and-animation); [cap] (version-profiles/lab-304-linux-2026-10-30.md#bushes-lifting-items) |
| 3.04 keys (Torque `config.cs`): arrows, A/S/D items, Q, P and M windows, T microphone, F3 options, F5 load level, F7 player list, F8 server list | [file] (version-profiles/lab-304-linux-2026-10-30.md#movement-and-animation) |
| 3.04 offline (Tutorial) loads `tiledefsOffline.txt` (`picso.png,offlinetutorial,1,0,0`), a terrain-only sheet; classic bushes, stones and pots draw wrongly and cannot be cut or lifted offline | [file][cap] (version-profiles/lab-304-linux-2026-10-30.md#offline) |
| The 3.04 UDP channel is the 2.05 one unchanged: id 0 movement every 100 ms, 22 chat, 26 trigger action (UDP only); one client stopped sending UDP to its peer after 11 to 20 s for an untraced reason; an unfocused player shows as `name (paused)` | [cap] (version-profiles/lab-304-linux-2026-10-30.md#two-players-the-udp-channel) |
| The 3.04 process is named `3` by the UPX stub, keeps prefs under `~/.garagegames/graalexe/`, and scans its folders only at startup | [cap] (version-profiles/lab-304-linux-2026-10-30.md#setup-for-repeating-it) |

### 1.8.5 Graal 4.x: Windows 4.04r2 and 4.20r8, Mac 4.20r6

| Rule | Source |
| --- | --- |
| On Windows 4.x is a Delphi launcher `Graal4.exe` (window, DirectDraw, input, web panel, external windows, URL handlers, `graal4config.txt`, `graal4console.log`) over an MSVC C++ `GraalEngine.dll` with about 2,000 exports, handed its callbacks through about 115 `graal_set…` calls. The Mac client is one PowerPC binary from the same source | [bin] (protocol/v4x-clients.md#what-these-clients-are) |
| The engine source tree is `K:\src\graalv4\…`; crypto is libtomcrypt (not Crypto++ as in 3.x), with zlib, bzip2, JasPer, giflib, libjpeg and libpng | [bin] (protocol/v4x-clients.md#what-these-clients-are) |
| At start-up the engine makes 0 to 1,023 heap allocations of random size, creates the player object, then frees them, so the player sits at a different address each run | [bin] (protocol/v4x-clients.md#what-these-clients-are) |
| There is no separate listserver protocol: the client connects to the `license.graal` host (`<login-host-4x>`, port 14900) as a game server named `Login` and gets the list inside that session (→ §6) | [bin][file] (protocol/v4x-clients.md#login-server-and-licensegraal) |
| Windows adds `sig.graallib` for the engine DLL; the check runs exe, DLL, license, and any missing file or bad signature stops the client ("The license file(s) have not been found", "The license file is invalid!"). Same RSA key as 3.x | [bin] (protocol/v4x-clients.md#login-server-and-licensegraal) |
| Saved passwords: accounts starting `guest` are never saved; the password is DES-encrypted under a key built from the machine (MAC and `DigitalProductId` bytes) and stored as `1` + 48 characters, so it decrypts only on the saving PC; 4.04r2 keeps one `password` value, 4.20 adds per-account `<account>_pass` | [bin] (protocol/v4x-clients.md#saved-passwords) |
| The "Packet Logger" 4.20r8 engine is a third-party modification: a one-byte patch skips the signature check, and a hook in zlib's `inflate` calls `g4_PackLog.dll`, which logs only incoming zlib frames, truncated to the compressed length, as `[id]rest`; it works only on Windows XP SP2 addresses | [bin][src] (protocol/v4x-clients.md#packet-logger-third-party-build) |
| The 4.04r2 installer is a Thinstall (2003) virtualised bundle: an outer loader found through the PE `LoaderFlags` field, an inner stub, and a compressed directory of 151 records (14 folders) with blocks tagged stored, LZ77, LZ77 XOR 0xF0 or range-coded; the extracted files verify against their signatures (→ §11) | [bin] (protocol/v4x-clients.md#how-the-installer-is-packed) |
| 4.04r2 ships `Graal4.exe`, `GraalEngine.dll` (3 March 2006), `Graal3DEngine.dll`, `fmod.dll`, `ExeReplacer_temp.exe` and `graalv4_installfiles.txt`; its `license.graal` and `pics1.png` are byte-identical to Mac 4.20r6's | [bin][file] (protocol/v4x-clients.md#what-404r2-ships) |
| `ExeReplacer` swaps in a new executable and restarts it for the `GRPKG001` update system; packages live in `localversions.txt` and are driven by S→C 105, 106, 193, 196 (→ §8.3) | [bin][inf] (protocol/v4x-clients.md#what-these-clients-are); [bin] (protocol/v4x-clients.md#file-formats) |
| 4.04r2 against 4.20r8: no layered board change (107), 108 or 196; one saved password; 4.20r8 adds a network thread, an XML parser, browser and array GUI controls, reconnect and "cheat window" checks and `MRandomLCG`; 4.04r2 still has `decryptGraalMemoryDES` | [bin] (protocol/v4x-clients.md#protocol-and-engine-differences-from-420r8) |
| 3D in 4.04r2 is the `Graal3DEngine.dll` plug-in, loaded for a server whose name starts `3 `; it takes over every `graal_set*` callback and owns the window and OpenGL, while the 2D engine keeps game logic and the Graal connection (→ §10) | [bin][inf] (protocol/v4x-clients.md#the-3d-plug-in-graal3denginedll) |
| Mac 4.20r6 in qemu: the login line is `mac,"",<md5>,""` (the MAC hash came out empty under qemu); it sends 34 and 46, which the static list missed; no flag 18 for the lab's movement weapon; chat is white with a blue shadow; Apple's software renderer needed a shim dropping two AGL attributes | [cap] (version-profiles/lab-mac-tiger-2026-10-31.md#420r6) |

### 1.8.6 Graal 5.x: Windows 5.00r7 to 5.31r4

| Rule | Source |
| --- | --- |
| 5.00r7 (July 2007) keeps the 4.x split: Delphi `Graal.exe`, MSVC 6 `GraalEngine.dll` (about 2,170 exports, source tree `graallib`, own SHA-1, RSA, DES, Blowfish and MD5), `Graal3DEngine.dll`, `ExeReplacer.exe`; a failed engine start shows "The execution file is corrupted" | [bin] (protocol/v5x-clients.md#architecture) |
| 5.12 to 5.24 and the 6.00 betas are wrapped by MoleBox, which serves its bundled files through hooked file APIs; 5.30r3, 5.31r4 and the later 6.x builds use Themida / WinLicense 2.x and bundle nothing. From 5.24 the launcher and engine DLL are one MSVC executable and the source tree is `quattroengine\quattro_lib` | [bin][cap] (protocol/v5v6-windows-unpacked.md#the-builds) |
| License files: 5.00r7 four (`license.graal`, `sig.graal`, `sig.graallib`, `sig.license`); 5.12 two (`license.graal`, `sig.license`); from 5.24 none, with the three login hosts compiled in. Every Windows build still connects to the `Login` server on 14900 | [bin][file][cap] (protocol/v5v6-windows-unpacked.md#login-server-and-license); [bin] (protocol/v5x-clients.md#license-file-and-signatures) |
| The 5.00r7 "CRC patch" is third-party: 8 changed bytes in the license loader skip the not-found, invalid and five-line checks, so any `license.graal` is accepted | [bin] (protocol/v5x-clients.md#the-crc-patch-third-party) |
| `GR-V1.05` adds tile layers and `GRESCR01` caches DES-encrypted class and weapon scripts whose key arrives in clear with each script (S→C 140, 197; → §3.1, → §8.3) | [bin] (protocol/v5x-clients.md#file-formats) |
| Every build logs in by itself as guest at the login screen, with a fixed guest password shared by all the Windows builds; the machine list gains a fifth field, the quoted Windows version (`"6.2 9200 "` under Windows 8 and later) | [cap] (protocol/v5v6-windows-unpacked.md#login-message) |
| 5.30r3, 5.31r4, 6.00r2 and 6.00r4 expire: on today's date they log "This is a beta release of Graal…" and exit, so they run only with the clock set back for the whole session; 6.03r7 has no such check | [cap][inf] (protocol/v5v6-windows-unpacked.md#running-them); [wire] (protocol/v5v6-lab-play.md#lab-setup-and-what-it-took) |
| 5.12 sends even short bodies zlib-compressed; 5.24r3 and later send them raw, as 2.22 does | [cap] (protocol/v5v6-windows-unpacked.md#cipher-and-framing) |
| 5.12 steps the gen-5 iterator `len / 4` rounded down for compressed frames, one step short of every later build whenever a compressed frame under 16 bytes is not a multiple of 4; a server for a 5.12 profile has to step the same way (→ §2.2.4) | [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |
| Login lobby mode: while the current server name starts with "login", the draw-layer mask is cut, so the client draws tiles, chests and image NPCs but no characters and no HUD, and never asks for sprites, heads or bodies. S→C 178 (`PLO_SERVERWARP`) to a server with another name ends it (→ §2.3) | [cap] (version-profiles/lab-v5-2026-10-30.md#login-mode-why-nothing-is-drawn-at-first); [wire][shot] (protocol/v5v6-lab-play.md#the-login-server-mode) |
| After the warp the client asks for `tiledefs<servername>.txt` with the space as `%032`; 5.31r4 and 6.03r7 draw no tiles before the warp | [wire][shot] (protocol/v5v6-lab-play.md#the-login-server-mode) |
| Stock gs2lib does not know `G3D15010` (5.24, 6.00 beta2) or `G3D03048` (6.00 beta1); it then sends the old file layout and 5.24 saves PNG data as a file name | [cap] (version-profiles/lab-v5-2026-10-30.md#setup-for-repeating-it) |
| There is no built-in chat bar: the engine looks for a GUI control named `ChatBar`, which the server's scripts supply; Escape asks "Do you really want to quit Graal?" | [bin][cap] (version-profiles/lab-v5-2026-10-30.md#how-it-looks); [wire][shot] (protocol/v5v6-lab-play.md#chat-text) |
| Chat is drawn above the head with a blue outline and no bubble, on one unwrapped line; the client clears it itself 2.97 to 2.99 s after the server set it. 5.24 draws in Arial, 6.03 in Tempus Sans ITC 24 | [wire][shot] (protocol/v5v6-lab-play.md#chat-text) |
| HUD: 5.00r7 and 5.12 letter the item boxes A, S, D and print the sword level; 5.24r4 under Wine draws neither (unconfirmed on Windows). The player list is a native window "Players: N online" with Staff, Buddies, Guild, Normal, Ignore and Offline | [cap] (version-profiles/lab-v5-2026-10-30.md#how-it-looks) |
| Movement timings in 5.00r7, 5.12, 5.24r4, 5.30r3 and 6.03r7 equal 2.05's: walk 0.5 tile per 50 ms tick, push after 18 blocked ticks (0.9 s), sword 5 ticks, lift 6 ticks, hidden walk 0.1 tile per tick (→ §4.2) | [cap] (version-profiles/lab-v5-2026-10-30.md#timings); [wire] (protocol/v5v6-lab-play.md#play-what-the-client-does) |
| The only new mannerisms on the wire are the trigger actions `pushed,0` (0.55 s into a push, then every second) and `pulled,1` (0.85 s into a pull); hurt pushes the player 5 tiles in 5 ticks and lasts about 1.55 s; swimming is as fast as walking | [wire] (protocol/v5v6-lab-play.md#grab-pull-hurt-and-swim) |
| Lifting a pot leaves its base (1770, 1771, 1786, 1787) and the server drops a heart (S→C 22); a pot cannot hide the player, a bush or stone can (status 22, `hiddenstill`) | [wire][shot] (protocol/v5v6-lab-play.md#pots-stones-and-hiding) |
| Under Wine 6.00r2 and 6.00r4 freeze after the first image; on real Windows with the date faked they play, so the freeze is a Wine fault | [shot] (protocol/v5v6-lab-play.md#600r2-and-600r4-on-real-windows) |

### 1.8.7 Graal 6.x: 6.00 to 6.03, Mac 6.11

| Rule | Source |
| --- | --- |
| 6.x is one native C++ program per platform from the `graallib` code base, with no Delphi launcher and no Torque layer; Linux links SDL_mixer, X11, OpenGL and avahi; 6.03 moves zlib to 1.2.5 | [bin] (protocol/v6x-clients.md#architecture) |
| Unpacked Windows 6.00r2 (product version 6.002, compiler date 12 June 2011) and 6.00r4 (6.004, 26 June 2011) are that program under the source tree `quattro_lib`: OpenGL drawing after a Direct3D 9 capability check, FMOD sound, GS2 shell scripts, `TServer*` world objects and a `TSocket` game connection; `ExeReplacer.exe` is still launched for packages (Torque names that remain → §10.1.5) | [bin] (client-internals/engine-600r2.md#how-the-program-is-split); [bin] (client-internals/engine-600r4.md#same-engine-as-600r2) |
| The packed uploads of Windows 6.037 (2012, Linux Cyberjoueurs) and 6.113 (2014, Eurocenter Games) decompile as packer stubs. 6.037 is the known 6.03r7 executable. 6.113 is not the Mac 6.11 bundle version | [bin] (client-internals/packed-6037.md#what-this-file-is); [bin] (client-internals/packed-6113.md#what-this-file-is) |
| Windows 6.1.1.3, re-read after the 2026-11-07 gap archive, is still that stub: version string `6.113`, fixed version 6.1.1.3, image timestamp 8 August 2014, one import `SetCurrentDirectoryA`, export directory `QPlay.exe`. The archive added no unpacked engine (→ §10.1.9) | [bin] (client-internals/engine-6113.md#what-this-file-is); [bin] (client-internals/engine-6113.md#still-no-engine-image) |
| That 6.113 listing has no login token, key byte, frame builder or property parser. Do not copy Windows `G3D26090` or either 6.03 token onto it. The Linux note and the Windows captures disagree on the key byte and on the 6.03 token | [bin] (protocol/v6113-wire.md#what-6113-cannot-show); [bin][cap] (protocol/v6113-wire.md#contradictions) |
| A running 6.113 client on port 14900 sends the clear hello `GNP1905C`, header `01 02 00 01 17 fd`, zlib `78 9c`, then `00 01 00 01 06 fc` and 256 session bytes. The server header is `01 02 00 01` plus `21 fd` or `22 fd`. The rest is ciphertext, so no generation-5 login line and no list or property id is visible (→ §6.1.3) | [cap] (protocol/v6113-list-capture.md#the-clear-hello) |
| The full 6.113 capture (241 s, 46225 frames) repeats that hello on TCP 14900 (two answered sessions, server marker 22) and on TCP 14882 (one session, server marker 17, 9639663 bytes from the server). No UDP datagram is to or from those remotes. No UDP port in the file is one greater than a TCP port (→ §2.9, → §10.2) | [cap] (protocol/v6113-udp.md#graal-tcp) |
| Unpacked Windows 6.1.1.3 does not store `GNP1905C`. `sendraw` can write those eight bytes with no header, and the six-byte header is the `setprotocol` framer (`L` counts the header plus the body). Unpacked 6.0.3.7 stores `g3d0311c` and sends it, upper-cased, as id 5 (→ §2.10.5) | [bin][cap] (protocol/v6113-hello.md#the-eight-characters) |
| A full 6.113 capture the same day has TCP 14900 (three completed sessions, each starting `GNP1905C`, and one unanswered SYN) and no UDP to those remotes. UDP 14900, 14901 and 14899 have no datagrams. The UDP in the file is other traffic on the same interface, including a short-header flow on UDP 443 to a separate remote | [cap] (protocol/v6113-udp.md#what-this-capture-shows) || Hosts, ports, tokens and URL parts are stored scrambled and decoded at run time by a per-byte decoder that depends on length and position, the same in 6.01, 6.03 and 6.11 | [bin] (protocol/v6x-clients.md#architecture) |
| No `license.graal`: the three login hosts are compiled in (6.03 as `host:14900` entries walked on failure) | [bin] (protocol/v6x-clients.md#login-server) |
| Linux machine ids: MD5 of the `eth0` MAC, MD5 of the `/etc` inode number, an empty field, and the kernel release and version | [bin] (protocol/v6x-clients.md#login-message-601-and-603) |
| Windows 6.03r7 sends `G3D0311C` and Linux 6.03r7 `G3D0511C`, so a server that accepts one need not accept the other; the token belongs to a protocol revision (four builds from 5.30r3 to 6.00r4 share `G3D26090`) | [cap][bin] (protocol/v5v6-windows-unpacked.md#tokens) |
| The 6.00 betas (Jan 2010) are older than 5.24r3, and 6.00 beta2 sends 5.24's token, so the two lines shared one code base in early 2010 | [bin][cap] (protocol/v5v6-windows-unpacked.md#the-builds) |
| 6.11 (Mac, 2014) fetches a connector script over HTTPS and lets the server set framing, ciphers and id tables (→ §2.10) | [bin] (protocol/v6x-clients.md#611-mac-the-connector-and-a-server-defined-protocol) |
| A server for 5.x/6.x needs a game server name that does not start with "login" (or a 178 warp), the tokens `G3D15010` and `G3D03048`, and must serve `basepackage.gupd` (a minimal `GRPKG001` with `NAME`, `VERSION`, `PLATFORM`, `MODE` will do) and `tiledefs<server>.txt`; the Themida builds fetch every image, gani and sound | [wire] (protocol/v5v6-lab-play.md#for-seihai-profiles); [wire] (protocol/v5v6-lab-play.md#the-session-on-the-wire) |
| GServer-v2 beta4 crashes on every 6.00 login while registering the GS1 weapon `-gr_movement`, taking the GS2 bytecode branch for a weapon with no bytecode | [srv] (protocol/v5v6-lab-play.md#600r2-and-600r4-on-real-windows) |

### 1.8.8 Profile tables

The profiles above also exist as machine-readable tables, one per range, that a client can load to behave as one exact build. Each `[[version]]` holds a build's full values, `[version.features]` its switches and `[version.assets]` its HUD and tileset revision [file] (client-internals/versions-133-139.md#using-the-table).

| Table | Builds | Source |
| --- | --- | --- |
| `v1998-v11.toml` | 1st Graal (Sept 1998) to 1.1 (Feb 1999) | [file] (client-internals/version-profiles/v1998-v11.toml) |
| `v121-v132.toml` | 1.21 to 1.32 | [file] (client-internals/version-profiles/v121-v132.toml) |
| `v133-v139.toml` | 1.33 to 1.39 | [file] (client-internals/version-profiles/v133-v139.toml) |
| `141-217.toml` | 1.41 rev1 to 2.1 test, with NewMain and GraalX | [file] (client-internals/version-profiles/141-217.toml) |
| `2.22-2.31.toml` | 2.22, 2.3, 2.31 | [file] (version-profiles/2.22-2.31.toml) |
| `3.04-3.153.toml` | 3.04, 3.153 | [file] (version-profiles/3.04-3.153.toml) |
| `4.04-4.20.toml` | 4.04r2, 4.20r6, 4.20r8 | [file] (version-profiles/4.04-4.20.toml) |
| `5.00-6.03.toml` | Windows 5.00r7 to 6.03r7 | [file] (version-profiles/5.00-6.03.toml) |

Lab measurements kept as tables beside them:

| Table | What it records | Source |
| --- | --- | --- |
| `lab-200-listserver-handshake.tsv` | the 2.00 listserver handshake, step by step | [lab] (version-profiles/lab-200-listserver-handshake.tsv) |
| `lab-boardmodify2-186-trailer.tsv` | how 2.31 treats extra bytes after an S→C 186 board block | [lab] (version-profiles/lab-boardmodify2-186-trailer.tsv) |
| `lab-enterlevel-231.tsv` | when 2.31 sends C→S 46: at login and on gmap cell crossings | [lab] (version-profiles/lab-enterlevel-231.tsv) |
| `lab-gs13-respawn.tsv` | respawn delays of board changes, and which client saw them | [lab] (version-profiles/lab-gs13-respawn.tsv) |
| `lab-levelchange-46-222-231.tsv` | level changes in 2.22 and 2.31: request, server reply and id 46 order | [lab] (version-profiles/lab-levelchange-46-222-231.tsv) |
| `lab-serverwarp178.tsv` | how 2.31 reacts to variants of the S→C 178 fields | [lab] (version-profiles/lab-serverwarp178.tsv) |
| `lab-showimg24-relay.tsv` | C→S 24 payloads and how the server relays them to other players | [lab] (version-profiles/lab-showimg24-relay.tsv) |
