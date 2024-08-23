# VRM-Spacing-Animation-Baking
A blender add-on for VRM models that offers Mixamo-like arm/leg spacing options, and shortcuts to quickly bake physics bones like hair and bust movement into animations, with the option of making the animation have the physics loop correctly.

>⚠️ You'll need the VRM Addon for Blender. https://vrm-addon-for-blender.info/en/
>
>⚠️ This will only work for VRM 1.0 models.

![img](https://i.imgur.com/Cx8IKyS.png)

## Features

# SPACING
| Without Spacing | With Spacing |
| --- | --- |
| ![img](https://i.imgur.com/CCpRayr.gif) | ![img](https://i.imgur.com/VULfK9g.gif) |

- Adjust the bone spacing in the current action (animation) for the legs, arms, and shoulders, *even on baked animations*: just like Mixamo's "Character Arm-Space" setting!
  - You can also independantly affect only one side!
  - Great for tweaking animations to better suit your character, such as with large dresses or outfits!
 
# BAKE PHYSICS TOOLSET
- An animation helper suite to bake your animation's spring bones (physics bones) like hair and bust into the animation, for external programs that don't support "easily" physics systems.
  - **Select Physics Bones**: Selects all the possible VRoid VRM bones that are used for physics. No more pattern selecting over and over!
  - **Delete Highlighted Bones (from Animation)**: Deletes the selected bones from the current animation, freeing them and letting them be affected by the VRM add-on's spring bones enabled setting.
  - **VRM Spring Bone Physics ON/OFF**: A quick toggle to enable/disable VRM physics in Blender (courtesy of the VRM add-on) in order to give Blender the tools to record the physics simulation!
  - **Adjust Playback & Bake**: Bakes the hair physics into the animation directly. You can then turn off VRM Spring Bone physics, and you'll notice that the hair still moves (in a predetermined way now) even without physics on!

# LOOPIFY PHYSICS
| Without Loopify | With Loopify |
| --- | --- |
| ![img](https://i.imgur.com/ukhU2cT.gif) | ![img](https://i.imgur.com/Mo2YZKY.gif) |
- **A looping tool to make baked spring bones physics loop (decently) well enough!**
  - Let's you select between using the first or last frame of physics as a looping point, and a user customizable range of frames to ease the animation's transition from the end of the loop to the start of the next!

## Credits
- ChatGPT, Copilot, for the AI assisted coding.
- Showcased model is made of elements from ～Starry Sea～☆彡 KOKONE (https://milkpeach.booth.pm/), Serena Kupopo (https://kupopo.booth.pm/), and Surcen (https://surcen.booth.pm/)
