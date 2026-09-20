package dev.atm11.japanesehelper;

import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;

public final class Labels {
    private static final String PREFIX = "atm11_japanese_helper.quarryplus.";

    private Labels() {}

    /** Resolve on each render, so both displayed text and width use the current language. */
    public static String text(String suffix) {
        return Component.translatable(PREFIX + suffix).getString();
    }

    /** Preserve the two symbol-only controls and all original button indices/callbacks. */
    public static MutableComponent chunkButton(String original) {
        return switch (original) {
            case "Top+" -> Component.translatable(PREFIX + "chunk_marker.top_increase");
            case "Top-" -> Component.translatable(PREFIX + "chunk_marker.top_decrease");
            case "Bottom+" -> Component.translatable(PREFIX + "chunk_marker.bottom_increase");
            case "Bottom-" -> Component.translatable(PREFIX + "chunk_marker.bottom_decrease");
            case "+", "-" -> Component.literal(original);
            default -> throw new IllegalStateException("Unsupported QuarryPlus button: " + original);
        };
    }
}
