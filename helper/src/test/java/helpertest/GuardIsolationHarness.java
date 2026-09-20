package helpertest;

import com.google.gson.GsonBuilder;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HexFormat;
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
 * Headless regression test for the two feature-specific Mixin guards.
 *
 * Usage: GuardIsolationHarness <output-directory> <mode>
 *
 * Modes are both, mining-absent, mining-mismatch, quarry-absent,
 * quarry-mismatch, and both-absent.  The offline service may hide a target
 * from Mixin's resource view using the two properties below.  A genuinely
 * omitted target JAR is preferred for absent cases; when a fixture remains on
 * the harness class path, the report records that it was a service-hidden
 * absence rather than a real missing-JAR case.
 */
public final class GuardIsolationHarness {
    private static final String QUARRY_CONFIG = "atm11_japanese_helper.mixins.json";
    private static final String MINING_CONFIG = "atm11_japanese_helper.mining.mixins.json";
    private static final String HIDE_QUARRY = "atm11.helper.offline.hide.quarry";
    private static final String HIDE_MINING = "atm11.helper.offline.hide.mining";

    private static final List<String> QUARRY_TARGETS = List.of(
            "com.yogpc.qp.machine.marker.ChunkMarkerScreen",
            "com.yogpc.qp.machine.module.ModuleScreen",
            "com.yogpc.qp.machine.placer.PlacerScreen");
    private static final String MINING_TARGET =
            "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen";
    private static final String MINING_HANDLER = "atm11helper$precision";

    private static void require(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }

