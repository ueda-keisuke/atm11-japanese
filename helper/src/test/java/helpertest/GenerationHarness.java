package helpertest;

import com.google.gson.GsonBuilder;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.zip.ZipFile;
import net.minecraft.ChatFormatting;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.BossEvent;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.CheckClassAdapter;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceMethodVisitor;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.mixin.Mixins;
import org.spongepowered.asm.service.MixinService;

/** Actual Mixin transformation plus native server consumer; no client, world or connection. */
public final class GenerationHarness {
    private static final String TARGET="net.neoforged.neoforge.server.command.generation.GenerationBar";
    private static final String OWNER=TARGET.replace('.','/');
    private static final String KEY="commands.neoforge.chunkgen.progress_bar_errors";
    private static final String HANDLER="atm11helper$errorCount";
    private static void require(boolean value,String message){if(!value)throw new AssertionError(message);}
    private static ClassNode node(byte[] raw){var n=new ClassNode();new ClassReader(raw).accept(n,ClassReader.SKIP_DEBUG|ClassReader.SKIP_FRAMES);return n;}
    private static String text(MethodNode m){var t=new Textifier();m.accept(new TraceMethodVisitor(t));var s=new StringWriter();t.print(new PrintWriter(s));return s.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n","");}
    private static String normalize(MethodNode source){
        var m=new MethodNode(source.access,source.name,source.desc,source.signature,source.exceptions.toArray(String[]::new));source.accept(m);
        for(var in:m.instructions.toArray())if(in instanceof MethodInsnNode call&&call.owner.equals(OWNER)&&call.name.endsWith(HANDLER)){
            var previous=call.getPrevious();
            for(int index=4;index>=1;index--){require(previous instanceof VarInsnNode v&&v.getOpcode()==Opcodes.ILOAD&&v.var==index,"Captured method argument order changed");var remove=previous;previous=remove.getPrevious();m.instructions.remove(remove);}
            require(previous instanceof VarInsnNode v&&v.getOpcode()==Opcodes.ALOAD,"Missing preserved key load");int slot=((VarInsnNode)previous).var;var store=previous.getPrevious();
            require(store instanceof VarInsnNode v&&v.getOpcode()==Opcodes.ASTORE&&v.var==slot,"Missing preserved key store");m.instructions.remove(previous);m.instructions.remove(store);
            call.owner="net/neoforged/neoforge/server/command/CommandUtils";call.name="makeTranslatableWithFallback";call.desc="(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;";
        }
        return text(m);
    }
    private static final class Values extends Language {
        private final Map<String,String> values;Values(Map<String,String> values){this.values=values;}
        @Override public String getOrDefault(String key,String fallback){return values.getOrDefault(key,fallback);}
        @Override public boolean has(String key){return values.containsKey(key);}
        @Override public boolean isDefaultRightToLeft(){return false;}
        @Override public FormattedCharSequence getVisualOrder(FormattedText text){return FormattedCharSequence.EMPTY;}
    }
    private static Class<?> define(byte[] raw){return new ClassLoader(GenerationHarness.class.getClassLoader()){
        Class<?> target(){return defineClass(TARGET,raw,0,raw.length);}
    }.target();}
    private static List<Map<String,Object>> calls(Class<?> type,Map<String,String> values,String locale,boolean repaired)throws Exception{
        Language.inject(new Values(values));
        var field=sun.misc.Unsafe.class.getDeclaredField("theUnsafe");field.setAccessible(true);var unsafe=(sun.misc.Unsafe)field.get(null);
        Object instance=unsafe.allocateInstance(type);var bar=new ServerBossEvent(new UUID(0,1),Component.literal("fixture"),BossEvent.BossBarColor.YELLOW,BossEvent.BossBarOverlay.PROGRESS);
        var member=type.getDeclaredField("bar");member.setAccessible(true);member.set(instance,bar);
        var update=type.getMethod("update",int.class,int.class,int.class,int.class);var rows=new ArrayList<Map<String,Object>>();
        for(int errors:new int[]{0,1,11}){
            update.invoke(instance,5,errors,3,25);String rendered=bar.getName().getString();float expected=(5+errors+3)/25F;
            require(Math.abs(bar.getProgress()-expected)<0.00001,"Progress calculation changed");
            var components=bar.getName().getSiblings();long suffixes=components.stream().filter(c->c.getContents() instanceof TranslatableContents t&&t.getKey().equals(KEY)).count();
            require(suffixes==(errors>0?1:0),"Error branch changed");
            require(components.getFirst().getStyle().getColor().getValue()==ChatFormatting.GOLD.getColor(),"Progress color changed");
            if(errors>0){
                var suffix=components.getLast();var contents=(TranslatableContents)suffix.getContents();
                require(suffix.getStyle().getColor().getValue()==ChatFormatting.RED.getColor(),"Error color changed");
                require(contents.getArgs().length==(repaired?1:0),"Unexpected argument count");
                if(repaired){require(contents.getArgs()[0].equals(errors),"Wrong error count captured");require(!rendered.contains("%1$s"),"Unexpanded error placeholder");}
                else require(rendered.contains("%1$s"),"Original missing-argument bug no longer reproduced");
            }
            rows.add(Map.of("locale",locale,"ok",5,"errors",errors,"skipped",3,"total",25,"rendered",rendered,"progress",bar.getProgress(),"repaired",repaired));
        }
        return rows;
    }
    private static Map<String,String> readLanguage(Path archive,String member)throws Exception{
        var values=new LinkedHashMap<String,String>();try(var z=new ZipFile(archive.toFile());var in=z.getInputStream(z.getEntry(member))){Language.loadFromJson(in,values::put);}return values;
    }
    public static void main(String[] args)throws Exception{
        Path out=Path.of(args[0]);Files.createDirectories(out);String side=args[1];String mode=args.length>4?args[4]:"normal";
        MixinBootstrap.init();var physical=MixinEnvironment.Side.valueOf(side);MixinEnvironment.getDefaultEnvironment().setSide(physical);MixinEnvironment.getCurrentEnvironment().setSide(physical);
        if(mode.equals("all-configs"))for(String config:List.of("atm11_japanese_helper.mixins.json","atm11_japanese_helper.mining.mixins.json","atm11_japanese_helper.measurements.mixins.json","atm11_japanese_helper.ae2.fluix.mixins.json","atm11_japanese_helper.ae2.charger.mixins.json"))Mixins.addConfiguration(config);
        Mixins.addConfiguration("atm11_japanese_helper.neoforge.mixins.json");var transformer=((OfflineMixinService)MixinService.getService()).transformer();
        new dev.atm11.japanesehelper.JapaneseHelper();
        var sides=(net.neoforged.api.distmarker.Dist[])net.neoforged.fml.common.Mod.class.getMethod("dist").getDefaultValue();
        require(Set.of(sides).containsAll(List.of(net.neoforged.api.distmarker.Dist.CLIENT,net.neoforged.api.distmarker.Dist.DEDICATED_SERVER)),"Common entry point lacks both sides");
        byte[] original;try(var in=GenerationHarness.class.getClassLoader().getResourceAsStream(OWNER+".class")){original=Objects.requireNonNull(in).readAllBytes();}
        if(mode.equals("missing-site")){
            var damaged=node(original);for(var m:damaged.methods)if(m.name.equals("update"))for(var in:m.instructions)if(in instanceof LdcInsnNode ldc&&KEY.equals(ldc.cst))ldc.cst="fixture.changed.error_key";
            var w=new ClassWriter(0);damaged.accept(w);original=w.toByteArray();
        }
        byte[] transformed=transformer.transformClassBytes(TARGET,TARGET,original);
        if(mode.equals("guard-disabled")){
            require(Arrays.equals(original,transformed),"Unsupported consumer was changed");
            Files.writeString(out.resolve("result.json"),"{\"pass\":true,\"unsupported_source_skipped\":true}\n");
            System.out.println("PASS unsupported source: generation repair skipped");return;
        }
        require(!mode.equals("missing-site"),"Changed consumer was unexpectedly transformed");
        require(!Arrays.equals(original,transformed),"Repair not applied");
        var before=node(original);var after=node(transformed);require(before.fields.size()==after.fields.size(),"Field shape changed");int changed=0,handlers=0;
        for(var m:before.methods){var actual=after.methods.stream().filter(x->x.name.equals(m.name)&&x.desc.equals(m.desc)).findFirst().orElseThrow();require(m.access==actual.access,"Method access changed");if(m.name.equals("update")){require(normalize(actual).equals(text(m)),"Instructions outside redirect changed");changed++;}else require(text(m).equals(text(actual)),"Unrelated method changed: "+m.name);}
        for(var m:after.methods)if(m.name.endsWith(HANDLER))handlers++;
        require(changed==1&&handlers==1&&after.methods.size()==before.methods.size()+1,"Unexpected injection count");
        new ClassReader(transformed).accept(new CheckClassAdapter(new ClassWriter(0),true),0);Files.write(out.resolve("GenerationBar.class"),transformed);
        var en=readLanguage(Path.of(args[2]),"assets/neoforge/lang/en_us.json");var ja=new LinkedHashMap<>(en);ja.putAll(readLanguage(Path.of(args[3]),"assets/neoforge/lang/ja_jp.json"));
        var rows=new ArrayList<Map<String,Object>>();Language old=Language.getInstance();try{var fixed=define(transformed);var baseline=define(original);rows.addAll(calls(baseline,en,"en_us",false));rows.addAll(calls(baseline,ja,"ja_jp",false));rows.addAll(calls(fixed,en,"en_us",true));rows.addAll(calls(fixed,ja,"ja_jp",true));rows.addAll(calls(fixed,en,"en_us_restored",true));}finally{Language.inject(old);}
        Files.writeString(out.resolve("result.json"),new GsonBuilder().setPrettyPrinting().create().toJson(Map.of("pass",true,"physical_side",side,"actual_native_consumer_cases",rows,"game_started",false,"visual_qa",0,"changed_original_methods",List.of("update(IIII)V")))+"\n");
        System.out.println("PASS "+side+": real Mixin redirect, original bug, 15 native consumer/locale cases, argument/count/style/progress preserved; world/visual0.");
    }
}
