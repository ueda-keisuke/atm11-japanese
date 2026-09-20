package dev.atm11.japanesehelper;

import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.ClassNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;
import org.spongepowered.asm.mixin.transformer.throwables.InvalidMixinException;
import org.spongepowered.asm.service.MixinService;

/** Adds display names only to the two supported Measurements enums. */
public final class ExactMeasurementsGuard implements IMixinConfigPlugin {
    private static final String PREFIX = "com.mrbysco.measurements.config.";
    private static final String INTERFACE = "net/neoforged/neoforge/common/TranslatableEnum";
    private static final Map<String, String> HASHES = Map.of(
            PREFIX + "LineColor", "4dd94a59b5d8f9771ba7663b6db9ba28dbb34f54b683e0ba6a1d5dc1df4411f4",
            PREFIX + "TextColor", "73323c37550ecb90efa4aba76d8c4015cb5b27c8c75a9c0a28fab74b3bc551d4",
            "net.neoforged.neoforge.common.TranslatableEnum", "5d087da717c28ce9eb50d1312b42fcd20aeb3d76a70dfbb28dcf9193e57a3b52",
            "net.neoforged.neoforge.client.gui.ConfigurationScreen$ConfigurationSectionScreen", "5e7c94bf81f50a8395f2b9aefb3ddc2530d87cd914293b94f29da776a2a86aeb");
    private static final Map<String, String> MIXINS = Map.of(
            PREFIX + "LineColor", "dev.atm11.japanesehelper.mixin.MeasurementsLineColorMixin",
            PREFIX + "TextColor", "dev.atm11.japanesehelper.mixin.MeasurementsTextColorMixin");
    private static final Set<String> LINE_VALUES = Set.of("RANDOM", "WHITE", "ORANGE", "MAGENTA", "LIGHT_BLUE",
            "YELLOW", "LIME", "PINK", "GRAY", "LIGHT_GRAY", "CYAN", "PURPLE", "BLUE", "BROWN", "GREEN", "RED", "BLACK");
    private boolean supported;

    @Override public void onLoad(String mixinPackage) {
        supported = false;
        try {
            for (var row : HASHES.entrySet()) {
                try (InputStream input = MixinService.getService().getResourceAsStream(row.getKey().replace('.', '/') + ".class")) {
                    if (input == null) throw new IllegalStateException("missing class " + row.getKey());
                    String actual = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(input.readAllBytes()));
                    if (!row.getValue().equals(actual)) throw new IllegalStateException("class hash mismatch: " + row.getKey());
                }
            }
            supported = true;
            MixinService.getService().getLogger("atm11_japanese_helper").info(
                    "ATM11_JAPANESE_HELPER_MEASUREMENTS_SOURCE_OK: Measurements 4.0.0 enums and NeoForge consumer/interface hashes match; eligible for transformation, visible GUI not verified.");
        } catch (Exception cause) {
            MixinService.getService().getLogger("atm11_japanese_helper").error(
                    "UNSUPPORTED Measurements: no Measurements helper mixin will be applied. " + cause.getMessage());
        }
    }
    @Override public boolean shouldApplyMixin(String target, String mixin) {
        if (!mixin.equals(MIXINS.get(target))) throw new IllegalStateException("Unexpected Measurements helper target/mixin: " + target + " / " + mixin);
        return supported;
    }
    @Override public String getRefMapperConfig() { return null; }
    @Override public void acceptTargets(Set<String> own, Set<String> others) {}
    @Override public List<String> getMixins() { return null; }
    @Override public void preApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        Set<String> expected = new java.util.HashSet<>(LINE_VALUES);
        if (target.equals(PREFIX + "TextColor")) expected.add("XYZRGB");
        Set<String> actual = node.fields.stream().filter(f -> (f.access & Opcodes.ACC_ENUM) != 0)
                .map(f -> f.name).collect(Collectors.toSet());
        if ((node.access & Opcodes.ACC_ENUM) == 0 || !"java/lang/Enum".equals(node.superName)
                || !actual.equals(expected) || node.interfaces.contains(INTERFACE)
                || node.methods.stream().anyMatch(m -> m.name.equals("getTranslatedName"))) {
            throw new InvalidMixinException(info, "Measurements enum shape or display method changed before transformation: " + target);
        }
    }
    @Override public void postApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        MixinService.getService().getLogger("atm11_japanese_helper").info(
                "ATM11_JAPANESE_HELPER_MEASUREMENTS_APPLIED target=" + target + " mixin=" + mixin
                + "; class transformation completed, visible GUI not verified.");
    }
}
