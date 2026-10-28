# Item list (Q key)

Date: 2026-10-28. From the 2.05 client (derived). 2.22 and 2.31 not read.

* The game actions by index: 0 up, 1 left, 2 down, 3 right, 4 item,
  5 attack, 6 action, 7 map, 8 switchtochat, 9 itemlist, 10 pause.
  `itemlist` (default Q) opens and closes the item list. It opens from the
  normal state only when a player flag allows it (flag not identified).
* The list holds the player's weapons: built-in weapons and NPC weapons.
  A `/` in a weapon name makes a folder; folders of the current level come
  first, as 32 x 32 cells. Names starting with `-` are skipped when
  selecting.
* Layout: a framed window from (16, 80) to 16 px from the right and bottom
  edges; cells inside from (48, 112) to 48 px from the right and 64 px from
  the bottom. Cell size: max(image width, label width) + 10 by image height
  + label height + 15; cells are packed in the first free place, left to
  right then down. Image centred with 5 px above; label centred below;
  no-image weapons get a fixed 32 x 32 placeholder. Selected cell filled
  RGB(255, 212, 128). Font size 16. Scroll arrows when cells are cut off.
* Arrow keys: stretch the selected cell to the edge in that direction and
  take the overlapping cell with the closest near edge. Moving selects the
  weapon immediately; nothing is sent. Item key or Enter on a folder opens
  it; attack key goes up a folder. Other game keys close the list; Esc
  closes it. A mouse click on a cell selects it.
* Delete on the selected weapon removes it; online it sends
  PLI_NPCWEAPONDEL (29) with the weapon name, or PLI_NPCDEL (22) with the
  NPC id for an NPC that is not a weapon.
