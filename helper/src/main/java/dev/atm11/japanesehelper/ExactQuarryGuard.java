package dev.atm11.japanesehelper;

import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.objectweb.asm.tree.ClassNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;
import org.spongepowered.asm.service.MixinService;

/** Reject changed/missing upstream classes before any of the three mixins is applied. */
public final class ExactQuarryGuard implements IMixinConfigPlugin {
    private boolean supported;
    private static final Map<String, String> HASHES = Map.of(
            "com.yogpc.qp.machine.marker.ChunkMarkerScreen", "c944d814c8cc12a82ff83050ece6516ad31f7bc0a9c07fc6c6144ed99eca45ce",
            "com.yogpc.qp.machine.module.ModuleScreen", "df10b5e8c8c9c368a43993b3587636288f1b25138bfaeb70f346884162669210",
            "com.yogpc.qp.machine.placer.PlacerScreen", "90a3b507f7c940d44f1e1d2e3ecd786462aab41eaaeff8edae17c7e095c86867");

    @Override
    public void onLoad(String mixinPackage) {
        supported = false;
        for (var entry : HASHES.entrySet()) {
            String resource = entry.getKey().replace('.', '/') + ".class";
            try (InputStream input = MixinService.getService().getResourceAsStream(resource)) {
                if (input == null) throw new IllegalStateException("missing class " + entry.getKey());
                String actual = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(input.readAllBytes()));
                if (!entry.getValue().equals(actual)) {
                    throw new IllegalStateException("class hash mismatch: " + entry.getKey() + " (" + actual + ")");
                }
            } catch (Exception cause) {
                MixinService.getService().getLogger("atm11_japanese_helper").error(
                        "UNSUPPORTED: ATM11 Japanese Helper supports only the pinned QuarryPlus 26.12.160 screen classes; "
                        + "no QuarryPlus helper mixins will be applied. " + cause.getMessage());
                return;
            }
        }
        supported = true;
        MixinService.getService().getLogger("atm11_japanese_helper").info(
                "ATM11_JAPANESE_HELPER_SOURCE_OK: all three original QuarryPlus 26.12.160 class hashes match; "
                + "eligible for transformation, not proof of application or visible GUI.");
    }

    @Override public boolean shouldApplyMixin(String target, String mixin) {
        if (!HASHES.containsKey(target)) throw new IllegalStateException("Unexpected helper target: " + target);
        return supported;
    }
    @Override public String getRefMapperConfig() { return null; }
    @Override public void acceptTargets(Set<String> own, Set<String> others) {}
    @Override public List<String> getMixins() { return null; }
    @Override public void preApply(String target, ClassNode node, String mixin, IMixinInfo info) {}
    @Override public void postApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        MixinService.getService().getLogger("atm11_japanese_helper").info(
                "ATM11_JAPANESE_HELPER_APPLIED target=" + target + " mixin=" + mixin
                + "; class transformation completed, visible GUI not verified.");
    }
}
