package helpertest;

import com.google.gson.GsonBuilder;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.Type;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.CheckClassAdapter;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceMethodVisitor;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.mixin.Mixins;
import org.spongepowered.asm.mixin.transformer.IMixinTransformer;
import org.spongepowered.asm.service.MixinService;

/**
 * Offline structural test for the Mining Gadgets precision-mode redirects.
 *
 * CLI: MiningTransformHarness <output-dir> [mixin-config] [missing-site]
 * The target Mining Gadgets class must be on the test class path.  No game is
 * started.  The second argument is intentionally explicit so the Mining
 * configuration cannot be accidentally tested through the Quarry config.
 */
public final class MiningTransformHarness {
    private static final String TARGET = "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen";
    private static final String TARGET_RESOURCE = TARGET.replace('.', '/') + ".class";
    private static final String KEY = "tooltip.screen.precision_mode";
    private static final String ORIGINAL_OWNER = TARGET.replace('.', '/');
    private static final String ORIGINAL_NAME = "getTrans";
    private static final String HELPER_SUFFIX = "atm11helper$precision";
    private static final String HANDLER_DESC = "(Ljava/lang/String;[Ljava/lang/Object;)Lnet/minecraft/network/chat/MutableComponent;";

    private static void require(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }

    private static String hash(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static ClassNode node(byte[] raw) {
        ClassNode node = new ClassNode();
        new ClassReader(raw).accept(node, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
        return node;
    }

    private static String methodText(MethodNode method) {
        Textifier printer = new Textifier();
        method.accept(new TraceMethodVisitor(printer));
        StringWriter text = new StringWriter();
        printer.print(new PrintWriter(text));
        return text.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n", "");
    }

    private static MethodNode find(ClassNode node, MethodNode wanted) {
        return node.methods.stream().filter(m -> m.name.equals(wanted.name) && m.desc.equals(wanted.desc))
                .findFirst().orElseThrow(() -> new AssertionError("Missing method " + wanted.name + wanted.desc));
    }

    private static boolean isPrecisionHandler(MethodInsnNode call) {
        return call.name.endsWith(HELPER_SUFFIX) && call.owner.equals(ORIGINAL_OWNER)
                && call.desc.equals(HANDLER_DESC) && call.getOpcode() == Opcodes.INVOKESTATIC;
    }

    /** Normalize only the redirected call; all other instructions and operands remain compared. */
    private static String normalized(MethodNode source) {
        MethodNode copy = new MethodNode(source.access, source.name, source.desc, source.signature,
                source.exceptions == null ? null : source.exceptions.toArray(String[]::new));
        source.accept(copy);
        for (AbstractInsnNode instruction : copy.instructions) {
            if (!(instruction instanceof MethodInsnNode call) || !isPrecisionHandler(call)) continue;
            AbstractInsnNode loadArgs = call.getPrevious();
            AbstractInsnNode loadKey = loadArgs == null ? null : loadArgs.getPrevious();
            AbstractInsnNode storeKey = loadKey == null ? null : loadKey.getPrevious();
            AbstractInsnNode storeArgs = storeKey == null ? null : storeKey.getPrevious();
            require(loadArgs instanceof VarInsnNode a && a.getOpcode() == Opcodes.ALOAD
                    && loadKey instanceof VarInsnNode k && k.getOpcode() == Opcodes.ALOAD
                    && storeKey instanceof VarInsnNode sk && sk.getOpcode() == Opcodes.ASTORE
                    && storeArgs instanceof VarInsnNode sa && sa.getOpcode() == Opcodes.ASTORE
                    && a.var == sa.var && k.var == sk.var,
                    "Unexpected redirect argument preservation scaffolding");
            copy.instructions.remove(loadArgs);
            copy.instructions.remove(loadKey);
            copy.instructions.remove(storeKey);
            copy.instructions.remove(storeArgs);
            call.setOpcode(Opcodes.INVOKESTATIC);
            call.owner = ORIGINAL_OWNER;
            call.name = ORIGINAL_NAME;
            call.desc = HANDLER_DESC;
            call.itf = false;
        }
        return methodText(copy);
    }

    private static Map<String, Integer> handlerCounts(ClassNode node) {
        Map<String, Integer> counts = new TreeMap<>();
        for (MethodNode method : node.methods) {
            for (AbstractInsnNode instruction : method.instructions) {
                if (instruction instanceof MethodInsnNode call && isPrecisionHandler(call)) {
                    counts.merge(method.name + method.desc, 1, Integer::sum);
                }
            }
        }
        return counts;
    }

    public static void main(String[] args) throws Exception {
        require(args.length >= 1, "Usage: MiningTransformHarness <output-dir> [mixin-config]");
        String config = args.length >= 2 ? args[1] : "atm11_japanese_helper.mining.mixins.json";
        MixinBootstrap.init();
        require(MixinService.getService() instanceof OfflineMixinService, "Wrong Mixin service");
        MixinEnvironment.getDefaultEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setOption(MixinEnvironment.Option.DEBUG_INJECTORS, true);
        Mixins.addConfiguration(config);
        IMixinTransformer transformer = ((OfflineMixinService) MixinService.getService()).transformer();

        byte[] original;
        try (var input = MiningTransformHarness.class.getClassLoader().getResourceAsStream(TARGET_RESOURCE)) {
            original = Objects.requireNonNull(input, "Mining Gadgets target class is absent from classpath").readAllBytes();
        }
        require(hash(original).equals("3b431f9b858bc95984dcdb48550f158ce503c1df5896d2e014a297ef8a571b53"), "Unexpected original Mining target hash");
        boolean missingSite = args.length >= 3 && args[2].equals("missing-site");
        if (missingSite) {
            ClassNode damaged = node(original);
            MethodNode init = damaged.methods.stream().filter(m -> m.name.equals("init") && m.desc.equals("()V"))
                    .findFirst().orElseThrow();
            boolean changed = false;
            for (AbstractInsnNode instruction : init.instructions) {
                if (instruction instanceof LdcInsnNode ldc && KEY.equals(ldc.cst)) {
                    ldc.cst = "fixture.changed.precision_key";
                    changed = true;
                    break;
                }
            }
            require(changed, "Missing-site fixture could not find precision constant");
            ClassWriter writer = new ClassWriter(0);
            damaged.accept(writer);
            original = writer.toByteArray();
        }
        byte[] transformed = transformer.transformClassBytes(TARGET, TARGET, original);
        if (missingSite) {
            throw new AssertionError("Missing-site fixture was unexpectedly accepted; expected injector failure");
        }
        require(!Arrays.equals(original, transformed), "Mining target was not transformed");

        ClassNode before = node(original), after = node(transformed);
        require(before.fields.size() == after.fields.size(), "Unexpected field addition/removal");
        Map<String, Integer> counts = handlerCounts(after);
        Map<String, Integer> expectedCounts = new TreeMap<>();
        expectedCounts.put("init()V", 1);
        expectedCounts.put("lambda$init$6(Lnet/minecraft/client/gui/components/Button;)V", 1);
        require(counts.equals(expectedCounts), "Expected exactly two precision redirects, got " + counts);

        List<String> changed = new ArrayList<>();
        for (MethodNode method : before.methods) {
            MethodNode actual = find(after, method);
            require(method.access == actual.access, "Original method access changed: " + method.name);
            if (method.name.equals("init") || method.name.equals("lambda$init$6")) {
                require(!methodText(method).equals(methodText(actual)), "Expected redirect in " + method.name);
                require(normalized(actual).equals(methodText(method)),
                        "Redirect changed non-call instructions in " + method.name);
                changed.add(method.name + method.desc);
            } else {
                require(methodText(method).equals(methodText(actual)),
                        "Out-of-scope method changed: " + method.name + method.desc);
            }
        }
        List<MethodNode> generated = after.methods.stream().filter(m -> m.name.endsWith(HELPER_SUFFIX)
                && m.desc.equals(HANDLER_DESC)).toList();
        require(generated.size() == 1, "Expected one generated precision handler, got " + generated.size());
        for (MethodNode method : after.methods) {
            boolean wasOriginal = before.methods.stream().anyMatch(m -> m.name.equals(method.name) && m.desc.equals(method.desc));
            require(wasOriginal || generated.contains(method), "Unexpected generated method: " + method.name + method.desc);
        }
        new ClassReader(transformed).accept(new CheckClassAdapter(new ClassWriter(0), true), 0);

        Path output = Path.of(args[0]);
        Files.createDirectories(output);
        Path classFile = output.resolve(TARGET_RESOURCE);
        Files.createDirectories(classFile.getParent());
        Files.write(classFile, transformed);
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("target", TARGET);
        report.put("original_sha256", hash(original));
        report.put("transformed_sha256", hash(transformed));
        report.put("mixin_config", config);
        report.put("redirect_counts", counts);
        report.put("changed_methods", changed);
        report.put("out_of_scope_methods_unchanged", true);
        report.put("asm_check", "PASS");
        report.put("minecraft_started", false);
        report.put("visual_qa", false);
        report.put("whole_gui_init_executed", false);
        report.put("whole_gui_click_executed", false);
        Files.writeString(output.resolve("mining-transform-report.json"),
                new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        System.out.println("PASS Mining Gadgets transform: exactly init and lambda$init$6 redirected; all other original methods unchanged");
    }
}
