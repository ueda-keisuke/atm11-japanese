package helpertest;

import com.google.gson.GsonBuilder;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.TreeMap;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.tree.AbstractInsnNode;
import org.objectweb.asm.tree.ClassNode;
import org.objectweb.asm.tree.MethodInsnNode;
import org.objectweb.asm.tree.MethodNode;
import org.spongepowered.asm.launch.MixinBootstrap;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.mixin.Mixins;
import org.spongepowered.asm.mixin.transformer.IMixinTransformer;
import org.spongepowered.asm.service.MixinService;

/**
 * Headless isolation harness for the three optional helper Mixin features.
 *
 * Usage: MeasurementsGuardHarness <output-directory> <mode>
 *
 * Modes are all, measurements-absent, line-mismatch, text-mismatch,
 * consumer-mismatch, interface-mismatch, quarry-absent, quarry-mismatch,
 * mining-absent, mining-mismatch and all-absent.  The runner must physically omit the requested JAR for absent
 * modes and prepend the named mismatch fixture for mismatch modes.  This
 * harness never starts Minecraft or a GUI.
 */
public final class MeasurementsGuardHarness {
    private static final String QUARRY_CONFIG = "atm11_japanese_helper.mixins.json";
    private static final String MINING_CONFIG = "atm11_japanese_helper.mining.mixins.json";
    private static final String MEASUREMENTS_CONFIG = "atm11_japanese_helper.measurements.mixins.json";
    private static final String COMPONENT = "net.minecraft.network.chat.Component";

    private static final List<String> QUARRY_TARGETS = List.of(
            "com.yogpc.qp.machine.marker.ChunkMarkerScreen",
            "com.yogpc.qp.machine.module.ModuleScreen",
            "com.yogpc.qp.machine.placer.PlacerScreen");
    private static final String MINING_TARGET =
            "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen";
    private static final List<String> MEASUREMENTS_TARGETS = List.of(
            "com.mrbysco.measurements.config.LineColor",
            "com.mrbysco.measurements.config.TextColor");
    private static final String MEASUREMENTS_CONSUMER =
            "net.neoforged.neoforge.client.gui.ConfigurationScreen$ConfigurationSectionScreen";
    private static final String MEASUREMENTS_INTERFACE =
            "net.neoforged.neoforge.common.TranslatableEnum";

    private static final Map<String, String> MEASUREMENTS_HASHES = Map.of(
            "com.mrbysco.measurements.config.LineColor",
            "4dd94a59b5d8f9771ba7663b6db9ba28dbb34f54b683e0ba6a1d5dc1df4411f4",
            "com.mrbysco.measurements.config.TextColor",
            "73323c37550ecb90efa4aba76d8c4015cb5b27c8c75a9c0a28fab74b3bc551d4",
            MEASUREMENTS_CONSUMER,
            "5e7c94bf81f50a8395f2b9aefb3ddc2530d87cd914293b94f29da776a2a86aeb",
            MEASUREMENTS_INTERFACE,
            "5d087da717c28ce9eb50d1312b42fcd20aeb3d76a70dfbb28dcf9193e57a3b52");

    private static final List<String> MODES = List.of(
            "all", "measurements-absent", "line-mismatch", "text-mismatch",
            "consumer-mismatch", "interface-mismatch", "quarry-absent",
            "quarry-mismatch", "mining-absent", "mining-mismatch", "all-absent");

    private static void require(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }

