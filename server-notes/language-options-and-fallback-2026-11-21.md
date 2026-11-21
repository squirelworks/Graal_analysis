# Reference-fork language options and translation fallback

Date: 2026-11-21

This is a bounded follow-up to the historical [server-option lead](../client-internals/graal-wiki-crosscheck-2026-11-11.md#leads-not-yet-researched-here),
not a replacement for its 99-option inventory. The pinned newer GPL reference
fork distinguishes accepted language settings, server-registration metadata,
player language and actual translation. Recognizing a key is not evidence
that it selects or filters translated text. **[srv][doc]**

All source links pin the GPL-3.0 Seihai GServer-v2 fork at
`0cf8f83d0ac658299abb4a9c93dab99cca805f37`. The findings use original prose;
no implementation or language table is copied.

## Settings versus implemented effects

- `defaultlanguage` has a tracked string cache defaulting to `en`. It is
  acknowledged in translation-loading logs, but the inspected text-selection
  path does not consume it as the player's default or requested language.
- `translatedlanguages` has a tracked, initially empty list. Its configured
  entries are acknowledged in logs; they do not filter the classic domain
  loader or choose its fallback order.
- No dedicated `serverlanguage` declaration or text-selection consumer was
  identified at this pin. Generic configuration access does not establish
  such an effect, and it is not evidence that this name aliases `language`.
- `language` is a separate effectful server-registration label, defaulting to
  English. The listserver registration serializes that label; it does not
  select a player's translated message.

[Cache declarations](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Server.h),
[tracking and load-time acknowledgment](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp),
[registration metadata](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/ServerList.cpp).

## Player selection and translator generation

The account's language starts as English. The client language message stores
its supplied string on that account; an empty message stores English. The
player translation method passes this account language to the translation
manager. The unused cache default above does not replace this path.
[Account default](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/Account.h),
[language getter](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/object/Player.h),
[language message and text lookup](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/Player.cpp).

Translation loading selects the modern manager for modern server generation
and the classic manager otherwise. This decision is made from generation,
not from the two tracked language-option values.
[Manager selection](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/Server.cpp).

The classic loader reads eligible `slanguage*.txt` files in the translation
directory and ensures an Original domain exists. For nonempty source text it
calculates the text hash, maps recognized language aliases, then looks in the
requested domain followed by Original. An unmapped language name is retained.
If neither domain has the text, it records that source text in an existing
Original domain and returns the source text. This is the implemented fallback; it is not a
`defaultlanguage` fallback. The modern loader is empty and its text lookup
returns the supplied source text unchanged.
[Classic loading and lookup](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/manager/TranslationManagerClassic.cpp),
[alias mapping](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/include/utilities/manager/ITranslationManager.h),
[modern stub](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/utilities/manager/TranslationManagerModern.cpp).

RPG-window and sign-message methods are concrete outgoing consumers of the
player translation method. Both normalize line breaks before lookup. This
does not establish that every outgoing string is translated.
[Message consumers](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/server/src/player/PlayerClient.cpp).

## Test definitions and remaining scope

The existing translation-key test definitions check key names, defaults and
cache updates. They do not test text selection, domain filtering, classic
fallback or modern translation. They cannot promote the tracked stubs into
implemented translation policy.
[Existing test definitions](https://github.com/squirelworks/seihai-gserver-v2/blob/0cf8f83d0ac658299abb4a9c93dab99cca805f37/Catch_tests/ServerOptions/TranslationKeys_tests.cpp).

- [ ] Original-server support and equivalence remain unverified.
- [ ] Translation-file reload, persistence and live option changes need separate verification.
- [ ] Client rendering and complete outgoing-text coverage are not established here.
- [ ] The wider option inventory remains open, with no replacement count.

This is a source audit with no new test execution or lab result. No GPL code
or language table is copied into a permissive implementation.
