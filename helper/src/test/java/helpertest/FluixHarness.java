package helpertest;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.ZipFile;
import net.minecraft.ChatFormatting;
import net.minecraft.core.*;
import net.minecraft.core.registries.*;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.*;
import net.minecraft.resources.*;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.*;
import net.minecraft.world.item.component.TooltipDisplay;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.*;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.service.MixinService;
/** Actual Mixin and actual item tooltips in isolated registries; no game or GUI. */
public final class FluixHarness {
 static final String TARGET="appeng.items.tools.fluix.FluixSmithingTemplateItem", OWNER=TARGET.replace('.','/'), HANDLER="atm11helper$fluixIngredient";
 static final String TITLE="item.ae2.fluix_upgrade_smithing_template", MATERIAL="block.ae2.fluix_block";
 static void require(boolean ok,String msg){if(!ok)throw new AssertionError(msg);}
 static ClassNode node(byte[] raw){var n=new ClassNode();new ClassReader(raw).accept(n,ClassReader.SKIP_DEBUG|ClassReader.SKIP_FRAMES);return n;}
 static String text(MethodNode m){var t=new Textifier();m.accept(new TraceMethodVisitor(t));var s=new StringWriter();t.print(new PrintWriter(s));return s.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n","");}
 static void variable(AbstractInsnNode in,int opcode,int slot){require(in instanceof VarInsnNode v&&v.getOpcode()==opcode&&v.var==slot,"Unexpected ModifyArg spill/reload sequence");}
 static String normalize(MethodNode method){
  var copy=new MethodNode(method.access,method.name,method.desc,method.signature,method.exceptions.toArray(String[]::new));method.accept(copy);
  var calls=new ArrayList<MethodInsnNode>();for(var in:copy.instructions)if(in instanceof MethodInsnNode c&&c.owner.equals("net/minecraft/world/item/SmithingTemplateItem")&&c.name.equals("<init>"))calls.add(c);
  require(calls.size()==1,"Wrong superclass constructor count");
  var cursor=calls.getFirst().getPrevious();var injected=new ArrayList<AbstractInsnNode>();
  for(int slot=7;slot>=3;slot--){variable(cursor,Opcodes.ALOAD,slot);injected.add(cursor);cursor=cursor.getPrevious();}
  require(cursor instanceof MethodInsnNode h&&h.getOpcode()==Opcodes.INVOKESTATIC&&h.owner.equals(OWNER)&&h.name.endsWith(HANDLER)&&h.desc.equals("(Lnet/minecraft/network/chat/Component;)Lnet/minecraft/network/chat/Component;"),"Wrong material handler");injected.add(cursor);cursor=cursor.getPrevious();
  variable(cursor,Opcodes.ALOAD,2);injected.add(cursor);cursor=cursor.getPrevious();
  for(int slot=2;slot<=7;slot++){variable(cursor,Opcodes.ASTORE,slot);injected.add(cursor);cursor=cursor.getPrevious();}
  variable(cursor,Opcodes.ALOAD,1);require(injected.size()==13,"Wrong injection instruction count");
  for(var instruction:injected)copy.instructions.remove(instruction);
  return text(copy);
 }
 static Class<?> define(byte[] raw){return new ClassLoader(FluixHarness.class.getClassLoader()){Class<?> make(){return defineClass(TARGET,raw,0,raw.length);}}.make();}
 static void ensureFmlLoader()throws Exception{
  var type=Class.forName("net.neoforged.fml.loading.FMLLoader");var f=type.getDeclaredField("current");f.setAccessible(true);Object ref=f.get(null);var get=ref.getClass().getMethod("get");if(get.invoke(ref)!=null)return;
  var uf=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");uf.setAccessible(true);var unsafe=(sun.misc.Unsafe)uf.get(null);Object fixture=unsafe.allocateInstance(type);
  var production=type.getDeclaredField("production");unsafe.putBoolean(fixture,unsafe.objectFieldOffset(production),true);
  var list=type.getDeclaredField("loadingModList");list.setAccessible(true);list.set(fixture,net.neoforged.fml.loading.LoadingModList.of(List.of(),List.of(),List.of(),List.of(),List.of(),Map.of()));ref.getClass().getMethod("set",Object.class).invoke(ref,fixture);
 }
 static final class Values extends Language{
  final Map<String,String> values;Values(Map<String,String> values){this.values=values;}
  @Override public String getOrDefault(String key,String fallback){return values.getOrDefault(key,fallback);}
  @Override public boolean has(String key){return values.containsKey(key);}
  @Override public boolean isDefaultRightToLeft(){return false;}
  @Override public FormattedCharSequence getVisualOrder(FormattedText t){return FormattedCharSequence.EMPTY;}
 }
 static Map<String,String> parse(InputStream in)throws Exception{try(in){var v=new LinkedHashMap<String,String>();Language.loadFromJson(in,v::put);return v;}}
 static Map<String,String> language(Path jar,String member)throws Exception{try(var z=new ZipFile(jar.toFile())){return parse(z.getInputStream(z.getEntry(member)));}}
 static SmithingTemplateItem register(Class<?> type,String id)throws Exception{
  var name=Identifier.parse(id);var props=new Item.Properties().setId(ResourceKey.create(Registries.ITEM,name)).overrideDescription(TITLE);
  var item=(SmithingTemplateItem)type.getConstructor(Item.Properties.class).newInstance(props);Registry.register(BuiltInRegistries.ITEM,name,item);return item;
 }
 static List<Component> tooltip(SmithingTemplateItem item){var stack=new ItemStack(item);var rows=new ArrayList<Component>();rows.add(stack.getHoverName());item.appendHoverText(stack,Item.TooltipContext.EMPTY,TooltipDisplay.DEFAULT,rows::add,TooltipFlag.NORMAL);return rows;}
 static List<String> strings(List<Component> rows){return rows.stream().map(Component::getString).toList();}
 public static void main(String[] args)throws Exception{
  Path out=Path.of(args[0]);Files.createDirectories(out);String side=args[1],mode=args[2];
  MixinBootstrap.init();var physical=MixinEnvironment.Side.valueOf(side);MixinEnvironment.getDefaultEnvironment().setSide(physical);MixinEnvironment.getCurrentEnvironment().setSide(physical);
  var configs=List.of("atm11_japanese_helper.mixins.json","atm11_japanese_helper.mining.mixins.json","atm11_japanese_helper.measurements.mixins.json","atm11_japanese_helper.ae2.fluix.mixins.json","atm11_japanese_helper.ae2.charger.mixins.json","atm11_japanese_helper.neoforge.mixins.json");
  for(var config:configs)Mixins.addConfiguration(config);
  var transformer=((OfflineMixinService)MixinService.getService()).transformer();
  if(mode.equals("ae2-absent")){
   var writer=new ClassWriter(0);writer.visit(Opcodes.V25,Opcodes.ACC_PUBLIC,"atm11/nativefixture/Sentinel",null,"java/lang/Object",null);writer.visitEnd();byte[] sentinel=writer.toByteArray();
   byte[] untouched=transformer.transformClassBytes("atm11.nativefixture.Sentinel","atm11.nativefixture.Sentinel",sentinel);
   require(Arrays.equals(sentinel,untouched),"Absent AE2 changed unrelated class");
   var guard=new dev.atm11.japanesehelper.ExactFluixGuard();guard.onLoad("dev.atm11.japanesehelper.mixin");require(!guard.shouldApplyMixin(TARGET,"FluixTemplateMixin"),"Absent AE2 guard enabled");
   Files.writeString(out.resolve("result.json"),new GsonBuilder().setPrettyPrinting().create().toJson(Map.of("pass",true,"ae2_absent",true,"unrelated_class_unchanged",true,"configs_registered",configs,"other_mod_targets_transformed",false,"game_started",false,"visual_qa",0))+"\n");System.out.println("PASS absent AE2: feature disabled, unrelated class unchanged");return;
  }
  byte[] original;try(var in=FluixHarness.class.getClassLoader().getResourceAsStream(OWNER+".class")){original=Objects.requireNonNull(in).readAllBytes();}
  if(mode.equals("changed-call")||mode.equals("changed-key")){
   var changed=node(original);for(var m:changed.methods)if(m.name.equals("<init>"))for(var in:m.instructions){
    if(mode.equals("changed-key")&&in instanceof LdcInsnNode l&&"item".equals(l.cst))l.cst="block";
    if(mode.equals("changed-call")&&in instanceof MethodInsnNode c&&c.name.equals("<init>")&&c.owner.equals("net/minecraft/world/item/SmithingTemplateItem"))c.desc=c.desc.replace("Lnet/minecraft/world/item/Item$Properties;","Ljava/lang/Object;");
   }
   var w=new ClassWriter(0);changed.accept(w);original=w.toByteArray();
  }
  byte[] transformed=transformer.transformClassBytes(TARGET,TARGET,original);
  if(mode.equals("guard-disabled")){require(Arrays.equals(original,transformed),"Unsupported target was changed");Files.writeString(out.resolve("result.json"),"{\"pass\":true,\"unsupported_target_unchanged\":true}\n");System.out.println("PASS guard disabled: unchanged target");return;}
  require(!mode.startsWith("changed-"),"Changed callsite unexpectedly accepted");require(!Arrays.equals(original,transformed),"No transform applied");
  var before=node(original);var after=node(transformed);require(before.fields.size()==after.fields.size(),"Fields changed");int modified=0;
  for(var m:before.methods){var actual=after.methods.stream().filter(x->x.name.equals(m.name)&&x.desc.equals(m.desc)).findFirst().orElseThrow();require(m.access==actual.access,"Method access changed");if(m.name.equals("<init>")){require(text(m).equals(normalize(actual)),"Original instructions outside injection changed");modified++;}else require(text(m).equals(text(actual)),"Unrelated method changed");}
  require(modified==1&&after.methods.size()==before.methods.size()+1,"Unexpected injection shape");new ClassReader(transformed).accept(new CheckClassAdapter(new ClassWriter(0),true),0);Files.write(out.resolve("FluixSmithingTemplateItem.class"),transformed);
  ensureFmlLoader();net.minecraft.SharedConstants.tryDetectVersion();net.minecraft.server.Bootstrap.bootStrap();var registry=(MappedRegistry<Item>)BuiltInRegistries.ITEM;registry.unfreeze(true);
  var fixed=register(define(transformed),"ae2:fluix_upgrade_smithing_template");var baseline=register(define(original),"atm11_native_fixture:original_fluix_template");registry.freeze();
  var lookup=net.minecraft.data.registries.VanillaRegistries.createLookup();for(var p:BuiltInRegistries.DATA_COMPONENT_INITIALIZERS.build(lookup))p.apply();
  var en=new LinkedHashMap<>(language(Path.of(args[3]),"assets/minecraft/lang/en_us.json"));en.putAll(language(Path.of(args[4]),"assets/ae2/lang/en_us.json"));
  var ja=new LinkedHashMap<>(en);ja.putAll(parse(Files.newInputStream(Path.of(args[5]))));ja.putAll(language(Path.of(args[4]),"assets/ae2/lang/ja_jp.json"));
  if(args.length>6)ja.putAll(language(Path.of(args[6]),"assets/ae2/lang/ja_jp.json"));
  var old=Language.getInstance();var observations=new ArrayList<Map<String,Object>>();
  try{
   Language.inject(new Values(en));var origRows=tooltip(baseline);var fixedRows=tooltip(fixed);require(origRows.size()==7&&fixedRows.size()==7,"Tooltip row count changed");
   for(var locale:List.of("en_us","ja_jp","en_us_restored")){
    var values=locale.equals("ja_jp")?ja:en;Language.inject(new Values(values));var orig=strings(origRows);var changed=strings(fixedRows);
    require(orig.subList(0,6).equals(changed.subList(0,6)),"Nonmaterial tooltip rows changed");require(changed.getFirst().equals(values.get(TITLE)),"Title changed");
    require(orig.getLast().equals(" "+values.get(TITLE)),"Baseline bug not reproduced");require(changed.getLast().equals(" "+values.get(MATERIAL)),"Incorrect repaired ingredient");
    require(fixed.getBaseSlotDescription().equals(baseline.getBaseSlotDescription())&&fixed.getAdditionSlotDescription().equals(baseline.getAdditionSlotDescription()),"Slot descriptions changed");
    require(fixed.getBaseSlotEmptyIcons().equals(baseline.getBaseSlotEmptyIcons())&&fixed.getAdditionalSlotEmptyIcons().equals(baseline.getAdditionalSlotEmptyIcons()),"Empty slot icons changed");
    var ingredient=fixedRows.getLast().getSiblings().getFirst();require(ingredient.getStyle().getColor().getValue()==ChatFormatting.BLUE.getColor(),"Material is not vanilla description blue");
    observations.add(Map.of("locale",locale,"before",orig,"after",changed,"same_component_locale_cycle",true,"material_color_rgb",ChatFormatting.BLUE.getColor()));
   }
  }finally{Language.inject(old);}
  var report=new LinkedHashMap<String,Object>();report.put("pass",true);report.put("physical_side",side);report.put("observations",observations);report.put("configs_registered",configs);report.put("other_mod_targets_transformed",false);report.put("changed_original_methods",List.of("<init>(Item.Properties)"));report.put("only_constructor_argument_index",1);report.put("all_other_original_instructions_preserved",true);report.put("game_started",false);report.put("visual_qa",0);report.put("registry_fixture","Actual AE2 classes; fixed item real id, baseline alias with same description key; isolated vanilla registries/component initializers, minimal FML production/empty modlist fixture; other helper targets are not exercised by this Fluix report");
  Files.writeString(out.resolve("result.json"),new GsonBuilder().setPrettyPrinting().create().toJson(report)+"\n");System.out.println("PASS "+side+": actual constructor argument repair and before/after native tooltip, EN/JA/EN, other instructions/icons/descriptions preserved; visual0");
 }
}
