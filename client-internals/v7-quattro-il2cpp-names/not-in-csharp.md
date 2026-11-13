# What is not in the C# dumps

Searched every `Dumped_GameAssembly/dump.cs` (548, 610, 612, 613, 614, 71243). This is not a protocol recovery. No opcode table is claimed from these files.

Confidence: high for the zero counts below.

| Looked for | Count in every build | Where similar words do appear |
| --- | --- | --- |
| `onSend` | 0 | nowhere |
| `setprotocol` / `setProtocol` | 0 | nowhere |
| `PLO` / `PLI` as whole tokens, and `PLO_` / `PLI_` | 0 | nowhere |
| `remapper` | 0 | nowhere |
| `GRESCR` / `GRESCR01` | 0 | nowhere |
| `GS2` as a whole token | 0 | nowhere |
| `Graal3DEngine` / `Flavor0` | 0 | native notes only; `Dumped_Graal3DEngine/` is empty |

`protocol` occurs about 27 times per dump. The hits are `Mono.Security.Protocol.Ntlm`, `TlsProtocols`, `FileRemoteProtocolInfo`, UnityWebRequest `UnsupportedProtocol` / `ProtocolError`, and a licensing field. None is a Graal packet table.

## Nearby type that is not a packet table

`Quattro.Graal.DatasFromGraal` (builds 610 through 71243) has static fields `playerPosition`, `level`, `map`, `sentFromGraal`, `serverPlayers`, `npcs`, and methods `GetFromGraal(int channel)`, `SendToGraal(int channel, string message)`, `DistanceFromPlayer`. `ActorType` is `NPC`, `ServerPlayer`, `Player`.

That is a string channel plus actor snapshots. It has no opcode list, no `onSend*`, and no PLO/PLI ids. Confidence: high that this is not the protocol table; medium that the channel methods are a game-side string pipe.

Protocol tables stay in the native DLL, which this pass did not open.
