package helpertest;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.ZipFile;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.*;
import net.minecraft.network.chat.contents.TranslatableContents;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.*;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.service.MixinService;
/** Actual createWidgets, WidgetFactory and Label; uninitialized Minecraft fixture, no GUI. */
public final class ChargerHarness {
 static final String TARGET="appeng.client.integrations.jei.ChargerCategory$1", OWNER=TARGET.replace('.','/');
 static final String KEY="ae2.rei_jei_integration.charger_required_power", HANDLER="atm11helper$chargerPower";
 static final String LITERAL="(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;";
 static final String WIDGETS="appeng.client.integrations.jei.widgets.";
 static void require(boolean ok,String why){if(!ok)throw new AssertionError(why);}
 static byte[] raw(String name)throws Exception{try(var in=ChargerHarness.class.getClassLoader().getResourceAsStream(name.replace('.','/')+".class")){return Objects.requireNonNull(in).readAllBytes();}}
 static ClassNode node(byte[] raw){var n=new ClassNode();new ClassReader(raw).accept(n,ClassReader.SKIP_DEBUG|ClassReader.SKIP_FRAMES);return n;}
 static String text(MethodNode m){var t=new Textifier();m.accept(new TraceMethodVisitor(t));var s=new StringWriter();t.print(new PrintWriter(s));return s.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n","");}
 static String normalize(MethodNode m){
  var copy=new MethodNode(m.access,m.name,m.desc,m.signature,m.exceptions.toArray(String[]::new));m.accept(copy);int calls=0;
  for(var in:copy.instructions)if(in instanceof MethodInsnNode c&&c.owner.equals(OWNER)&&c.name.endsWith(HANDLER)){
   require(c.getOpcode()==Opcodes.INVOKESTATIC&&c.desc.equals(LITERAL)&&!c.itf,"Incorrect redirected handler descriptor");
   var load=c.getPrevious();var store=load.getPrevious();require(load instanceof VarInsnNode v&&v.getOpcode()==Opcodes.ALOAD&&v.var==4,"Unexpected redirect reload");require(store instanceof VarInsnNode v&&v.getOpcode()==Opcodes.ASTORE&&v.var==4,"Unexpected redirect spill");copy.instructions.remove(load);copy.instructions.remove(store);
   c.owner="net/minecraft/network/chat/Component";c.name="literal";c.itf=true;calls++;
  }
  require(calls==1,"Expected exactly one replacement invocation");return text(copy);
 }
 static Class<?> define(byte[] bytes){return new ClassLoader(ChargerHarness.class.getClassLoader()){Class<?> make(){return defineClass(TARGET,bytes,0,bytes.length);}}.make();}
 static sun.misc.Unsafe unsafe()throws Exception{var f=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");f.setAccessible(true);return (sun.misc.Unsafe)f.get(null);}
 static Object field(Object obj,String name)throws Exception{var f=obj.getClass().getDeclaredField(name);f.setAccessible(true);return f.get(obj);}
 static Map<String,Object> capture(Class<?> type)throws Exception{
  var factoryType=Class.forName(WIDGETS+"WidgetFactory");var factory=unsafe().allocateInstance(factoryType);
  // createWidgets does not draw or dereference the unfilledArrow drawable.
  // Its real constructor records null, x, y; no JEI GUI object is synthesized.
  var instance=unsafe().allocateInstance(type);var widgets=new ArrayList<Object>();
  var method=type.getDeclaredMethod("createWidgets",factoryType,List.class);method.setAccessible(true);method.invoke(instance,factory,widgets);
  require(widgets.size()==2,"Widget count changed");var arrow=widgets.getFirst();var label=widgets.getLast();
  require(arrow.getClass().getName().equals(WIDGETS+"DrawableWidget")&&label.getClass().getName().equals(WIDGETS+"Label"),"Widget types changed");
  require(field(arrow,"x").equals(52)&&field(arrow,"y").equals(8),"Arrow coordinates changed");
  require(field(label,"x").equals(20f)&&field(label,"y").equals(35f),"Label coordinates changed");
  require(field(label,"color").equals(0xFF7E7E7E)&&field(label,"shadow").equals(false)&&field(label,"align").toString().equals("LEFT"),"Label style changed");
  require(field(label,"maxWidth").equals(-1),"Label width changed");
  return Map.of("component",field(label,"text"),"arrow_x",52,"arrow_y",8,"label_x",20,"label_y",35,"color_argb",0xFF7E7E7E,"shadow",false,"align","LEFT","max_width",-1);
 }
 static void result(Path out,Map<String,?> report)throws Exception{Files.writeString(out.resolve("result.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report)+"\n");System.out.println("PASS Charger "+report);}
 public static void main(String[] args)throws Exception{
  Path out=Path.of(args[0]);Files.createDirectories(out);String side=args[1],mode=args[2];
  MixinBootstrap.init();var physical=MixinEnvironment.Side.valueOf(side);MixinEnvironment.getDefaultEnvironment().setSide(physical);MixinEnvironment.getCurrentEnvironment().setSide(physical);
  var configs=List.of("atm11_japanese_helper.mixins.json","atm11_japanese_helper.mining.mixins.json","atm11_japanese_helper.measurements.mixins.json","atm11_japanese_helper.neoforge.mixins.json","atm11_japanese_helper.ae2.fluix.mixins.json","atm11_japanese_helper.ae2.charger.mixins.json");
  for(var config:configs)Mixins.addConfiguration(config);
  var transformer=((OfflineMixinService)MixinService.getService()).transformer();
  if(mode.equals("ae2-absent")||mode.equals("jei-absent")){
   var w=new ClassWriter(0);w.visit(Opcodes.V25,Opcodes.ACC_PUBLIC,"helpertest/Sentinel",null,"java/lang/Object",null);w.visitEnd();byte[] before=w.toByteArray();
   require(Arrays.equals(before,transformer.transformClassBytes("helpertest.Sentinel","helpertest.Sentinel",before)),"Missing dependency changed unrelated class");
   var guard=new dev.atm11.japanesehelper.ExactChargerGuard();guard.onLoad("dev.atm11.japanesehelper.mixin");require(!guard.shouldApplyMixin(TARGET,"ChargerCategoryMixin"),"Absent dependency guard enabled");
   result(out,Map.of("pass",true,"mode",mode,"physical_side",side,"unrelated_class_unchanged",true,"game_started",false,"visual_qa",0));return;
  }
  byte[] original=raw(TARGET);
  if(mode.startsWith("changed-")){
   var n=node(original);var m=n.methods.stream().filter(x->x.name.equals("createWidgets")).findFirst().orElseThrow();
   if(mode.equals("changed-descriptor"))m.desc=m.desc.replace("Ljava/util/List;","Ljava/util/Collection;");
   if(mode.equals("changed-access"))m.access|=Opcodes.ACC_SYNCHRONIZED;
   for(var in:m.instructions){
    if(mode.equals("changed-constant")&&in instanceof IntInsnNode i&&i.operand==10)i.operand=11;
    if(mode.equals("changed-recipe")&&in instanceof InvokeDynamicInsnNode d)d.bsmArgs[0]="\u0001 turns or 1700 AE";
    if(mode.equals("changed-call")&&in instanceof MethodInsnNode c&&c.name.equals("literal"))c.name="translatable";
   }
   var w=new ClassWriter(0);n.accept(w);original=w.toByteArray();
  }
  byte[] transformed=transformer.transformClassBytes(TARGET,TARGET,original);
  if(side.equals("SERVER")||mode.equals("guard-disabled")){
   require(Arrays.equals(original,transformed),"Server or unsupported target changed");
   result(out,Map.of("pass",true,"physical_side",side,"mode",mode,"target_unchanged",true,"game_started",false,"visual_qa",0));return;
  }
  require(!mode.startsWith("changed-"),"Altered consumer unexpectedly transformed");require(!Arrays.equals(original,transformed),"Target not transformed");
  var before=node(original);var after=node(transformed);require(before.fields.size()==after.fields.size(),"Fields changed");int changed=0;
  for(var m:before.methods){var actual=after.methods.stream().filter(x->x.name.equals(m.name)&&x.desc.equals(m.desc)).findFirst().orElseThrow();require(m.access==actual.access,"Original method access changed");if(m.name.equals("createWidgets")){Files.writeString(out.resolve("original-method.txt"),text(m));Files.writeString(out.resolve("normalized-method.txt"),normalize(actual));require(text(m).equals(normalize(actual)),"Other createWidgets instructions changed");changed++;}else require(text(m).equals(text(actual)),"Unrelated original method changed");}
  require(changed==1&&after.methods.size()==before.methods.size()+1,"Unexpected transformed method count");new ClassReader(transformed).accept(new CheckClassAdapter(new ClassWriter(0),true),0);Files.write(out.resolve("ChargerCategory$1.class"),transformed);
  FluixHarness.ensureFmlLoader();net.minecraft.SharedConstants.tryDetectVersion();
  // Do not construct Minecraft, create registries, initialize GLFW or call font/draw.
  var mc=Class.forName("net.minecraft.client.Minecraft");var singleton=mc.getDeclaredField("instance");singleton.setAccessible(true);var prior=singleton.get(null);
  require(prior==null,"Unexpected active Minecraft singleton in offline harness");var fixture=unsafe().allocateInstance(mc);singleton.set(null,fixture);
  var previous=Language.getInstance();
  try{
   var baseline=capture(define(original));var fixedType=define(transformed);var repaired=capture(fixedType);
   var orig=(Component)baseline.get("component");var component=(Component)repaired.get("component");
   require(component.getContents() instanceof TranslatableContents,"Output is not translatable");var contents=(TranslatableContents)component.getContents();
   require(contents.getKey().equals(KEY)&&Arrays.equals(contents.getArgs(),new Object[]{10,1600}),"Translation key/numeric args changed");
   var en=FluixHarness.language(Path.of(args[3]),"assets/ae2/lang/en_us.json");var ja=new LinkedHashMap<>(en);ja.putAll(FluixHarness.language(Path.of(args[4]),"assets/ae2/lang/ja_jp.json"));
   var observations=new ArrayList<Map<String,Object>>();
   for(var locale:List.of("en_us","ja_jp","en_us_restored")){
    var values=locale.equals("ja_jp")?ja:en;Language.inject(new FluixHarness.Values(values));
    require(orig.getString().equals("10 turns or 1600 AE"),"Baseline gap not reproduced");
    var expected=String.format(Locale.ROOT,values.get(KEY),10,1600);require(component.getString().equals(expected),"Native label language mismatch");
    observations.add(Map.of("locale",locale,"before",orig.getString(),"after",component.getString(),"same_component_locale_cycle",true));
   }
   var handler=Arrays.stream(fixedType.getDeclaredMethods()).filter(m->m.getName().endsWith(HANDLER)).findFirst().orElseThrow();handler.setAccessible(true);
   var parserCases=new ArrayList<Map<String,Object>>();
   for(String input:List.of("0 turns or 0 AE","1 turns or 32 AE","2147483647 turns or 2147483647 AE","unchanged","10 turns or 1600 AE\n","-1 turns or 1600 AE","2147483648 turns or 1600 AE","10 turns or 2147483648 AE")){
    var parsed=(Component)handler.invoke(null,input);boolean valid=input.equals("0 turns or 0 AE")||input.equals("1 turns or 32 AE")||input.equals("2147483647 turns or 2147483647 AE");
    require((parsed.getContents() instanceof TranslatableContents)==valid,"Parser classification wrong");require(parsed.getString().equals(input),"Parser changes English quantity/fallback");
    parserCases.add(Map.of("input",input,"translatable",valid,"output",parsed.getString()));
   }
   var report=new LinkedHashMap<String,Object>();report.put("pass",true);report.put("physical_side",side);report.put("observations",observations);report.put("parser_cases",parserCases);report.put("configs_registered",configs);report.put("actual_createWidgets_executed",true);report.put("actual_WidgetFactory_label_and_Label_constructor_executed",true);report.put("all_original_instructions_except_one_literal_call_preserved",true);var style=new LinkedHashMap<>(repaired);style.remove("component");report.put("widget_assertions",style);report.put("game_started",false);report.put("visual_qa",0);report.put("fixture_limitations","Unsafe-allocated Minecraft singleton with null font, WidgetFactory with null drawable, anonymous View without constructor; actual createWidgets/label/style code runs, but no recipe buildSlots, bounds, draw, font, real JEI GUI, game initialization or dedicated server launch.");
   result(out,report);
  }finally{Language.inject(previous);singleton.set(null,prior);}
 }
}
