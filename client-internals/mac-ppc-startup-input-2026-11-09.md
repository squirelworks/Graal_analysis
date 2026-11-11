# Mac PowerPC 4.04r2, 4.20r6 and v5: startup and input

This note reads how three Mac OS X PowerPC clients start, pump events and turn Carbon input into engine records. It is static: saved function bodies and their PowerPC assembly, with pointer values read from the original Mach-O files. No guest was started and no client was run for it. Evidence `MAC-PPC-404-STARTUP-INPUT-20261109`, `MAC-PPC-420-STARTUP-INPUT-20261109` and `MAC-PPC-V5-STARTUP-INPUT-STATIC-20261109`. **[bin]**

| Build | Executable SHA-256 |
| --- | --- |
| Mac 4.04r2 | `01dbf094d84aff84f7fcaa2f38ad42f9215cf60154aaa0ff730ff098a44dc847` |
| Mac 4.20r6 | `304a4d480a63cbaf70822cca56066284f392973bf9e00f3192551bff4b540f92` |
| Mac v5 (one image shared by the v5 builds studied) | `a76dc557f7a1db8ac385f3f5fcceb6629ba53cab09d9ddbc4d989d942d206f10` |

The three builds share one design. Where a finding was read in only one of them, the text says so; method tables and callbacks were not assumed to carry over between builds.

## Start-up: one timer that runs the whole engine

**[bin]** The program's C start-up sets up the arguments and environment and calls the application bootstrap. On v5 the bootstrap sets the cursor and event mask, reads the system version, normalizes the bundle path, installs an event-loop timer and enters the Carbon application event loop.

**[bin]** When the timer fires, it calls an engine entry with the argument count and vector, cleans up, stores the result and quits the event loop. So the timer does not drive frames. It is called once and runs the engine's whole life. Read on 4.04r2, 4.20r6 and v5.

**[bin]** On v5 the engine entry calls one virtual method once. If that returns non-zero, it calls a second one repeatedly until it returns zero, and then a third. The entry always returns zero. Read in order, these look like initialize, update and shut down; the names are a reading of the order, not recovered symbols. The 4.04r2 run helper has the same shape.

**[bin]** On v5 a static initializer builds the engine object with the base constructor and then replaces its method table with a derived one. In the derived table:

- initialization creates several objects, registers a material-property object, opens the native window at 640×480 with the title `Graal`, and calls two more start-up helpers. If a `moveMap2D` object can be looked up by name, another helper runs on it.
- the update method runs while an "engine running" flag is set. Each pass normalizes the locale and calls four update or poll helpers.
- shutdown tears down several object pairs, clears the global pointers and shuts down subsystems.
- redraw calls three helpers when a global object exists. This is a native redraw route, not proof of particular widgets.

**[bin]** The v5 GUI start-up allocates a root object, builds the `DefaultCursor` from `defaultCursor.png` and attaches it, then calls a series of registration helpers. That matches the Windows 4.2.0.8 order in [torque/4208-engine.md](../torque/4208-engine.md#the-order-startscript-objects-are-created).

**[bin]** On 4.04r2 and 4.20r6 the game initialization sets the argument variables and registers the native window with a title and its first size. It also has a conditional lookup of a named action map.

## The event pump

**[bin]** The pump uses the Carbon receive, send and release calls or the classic event-record poll, chosen by global flags. Its caller can emit a shutdown-like record and, behind another flag, sleeps one millisecond when idle. The "request shutdown" helper only sets a flag on the engine object; it does not leave the event loop itself.

## Which events are registered

**[bin]** Both 4.x builds and v5 register 12 window events and 15 application events. On v5 the window set is keyboard kinds 4, 1, 3 and 2; mouse kinds 1, 2, 5, 6 and 10; and window kinds 2, 5 and 6. The application set is a high-level event (kind 1), application kinds 3, 1 and 2, the same keyboard and mouse kinds, and window kinds 73 and 27. The numbers are Carbon's own event kinds. The code does not check that registration succeeded.

## Turning input into engine records

**[bin]** One translator handles keyboard and mouse events and sends each record to the engine through a virtual call:

- **Keys.** Key down, repeat and up (Carbon kinds 1, 2, 3) become press, repeat and release records with values 1, 1 and 0. The raw key code goes through a byte lookup table; the table's contents were not exported, so the key map is still unknown.
- **Characters.** One byte is converted at a time. On v5 the converter is created on first use and converts from a fixed encoding (Carbon number 527) to the application's; if nothing comes out, the input byte is used as it is. Only the first output byte is kept. This is not a Unicode input path.
- **Modifiers.** Kind 4 is compared against the saved modifier mask, bit by bit, for eight masks. A bit that turns on emits a press with value 1, and a bit that turns off emits a release with value 0. An unchanged mask emits nothing. Read on 4.04r2, 4.20r6 and v5.
- **Mouse.** Button events make button records and update a button-state array; the primary button can be remapped when a modifier is held. Movement is either window-local absolute coordinates or relative deltas, and horizontal, vertical and wheel movement each have their own code.

**[bin]** The application router passes keyboard and mouse events to the translator, tracks activation and deactivation, recognizes quit, and handles window-size changes behind a guard. The window focus helper treats its two flags independently: one chooses between resetting the cursor and showing, selecting and raising the window, the other runs an activation helper. Then it asks the engine to redraw.

**[bin]** On 4.04r2 the same engine receiver also gets socket records, so it is not an input-only object.

## Where input goes on v5

**[bin]** The derived method table's event dispatcher needs the engine-running flag and a guard helper to pass. Each event type then goes to its own virtual consumer; type 5 and unknown types are dropped. Keyboard, button and relative-motion records are type 0, and absolute pointer records are type 1.

**[bin]** The type-0 consumer offers the event to several consumers, including the GUI root. One early consumer is skipped when the focused control is a `GuiInputCtrl`. The last fallback takes a press-like keyboard event with a modifier mask and a character in a bounded range and builds a command string that starts `e:`. The type-1 consumer checks that a GUI root exists and passes the event on; the end of that path was not read.

## Limits

- Static only. A visible window, live input delivery, rendering, login and script execution were not observed.
- The end consumers of the v5 event types, the two post-window start-up helpers and the key table are unread. On 4.04r2 a third writer of the engine pointer and most of the 28 functions that touch it were not opened.
- 4.04r2 and 4.20r6 share the inspected branch structure in seven bodies; that is not a whole-client equivalence.
- A Tiger guest run of an unmodified 4.04 copy switched to a smaller black display and then quit to the desktop. It is a prerequisite problem for a later runtime test, not an input result. The earlier software-rendering run is in [lab-mac-tiger-2026-10-31.md](../version-profiles/lab-mac-tiger-2026-10-31.md).
