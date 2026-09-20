package helpertest;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.util.FormattedCharSequence;

/**
 * Executes the actual transformed static precision handler without starting Minecraft.
 *
 * CLI: MiningLanguageHarness <transformed-class-file> <candidate-json>
 * The transformed class is defined in an isolated loader.  The handler contract
 * is private static (String,Object[]) -> MutableComponent, named atm11helper$precision.
 */
public final class MiningLanguageHarness {
    private static final String HANDLER_SUFFIX = "atm11helper$precision";
    private static final String HANDLER_DESC = "(Ljava/lang/String;[Ljava/lang/Object;)Lnet/minecraft/network/chat/MutableComponent;";
    private static final String SOURCE_KEY = "tooltip.screen.precision_mode";
    private static final String MOD_KEY = "mininggadgets." + SOURCE_KEY;
    private static final String ENABLED = "atm11_japanese_helper.mininggadgets.precision_mode.enabled";
    private static final String DISABLED = "atm11_japanese_helper.mininggadgets.precision_mode.disabled";
    private static final Set<String> BUILT_KEYS = Set.of(
            "atm11_japanese_helper.quarryplus.chunk_marker.size",
            "atm11_japanese_helper.quarryplus.chunk_marker.top_increase",
            "atm11_japanese_helper.quarryplus.chunk_marker.top_decrease",
            "atm11_japanese_helper.quarryplus.chunk_marker.bottom_increase",
            "atm11_japanese_helper.quarryplus.chunk_marker.bottom_decrease",
            "atm11_japanese_helper.quarryplus.module.modules",
            "atm11_japanese_helper.quarryplus.placer.pulse",
            "atm11_japanese_helper.quarryplus.placer.break_only",
            "atm11_japanese_helper.quarryplus.placer.place_only",
            ENABLED, DISABLED);

    private static void require(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }

    private static String hash(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static final class TestLanguage extends Language {
        private final Map<String, String> values;
        TestLanguage(Map<String, String> values) { this.values = values; }
        @Override public String getOrDefault(String key, String fallback) { return values.getOrDefault(key, fallback); }
        @Override public boolean has(String key) { return values.containsKey(key); }
        @Override public boolean isDefaultRightToLeft() { return false; }
        @Override public FormattedCharSequence getVisualOrder(FormattedText text) { return FormattedCharSequence.EMPTY; }
    }

    private static final class TargetLoader extends ClassLoader {
        private final String targetName;
        private final byte[] targetBytes;
        TargetLoader(String targetName, byte[] targetBytes) {
            super(MiningLanguageHarness.class.getClassLoader());
            this.targetName = targetName;
            this.targetBytes = targetBytes;
        }
        @Override public Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
            if (name.equals(targetName)) {
                Class<?> already = findLoadedClass(name);
                Class<?> value = already == null ? findClass(name) : already;
                if (resolve) resolveClass(value);
                return value;
            }
            return super.loadClass(name, resolve);
        }
        @Override protected Class<?> findClass(String name) throws ClassNotFoundException {
            if (name.equals(targetName)) return defineClass(name, targetBytes, 0, targetBytes.length);
            return super.findClass(name);
        }
    }

    private static Map<String, String> candidate(Path path) throws Exception {
        Map<String, Object> raw = new Gson().fromJson(Files.newBufferedReader(path, StandardCharsets.UTF_8),
                new TypeToken<Map<String, Object>>() {}.getType());
        @SuppressWarnings("unchecked") Map<String, String> values = (Map<String, String>) raw.get("entries");
        @SuppressWarnings("unchecked") Map<String, String> fallback = (Map<String, String>) raw.get("english_fallback");
        require(values != null && fallback != null && values.size() == 2 && fallback.size() == 2,
                "Candidate must contain exactly two Japanese and English entries");
        require(values.containsKey(ENABLED) && values.containsKey(DISABLED), "Missing precision language keys");
        require("Precision Mode: Enabled".equals(fallback.get(ENABLED))
                && "Precision Mode: Disabled".equals(fallback.get(DISABLED)), "English fallback mismatch");
        return values;
    }

    private static Map<String, String> builtAsset(String locale) throws Exception {
        try (var input = MiningLanguageHarness.class.getClassLoader().getResourceAsStream(
                "assets/atm11_japanese_helper/lang/" + locale + ".json")) {
            require(input != null, "Missing built helper language asset: " + locale);
            Map<String, String> values = new LinkedHashMap<>();
            Language.loadFromJson(input, values::put);
            require(values.size() == BUILT_KEYS.size() && values.keySet().equals(BUILT_KEYS),
                    "Built helper asset key set is not the frozen 11-key set: " + locale);
            return values;
        }
    }

    private static Method handler(Path classFile) throws Exception {
        String targetName = "com.direwolf20.mininggadgets.client.screens.MiningSettingScreen";
        Class<?> target = new TargetLoader(targetName, Files.readAllBytes(classFile)).loadClass(targetName);
        Method found = null;
        for (Method method : target.getDeclaredMethods()) {
            if (method.getName().endsWith(HANDLER_SUFFIX) && method.toGenericString().contains("java.lang.Object[]")) {
                require(found == null, "Duplicate precision handler");
                found = method;
            }
        }
        require(found != null, "Transformed target has no precision handler");
        require(java.lang.reflect.Modifier.isStatic(found.getModifiers()), "Precision handler must be static");
        require(found.getName().endsWith(HANDLER_SUFFIX) && found.getParameterCount() == 2 && found.getParameterTypes()[0] == String.class
                && found.getParameterTypes()[1] == Object[].class,
                "Precision handler contract must be (String,Object[])");
        require("net.minecraft.network.chat.MutableComponent".equals(found.getReturnType().getName()),
                "Precision handler return type changed");
        found.setAccessible(true);
        return found;
    }