    private static String sha256(byte[] bytes) throws Exception {
        return java.util.HexFormat.of().formatHex(
                MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static ClassNode node(byte[] bytes) {
        ClassNode node = new ClassNode();
        new ClassReader(bytes).accept(node, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
        return node;
    }

    private static byte[] classBytes(String binaryName) throws Exception {
        String resource = binaryName.replace('.', '/') + ".class";
        try (InputStream input = MeasurementsGuardHarness.class.getClassLoader()
                .getResourceAsStream(resource)) {
            return input == null ? null : input.readAllBytes();
        }
    }

    private static int miningRedirectCount(ClassNode classNode) {
        int count = 0;
        for (MethodNode method : classNode.methods) {
            for (AbstractInsnNode instruction : method.instructions) {
                if (instruction instanceof MethodInsnNode call
                        && call.owner.equals(classNode.name)
                        && call.name.endsWith("atm11helper$precision")) count++;
            }
        }
        return count;
    }

    private static int quarryRedirectCount(ClassNode classNode) {
        int count = 0;
        for (MethodNode method : classNode.methods) {
            for (AbstractInsnNode instruction : method.instructions) {
                if (instruction instanceof MethodInsnNode call
                        && call.owner.equals(classNode.name)
                        && call.name.contains("atm11helper$")) count++;
            }
        }
        return count;
    }

    private static int translatedNameCount(ClassNode classNode) {
        int count = 0;
        for (MethodNode method : classNode.methods) {
            if (method.name.equals("getTranslatedName")
                    && method.desc.equals("()Lnet/minecraft/network/chat/Component;")) count++;
        }
        return count;
    }

    private static boolean hasInterface(ClassNode classNode) {
        return classNode.interfaces.contains("net/neoforged/neoforge/common/TranslatableEnum");
    }

    private static boolean isFeatureAbsent(String mode, String feature) {
        return mode.equals("all-absent")
                || (feature.equals("measurements") && mode.equals("measurements-absent"))
                || (feature.equals("quarry") && mode.equals("quarry-absent"))
                || (feature.equals("mining") && mode.equals("mining-absent"));
    }

    private static boolean isMeasurementsMismatch(String mode) {
        return mode.equals("line-mismatch") || mode.equals("text-mismatch")
                || mode.equals("consumer-mismatch") || mode.equals("interface-mismatch");
    }

    private static boolean isFeatureMismatch(String mode, String feature) {
        return (feature.equals("quarry") && mode.equals("quarry-mismatch"))
                || (feature.equals("mining") && mode.equals("mining-mismatch"));
    }

    private static boolean measurementsExpectedActive(String mode) {
        return !isFeatureAbsent(mode, "measurements") && !isMeasurementsMismatch(mode);
    }

    private static String mismatchTarget(String mode) {
        return switch (mode) {
            case "line-mismatch" -> MEASUREMENTS_TARGETS.get(0);
            case "text-mismatch" -> MEASUREMENTS_TARGETS.get(1);
            case "consumer-mismatch" -> MEASUREMENTS_CONSUMER;
            case "interface-mismatch" -> MEASUREMENTS_INTERFACE;
            default -> null;
        };
    }

    private static Map<String, Object> dependencyRecord(String target, String mode) throws Exception {
        byte[] original = classBytes(target);
        Map<String, Object> record = new LinkedHashMap<>();
        record.put("target", target);
        record.put("expected_sha256", MEASUREMENTS_HASHES.get(target));
        record.put("resource_present", original != null);
        record.put("sha256", original == null ? null : sha256(original));
        record.put("expected_mismatch_fixture", target.equals(mismatchTarget(mode)));
        record.put("hash_matches", original != null && MEASUREMENTS_HASHES.get(target).equals(sha256(original)));
        return record;
    }

    private static Map<String, Object> transformOne(IMixinTransformer transformer, String target,
            String feature, String mode, int expectedCount, Path output) throws Exception {
        byte[] original = classBytes(target);
        boolean physicallyAbsent = original == null;
        boolean expectedAbsent = isFeatureAbsent(mode, feature);
        require(!expectedAbsent || physicallyAbsent,
                "Absent mode must omit the target JAR from the class path: " + target);
        require(expectedAbsent || !physicallyAbsent,
                "Unexpected target absence outside an absent mode: " + target);

        Map<String, Object> record = new LinkedHashMap<>();
        record.put("feature", feature);
        record.put("target", target);
        record.put("mode", mode);
        record.put("resource_present_to_harness", !physicallyAbsent);
        record.put("real_missing_jar_case", physicallyAbsent && expectedAbsent);

        if (physicallyAbsent) {
            record.put("transformed", false);
            record.put("result", "target resource absent; feature skipped");
            return record;
        }

        byte[] transformed = transformer.transformClassBytes(target, target, original);
        boolean changed = !Arrays.equals(original, transformed);
        boolean shouldTransform = feature.equals("measurements")
                ? measurementsExpectedActive(mode)
                : !isFeatureAbsent(mode, feature) && !isFeatureMismatch(mode, feature);
        require(changed == shouldTransform,
                "Feature isolation mismatch for " + feature + " in " + mode
                        + ": expected transformed=" + shouldTransform + " observed=" + changed);
        record.put("original_sha256", sha256(original));
        record.put("transformed_sha256", sha256(transformed));
        record.put("transformed", changed);

        if (feature.equals("measurements") && changed) {
            ClassNode transformedNode = node(transformed);
            require(hasInterface(transformedNode), "Measurements enum lacks TranslatableEnum: " + target);
            require(translatedNameCount(transformedNode) == 1,
                    "Measurements enum must expose exactly one getTranslatedName: " + target);
            record.put("translatable_enum_interface", true);
            record.put("get_translated_name_count", translatedNameCount(transformedNode));
        } else if (feature.equals("measurements")) {
            require(Arrays.equals(original, transformed),
                    "Unsupported Measurements mode changed enum bytes: " + target);
            record.put("unsupported_bytes_unchanged", true);
        }
        if (feature.equals("mining") && changed) {
            int count = miningRedirectCount(node(transformed));
            require(count == expectedCount, "Mining precision redirect count mismatch: " + count);
            record.put("precision_redirect_count", count);
        }
        if (feature.equals("quarry") && changed) {
            int count = quarryRedirectCount(node(transformed));
            require(count == expectedCount, "Quarry injection count mismatch for " + target + ": " + count);
            record.put("legacy_injection_count", count);
        }
        if (!changed) record.put("unsupported_bytes_unchanged", true);

        Path destination = output.resolve(feature).resolve(target.replace('.', '/') + ".class");
        Files.createDirectories(destination.getParent());
        Files.write(destination, transformed);
        record.put("transformed_class_snapshot", output.relativize(destination).toString());
        return record;
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Usage: MeasurementsGuardHarness <output-directory> <mode>");
        Path output = Path.of(args[0]);
        String mode = args[1];
        require(MODES.contains(mode), "Unknown mode: " + mode);

        MixinBootstrap.init();
        require(MixinService.getService() instanceof OfflineMixinService, "Wrong Mixin service");
        MixinEnvironment.getDefaultEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setOption(MixinEnvironment.Option.DEBUG_INJECTORS, true);
        // Register all optional feature configurations in every mode. Each
        // plugin must fail closed independently when its own target is absent
        // or its pinned class hash is mismatched.
        Mixins.addConfiguration(QUARRY_CONFIG);
        Mixins.addConfiguration(MINING_CONFIG);
        Mixins.addConfiguration(MEASUREMENTS_CONFIG);
        IMixinTransformer transformer = ((OfflineMixinService) MixinService.getService()).transformer();

        byte[] untouched = Objects.requireNonNull(classBytes(COMPONENT));
        require(Arrays.equals(untouched, transformer.transformClassBytes(COMPONENT, COMPONENT, untouched)),
                "Out-of-scope Component class changed");

        Files.createDirectories(output);
        List<Map<String, Object>> records = new ArrayList<>();
        records.add(transformOne(transformer, QUARRY_TARGETS.get(0), "quarry", mode, 8, output));
        records.add(transformOne(transformer, QUARRY_TARGETS.get(1), "quarry", mode, 1, output));
        records.add(transformOne(transformer, QUARRY_TARGETS.get(2), "quarry", mode, 3, output));
        records.add(transformOne(transformer, MINING_TARGET, "mining", mode, 2, output));
        records.add(transformOne(transformer, MEASUREMENTS_TARGETS.get(0), "measurements", mode, 1, output));
        records.add(transformOne(transformer, MEASUREMENTS_TARGETS.get(1), "measurements", mode, 1, output));

        List<Map<String, Object>> dependencies = new ArrayList<>();
        for (String target : MEASUREMENTS_TARGETS) dependencies.add(dependencyRecord(target, mode));
        dependencies.add(dependencyRecord(MEASUREMENTS_CONSUMER, mode));
        dependencies.add(dependencyRecord(MEASUREMENTS_INTERFACE, mode));

        boolean measurementsSupported = measurementsExpectedActive(mode);
        for (Map<String, Object> dependency : dependencies) {
            boolean mismatch = Boolean.TRUE.equals(dependency.get("expected_mismatch_fixture"));
            boolean present = Boolean.TRUE.equals(dependency.get("resource_present"));
            if (measurementsSupported) require(present && Boolean.TRUE.equals(dependency.get("hash_matches")),
                    "Measurements dependency must match in all mode: " + dependency.get("target"));
            if (mismatch) require(!Boolean.TRUE.equals(dependency.get("hash_matches")),
                    "Mismatch fixture unexpectedly matches: " + dependency.get("target"));
        }

        Map<String, Object> summary = new TreeMap<>();
        summary.put("schema_version", 1);
        summary.put("mode", mode);
        summary.put("mixin_service", transformer.getClass().getName());
        summary.put("measurements_supported_expected", measurementsSupported);
        summary.put("all_three_mixin_configs_registered", true);
        summary.put("records", records);
        summary.put("measurements_dependency_records", dependencies);
        summary.put("minecraft_started", false);
        summary.put("visual_qa", false);
        summary.put("physical_jar_omission_required_for_absent_modes", true);
        summary.put("full_client_mod_discovery_executed", false);
        Files.writeString(output.resolve("measurements-guard-report.json"),
                new GsonBuilder().setPrettyPrinting().create().toJson(summary) + "\n");
        System.out.println("PASS three-feature guard isolation: mode=" + mode
                + " Quarry, Mining Gadgets and Measurements outcomes recorded independently");
    }
}
