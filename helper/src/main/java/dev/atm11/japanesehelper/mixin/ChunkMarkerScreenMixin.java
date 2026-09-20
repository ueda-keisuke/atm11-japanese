package dev.atm11.japanesehelper.mixin;

import dev.atm11.japanesehelper.Labels;
import net.minecraft.network.chat.MutableComponent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.ModifyConstant;
import org.spongepowered.asm.mixin.injection.Redirect;

@Mixin(targets = "com.yogpc.qp.machine.marker.ChunkMarkerScreen", remap = false)
public abstract class ChunkMarkerScreenMixin {
    @ModifyConstant(method = "extractLabels", constant = @Constant(stringValue = "Size"),
            require = 2, expect = 2, allow = 2, remap = false)
    private String atm11helper$size(String original) {
        return Labels.text("chunk_marker.size");
    }

    @Redirect(method = "init", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/network/chat/Component;literal(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;"),
            require = 6, expect = 6, allow = 6, remap = false)
    private MutableComponent atm11helper$button(String original) {
        return Labels.chunkButton(original);
    }
}
