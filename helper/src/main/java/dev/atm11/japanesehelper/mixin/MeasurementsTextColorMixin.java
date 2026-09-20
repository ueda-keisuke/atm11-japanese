package dev.atm11.japanesehelper.mixin;

import net.minecraft.network.chat.Component;
import net.neoforged.neoforge.common.TranslatableEnum;
import org.spongepowered.asm.mixin.Mixin;

@Mixin(targets = "com.mrbysco.measurements.config.TextColor", remap = false)
public abstract class MeasurementsTextColorMixin implements TranslatableEnum {
    @Override public Component getTranslatedName() {
        String name = ((Enum<?>) (Object) this).name();
        return Component.translatableWithFallback("atm11_japanese_helper.measurements.enum.TextColor." + name, name);
    }
}
