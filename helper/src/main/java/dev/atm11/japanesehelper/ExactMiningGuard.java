package dev.atm11.japanesehelper;

import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;
import java.util.Set;
import java.util.ArrayList;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.tree.AbstractInsnNode;
import org.objectweb.asm.tree.ClassNode;
import org.objectweb.asm.tree.FieldInsnNode;
import org.objectweb.asm.tree.LdcInsnNode;
import org.objectweb.asm.tree.MethodInsnNode;
import org.objectweb.asm.tree.MethodNode;
import org.objectweb.asm.tree.TypeInsnNode;
import org.objectweb.asm.tree.VarInsnNode;
import org.spongepowered.asm.mixin.extensibility.IMixinConfigPlugin;
import org.spongepowered.asm.mixin.extensibility.IMixinInfo;
import org.spongepowered.asm.mixin.transformer.throwables.InvalidMixinException;
import org.spongepowered.asm.service.MixinService;

/** A missing or changed Mining Gadgets class disables only this feature. */
public final class ExactMiningGuard implements IMixinConfigPlugin {
    private static final String TARGET = "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen";
    private static final String SHA256 = "3b431f9b858bc95984dcdb48550f158ce503c1df5896d2e014a297ef8a571b53";
    private boolean supported;

    @Override public void onLoad(String mixinPackage) {
        supported = false;
        try (InputStream input = MixinService.getService().getResourceAsStream(TARGET.replace('.', '/') + ".class")) {
            if (input == null) throw new IllegalStateException("missing class " + TARGET);
            String actual = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(input.readAllBytes()));
            if (!SHA256.equals(actual)) throw new IllegalStateException("class hash mismatch: " + TARGET + " (" + actual + ")");
            supported = true;
            MixinService.getService().getLogger("atm11_japanese_helper").info(
                    "ATM11_JAPANESE_HELPER_MINING_SOURCE_OK: original Mining Gadgets 1.19.3 screen hash matches; eligible for transformation, not proof of application or visible GUI.");
        } catch (Exception cause) {
            MixinService.getService().getLogger("atm11_japanese_helper").error(
                    "UNSUPPORTED Mining Gadgets: no Mining Gadgets helper mixin will be applied. " + cause.getMessage());
        }
    }
    @Override public boolean shouldApplyMixin(String target, String mixin) {
        if (!TARGET.equals(target)) throw new IllegalStateException("Unexpected Mining Gadgets helper target: " + target);
        return supported;
    }
    @Override public String getRefMapperConfig() { return null; }
    @Override public void acceptTargets(Set<String> own, Set<String> others) {}
    @Override public List<String> getMixins() { return null; }
    private static void requireShape(boolean matches, String method) {
        if (!matches) throw new IllegalStateException("Mining precision consumer shape changed before transformation: " + method);
    }
    private static void checkConsumer(ClassNode node, String name, String descriptor) {
        List<MethodNode> methods = node.methods.stream().filter(m -> m.name.equals(name) && m.desc.equals(descriptor)).toList();
        requireShape(methods.size() == 1, name);
        List<AbstractInsnNode> instructions = new ArrayList<>();
        for (AbstractInsnNode instruction : methods.get(0).instructions) {
            if (instruction.getOpcode() >= 0) instructions.add(instruction);
        }
        int start = -1, literals = 0;
        for (int i = 0; i < instructions.size(); i++) {
            if (instructions.get(i) instanceof LdcInsnNode value && "tooltip.screen.precision_mode".equals(value.cst)) {
                start = i + 1;
                literals++;
            }
        }
        requireShape(literals == 1 && start + 9 <= instructions.size(), name);
        int[] opcodes = {Opcodes.ICONST_1, Opcodes.ANEWARRAY, Opcodes.DUP, Opcodes.ICONST_0,
                Opcodes.ALOAD, Opcodes.GETFIELD, Opcodes.INVOKESTATIC, Opcodes.AASTORE, Opcodes.INVOKESTATIC};
        for (int i = 0; i < opcodes.length; i++) requireShape(instructions.get(start + i).getOpcode() == opcodes[i], name);
        requireShape(instructions.get(start + 1) instanceof TypeInsnNode type && type.desc.equals("java/lang/Object"), name);
        requireShape(instructions.get(start + 4) instanceof VarInsnNode receiver && receiver.var == 0, name);
        requireShape(instructions.get(start + 5) instanceof FieldInsnNode field && field.owner.equals(node.name)
                && field.name.equals("isPrecision") && field.desc.equals("Z"), name);
        requireShape(instructions.get(start + 6) instanceof MethodInsnNode box && box.owner.equals("java/lang/Boolean")
                && box.name.equals("valueOf") && box.desc.equals("(Z)Ljava/lang/Boolean;") && !box.itf, name);
        requireShape(instructions.get(start + 8) instanceof MethodInsnNode call && call.owner.equals(node.name)
                && call.name.equals("getTrans") && call.desc.equals("(Ljava/lang/String;[Ljava/lang/Object;)Lnet/minecraft/network/chat/MutableComponent;") && !call.itf, name);
    }
    @Override public void preApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        // A missing Slice anchor otherwise defaults to the method start. Reject
        // earlier-transformer interference instead of redirecting another label.
        try {
            checkConsumer(node, "init", "()V");
            checkConsumer(node, "lambda$init$6", "(Lnet/minecraft/client/gui/components/Button;)V");
        } catch (IllegalStateException changed) {
            throw new InvalidMixinException(info, changed.getMessage(), changed);
        }
    }
    @Override public void postApply(String target, ClassNode node, String mixin, IMixinInfo info) {
        MixinService.getService().getLogger("atm11_japanese_helper").info(
                "ATM11_JAPANESE_HELPER_MINING_APPLIED target=" + target + " mixin=" + mixin
                + "; class transformation completed, visible GUI not verified.");
    }
}