    private static String sha256(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static ClassNode node(byte[] bytes) {
        ClassNode node = new ClassNode();
        new ClassReader(bytes).accept(node, ClassReader.SKIP_DEBUG | ClassReader.SKIP_FRAMES);
        return node;
    }

    private static byte[] classBytes(String binaryName) throws Exception {
        String resource = binaryName.replace('.', '/') + ".class";
        try (InputStream input = GuardIsolationHarness.class.getClassLoader().getResourceAsStream(resource)) {
            return input == null ? null : input.readAllBytes();
        }
    }

    private static boolean validMode(String mode, String feature) {
        return switch (mode) {
            case "both" -> true;
            case "mining-absent", "mining-mismatch" -> feature.equals("quarry");
            case "quarry-absent", "quarry-mismatch" -> feature.equals("mining");
            case "both-absent" -> false;
            default -> throw new IllegalArgumentException("Unknown mode: " + mode);
        };
    }

    private static boolean absentMode(String mode, String feature) {
        return (feature.equals("mining") && (mode.equals("mining-absent") || mode.equals("both-absent")))
                || (feature.equals("quarry") && (mode.equals("quarry-absent") || mode.equals("both-absent")));
    }

    private static boolean mismatchMode(String mode, String feature) {
        return (feature.equals("mining") && mode.equals("mining-mismatch"))
                || (feature.equals("quarry") && mode.equals("quarry-mismatch"));
    }

    private static int miningRedirectCount(ClassNode classNode) {
        int count = 0;
        for (MethodNode method : classNode.methods) {
            for (AbstractInsnNode instruction : method.instructions) {
                if (instruction instanceof MethodInsnNode call && call.owner.equals(classNode.name) && call.name.endsWith(MINING_HANDLER)) count++;
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

    private static Map<String, Object> transformOne(IMixinTransformer transformer, String target,
            String feature, String mode, Path output) throws Exception {
        byte[] original = classBytes(target);
        boolean resourcePresent = original != null;
        boolean absent = absentMode(mode, feature);
        require(!absent || !resourcePresent, "Absent cases must physically omit the original MOD JAR: " + target);
        boolean mismatch = mismatchMode(mode, feature);
        Map<String, Object> record = new LinkedHashMap<>();
        record.put("feature", feature);
        record.put("target", target);
        record.put("mode", mode);
        record.put("resource_present_to_harness", resourcePresent);

        record.put("fixture_expected_mismatch", mismatch);
        record.put("real_missing_jar_case", !resourcePresent && absent);

        if (!resourcePresent) {
            require(absent, "Target absent outside an absent-feature mode: " + target);
            record.put("transformed", false);
            record.put("result", "target resource absent; feature skipped");
            return record;
        }

        byte[] transformed = transformer.transformClassBytes(target, target, original);
        boolean changed = !Arrays.equals(original, transformed);
        record.put("original_sha256", sha256(original));
        record.put("transformed_sha256", sha256(transformed));
        record.put("transformed", changed);

        boolean shouldTransform = validMode(mode, feature);
        require(changed == shouldTransform,
                "Guard isolation mismatch for " + feature + " in " + mode
                        + ": expected transformed=" + shouldTransform + " observed=" + changed);

        if (feature.equals("mining") && changed) {
            int count = miningRedirectCount(node(transformed));
            require(count == 2, "Mining must redirect exactly two precision consumers, got " + count);
            record.put("precision_redirect_count", count);
        }
        if (feature.equals("quarry") && changed) {
            int count = quarryRedirectCount(node(transformed));
            int expected = target.endsWith("ChunkMarkerScreen") ? 8 : target.endsWith("ModuleScreen") ? 1 : 3;
            require(count == expected, "Quarry injection count mismatch for " + target + ": " + count);
            record.put("legacy_injection_count", count);
        }
        if (!changed) {
            require(Arrays.equals(original, transformed), "Unsupported feature changed target bytes: " + target);
            record.put("unsupported_bytes_unchanged", true);
        }
        Path relative = Path.of(target.replace('.', '/') + ".class");
        Path destination = output.resolve(feature).resolve(relative);
        Files.createDirectories(destination.getParent());
        Files.write(destination, transformed);
        record.put("transformed_class_snapshot", output.relativize(destination).toString());
        return record;
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Usage: GuardIsolationHarness <output-directory> <mode>");
        Path output = Path.of(args[0]);
        String mode = args[1];
        List.of("both", "mining-absent", "mining-mismatch", "quarry-absent", "quarry-mismatch", "both-absent")
                .stream().filter(mode::equals).findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Unknown mode: " + mode));

        // OfflineMixinService filters only Mixin's resource view.  The direct
        // harness class loader is intentionally used above to distinguish a
        // real absent JAR from a service-hidden fixture.


        MixinBootstrap.init();
        require(MixinService.getService() instanceof OfflineMixinService, "Wrong Mixin service");
        MixinEnvironment.getDefaultEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setSide(MixinEnvironment.Side.CLIENT);
        MixinEnvironment.getCurrentEnvironment().setOption(MixinEnvironment.Option.DEBUG_INJECTORS, true);
        Mixins.addConfiguration(QUARRY_CONFIG);
        Mixins.addConfiguration(MINING_CONFIG);
        IMixinTransformer transformer = ((OfflineMixinService) MixinService.getService()).transformer();

        // Force configuration preparation even when both optional JARs are absent.
        String unrelated = "net.minecraft.network.chat.Component";
        byte[] untouched = Objects.requireNonNull(classBytes(unrelated));
        require(Arrays.equals(untouched, transformer.transformClassBytes(unrelated, unrelated, untouched)),
                "Out-of-scope Component class changed");

        Files.createDirectories(output);
        List<Map<String, Object>> records = new ArrayList<>();
        for (String target : QUARRY_TARGETS) records.add(transformOne(transformer, target, "quarry", mode, output));
        records.add(transformOne(transformer, MINING_TARGET, "mining", mode, output));

        Map<String, Object> summary = new TreeMap<>();
        summary.put("schema_version", 1);
        summary.put("mode", mode);
        summary.put("mixin_service", transformer.getClass().getName());
        summary.put("records", records);
        summary.put("minecraft_started", false);
        summary.put("visual_qa", false);
        summary.put("absent_jars_physically_omitted", true);
        summary.put("full_client_mod_discovery_executed", false);
        Files.writeString(output.resolve("guard-isolation-report.json"),
                new GsonBuilder().setPrettyPrinting().create().toJson(summary) + "\n");
        System.out.println("PASS guard isolation: mode=" + mode + " Quarry and Mining feature outcomes are independent");
    }
}
