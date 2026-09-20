package dev.atm11.japanesehelper.mixin;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;
/** Correct the materials component, preserving the separate item-name key. */
@Mixin(targets="appeng.items.tools.fluix.FluixSmithingTemplateItem", remap=false)
public abstract class FluixTemplateMixin {
 @ModifyArg(method="<init>(Lnet/minecraft/world/item/Item$Properties;)V",
   at=@At(value="INVOKE",target="Lnet/minecraft/world/item/SmithingTemplateItem;<init>(Lnet/minecraft/network/chat/Component;Lnet/minecraft/network/chat/Component;Lnet/minecraft/network/chat/Component;Lnet/minecraft/network/chat/Component;Ljava/util/List;Ljava/util/List;Lnet/minecraft/world/item/Item$Properties;)V"),
   index=1, require=1, expect=1, allow=1)
 private static Component atm11helper$fluixIngredient(Component previous) {
  return Component.translatable("block.ae2.fluix_block").withStyle(ChatFormatting.BLUE);
 }
}
