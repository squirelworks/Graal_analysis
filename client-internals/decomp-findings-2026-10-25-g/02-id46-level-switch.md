# Id 46 (`PLI_ENTERLEVEL`)

Read in the 2.31 client; 2.17.1 and 2.22 were checked for a send site and have none.

- One send site. It is at the start of the routine that switches the client's current level, whenever the client is connected, before anything else the routine does. This fits the lab: one 46 at login, one per level change, and in a gmap one per edge crossing, always before the props frame that carries the new cell prop.
- The payload is the one-character text GCHAR 1. It is a constant in the code. No level, player count, connection or option value goes into it. GServer-v2's comment guessing "a player count for the gmap level" is not what the client sends.
- The server side in GServer-v2 is a stub that does nothing.
- 2.17.1 and 2.22 have no send site for id 46. This agrees with the lab (neither sent it) and with the version profiles (46 is added in the 2.3 step).

Not resolved: what a real service does with it. Stock GServer-v2 does nothing, so no capture against it can show a reaction.
