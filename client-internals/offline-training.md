# Offline training levels

Date: 2026-10-14

## Observation

Tutorial levels are embedded in the executable. They can be drawn and walked without a network connection.

## Difference from session levels

The global that holds the current level name is set only by the session “set level” message (the byte that arrives after a successful world login). Offline training levels never set that global. A debugger session that shows a training level drawn while the level pointer remains null is expected.

## Enter path

Entering a training level stores the level name on the player object and the arrival coordinates. Nearby links (for example to a house) are present in the embedded data.

## Offline implication

An offline session that loads a GLEVNW01 file from disk is already past the embedded-tutorial case. The same collision, sign, and script paths apply. The only difference is the source of the level data (disk versus embedded).
