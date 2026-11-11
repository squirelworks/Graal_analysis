# GS1 condition truth and constant-comparison folding in original 2.05r2

Evidence ID: GS1-TRUTH-205R2-20261109-03, extending GS1-205R2-20261109-01. Target: original Windows Graal2.05 revision2, executable SHA-256 b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08. Target identity, static checks and visual review are researcher supplied, not an independent publication reviewer's binary verification.

## Condition execution and parsing

[2.05][bin] The command compiler selects a condition parsing context. The IF executor evaluates the resulting expression and skips its block when that numeric result equals zero. A fresh original-file read confirms the floating comparison's operand is zero. The evaluator's actual floating return-load continuation was checked separately rather than inferred from a weak recovered return type. This is a zero/nonzero execution rule for ordinary finite values, not a one-or-greater threshold.

[2.05][lab] New owned offline scenes distinguish the disputed cases: computed `(0.5+0)` displays0.5 and takes the true branch; `(-0.5)` displays-0.5 and takes the true branch; `(0+0)` displays0 and remains false. Bare `0.5`, however, displays0.5 but remains false in condition context. The `created` condition is true while its numeric message expansion displays0. These outcomes are separate observations, not one shared numerical oracle.

[2.05][bin] Condition parsing and the numeric parsing used by message expansion are distinct. An unrecognized bare condition token can become a named-flag test, while arithmetic operands are parsed numerically. The observed false result for bare0.5 therefore does not establish rounding, a numerical threshold, or a rule that the arithmetic value one half is false. Flag contents and recognized state names matter. This pass did not set a numeric-looking named flag to prove every possible name collision.

## Constant-comparison folding

[2.05][bin] Comparison syntax is present. When both operands compile as constant numeric leaves, the compiler changes the comparison parent into a numeric leaf before asking the evaluator to calculate its value. That new parent starts at zero, so this ordering evaluates its stored zero instead of performing the comparison. Ordinary arithmetic folding evaluates first and replaces the parent type afterwards. The two paths must not be conflated.

[2.05][lab] The new scenes show false with numeric display0 for `1==1`, `1!=0`, `1<2`, `2>1`, `1=1`, and `(1+0)==1`. Dynamic `playerx==playerx`, `playerx<=playerx`, and `playerx>=playerx` display1 and are true. Dynamic `playerx!=playerx` displays0 and is false. Assigning1 to an NPC-local variable and testing `this.a==1` displays1 and is true. These controls distinguish the constant-folding defect from absent comparison support. They do not validate every operator alias, mixed type, precedence or boundary condition.

## Verification and limits

[lab] Sixteen independently authored cases were run in two fresh offline fixtures. The first layout had HUD/minimap overlap. A second layout moved labels clear of that UI; fifteen labels were wholly readable there. The actor partly overlapped the greater-than control, so its outcome is taken from the identical script's unobscured label in the first run. No missing or obscured label was counted as false. The companion observations.json records numeric display, branch result and readable run separately for every case.

[2.05][bin] Ten selected original-file instruction regions were read afresh and matched the earlier selected assembly. They cover condition compilation, numeric/condition leaves, the IF branch, comparison and arithmetic folding, allocation/initialization, numeric evaluation and its floating return. The zero comparison operand was read directly. This static mechanism is corroborated by distinguishing displayed outcomes; no live expression-node memory was inspected.

[lab] Both runs used Wine and a private virtual display in isolated user/PID/network namespaces, with no server and no external network. Executable bytes were unchanged. Exact target-package files were overlaid on explicitly labeled2.31 donor assets and an owned synthetic level; this is not an authentic complete original2.05 distribution. Both runs exited with supervisor status0 and completed cleanup. Original screenshots, private instruction material and exact harness/configuration hashes remain in the private evidence bundle.

Only this exact build is qualified. Other revisions, nonfinite values, malformed syntax, every comparison alias, complete precedence, lexical corner cases and named-flag collisions remain open. Reproductions should keep numerical evaluation, condition-name resolution and this build's comparison-folding behavior separate. Silently correcting the compiler defect changes compatibility behavior.

Evidence retrieval: `GS1-TRUTH-205R2-20261109-03` in [the evidence index](../docs/evidence-index.tsv). Frozen private manifest SHA-256: `dd3ca4e8d23cbcad90c8d0a28dbe657e36c7b4c376a19d76839c68a70909b10d` (researcher supplied; private material not inspected by the editor).