    private static MutableComponent invoke(Method method, String key, Object[] args) throws Exception {
        return (MutableComponent) method.invoke(null, key, args);
    }

    private static void componentKey(MutableComponent component, String expected) {
        require(component.getContents() instanceof TranslatableContents contents
                && contents.getKey().equals(expected), "Unexpected fallback component key: " + component.getContents());
    }

    private static void originalFallback(Method handler, String key, Object[] arguments) throws Exception {
        Method original = handler.getDeclaringClass().getDeclaredMethod("getTrans", String.class, Object[].class);
        original.setAccessible(true);
        Object expected = null, actual = null;
        Throwable expectedError = null, actualError = null;
        try { expected = original.invoke(null, key, arguments); }
        catch (java.lang.reflect.InvocationTargetException e) { expectedError = e.getCause(); }
        try { actual = handler.invoke(null, key, arguments); }
        catch (java.lang.reflect.InvocationTargetException e) { actualError = e.getCause(); }
        if (expectedError != null || actualError != null) {
            require(expectedError != null && actualError != null
                    && expectedError.getClass().equals(actualError.getClass())
                    && Objects.equals(expectedError.getMessage(), actualError.getMessage()),
                    "Fallback exception behavior differs from original getTrans");
            return;
        }
        MutableComponent before = (MutableComponent) expected, after = (MutableComponent) actual;
        require(before.equals(after), "Fallback component differs from original getTrans");
        TranslatableContents a = (TranslatableContents) before.getContents();
        TranslatableContents b = (TranslatableContents) after.getContents();
        require(a.getKey().equals(b.getKey()) && Arrays.deepEquals(a.getArgs(), b.getArgs()),
                "Fallback key or argument values changed");
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 2, "Usage: MiningLanguageHarness <transformed-class-file> <candidate-json>");
        Map<String, String> candidateJa = candidate(Path.of(args[1]));
        Map<String, String> en = builtAsset("en_us");
        Map<String, String> ja = builtAsset("ja_jp");
        require(ja.get(ENABLED).equals(candidateJa.get(ENABLED)) && ja.get(DISABLED).equals(candidateJa.get(DISABLED)),
                "Built Japanese asset differs from the submitted two-key candidate");
        Path transformedClass = Path.of(args[0]);
        Path candidatePath = Path.of(args[1]);
        Method method = handler(transformedClass);
        Language original = Language.getInstance();
        List<String> checks = new ArrayList<>();
        Map<String, Object> observations = new LinkedHashMap<>();
        try {
            Language.inject(new TestLanguage(en));
            MutableComponent retainedEnabled = invoke(method, SOURCE_KEY, new Object[]{Boolean.TRUE});
            MutableComponent retainedDisabled = invoke(method, SOURCE_KEY, new Object[]{Boolean.FALSE});
            require(en.get(ENABLED).equals(retainedEnabled.getString()) && en.get(DISABLED).equals(retainedDisabled.getString()),
                    "English built-asset captions mismatch");
            checks.add("English built asset captions; Japanese overlay absent");
            observations.put("english_only", List.of(retainedEnabled.getString(), retainedDisabled.getString()));
            Language.inject(new TestLanguage(ja));
            require(ja.get(ENABLED).equals(retainedEnabled.getString()) && ja.get(DISABLED).equals(retainedDisabled.getString()),
                    "Retained components did not transition English -> Japanese");
            checks.add("retained English-to-Japanese transition");
            observations.put("japanese", List.of(retainedEnabled.getString(), retainedDisabled.getString()));
            MutableComponent newJapanese = invoke(method, SOURCE_KEY, new Object[]{Boolean.TRUE});
            require(ja.get(ENABLED).equals(newJapanese.getString()), "Japanese enabled caption mismatch");
            Language.inject(new TestLanguage(en));
            require(en.get(ENABLED).equals(retainedEnabled.getString()) && en.get(DISABLED).equals(retainedDisabled.getString()),
                    "Retained components did not transition Japanese -> English");
            require(en.get(ENABLED).equals(newJapanese.getString()), "English fallback transition mismatch");
            checks.add("retained Japanese-to-English transition");
            observations.put("english_again", List.of(retainedEnabled.getString(), retainedDisabled.getString()));
            originalFallback(method, "tooltip.screen.other", new Object[]{Boolean.TRUE});
            originalFallback(method, SOURCE_KEY, new Object[]{"true"});
            originalFallback(method, SOURCE_KEY, new Object[]{});
            originalFallback(method, SOURCE_KEY, new Object[]{Boolean.TRUE, "extra"});
            originalFallback(method, SOURCE_KEY, new Object[]{null});
            originalFallback(method, SOURCE_KEY, null);
            originalFallback(method, null, new Object[]{27});
            checks.add("wrong-key/type/arity/null original fallback");
        } finally {
            Language.inject(original);
        }
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("transformed_class_sha256", hash(Files.readAllBytes(transformedClass)));
        report.put("candidate_reference", "reviews/" + candidatePath.getFileName());
        report.put("observations", observations);
        report.put("actual_language_load_from_json", true);
        report.put("fallback_compared_to_original_method", true);
        report.put("candidate_sha256", hash(Files.readAllBytes(candidatePath)));
        report.put("checks", checks);
        report.put("built_asset_key_count", BUILT_KEYS.size());
        report.put("whole_gui_init_executed", false);
        report.put("whole_gui_click_executed", false);
        report.put("visual_qa", false);
        Files.writeString(transformedClass.getParent().resolve("mining-language-report.json"),
                new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
        System.out.println("PASS actual transformed precision handler: built 11-key assets, English/Japanese retained transitions, and wrong-key/type/arity/null fallback");
    }
}
