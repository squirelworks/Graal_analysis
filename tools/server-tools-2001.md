# Fan server tools (1999–2012)

Date: 2026-10-21

Notes on the small server-side tools uploaded with the NPC Control bundle. Tags: **[bin]** read from a binary · **[src]** read from source or script.

## Win32 ListServer by "Rick" (2003) — contains a password stealer **[bin]**

`ListServer.exe` (UPX-packed Delphi, 2003-03-26) is a stand-in listserver for Graal clients. It reads `servers.ini` (`[Options]` `ShowMore`, `List`; one section per server with `Name`, `IP`, `Port`, `Description`, `Language`, `Version`, `Players`, `URL`, `Favorite`) and answers each client connection with the list. `Favorite=Yes` prefixes the name with `P ` so the client files the server under Gold.

**Do not run it.** On first start it:

1. checks a marker value `Drag` under `HKCU\...\Internet Settings` and sets it to `WindowsUser@` so this runs only once;
2. reads every value under `HKCU\Software\Graal\Client` (where the Graal client keeps its saved login) and joins them as `name:<tab>value` lines;
3. Base64-encodes that text and opens `iexplore` on a third-party URL (stored Base64-encoded in the exe) with the data appended.

That sends the user's saved Graal account details to someone else's web server. The About box also opens a <graalonline-site> URL whose parameter is an insulting message. The tool's listserver behavior is not otherwise interesting.

## gs2emu-serverlist (TheDgtl snapshot `de66a3f`) **[src]**

The C++ listserver used by Graal Reborn, an earlier form of the `graal-serverlist` already summarized in `protocol/listserver.md`. What this snapshot adds:

- `settings.ini`: game servers register on port 14900, clients connect on 14922, and pre-2.2 clients on 14923 (`clientPortOld`). Options for duplicate limits, max servers, and `auth`.
- MySQL tables: `graal_users` (account, password, salt, a second password/salt pair, activated, banned, profile fields), `graal_servers` (name, ip, port, player count, max players, description, url, language, two-character type, version, uptime, player list), `graal_servershq` (per-server HQ password, max/current level, parked flag), `graal_ipban`, `graal_guilds`, `graal_guilds_members` (account, guild, nickname, rank).
- Account passwords are `md5(md5(password) + salt)` with a three-character salt. Optional phpBB login and vBulletin friend lists.

## GServer 1.39 web scripts (2001) **[src]**

- `gserverstats.pl` (TTH): a CGI page that reads the server's text outputs `playercount.txt`, `accountcount.txt`, `serveruptime.txt`, `toppkers.txt`, `topdeaths.txt`, `toponline.txt`, `topap.txt`. The top lists are `nickname:value` lines; online time is in seconds.
- `accountcreator.php` (The Expanse server): self-service sign-up into the GServer 1.39 MySQL `accounts` table. Columns used: `accname`, `encrpass`, `email`, `blocked`, `onlyload`, `adminlevel`, `adminworlds`, `lastused`. The script enforces Hotmail addresses and 20-character alphanumeric account names. Its welcome mail lists the 1.39 chat commands: `sethead`, `setsword`, `setshield`, `setnick`, `showname`, `showap`, `showdeaths`, `showkills`, `showonlinetime`, `showguild`, `showadmins`, `unstuck me`, `toguild:`, `toall:`.
- `makepass` (Linux ELF helper) **[bin]**: prints `crypt(3)` of its argument, so `encrpass` is traditional DES crypt. It picks the two salt characters with `rand()` but never seeds it, so every hash it makes uses the same salt, `Ng`.

## Graal 1.1 Guildmaker (1999) **[bin]**

`Guildmaker1.1.exe` writes `guildname.code`; the later `Guildmaker.exe` adds "Save As" for any `.code` file. The Graal 1.1 client reads the same format for `guildname.code` (used by `playeringuild`) and for its registration key `reg.code`.

Format, 48 bytes:

1. Plaintext block of 24 bytes: `len` (one byte), up to 23 bytes of text, random padding.
2. Bytes 0–23: that block encrypted with key `AXBORG15`. Bytes 24–47: the same block encrypted with key `VERGRAAL`.
3. The cipher is the same LSB-first-key DES variant as the RemoteControl password (three ECB blocks).
4. On load both halves are decrypted and must match byte for byte, otherwise the file is rejected.

The sample files decode to `Baddy` (`guildname.code`), `if (playersays(killall)` (`npc.code`, cut at 23 characters), and the first bytes of a `GR-V1.03` level (`level1.graal` and `level1.graal.code`, which are identical).
