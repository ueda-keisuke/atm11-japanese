package helpertest;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import dev.atm11.japanesehelper.Labels;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.util.FormattedCharSequence;

public final class LanguageHarness {
    private static final String PREFIX = "atm11_japanese_helper.quarryplus.";
    private static final Map<String, String> BUTTONS = Map.of("Top+", "chunk_marker.top_increase",
            "Top-", "chunk_marker.top_decrease", "Bottom+", "chunk_marker.bottom_increase", "Bottom-", "chunk_marker.bottom_decrease");
    private static Map<String, String> values(String locale) throws Exception {
        try (var input = LanguageHarness.class.getClassLoader().getResourceAsStream(
                "assets/atm11_japanese_helper/lang/" + locale + ".json")) {
            return new Gson().fromJson(new InputStreamReader(Objects.requireNonNull(input), StandardCharsets.UTF_8),
                    new TypeToken<Map<String, String>>() {}.getType());
        }
    }
    private static void require(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    private static final class TestLanguage extends Language {
        private final Map<String, String> values;
        TestLanguage(Map<String, String> values) { this.values = values; }
        @Override public String getOrDefault(String key, String fallback) { return values.getOrDefault(key, fallback); }
        @Override public boolean has(String key) { return values.containsKey(key); }
        @Override public boolean isDefaultRightToLeft() { return false; }
        @Override public FormattedCharSequence getVisualOrder(FormattedText text) { return FormattedCharSequence.EMPTY; }
    }
    public static void main(String[] args) throws Exception {
        Map<String, MutableComponent> components = new LinkedHashMap<>();
        for (var pair : BUTTONS.entrySet()) {
            MutableComponent component = Labels.chunkButton(pair.getKey());
            require(component.getContents() instanceof TranslatableContents translatable
                    && translatable.getKey().equals(PREFIX + pair.getValue()), "Button must retain a translatable component");
            components.put(pair.getValue(), component);
        }
        Language original = Language.getInstance();
        try {
            for (String locale : new String[]{"en_us", "ja_jp", "en_us"}) {
                Map<String, String> expected = values(locale);
                Language.inject(new TestLanguage(expected));
                require(expected.keySet().stream().filter(k -> k.startsWith(PREFIX)).count() == 9, "Expected nine preserved Quarry labels");
                for (String key : expected.keySet()) {
                    if (!key.startsWith(PREFIX)) continue;
                    String suffix = key.substring(PREFIX.length());
                    String actual = components.containsKey(suffix) ? components.get(suffix).getString() : Labels.text(suffix);
                    require(expected.get(key).equals(actual), "Current-language resolution failed: " + locale + ":" + key);
                }
                require(Labels.chunkButton("+").getString().equals("+") && Labels.chunkButton("-").getString().equals("-"), "Symbol changed");
            }
        } finally { Language.inject(original); }
        System.out.println("PASS real Component/Language: all nine EN -> accepted JA -> EN values; retained button components update; +/- unchanged");
    }
}
