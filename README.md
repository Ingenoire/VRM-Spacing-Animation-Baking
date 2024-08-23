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
 
# Usage Guide
- Add an animation on your VRoid VRM Model. One excellent add-on to use is [Mwni's Blender Animation Retargeting Add-on](https://github.com/Mwni/blender-animation-retargeting), which works nearly flawlessly for Mixamo sourced animations (that were rigged to the X bot model, 60fps, no model), and only requires a few bone pairings to be edited for other animations like from Actorcore. Remember to delete the mixamo/sourced animation armature after you bake the animation!
- (Optional) If your animation's legs or arms clip or are too spaced out (ex: wide body armature retargetted to a short body armature), you can choose from the drop down menu one of the bone pairs that looks like the culprit, and then press Adjust Spacing. Do this several times (adjust the value above if you're confident you need to adjust way more) and choose other pair of bones (or only affect one of the two by ticking the left or right box) until you're satisfied.
  - It's generally better to do this before you start baking the spring bones (physics), as it'll correspond better to your newer pose, but you can do these adjustments at any point.
- To bake the spring bones (physics), press "Select Physics Bones", then "Delete Highlighted Bones" (from animation).
  - The first step selects all possible VRoid VRM bones that are physics based. (If you need to do some adjustments later on for the physics, such as manually adjusting the physics keys, you can press this to select it all again)
  - The second step deletes the bones from the animation itself. This liberates the bones so that the VRM add-on's spring bones physics can take effect.
- Then, press the VRM Spring Bones Physics OFF button, which turns it off.
- (Optional) It's a good idea to scrub through the timeline (move your position in the timeline) by dragging the timeline cursor, then returning to Frame 0, and rapidly clicking on the timeline cursor, to get a physics positioning you feel would work well for a loop.
- Choose between either using the Last Frame as a physics reference for the start of your animation, or the First frame as a physics reference for the end of your animation.
- Decide on how many physics frames should be deleted from either the end or start of the animation with the Frame Easing slider. The bigger it is, the more smoothing the loop will have at the cost of realism.
- Press Loopify Physics, and then toggle the VRM Spring Bones Physics ON to OFF. Play the animation and you'll see that the animation loops with baked-in physics!

## Credits
- ChatGPT, Copilot, for the AI assisted coding.
- Showcased model is made of elements from ～Starry Sea～☆彡 KOKONE (https://milkpeach.booth.pm/), Serena Kupopo (https://kupopo.booth.pm/), and Surcen (https://surcen.booth.pm/)
