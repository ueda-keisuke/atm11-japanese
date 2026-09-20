package dev.atm11.japanesehelper.mixin;

import dev.atm11.japanesehelper.Labels;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.ModifyConstant;

@Mixin(targets = "com.yogpc.qp.machine.placer.PlacerScreen", remap = false)
public abstract class PlacerScreenMixin {
    @ModifyConstant(method = "renderModeLabel", constant = @Constant(stringValue = "Pulse"),
            require = 1, expect = 1, allow = 1, remap = false)
    private String atm11helper$pulse(String original) {
        return Labels.text("placer.pulse");
    }

    @ModifyConstant(method = "renderModeLabel", constant = @Constant(stringValue = "Break Only"),
            require = 1, expect = 1, allow = 1, remap = false)
    private String atm11helper$breakOnly(String original) {
        return Labels.text("placer.break_only");
    }

    @ModifyConstant(method = "renderModeLabel", constant = @Constant(stringValue = "Place Only"),
            require = 1, expect = 1, allow = 1, remap = false)
    private String atm11helper$placeOnly(String original) {
        return Labels.text("placer.place_only");
    }
}
