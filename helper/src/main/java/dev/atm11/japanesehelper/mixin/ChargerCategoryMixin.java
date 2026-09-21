package dev.atm11.japanesehelper.mixin;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Reuses AE2's accepted language key without changing the computed quantities. */
@Mixin(targets="appeng.client.integrations.jei.ChargerCategory$1",remap=false)
public abstract class ChargerCategoryMixin {
 @Redirect(method="createWidgets(Lappeng/client/integrations/jei/widgets/WidgetFactory;Ljava/util/List;)V",
  at=@At(value="INVOKE",target="Lnet/minecraft/network/chat/Component;literal(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;"),
  require=1,expect=1,allow=1,remap=false)
 private static MutableComponent atm11helper$chargerPower(String original){
  var match=java.util.regex.Pattern.compile("([0-9]+) turns or ([0-9]+) AE").matcher(original);
  if(match.matches())try{
   int turns=Integer.parseInt(match.group(1)),energy=Integer.parseInt(match.group(2));
   return Component.translatable("ae2.rei_jei_integration.charger_required_power",turns,energy);
  }catch(NumberFormatException ignored){ /* Preserve an unexpected quantity verbatim. */ }
  return Component.literal(original);
 }
}
