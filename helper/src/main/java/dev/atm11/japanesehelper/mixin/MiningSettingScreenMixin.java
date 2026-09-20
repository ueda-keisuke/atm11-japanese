package dev.atm11.japanesehelper.mixin;

import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.Slice;

/** Localize only the two precision-state captions in the hash-pinned screen. */
@Mixin(targets = "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen", remap = false)
public abstract class MiningSettingScreenMixin {
    @Shadow
    private static MutableComponent getTrans(String key, Object... args) {
        throw new AssertionError("Mixin shadow was not applied");
    }

    @Redirect(
            method = {"init()V", "lambda$init$6(Lnet/minecraft/client/gui/components/Button;)V"},
            slice = @Slice(from = @At(value = "CONSTANT", args = "stringValue=tooltip.screen.precision_mode")),
            at = @At(value = "INVOKE", target = "Lcom/direwolf20/mininggadgets/client/screens/MiningSettingScreen;getTrans(Ljava/lang/String;[Ljava/lang/Object;)Lnet/minecraft/network/chat/MutableComponent;", ordinal = 0),
            require = 2, expect = 2, allow = 2)
    private static MutableComponent atm11helper$precision(String key, Object[] args) {
        if ("tooltip.screen.precision_mode".equals(key) && args != null && args.length == 1
                && args[0] instanceof Boolean enabled) {
            return Component.translatable("atm11_japanese_helper.mininggadgets.precision_mode."
                    + (enabled ? "enabled" : "disabled"));
        }
        return getTrans(key, args);
    }
}
