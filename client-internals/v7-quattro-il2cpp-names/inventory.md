# v7 C# dump inventory

Source: owner-held Il2CppDumper output for Worlds builds 548–71243. Each `DumpedAssemblies/dump.cs` is byte-identical to `Dumped_GameAssembly/dump.cs` for the same build. `Dumped_Graal3DEngine/` exists for every build and contains no files.

Confidence: high (sizes and identity checked on disk).

| Build | dump.cs bytes | Lines | Assemblies copy | Graal3DEngine dump |
| --- | ---: | ---: | --- | --- |
| 548 | 2,523,249 | 65,621 | identical | empty |
| 610 | 2,298,893 | 59,691 | identical | empty |
| 612 | 2,635,222 | 66,041 | identical | empty |
| 613 | 2,896,699 | 73,038 | identical | empty |
| 614 | 2,788,128 | 70,525 | identical | empty |
| 71243 | 2,679,500 | 67,633 | identical | empty |

These are Il2CppDumper `dump.cs` files. Type names are scrambled: `QuattroC2DRenderer` and `QuattroObjectRenderer` are reused as stand-in types on Unity, X509, and crash-reporter classes. Method lists below keep only names that still read as Quattro or tile APIs.
