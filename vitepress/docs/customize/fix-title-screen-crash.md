# Fix for Retro Rewind v6.13.5+: Crashes Immediately After Selecting a License

Last Updated: November 17, 2026

It's been a while. This is the administrator of BetterRecolor.

I received reports from users who updated to **Retro Rewind v6.13.5** or later that the game "crashes when loading the title screen," and I have resolved the issue, so I'm documenting it here.

This applies to **users using SZS that has been edited to allow button colors to be defined on the brlyt side** (hereafter referred to as the "Recolor" family). If your button colors have changed in a way that is independent of in-game color settings, you are almost certainly affected by this issue.

## Solution
If a Pane named `fuchi_pattern` does not exist in the target BRLYT file, create a new Pane name as a dummy.

### Target Files
- /button/blyt/common_w067_title_large_3parts.brlyt
- /button/blyt/common_w071_title_large_2parts.brlyt
- /button/blyt/common_w072_title_large_1parts.brlyt

Detailed information will be provided below.

## When Did This Issue Start?

On 2026/11/07, RR was updated to **v6.13.5**. The change log announced on Discord contained the following description. This appears to be the cause:

```text
- Modified the button colors to readd the button animations.
```

Due to this update, some My Stuff users began experiencing crashes immediately after selecting a license on the title screen.

## The Code Causing the Issue
Looking at the git commit history, the following code was added prior to the RR update:
```cpp
void UpdateTitleButtonColors(Pages::MainMenu *page) {
    // The Channel frame is not loaded on Dolphin. Use the page's loaded count.
    for (u32 i = 0; i < page->internControlCount; ++i) {
        LayoutUIControl &frame = page->buttonTitles[i];
        for (u32 j = 0; j < frame.childrenGroup.controlCount; ++j) {
            PushButton *button = frame.childrenGroup.GetControl<PushButton>(j);
            nw4r::lyt::Picture *pattern = static_cast<nw4r::lyt::Picture *>(button->fuchi_pattern);
            // Remove the title layout's yellow tint without changing animation alpha.
            for (u32 k = 0; k < 4; ++k) {
                pattern->vertexColours[k].r = 255;
                pattern->vertexColours[k].g = 255;
                pattern->vertexColours[k].b = 255;
            }
        }
    }
}
kmBranch(0x80851108, UpdateTitleButtonColors);
```

