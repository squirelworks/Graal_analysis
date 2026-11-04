# Dialogue: talkers, quests, shops

Part of the [original NPC library](../README.md). Covers `dialogue / speech` in [`behaviours.md`](../../behaviours.md), plus the shop and merchant class of the archived catalogue (manual §8.1.10). The seats from the same category are in `interaction/seat.gs1`.

Most of these NPCs are drawn with `showcharacter` and speak through the chat bubble (`setcharprop #c,...`). Chat input is read with `playerchats` and `#c`. Text with spaces is quoted in function arguments, which matches the `S` argument rule of §8.2.1.

These scripts change money and health by assigning to `playerrupees`, `playerbombs`, `playerdarts`, `playerhearts` and `playerfullhearts`. The manual lists them as 2.05 variables (§8.2.5) but does not say which are writable. Writing them is an inference that a lab run should confirm.

| File | What it does |
| --- | --- |
| `talker.gs1` | Character that cycles through four lines in a chat bubble. The bubble clears after 4 s. |
| `talker-signs.gs1` | Shows level sign 0, 1 or 2 (`say n`) depending on quest progress. |
| `quest-giver.gs1` | Fetch quest in three steps: it asks, counts the herbs left, then takes them and pays rupees and a heart container. |
| `herb.gs1` | The quest item, which only appears while the quest runs. |
| `keyword-npc.gs1` | Answers chat lines that contain "tower", "lake" or "king". |
| `shopkeeper.gs1` | "buy bombs", "buy arrows" or "buy heart" in chat. It checks the price and pays out. |
| `shop-shelf.gs1` | Keeperless shelf item. Touch to see the price, touch again within 3 s to buy. Won't sell what you already have. |
| `innkeeper.gs1` | Saying "yes" pays and refills hearts. A player at full health keeps the money. |
| `trader.gs1` | One link of a trading chain: takes one item flag and gives the next. |
| `gossip.gs1` | One of five random rumours per touch. |
| `villager-stroll.gs1` | Walks between two points, pauses at the ends, stops to talk when touched. |
