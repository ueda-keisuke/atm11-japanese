package dev.atm11.japanesehelper;

import java.io.InputStream;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.AbstractInsnNode;
import org.objectweb.asm.tree.ClassNode;
import org.objectweb.asm.tree.JumpInsnNode;
import org.objectweb.asm.tree.LdcInsnNode;
import org.objectweb.asm.tree.MethodInsnNode;
import org.objectweb.asm.tree.VarInsnNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;
import org.spongepowered.asm.mixin.transformer.throwables.InvalidMixinException;
import org.spongepowered.asm.service.MixinService;

/** This repair is independent of the optional client-screen features. */
public final class ExactGenerationGuard implements IMixinConfigPlugin {
    private static final String TARGET = "net.neoforged.neoforge.server.command.generation.GenerationBar";
    private static final String KEY = "commands.neoforge.chunkgen.progress_bar_errors";
    private static final String OWNER = "net/neoforged/neoforge/server/command/CommandUtils";
    private static final Map<String,String> SOURCES = Map.of(
            TARGET, "acfccf38fafaa0a7c760269d27c0f652e18ae301f417e10c1fda2539a42a7e2d",
            "net.neoforged.neoforge.server.command.CommandUtils", "26b11c3499f28f2f6fbc094ed2be5e82404746954e2bf119664268994e63f450");
    private boolean supported;
    @Override public void onLoad(String mixinPackage) {
        supported = false;
        try {
            for (var row : SOURCES.entrySet()) {
                try (InputStream in = MixinService.getService().getResourceAsStream(row.getKey().replace('.', '/') + ".class")) {
                    if (in == null) throw new IllegalStateException("missing class " + row.getKey());
                    String hash = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(in.readAllBytes()));
                    if (!row.getValue().equals(hash)) throw new IllegalStateException("class hash mismatch " + row.getKey());
                }
            }
            supported = true;
            MixinService.getService().getLogger("atm11_japanese_helper").info(
                    "ATM11_JAPANESE_HELPER_GENERATION_SOURCE_OK: fixed NeoForge 26.1.2.106 classes match; eligible for transformation.");
        } catch (Exception problem) {
            MixinService.getService().getLogger("atm11_japanese_helper").error(
                    "UNSUPPORTED NeoForge generation consumer: error-count repair disabled. " + problem.getMessage());
        }
    }
    @Override public boolean shouldApplyMixin(String target, String mixin) {
        if (!TARGET.equals(target)) throw new IllegalStateException("Unexpected generation target: " + target);
        return supported;
    }
    @Override public String getRefMapperConfig() { return null; }
    @Override public void acceptTargets(Set<String> own, Set<String> others) {}
    @Override public List<String> getMixins() { return null; }
    private static void require(boolean condition) {
        if (!condition) throw new IllegalStateException("Generation error consumer shape changed before transformation");
    }
    @Override public void preApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        try {
            var methods = node.methods.stream().filter(m -> m.name.equals("update") && m.desc.equals("(IIII)V")).toList();
            require(methods.size() == 1 && (methods.getFirst().access & Opcodes.ACC_STATIC) == 0);
            List<AbstractInsnNode> code = new ArrayList<>();
            for (var instruction : methods.getFirst().instructions) if (instruction.getOpcode() >= 0) code.add(instruction);
            int index = -1, keys = 0;
            for (int i = 0; i < code.size(); i++) if (code.get(i) instanceof LdcInsnNode ldc && KEY.equals(ldc.cst)) {index=i;keys++;}
            require(keys == 1 && index >= 3 && index + 1 < code.size());
            require(code.get(index - 3) instanceof VarInsnNode load && load.getOpcode() == Opcodes.ILOAD && load.var == 2);
            require(code.get(index - 2) instanceof JumpInsnNode jump && jump.getOpcode() == Opcodes.IFLE);
            require(code.get(index - 1) instanceof VarInsnNode title && title.getOpcode() == Opcodes.ALOAD);
            require(code.get(index + 1) instanceof MethodInsnNode call && call.getOpcode() == Opcodes.INVOKESTATIC && !call.itf
                    && call.owner.equals(OWNER) && call.name.equals("makeTranslatableWithFallback")
                    && call.desc.equals("(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;"));
        } catch (IllegalStateException changed) {
            throw new InvalidMixinException(info, changed.getMessage(), changed);
        }
    }
    @Override public void postApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        MixinService.getService().getLogger("atm11_japanese_helper").info(
                "ATM11_JAPANESE_HELPER_GENERATION_APPLIED target=" + target + "; argument repair transformed; no live-world or visual claim.");
    }
}
