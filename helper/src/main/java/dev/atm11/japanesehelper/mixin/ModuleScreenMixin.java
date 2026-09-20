package dev.atm11.japanesehelper.mixin;

import dev.atm11.japanesehelper.Labels;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.Constant;
import org.spongepowered.asm.mixin.injection.ModifyConstant;

@Mixin(targets = "com.yogpc.qp.machine.module.ModuleScreen", remap = false)
public abstract class ModuleScreenMixin {
    @ModifyConstant(method = "extractLabels", constant = @Constant(stringValue = "Modules"),
            require = 1, expect = 1, allow = 1, remap = false)
    private String atm11helper$modules(String original) {
        return Labels.text("module.modules");
    }
}
