package dev.atm11.japanesehelper.mixin;

import net.minecraft.network.chat.MutableComponent;
import net.neoforged.neoforge.server.command.CommandUtils;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;
import org.spongepowered.asm.mixin.injection.Slice;

/** Restore the omitted argument; the existing language key selects the text. */
@Mixin(targets = "net.neoforged.neoforge.server.command.generation.GenerationBar", remap = false)
public abstract class GenerationBarMixin {
    @Redirect(method = "update(IIII)V",
            slice = @Slice(from = @At(value = "CONSTANT", args = "stringValue=commands.neoforge.chunkgen.progress_bar_errors")),
            at = @At(value = "INVOKE", target = "Lnet/neoforged/neoforge/server/command/CommandUtils;makeTranslatableWithFallback(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;", ordinal = 0),
            require = 1, expect = 1, allow = 1)
    private static MutableComponent atm11helper$errorCount(String key, int ok, int error, int skipped, int total) {
        return CommandUtils.makeTranslatableWithFallback(key, error);
    }
}
