package dev.atm11.japanesehelper;
import java.io.InputStream;
import java.security.MessageDigest;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.spongepowered.asm.mixin.extensibility.*;
import org.spongepowered.asm.mixin.transformer.throwables.InvalidMixinException;
import org.spongepowered.asm.service.MixinService;
/** Version guard scoped independently to AE2's smithing-template consumer. */
public final class ExactFluixGuard implements IMixinConfigPlugin {
 private static final String TARGET="appeng.items.tools.fluix.FluixSmithingTemplateItem";
 private static final Map<String,String> HASHES=Map.of(
  TARGET,"8dc05256c85429b1e4df18e36e5c8bdb93fc4171056cd1eb21a55461ad2b7e1c",
  "net.minecraft.world.item.SmithingTemplateItem","bd22e7bf41ed0f44b61808bb350489be81b463b68de429fc806ae9811d646b83");
 private boolean supported;
 private List<String> constructorShape;
 private static List<String> shape(ClassNode node){
  var methods=node.methods.stream().filter(m->m.name.equals("<init>")&&m.desc.equals("(Lnet/minecraft/world/item/Item$Properties;)V")).toList();
  if(methods.size()!=1)throw new IllegalStateException("constructor count changed");
  var result=new ArrayList<String>();
  for(var in:methods.getFirst().instructions){
   int op=in.getOpcode();if(op<0)continue;
   String value="";
   if(in instanceof VarInsnNode v)value="var="+v.var;
   else if(in instanceof FieldInsnNode f)value=f.owner+"."+f.name+f.desc;
   else if(in instanceof MethodInsnNode m)value=m.owner+"."+m.name+m.desc+":"+m.itf;
   else if(in instanceof LdcInsnNode l)value=String.valueOf(l.cst);
   else if(!(in instanceof InsnNode))throw new IllegalStateException("unexpected constructor instruction");
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
    if(entry.getKey().equals(TARGET)){var node=new ClassNode();new ClassReader(raw).accept(node,0);constructorShape=shape(node);}
   }
   supported=true;MixinService.getService().getLogger("atm11_japanese_helper").info("ATM11_FLUIX_SOURCE_OK: fixed AE2 and Minecraft consumer classes match.");
  }catch(Exception failure){MixinService.getService().getLogger("atm11_japanese_helper").error("UNSUPPORTED AE2 Fluix template: material repair disabled. "+failure.getMessage());}
 }
 @Override public boolean shouldApplyMixin(String target,String mixin){if(!target.equals(TARGET))throw new IllegalStateException("Unexpected Fluix target");return supported;}
 @Override public void preApply(String target,ClassNode node,String mixin,IMixinInfo info){
  try{if(!shape(node).equals(constructorShape))throw new IllegalStateException("constructor shape changed");}
  catch(IllegalStateException failure){throw new InvalidMixinException(info,"Fluix constructor changed before transformation",failure);}
 }
 @Override public void postApply(String target,ClassNode node,String mixin,IMixinInfo info){MixinService.getService().getLogger("atm11_japanese_helper").info("ATM11_FLUIX_APPLIED: ingredient component repaired; no visual claim.");}
 @Override public String getRefMapperConfig(){return null;}
 @Override public void acceptTargets(Set<String> own,Set<String> others){}
 @Override public List<String> getMixins(){return null;}
}