Reference: [Fix title button UI colors - rr-pulsar](https://github.com/Retro-Rewind-Team/rr-pulsar/commit/c67b16b18d62bd27193a29de890ddb0482a85c13)

It is fine if you do not know how to read C++ code. As you can tell from the function name, this is responsible for updating the button colors on the title screen.

Let's look at this specifically. The target Pane name is `fuchi_pattern`. An implementation like `pattern->vertexColours[k].r = 255` sets the vertex color value to 255. Since the same process is performed in RGB, representing a vertex color in HTML color codes would be `#FFFFFF` (white).

## Checking the brlyt Configuration
![The vertex color of fuchi_pattern in the official brlyt is yellow (#FFFF00FF)](/img/fix-title-screen-crash/01.png)

This is a preview when opening `/button/blyt/common_w071_title_large_2parts.brlyt` included in the official Title.szs using Switch Toolbox. If you select the `fuchi_pattern` Pane and check the Vertex Color field, it shows `#FFFF00FF` (yellow). The final `FF` is the alpha value (transparency).

The aforementioned C++ code is responsible for changing this yellow to white. In other words, while it was `#FFFF00FF` before the change, it becomes `#FFFFFFFF` after the code is applied. Please see below for an image of the result after the change.

![Preview of fuchi_pattern's vertex color set to white](/img/fix-title-screen-crash/02.png)

You might notice the pink sections, but you can safely ignore them for now. In the official brlyt, button colors are determined by the game, so these pink sections aren't actually visible.

::: details Why the yellow must be changed to white
In Retro Rewind, you can set HUD colors in-game, but the colors set there are not properly reflected for the title buttons. For example, if you set the HUD color to blue, the title button color appears green instead of blue. This is because yellow and blue are mixed on the brlyt side. To resolve this visual issue, RR uses C++ code to change the yellow to white.
:::

## Cause of Crashes in the "Recolor" Family
In the "Recolor" family, the Pane name has been changed from `fuchi_pattern`. For example, in BTRC, the name was changed to `fuchi_pattern2` so that colors can be applied at the SZS level rather than through the game system. I believe others also adopt this method of changing Pane names.

In the aforementioned C++ code, if the Pane name `fuchi_pattern` does not exist, the proper processing cannot be performed, resulting in a crash.

## Solution: Create a Dummy `fuchi_pattern`
Conversely, as long as the Pane name `fuchi_pattern` exists, the crash issue can be prevented.

Since colors are applied at the SZS level, we cannot delete `fuchi_pattern2`. Let's create a new Pane in brlyt named `fuchi_pattern`.

This guide explains how to edit BRLYT using the GUI application Switch Toolbox.

In the working folder, I recommend placing not only Title.szs but also the extracted folder (Title.d).

![Screen showing the file list in File Explorer](/img/fix-title-screen-crash/10.png)

### 1. Open SZS with Switch Toolbox
SZS files can be opened with Switch Toolbox. Once opened, navigate to `button` → `blyt` and double-click the target `.brlyt` file to open it.

![Screen showing SZS opened in Switch Toolbox, displaying brlyt within button/blyt](/img/fix-title-screen-crash/03.png)

The `.brlyt` files to be edited are as follows:
- /button/blyt/common_w067_title_large_3parts.brlyt
- /button/blyt/common_w071_title_large_2parts.brlyt
- /button/blyt/common_w072_title_large_1parts.brlyt

### 2. Create a New Pane

After the preview appears, right-click on the preview grid and select **Create Pane (New Pane Creation)** → **Picture Pane**.
![Selecting Create Pane → Picture Pane from the right-click menu in the preview](/img/fix-title-screen-crash/04.png)

You should see a new white square. The Pane has now been created. By default, the Pane should be named `P_pict`.

![Picture Pane created with the name P_pict](/img/fix-title-screen-crash/05.png)

### 3. Change the Pane Name/Coordinates
Select `P_pict` and choose **Pane** on the left.
You can change the Pane name by modifying the **Name** field located just below the Pane info. In this case, please change it to `fuchi_pattern`.

![Checking the Name field and Translate coordinates in the Pane tab](/img/fix-title-screen-crash/06.png)

Next, change the coordinates. To be honest, this isn't strictly necessary, but let's do it anyway.

Find **Translate** located slightly below the name change. In the image above, the coordinates are X: -100/Y: -37, but these values vary by person. Change both X and Y coordinates to 0. The square should now be centered.

### 4. Change the Pane Transparency
Now, move to the **Picture Pane** tab and change the transparency of the Vertex Color.
![Vertex Colors field in the Picture Pane tab](/img/fix-title-screen-crash/07.png)

Selecting the **ALL** section will bring up the color palette. Set the transparency to 0.

![Color Dialog with A set to 0 and Hex set to FFFFFF00](/img/fix-title-screen-crash/08.png)

The white square is no longer visible in the preview. Since the RR-side code does not modify the alpha value, the white square will not be displayed in the game either.

### 5. Save the brlyt
You can save the brlyt via **File** → **Save As** in the top left. Save it by overwriting the brlyt in the extracted SZS file.

![Saving brlyt via File → Save As](/img/fix-title-screen-crash/09.png)

::: warning
Operations for extracting and compressing SZS files will not be covered here.
:::
Since we edited `common_w067_title_large_3parts.brlyt` this time, please follow the same steps to create Panes for other files as well.

## Verify in Game
Once you have compressed the SZS containing the modified brlyt, verify that it works correctly in-game. If you can proceed without crashing, you have succeeded. Great job!

Translation by [PLaMo Translate Desktop](https://github.com/tanakh/plamo-translate-desktop)
