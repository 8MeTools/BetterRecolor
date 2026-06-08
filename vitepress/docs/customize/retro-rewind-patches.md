# Retro Rewind Patches

Last updated: May 18, 2026

This page summarizes the parts of Retro Rewind's `Patches` system that matter when working with UI files.

::: info
This page is supplemental documentation based on [Patches on Tockdom Wiki](https://wiki.tockdom.com/wiki/Patches). Check the original page for the latest specification.
:::

## Overview

`Patches` is a file override system. When the game requests a file, the system can load a user-provided file instead. If no matching user file exists, the game falls back to the file bundled with the pack.

It can be used similarly to My Stuff, but it is more flexible. You can replace an entire `.szs` file, or patch specific files inside an archive.

Implementation references:

- [LooseArchiveOverrides.cpp](https://github.com/Retro-Rewind-Team/rr-pulsar/blob/main/PulsarEngine/IO/LooseArchiveOverrides.cpp)
- [LooseBRSAROverrides.cpp](https://github.com/Retro-Rewind-Team/rr-pulsar/blob/main/PulsarEngine/Sound/LooseBRSAROverrides.cpp)

## Supported Override Types

`Patches` supports the following override types.

| Type | Description |
| --- | --- |
| Full-file override | Replaces a requested game file with a loose file. |
| `.szs` archive member override | Replaces, adds, or deletes files such as `.brlyt`, `.brlan`, or `.tpl` inside an `.szs` archive. |
| `revo_kart.brsar` sound override | Replaces `.brwsd`, `.brbnk`, or `.brseq` files by BRSAR File ID. |
| Packed patch archive | Bundles multiple patch files into a single U8 / SZS archive. |

## Full-File Overrides

To replace an entire file, place the edited file in the `Patches` folder and give it the same name as the target file.

Example:

```text
beginner_course.szs
n_Circuit32_n.brstm
n_Circuit32_f.brstm
```

When the game loads a matching file, the file from `Patches` is used instead.

This method is best for replacing complete `.szs`, `.brstm`, or similar files.

::: warning
Full-file overrides are matched by file name. If multiple game files share the same base name, one loose file may affect more than one target.
:::

## Replace Files Inside an `.szs` Archive

To replace files such as `.brlyt` or `.brlan` inside an `.szs` archive, use this naming format:

```text
[Folder1][Folder2]filename.originalFormat.ArchiveTag
```

| Segment | Description |
| --- | --- |
| `Folder1` | A top-level folder inside the `.szs`, such as `bg`, `button`, or `control`. |
| `Folder2` | A child folder inside `Folder1`, such as `anim`, `blyt`, `ctrl`, or `timg`. |
| `filename` | The target file name, such as `common_w004_menu`. |
| `originalFormat` | The original extension, such as `.brlan`, `.brlyt`, or `.tpl`. |
| `ArchiveTag` | The target `.szs` file name without `.szs`, such as `menusingle`. |

`ArchiveTag` is case-insensitive. For example, `MenuSingle.szs` can be targeted with `menusingle`.

### Without Folder Tags

```text
common_w004_menu.brlyt.menusingle
```

This targets every `common_w004_menu.brlyt` inside `MenuSingle.szs`.

Examples:

- `MenuSingle.szs/button/blyt/common_w004_menu.brlyt`
- `MenuSingle.szs/message_window/blyt/common_w004_menu.brlyt`

This is useful when you intentionally want to replace every matching file, but it can also cause unintended changes.

### With Folder Tags

```text
[button][blyt]common_w004_menu.brlyt.menusingle
```

This targets only `MenuSingle.szs/button/blyt/common_w004_menu.brlyt`.

The same pattern can be used for any `.szs` archive as long as you know the internal path and the archive tag.

## Add Files to an `.szs` Archive

Use the same naming format to add a file:

```text
[Folder1][Folder2]filename.originalFormat.ArchiveTag
```

For example, to add `hogehoge.brlyt` under `button/blyt` in `MenuSingle.szs`:

```text
[button][blyt]hogehoge.brlyt.menusingle
```

The parent directory must already exist in the target archive.

## Delete Files from an `.szs` Archive

To delete a file, add `.delete` after the original extension.

```text
[Folder1][Folder2]filename.originalFormat.delete.ArchiveTag
```

Example:

```text
[button][blyt]common_w004_menu.brlyt.delete.menusingle
```

If you omit the folder tags, every matching file in the archive is deleted.

```text
common_w004_menu.brlyt.delete.menusingle
```

::: warning
Adding or deleting archive members requires the archive to be rebuilt in memory. This is more expensive than a simple replacement.
:::

## Use Packed Patch Archives

When you need to replace many subfiles, a packed patch archive is easier to manage than many loose files.

Naming format:

```text
ModName.ArchiveTag.szs
```

| Segment | Description |
| --- | --- |
| `ModName` | Any name you choose. |
| `ArchiveTag` | The target `.szs` file name without `.szs`. |

Example:

```text
MyMenuPack.menusingle.szs
```

Suppose the archive contains this tree:

```text
MyMenuPack.menusingle.szs
└── bg
    └── timg
        └── tt_obi_check_000.tpl
```

The system treats it like this loose patch:

```text
[bg][timg]tt_obi_check_000.tpl.menusingle
```

Packed patch archives must be regular U8 archives or Yaz0-compressed `.szs` files.

### Priority

If multiple packed archives target the same internal file, add numeric prefixes to control priority. Lower numbers take priority.

```text
001.MyMenuPack.menusingle.szs
010.MyMenuPack2.menusingle.szs
```

## Replace Files Inside BRSAR

Files inside `revo_kart.brsar` are replaced by BRSAR File ID.

Basic format:

```text
FileId.extension
```

Format with a label:

```text
FileId.label.extension
```

Supported extensions:

- `.brwsd` or `.rwsd`
- `.brbnk` or `.rbnk`
- `.brseq` or `.rseq`

Examples:

```text
123.brwsd
123.menu_click.brwsd
456.brbnk
789.brseq
```

The File ID must be in the range `0` to `1023`.

## Choosing an Override Type

| Type | Use when |
| --- | --- |
| Full-file override | You want to replace a complete `.szs`, `.brstm`, or similar file. |
| `.szs` archive member override | You only need to change part of a larger archive. |
| Packed patch archive | You want to manage multiple archive member overrides as one file. |
| BRSAR override | You want to replace effects, sequences, or banks inside `revo_kart.brsar`. |

## Limitations and Notes

- Full-file overrides may be matched by file name only.
- Tagged archive member overrides and full-file overrides each have index limits.
- BRSAR overrides use File IDs from `0` to `1023`.
- Internal archive patches are applied when compressed `.szs` files are loaded.
- If the file name or internal path is wrong, the patch will not match.

If an internal archive patch is too large, Dolphin may log a message like this:

```text
[Pulsar] Loose override repack allocation failed for 'SZSName': old=0x0 new=0x0 growth=0xSize source-heap growth capped.
```

In that case, use a full-file override instead of an internal archive patch.

