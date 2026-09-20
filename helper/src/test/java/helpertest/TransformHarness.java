package helpertest;

import com.google.gson.GsonBuilder;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;
import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.CheckClassAdapter;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceMethodVisitor;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.mixin.Mixins;
import org.spongepowered.asm.mixin.transformer.IMixinTransformer;
import org.spongepowered.asm.service.MixinService;

public final class TransformHarness {
    private static final Map<String, Set<String>> TARGETS = Map.of(
            "com.yogpc.qp.machine.marker.ChunkMarkerScreen", Set.of("extractLabels", "init"),
            "com.yogpc.qp.machine.module.ModuleScreen", Set.of("extractLabels"),
            "com.yogpc.qp.machine.placer.PlacerScreen", Set.of("renderModeLabel"));
    private static final Map<String, Integer> EXPECTED = Map.of(
            "size", 2, "button", 6, "modules", 1, "pulse", 1, "breakOnly", 1, "placeOnly", 1);

    private static void require(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }
    private static String hash(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }
    private static ClassNode node(byte[] raw) {
        ClassNode node = new ClassNode();
        new ClassReader(raw).accept(node, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
        return node;
    }
    private static String method(MethodNode method) {
        Textifier printer = new Textifier();
        method.accept(new TraceMethodVisitor(printer));
        StringWriter text = new StringWriter();
        printer.print(new PrintWriter(text));
        // Max stack changes are not behavior changes; actual instructions, branches and operands remain compared.
        return text.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n", "");
    }
    private static MethodNode find(ClassNode node, MethodNode original) {
        return node.methods.stream().filter(m -> m.name.equals(original.name) && m.desc.equals(original.desc)).findFirst().orElseThrow();
    }

    /** Reverse only the known injector scaffolding, then compare every original instruction. */
    private static void undoLabelInjections(MethodNode method, String owner) {
        for (AbstractInsnNode instruction : method.instructions.toArray()) {
            if (!(instruction instanceof MethodInsnNode call) || !call.owner.equals(owner)
                    || !call.name.contains("atm11helper$")) continue;
            if (call.name.endsWith("atm11helper$button")) {
                AbstractInsnNode loadArg = call.getPrevious();
                AbstractInsnNode loadThis = loadArg.getPrevious();
                AbstractInsnNode storeArg = loadThis.getPrevious();
                require(loadArg instanceof VarInsnNode a && a.getOpcode() == Opcodes.ALOAD
                        && storeArg instanceof VarInsnNode b && b.getOpcode() == Opcodes.ASTORE && a.var == b.var,
                        "Unexpected redirect argument preservation");
                require(loadThis instanceof VarInsnNode v && v.getOpcode() == Opcodes.ALOAD && v.var == 0,
                        "Unexpected redirect receiver");
                method.instructions.remove(loadArg);
                method.instructions.remove(loadThis);
                method.instructions.remove(storeArg);
                method.instructions.set(call, new MethodInsnNode(Opcodes.INVOKESTATIC,
                        "net/minecraft/network/chat/Component", "literal",
                        "(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;", true));
            } else {
                require(call.getPrevious() instanceof LdcInsnNode, "Unexpected constant injector");
                AbstractInsnNode loadThis = call.getPrevious().getPrevious();
                require(loadThis instanceof VarInsnNode v && v.getOpcode() == Opcodes.ALOAD && v.var == 0,
                        "Unexpected constant receiver");
                method.instructions.remove(loadThis);
                method.instructions.remove(call);
            }
        }
    }

    public static void main(String[] args) throws Exception {
        MixinBootstrap.init();
        require(MixinService.getService() instanceof OfflineMixinService, "Wrong Mixin service");
        MixinEnvironment.getDefaultEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setOption(MixinEnvironment.Option.DEBUG_INJECTORS, true);
        Mixins.addConfiguration("atm11_japanese_helper.mixins.json");
        IMixinTransformer transformer = ((OfflineMixinService) MixinService.getService()).transformer();
        Path output = Path.of(args[0]);
        Files.createDirectories(output);
        Map<String, Integer> counts = new TreeMap<>();
        List<Map<String, Object>> records = new ArrayList<>();
        for (String target : new TreeSet<>(TARGETS.keySet())) {
            String resource = target.replace('.', '/') + ".class";
            byte[] original;
            try (var input = TransformHarness.class.getClassLoader().getResourceAsStream(resource)) {
                original = Objects.requireNonNull(input).readAllBytes();
            }
            if (args.length > 1 && args[1].equals("missing-site") && target.endsWith("ChunkMarkerScreen")) {
                ClassNode damaged = node(original);
                outer: for (MethodNode m : damaged.methods) {
                    for (AbstractInsnNode i : m.instructions) {
                        if (i instanceof LdcInsnNode ldc && "Size".equals(ldc.cst)) {
                            ldc.cst = "fixture changed constant";
                            break outer;
                        }
                    }
                }
                ClassWriter writer = new ClassWriter(0);
                damaged.accept(writer);
                original = writer.toByteArray();
            }
            byte[] transformed = transformer.transformClassBytes(target, target, original);
            if (args.length > 1 && args[1].equals("unsupported")) {
                require(Arrays.equals(original, transformed), "Unsupported source must disable ALL helper mixins: " + target);
                continue;
            }
            require(!Arrays.equals(original, transformed), "No real Mixin transformation: " + target);
            ClassNode before = node(original), after = node(transformed);
            require(before.fields.size() == after.fields.size(), "Unexpected field addition");
            List<String> unchanged = new ArrayList<>();
            for (MethodNode m : before.methods) {
                MethodNode actual = find(after, m);
                require(m.access == actual.access, "Method access changed: " + m.name);
                if (!TARGETS.get(target).contains(m.name)) {
                    require(method(m).equals(method(actual)), "Original non-label method changed: " + target + ":" + m.name);
                    unchanged.add(m.name + m.desc);
                } else {
                    require(!method(m).equals(method(actual)), "Expected label method unchanged: " + m.name);
                    for (AbstractInsnNode instruction : actual.instructions) {
                        if (instruction instanceof MethodInsnNode call && call.owner.equals(after.name)
                                && call.name.contains("atm11helper$")) {
                            for (String name : EXPECTED.keySet()) {
                                if (call.name.endsWith("atm11helper$" + name)) counts.merge(name, 1, Integer::sum);
                            }
                        }
                    }
                    undoLabelInjections(actual, after.name);
                    require(method(m).equals(method(actual)), "Non-label instructions changed in " + target + ":" + m.name);
                }
            }
            // ASM validates classfile structure/instruction well-formedness without loading a game class.
            new ClassReader(transformed).accept(new CheckClassAdapter(new ClassWriter(0), true), 0);
            Path file = output.resolve(resource);
            Files.createDirectories(file.getParent());
            Files.write(file, transformed);
            records.add(Map.of("target", target, "original_sha256", hash(original),
                    "transformed_sha256", hash(transformed), "unchanged_methods", unchanged,
                    "label_methods_other_instructions_identical", true));
        }
        if (args.length > 1 && args[1].equals("unsupported")) {
            System.out.println("PASS unsupported source: all three target classes remain byte-for-byte unchanged");
            return;
        }
        require(counts.equals(EXPECTED), "Injection count mismatch: " + counts);
        // Out-of-scope player/chat class must remain byte-for-byte untouched by this mixin configuration.
        String other = "com.yogpc.qp.machine.misc.GeneratorBlock";
        try (var input = TransformHarness.class.getClassLoader().getResourceAsStream(other.replace('.', '/') + ".class")) {
            byte[] bytes = Objects.requireNonNull(input).readAllBytes();
            require(Arrays.equals(bytes, transformer.transformClassBytes(other, other, bytes)), "Out-of-scope class changed");
        }
        Map<String, Object> report = Map.of("actual_mixin_transformer", transformer.getClass().getName(),
                "target_classes", records, "injection_counts", counts, "generator_unchanged", true,
                "minecraft_started", false, "visual_qa", false);
        Files.writeString(output.resolve("transform-report.json"), new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        System.out.println("PASS real Mixin transform: three exact QuarryPlus screen classes, twelve injection sites; original non-label methods unchanged");
    }
}
