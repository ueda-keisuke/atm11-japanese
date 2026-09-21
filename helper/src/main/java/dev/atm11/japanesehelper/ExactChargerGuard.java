package dev.atm11.japanesehelper;
import java.io.InputStream;
import java.security.MessageDigest;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.spongepowered.asm.mixin.extensibility.*;
import org.spongepowered.asm.mixin.transformer.throwables.InvalidMixinException;
import org.spongepowered.asm.service.MixinService;
/** Independent, client-only guard for the fixed AE2/JEI Charger label consumer. */
public final class ExactChargerGuard implements IMixinConfigPlugin {
 private static final String TARGET="appeng.client.integrations.jei.ChargerCategory$1";
 private static final String DESCRIPTOR="(Lappeng/client/integrations/jei/widgets/WidgetFactory;Ljava/util/List;)V";
 private static final Map<String,String> HASHES=Map.of(
  TARGET,"f6cbae643d580de1b29d6e33847b8d08b5e119f655901cb6d3f451d0f8be45ea",
  "appeng.client.integrations.jei.ChargerCategory","911c8342d717332af44a4895869aa22a2046df9c0a2efda39200c8733c2b4e1e",
  "appeng.client.integrations.jei.widgets.WidgetFactory","97e20b685495fb3b88324ccc0ce85d0f530b35dbd44830d8590c6faf5b8415bc",
  "appeng.client.integrations.jei.widgets.Label","6402ea1d3b0f43c6a9f39d7d425adb54dabd123f59c017d64f959fffc1e8414c",
  "mezz.jei.api.gui.drawable.IDrawable","18948a204b8fddd3fddb3e2adcb52d4d099a442e9e1eee8a7ca3312f0cbe5cb5",
  "mezz.jei.api.helpers.IJeiHelpers","23468a4af4c3740f467f14a2675cdfdf1c6330afc4d0644585730f1e93f87baf",
  "mezz.jei.api.gui.builder.IRecipeLayoutBuilder","248bb91f4f0952dbe747b42248481299840d588008a0179c80a2c7a37cfda26e");
 private boolean supported;
 private List<String> originalShape;
 private static List<String> shape(ClassNode node){
  if(!node.name.equals(TARGET.replace('.','/')))throw new IllegalStateException("target owner changed");
  var methods=node.methods.stream().filter(m->m.name.equals("createWidgets")&&m.desc.equals(DESCRIPTOR)).toList();
  if(methods.size()!=1)throw new IllegalStateException("createWidgets descriptor/count changed");
  var method=methods.getFirst();
  if(method.access!=Opcodes.ACC_PUBLIC||!method.tryCatchBlocks.isEmpty())throw new IllegalStateException("method access/handlers changed");
  var result=new ArrayList<String>();
  for(var in:method.instructions){
   int op=in.getOpcode();if(op<0)continue;
   String value="";
   if(in instanceof VarInsnNode v)value="var="+v.var;
   else if(in instanceof IntInsnNode i)value="operand="+i.operand;
   else if(in instanceof MethodInsnNode m)value=m.owner+"."+m.name+m.desc+":"+m.itf;
   else if(in instanceof LdcInsnNode l)value=l.cst.getClass().getName()+":"+l.cst;
   else if(in instanceof InvokeDynamicInsnNode d)value=d.name+d.desc+":"+d.bsm+":"+Arrays.deepToString(d.bsmArgs);
   else if(!(in instanceof InsnNode))throw new IllegalStateException("unexpected createWidgets instruction");
   result.add(op+":"+value);
  }
  return result;
 }
 @Override public void onLoad(String pkg){
  supported=false;
  try{
   for(var entry:HASHES.entrySet())try(InputStream in=MixinService.getService().getResourceAsStream(entry.getKey().replace('.','/')+".class")){
    if(in==null)throw new IllegalStateException("missing "+entry.getKey());
    byte[] raw=in.readAllBytes();String digest=HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(raw));
    if(!digest.equals(entry.getValue()))throw new IllegalStateException("class changed "+entry.getKey());
    if(entry.getKey().equals(TARGET)){var node=new ClassNode();new ClassReader(raw).accept(node,0);originalShape=shape(node);}
   }
   supported=true;MixinService.getService().getLogger("atm11_japanese_helper").info("ATM11_CHARGER_SOURCE_OK: fixed AE2/JEI consumer classes match.");
  }catch(Exception failure){MixinService.getService().getLogger("atm11_japanese_helper").error("UNSUPPORTED AE2/JEI Charger: label repair disabled. "+failure.getMessage());}
 }
 @Override public boolean shouldApplyMixin(String target,String mixin){if(!target.equals(TARGET))throw new IllegalStateException("Unexpected Charger target");return supported;}
 @Override public void preApply(String target,ClassNode node,String mixin,IMixinInfo info){
  try{if(!shape(node).equals(originalShape))throw new IllegalStateException("createWidgets shape changed");}
  catch(IllegalStateException failure){throw new InvalidMixinException(info,"Charger createWidgets changed before transformation",failure);}
 }
 @Override public void postApply(String target,ClassNode node,String mixin,IMixinInfo info){MixinService.getService().getLogger("atm11_japanese_helper").info("ATM11_CHARGER_APPLIED: required-power component repaired; no visual claim.");}
 @Override public String getRefMapperConfig(){return null;}
 @Override public void acceptTargets(Set<String> own,Set<String> others){}
 @Override public List<String> getMixins(){return null;}
}
