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
import org.objectweb.asm.tree.*;
import org.objectweb.asm.util.CheckClassAdapter;
import org.objectweb.asm.util.Textifier;
import org.objectweb.asm.util.TraceMethodVisitor;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.mixin.Mixins;
import org.spongepowered.asm.mixin.transformer.IMixinTransformer;
import org.spongepowered.asm.service.MixinService;

/** Real Mixin transformation; the target enum's original methods are all compared. */
public final class MeasurementsTransformHarness {
    private static final String PREFIX = "com.mrbysco.measurements.config.";
    private static final String API = "net/neoforged/neoforge/common/TranslatableEnum";
    private static final String DESC = "()Lnet/minecraft/network/chat/Component;";
    private static final Map<String, String> HASHES = Map.of(
            "LineColor", "4dd94a59b5d8f9771ba7663b6db9ba28dbb34f54b683e0ba6a1d5dc1df4411f4",
            "TextColor", "73323c37550ecb90efa4aba76d8c4015cb5b27c8c75a9c0a28fab74b3bc551d4");
    private static void require(boolean value, String message) { if (!value) throw new AssertionError(message); }
    private static String sha(byte[] raw) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(raw));
    }
    private static ClassNode node(byte[] raw) {
        var node = new ClassNode();
        new ClassReader(raw).accept(node, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
        return node;
    }
    private static String text(MethodNode method) {
        Textifier printer = new Textifier();
        method.accept(new TraceMethodVisitor(printer));
        StringWriter out = new StringWriter(); printer.print(new PrintWriter(out));
        return method.access + ":" + method.name + method.desc + ":" + method.signature + ":" + method.exceptions + ":"
                + out.toString().replaceAll("(?m)^.*MAX(?:STACK|LOCALS) = .*\\n", "");
    }
    private static List<String> fields(ClassNode node) {
        return node.fields.stream().map(f -> f.access + ":" + f.name + ":" + f.desc + ":" + f.signature + ":" + f.value).toList();
    }
    public static void main(String[] args) throws Exception {
        Path output = Path.of(args[0]);
        boolean collision = args.length > 1 && args[1].equals("method-collision");
        MixinBootstrap.init();
        require(MixinService.getService() instanceof OfflineMixinService, "Wrong Mixin service");
        MixinEnvironment.getDefaultEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        Mixins.addConfiguration("atm11_japanese_helper.measurements.mixins.json");
        IMixinTransformer transformer = ((OfflineMixinService) MixinService.getService()).transformer();
        List<Map<String, Object>> rows = new ArrayList<>();
        for (String simple : List.of("LineColor", "TextColor")) {
            String name = PREFIX + simple, member = name.replace('.', '/') + ".class";
            byte[] original;
            try (var in = MeasurementsTransformHarness.class.getClassLoader().getResourceAsStream(member)) {
                require(in != null, "Missing target: " + member); original = in.readAllBytes();
            }
            require(sha(original).equals(HASHES.get(simple)), "Original hash changed");
            ClassNode before = node(original);
            byte[] input = original;
            if (collision) {
                ClassNode fixture = node(original);
                MethodNode method = new MethodNode(Opcodes.ACC_PUBLIC, "getTranslatedName", DESC, null, null);
                method.instructions.add(new InsnNode(Opcodes.ACONST_NULL));
                method.instructions.add(new InsnNode(Opcodes.ARETURN));
                method.maxStack = 1; method.maxLocals = 1; fixture.methods.add(method);
                ClassWriter writer = new ClassWriter(0); fixture.accept(writer); input = writer.toByteArray();
            }
            byte[] transformed = transformer.transformClassBytes(name, name, input);
            require(!collision, "Expected enum method collision to be rejected");
            require(!Arrays.equals(original, transformed), "Target was not transformed: " + name);
            ClassNode after = node(transformed);
            require(before.access == after.access && before.name.equals(after.name) && before.superName.equals(after.superName), "Enum class identity changed");
            List<String> expectedInterfaces = new ArrayList<>(before.interfaces); expectedInterfaces.add(API);
            require(after.interfaces.equals(expectedInterfaces), "Unexpected interface change");
            require(fields(before).equals(fields(after)), "Enum fields/order changed");
            require(after.methods.size() == before.methods.size() + 1, "Unexpected method additions");
            for (MethodNode old : before.methods) {
                List<MethodNode> matches = after.methods.stream().filter(m -> m.name.equals(old.name) && m.desc.equals(old.desc)).toList();
                require(matches.size() == 1 && text(old).equals(text(matches.getFirst())), "Original method changed: " + old.name + old.desc);
            }
            List<MethodNode> additions = after.methods.stream().filter(m -> m.name.equals("getTranslatedName") && m.desc.equals(DESC)).toList();
            require(additions.size() == 1 && (additions.getFirst().access & Opcodes.ACC_PUBLIC) != 0, "Missing public interface implementation");
            StringWriter verification = new StringWriter();
            CheckClassAdapter.verify(new ClassReader(transformed), false, new PrintWriter(verification));
            require(verification.toString().isEmpty(), "ASM verification failed: " + verification);
            Path target = output.resolve(member); Files.createDirectories(target.getParent()); Files.write(target, transformed);
            rows.add(Map.of("class", name, "original_sha256", sha(original), "transformed_sha256", sha(transformed),
                    "original_method_count", before.methods.size(), "original_methods_unchanged", true,
                    "original_fields_and_enum_order_unchanged", true, "added_translatable_interface", true,
                    "added_methods", List.of("getTranslatedName" + DESC), "asm_verified", true));
        }
        Files.createDirectories(output);
        Files.writeString(output.resolve("measurements-transform-report.json"), new GsonBuilder().setPrettyPrinting().create().toJson(
                Map.of("status", "PASS", "targets", rows, "game_started", false, "full_screen_initialized", false, "visual_qa", false)) + "\n");
        System.out.println("PASS Measurements: two exact enums transformed; original methods/fields/order unchanged; interface plus one display method each; ASM verified.");
    }
}
