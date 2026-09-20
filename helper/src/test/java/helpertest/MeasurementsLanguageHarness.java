package helpertest;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.io.StringWriter;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Supplier;
import com.electronwill.nightconfig.core.CommentedConfig;
import net.neoforged.fml.config.IConfigSpec;
import com.electronwill.nightconfig.toml.TomlParser;
import com.electronwill.nightconfig.toml.TomlWriter;
import net.minecraft.client.OptionInstance;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.locale.Language;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.item.DyeColor;
import net.neoforged.neoforge.client.gui.ConfigurationScreen;
import net.neoforged.neoforge.client.gui.ConfigurationScreen.ConfigurationSectionScreen;
import net.neoforged.neoforge.common.ModConfigSpec;
import sun.misc.Unsafe;

/**
 * Offline consumer harness for the Measurements enum helper candidate.
 *
 * CLI: MeasurementsLanguageHarness <transformed-dir> <accepted-submission-json> <output-report-json>
 * The real NeoForge createEnumValue method and its OptionInstance formatter are
 * invoked; no Minecraft process, GUI constructor, or rendering is started.
 */
public final class MeasurementsLanguageHarness {
    private static final String MEASUREMENTS = "com.mrbysco.measurements.";
    private static final String LINE = "com.mrbysco.measurements.config.LineColor";
    private static final String TEXT = "com.mrbysco.measurements.config.TextColor";
    private static final String HELPER_PREFIX = "atm11_japanese_helper.measurements.enum.";
    private static final String JAR_SHA = "e72dadf160dce841d3c395138938eaee0ce09b9986bb7c1d5d3591c27752af11";
    private static final String INNER_HASH = "5e7c94bf81f50a8395f2b9aefb3ddc2530d87cd914293b94f29da776a2a86aeb";
    private static final String LINE_HASH = "4dd94a59b5d8f9771ba7663b6db9ba28dbb34f54b683e0ba6a1d5dc1df4411f4";
    private static final String TEXT_HASH = "73323c37550ecb90efa4aba76d8c4015cb5b27c8c75a9c0a28fab74b3bc551d4";

    private static void require(boolean ok, String message) {
        if (!ok) throw new AssertionError(message);
    }

    private static String sha(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static byte[] resource(ClassLoader loader, String name) throws Exception {
        try (InputStream in = loader.getResourceAsStream(name)) {
            require(in != null, "Missing classpath resource: " + name);
            return in.readAllBytes();
        }
    }

    private static final class MeasurementsLoader extends ClassLoader {
        private final Path transformed;

        MeasurementsLoader(Path transformed) {
            super(MeasurementsLanguageHarness.class.getClassLoader());
            this.transformed = transformed;
        }

        @Override public Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
            if (name.startsWith(MEASUREMENTS)) {
                Class<?> loaded = findLoadedClass(name);
                Class<?> value = loaded == null ? findClass(name) : loaded;
                if (resolve) resolveClass(value);
                return value;
            }
            return super.loadClass(name, resolve);
        }

        @Override protected Class<?> findClass(String name) throws ClassNotFoundException {
            String resource = name.replace('.', '/') + ".class";
            Path candidate = transformed.resolve(resource);
            try {
                if (Files.isRegularFile(candidate)) {
                    byte[] bytes = Files.readAllBytes(candidate);
                    return defineClass(name, bytes, 0, bytes.length);
                }
                byte[] bytes = resource(getParent(), resource);
                return defineClass(name, bytes, 0, bytes.length);
            } catch (Exception e) {
                throw new ClassNotFoundException(name, e);
            }
        }
    }

    private static final class JsonLanguage extends Language {
        private final Map<String, String> values;

        JsonLanguage(Map<String, String> values) { this.values = Map.copyOf(values); }
        @Override public String getOrDefault(String key, String fallback) { return values.getOrDefault(key, fallback); }
        @Override public boolean has(String key) { return values.containsKey(key); }
        @Override public boolean isDefaultRightToLeft() { return false; }
        @Override public FormattedCharSequence getVisualOrder(FormattedText text) { return FormattedCharSequence.EMPTY; }
    }

    private enum Unrelated { ONE }

    private record FieldRun(String enumClass, List<String> enumNames, List<String> captions,
                            List<String> callbackValues, String selectedBefore, String selectedAfter,
                            boolean optionValuesExact, boolean configRestored) {}

    private static Map<String, Object> objectMap(Path path) throws Exception {
        try (var reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            return new Gson().fromJson(reader, new TypeToken<Map<String, Object>>() {}.getType());
        }
    }

    @SuppressWarnings("unchecked")
    private static Map<String, String> stringMap(Object value) {
        Map<String, String> result = new LinkedHashMap<>();
        ((Map<String, Object>) value).forEach((key, item) -> result.put(key, String.valueOf(item)));
        return result;
    }

    private static Map<String, String> loadAsset(ClassLoader loader, String locale) throws Exception {
        Map<String, String> result = new LinkedHashMap<>();
        try (InputStream in = loader.getResourceAsStream("assets/atm11_japanese_helper/lang/" + locale + ".json")) {
            require(in != null, "Missing helper language asset: " + locale);
            Language.loadFromJson(in, result::put);
        }
        return result;
    }

    private static Object unsafeScreen(ContextAndSpec context) throws Exception {
        Field field = Unsafe.class.getDeclaredField("theUnsafe");
        field.setAccessible(true);
        Unsafe unsafe = (Unsafe) field.get(null);
        Object screen = unsafe.allocateInstance(ConfigurationSectionScreen.class);
        Field contextField = ConfigurationSectionScreen.class.getDeclaredField("context");
        contextField.setAccessible(true);
        contextField.set(screen, context.context);
        Field undoField = ConfigurationSectionScreen.class.getDeclaredField("undoManager");
        undoField.setAccessible(true);
        undoField.set(screen, new ConfigurationScreen.UndoManager());
        Field restartField = ConfigurationSectionScreen.class.getDeclaredField("needsRestart");
        restartField.setAccessible(true);
        restartField.set(screen, ModConfigSpec.RestartType.NONE);
        return screen;
    }

    private record ContextAndSpec(ModConfigSpec spec, ConfigurationSectionScreen.Context context,
                                  Map<String, ModConfigSpec.ValueSpec> fieldSpecs,
                                  Map<String, Object> fieldValues) {}

    private static void acceptInMemoryConfig(ContextAndSpec context) throws Exception {
        // The spec tree already contains every section and default, so copying it
        // preserves the exact shape expected by ModConfigSpec.isCorrect().
        CommentedConfig values = CommentedConfig.copy(context.spec.getSpec());
        context.spec.correct(values);
        require(context.spec.isCorrect(values), "In-memory config did not satisfy Measurements spec");
        Class<?> loadedType = Class.forName("net.neoforged.fml.config.LoadedConfig");
        var constructor = loadedType.getDeclaredConstructor(CommentedConfig.class, Path.class,
                Class.forName("net.neoforged.fml.config.ModConfig"));
        constructor.setAccessible(true);
        IConfigSpec.ILoadedConfig loaded = (IConfigSpec.ILoadedConfig) constructor.newInstance(values, null, null);
        context.spec.acceptConfig(loaded);
    }

    private static ContextAndSpec context(ClassLoader loader) throws Exception {
        Class<?> config = Class.forName("com.mrbysco.measurements.config.MeasurementConfig", true, loader);
        ModConfigSpec spec = (ModConfigSpec) config.getField("clientSpec").get(null);
        Method getValues = spec.getClass().getMethod("getValues");
        Object topValues = getValues.invoke(spec);
        Method valueMap = topValues.getClass().getMethod("valueMap");
        Method entrySet = topValues.getClass().getMethod("entrySet");
        valueMap.setAccessible(true);
        entrySet.setAccessible(true);
        @SuppressWarnings("unchecked") Map<String, Object> topMap = (Map<String, Object>) valueMap.invoke(topValues);
        Object specRoot = spec.getClass().getMethod("getSpec").invoke(spec);
        Method rootValueMap = specRoot.getClass().getMethod("valueMap");
        rootValueMap.setAccessible(true);
        @SuppressWarnings("unchecked") Map<String, Object> specMap = (Map<String, Object>) rootValueMap.invoke(specRoot);
        Class<?> modConfig = Class.forName("net.neoforged.fml.config.ModConfig");
        Class<?> contextClass = ConfigurationSectionScreen.Context.class;
        Object topContext = contextClass.getConstructor(String.class, Screen.class, modConfig, ModConfigSpec.class,
                Set.class, Map.class, List.class, ConfigurationSectionScreen.Filter.class)
                .newInstance("measurements", null, null, spec, entrySet.invoke(topValues), specMap, List.of(), null);
        Object clientObject = topMap.get("client");
        require(clientObject != null, "Measurements client config section missing");
        Method clientValueMap = clientObject.getClass().getMethod("valueMap");
        clientValueMap.setAccessible(true);
        @SuppressWarnings("unchecked") Map<String, Object> clientMap = (Map<String, Object>) clientValueMap.invoke(clientObject);
        Map<String, ModConfigSpec.ValueSpec> fieldSpecs = new LinkedHashMap<>();
        Map<String, Object> fieldValues = new LinkedHashMap<>();
        for (var entry : clientMap.entrySet()) {
            require(entry.getValue() instanceof ModConfigSpec.ConfigValue<?>,
                    "Unexpected client config entry: " + entry.getKey());
            ModConfigSpec.ConfigValue<?> value = (ModConfigSpec.ConfigValue<?>) entry.getValue();
            fieldSpecs.put(entry.getKey(), value.getSpec());
            fieldValues.put(entry.getKey(), value);
        }
        Method section = contextClass.getMethod("section", contextClass, Screen.class, Set.class, Map.class, String.class);
        Object fieldContext = section.invoke(null, topContext, null,
                entrySet(clientObject), new LinkedHashMap<>(fieldSpecs), "client");
        return new ContextAndSpec(spec, (ConfigurationSectionScreen.Context) fieldContext, fieldSpecs, fieldValues);
    }

    private static Object entrySet(Object value) throws Exception {
        Method method = value.getClass().getMethod("entrySet");
        method.setAccessible(true);
        return method.invoke(value);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static Method createMethod() throws Exception {
        Method create = ConfigurationSectionScreen.class.getDeclaredMethod("createEnumValue", String.class,
                ModConfigSpec.ValueSpec.class, Supplier.class, Consumer.class);
        create.setAccessible(true);
        return create;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private static OptionInstance<?> enumOption(Object screen, String key, ModConfigSpec.ValueSpec valueSpec,
                                                Object configValue, Consumer<Object> target) throws Exception {
        Supplier<Object> source = () -> {
            try { return ((ModConfigSpec.ConfigValue<?>) configValue).getRaw(); }
            catch (Exception e) { throw new RuntimeException(e); }
        };
        Object element = createMethod().invoke(screen, key, valueSpec, source, target);
        return (OptionInstance<?>) element.getClass().getMethod("option").invoke(element);
    }

    @SuppressWarnings("unchecked")
    private static Function<Object, Component> formatter(OptionInstance<?> option) throws Exception {
        Field field = OptionInstance.class.getDeclaredField("toString");
        field.setAccessible(true);
        return (Function<Object, Component>) field.get(option);
    }

    private static List<Map<String, String>> captions(OptionInstance<?> option, Class<?> enumClass) throws Exception {
        Function<Object, Component> toString = formatter(option);
        List<Map<String, String>> result = new ArrayList<>();
        for (Object value : enumClass.getEnumConstants()) {
            result.add(Map.of("enum", ((Enum<?>) value).name(), "caption", toString.apply(value).getString()));
        }
        return result;
    }

    private static FieldRun runField(Object screen, String key, Class<?> enumClass,
                                     ModConfigSpec.ValueSpec valueSpec, Object configValue) throws Exception {
        List<Object> callbacks = new ArrayList<>();
        Consumer<Object> target = value -> {
            callbacks.add(value);
            ((ModConfigSpec.ConfigValue<Object>) configValue).set(value);
        };
        OptionInstance option = (OptionInstance) enumOption(screen, key, valueSpec, configValue, target);
        List<Object> constants = List.of(enumClass.getEnumConstants());
        Field valuesField = OptionInstance.class.getDeclaredField("values");
        valuesField.setAccessible(true);
        Object valueSet = valuesField.get(option);
        Method valuesMethod = valueSet.getClass().getMethod("values");
        List<?> optionValues = (List<?>) valuesMethod.invoke(valueSet);
        List<String> names = constants.stream().map(v -> ((Enum<?>) v).name()).toList();
        List<String> captions = new ArrayList<>();
        for (Object constant : constants) captions.add(formatter(option).apply(constant).getString());
        require(optionValues.equals(constants), "OptionInstance value order changed for " + enumClass.getName());
        Object selectedBefore = option.get();
        Object firstOther = constants.stream().filter(v -> v != selectedBefore).findFirst().orElse(selectedBefore);
        setOffline(option, firstOther);
        for (Object constant : constants) setOffline(option, constant);
        Object selectedAfterCycle = option.get();
        setOffline(option, selectedBefore);
        Object selectedAfter = option.get();
        Object restored = ((ModConfigSpec.ConfigValue<?>) configValue).getRaw();
        boolean callbacksAreEnums = callbacks.stream().allMatch(v -> enumClass.isInstance(v));
        require(callbacksAreEnums && callbacks.size() == constants.size() + 2,
                "Callback did not receive every enum selection for " + key);
        require(enumClass.isInstance(selectedAfterCycle) && selectedAfter == selectedBefore,
                "Option selected value was not restored for " + key);
        require(enumClass.isInstance(restored) && restored == selectedBefore, "Config value was not restored for " + key);
        return new FieldRun(enumClass.getName(), names, captions,
                callbacks.stream().map(v -> ((Enum<?>) v).name()).toList(),
                ((Enum<?>) selectedBefore).name(), ((Enum<?>) selectedAfter).name(), true, true);
    }

    /**
     * OptionInstance.set() deliberately requires Minecraft.isRunning().  The
     * harness has no client, so it applies the value field and invokes the
     * actual OptionInstance.onValueUpdate consumer; formatter behavior remains
     * the real OptionInstance. This preserves the callback/undo path supplied
     * by NeoForge's createEnumValue without starting a client.
     */
    private static void setOffline(OptionInstance<?> option, Object value) throws Exception {
        Field valueField = OptionInstance.class.getDeclaredField("value");
        valueField.setAccessible(true);
        valueField.set(option, value);
        Field callbackField = OptionInstance.class.getDeclaredField("onValueUpdate");
        callbackField.setAccessible(true);
        @SuppressWarnings("unchecked") Consumer<Object> callback = (Consumer<Object>) callbackField.get(option);
        callback.accept(value);
    }

    private static Map<String, String> install(Map<String, String> values) {
        Language.inject(new JsonLanguage(values));
        return values;
    }

    private static Map<String, Object> semantic(ClassLoader loader, String className) throws Exception {
        Class<?> type = Class.forName(className, true, loader);
        Map<String, Object> out = new LinkedHashMap<>();
        Method lineMethod = className.endsWith("LineColor")
                ? type.getDeclaredMethod("getColor", Random.class)
                : type.getDeclaredMethod("getColor", Random.class, Class.forName("net.minecraft.core.Direction$Axis"));
        Class<?> axis = Class.forName("net.minecraft.core.Direction$Axis");
        Object[] constants = type.getEnumConstants();
        Map<String, Object> results = new LinkedHashMap<>();
        Set<String> dyeNames = new HashSet<>();
        for (DyeColor color : DyeColor.values()) dyeNames.add(color.name());
        for (Object constant : constants) {
            String name = ((Enum<?>) constant).name();
            if (className.endsWith("LineColor")) {
                Object value = lineMethod.invoke(constant, new Random(7));
                String result = ((Enum<?>) value).name();
                require(dyeNames.contains(result), "LineColor returned non-DyeColor: " + name + "=" + result);
                if (!name.equals("RANDOM")) require(result.equals(name), "LineColor mapping changed: " + name + "=" + result);
                if (name.equals("RANDOM")) {
                    Object second = lineMethod.invoke(constant, new Random(19));
                    require(dyeNames.contains(((Enum<?>) second).name()), "LineColor RANDOM returned non-DyeColor");
                    results.put(name + "_seed19", ((Enum<?>) second).name());
                }
                results.put(name, result);
            } else if (name.equals("XYZRGB")) {
                Map<String, String> byAxis = new LinkedHashMap<>();
                for (String axisName : List.of("X", "Y", "Z")) {
                    Object value = lineMethod.invoke(constant, new Random(7), Enum.valueOf((Class) axis, axisName));
                    byAxis.put(axisName, ((Enum<?>) value).name());
                }
                Object nullAxis = lineMethod.invoke(constant, new Object[]{new Random(7), null});
                byAxis.put("null", ((Enum<?>) nullAxis).name());
                require("RED".equals(byAxis.get("X")) && "GREEN".equals(byAxis.get("Y"))
                        && "BLUE".equals(byAxis.get("Z")) && "YELLOW".equals(byAxis.get("null")),
                        "TextColor XYZRGB axis mapping changed: " + byAxis);
                results.put(name, byAxis);
            } else {
                Object value = lineMethod.invoke(constant, new Object[]{new Random(7), null});
                String result = ((Enum<?>) value).name();
                require(dyeNames.contains(result), "TextColor returned non-DyeColor: " + name + "=" + result);
                if (!name.equals("RANDOM")) require(result.equals(name), "TextColor mapping changed: " + name + "=" + result);
                if (name.equals("RANDOM")) {
                    Object second = lineMethod.invoke(constant, new Object[]{new Random(19), null});
                    require(dyeNames.contains(((Enum<?>) second).name()), "TextColor RANDOM returned non-DyeColor");
                    results.put(name + "_seed19", ((Enum<?>) second).name());
                }
                results.put(name, result);
            }
        }
        out.put("values", results);
        return out;
    }

    private static Map<String, Object> enumNameRoundTrip(Class<?> lineClass, Class<?> textClass) throws Exception {
        CommentedConfig source = CommentedConfig.inMemory();
        List<String> expected = new ArrayList<>();
        for (Class<?> type : List.of(lineClass, textClass)) {
            for (Object value : type.getEnumConstants()) {
                String path = type.getSimpleName() + "." + ((Enum<?>) value).name();
                expected.add(path);
                source.set(List.of("measurements", type.getSimpleName(), ((Enum<?>) value).name()), value);
            }
        }
        StringWriter text = new StringWriter();
        new TomlWriter().write(source, text);
        CommentedConfig parsed = new TomlParser().parse(new StringReader(text.toString()));
        List<String> restored = new ArrayList<>();
        for (Class<?> type : List.of(lineClass, textClass)) {
            for (Object value : type.getEnumConstants()) {
                String name = ((Enum<?>) value).name();
                Object round = parsed.get(List.of("measurements", type.getSimpleName(), name));
                require(name.equals(round), "NightConfig TOML enum round-trip changed " + type.getSimpleName() + "." + name);
                restored.add(type.getSimpleName() + "." + name);
            }
        }
        require(expected.equals(restored), "NightConfig TOML enum key order/count changed");
        return Map.of("values", expected.size(), "serialized_sha256", sha(text.toString().getBytes(StandardCharsets.UTF_8)),
                "parsed_values", restored.size(), "pass", true);
    }

    private static String sha(String text) throws Exception {
        return sha(text.getBytes(StandardCharsets.UTF_8));
    }

    private static void write(Path path, Map<String, Object> report) throws Exception {
        Files.createDirectories(path.toAbsolutePath().getParent());
        Files.writeString(path, new GsonBuilder().setPrettyPrinting().create().toJson(report) + "\n");
    }

    public static void main(String[] args) throws Exception {
        require(args.length == 3, "Usage: MeasurementsLanguageHarness <transformed-dir> <accepted-submission-json> <output-report-json>");
        Path transformed = Path.of(args[0]);
        Path submission = Path.of(args[1]);
        Path reportPath = Path.of(args[2]);
        Map<String, Object> report = new LinkedHashMap<>();
        report.put("visual_qa", false);
        report.put("minecraft_started", false);
        report.put("whole_gui_navigation_executed", false);
        report.put("option_set_mode", "offline_value_field_plus_actual_onValueUpdate_callback");
        report.put("option_set_limitation", "OptionInstance.set requires a running Minecraft client; no GUI/client was started");
        report.put("hashes_before_and_after", new LinkedHashMap<>());
        try {
            Map<String, Object> sub = objectMap(submission);
            Map<String, String> jaExpected = stringMap(sub.get("entries"));
            Map<String, String> enExpected = stringMap(sub.get("english_fallback"));
            require(jaExpected.size() == 35 && enExpected.size() == 35, "Submission must contain exactly 35 values");
            ClassLoader parent = MeasurementsLanguageHarness.class.getClassLoader();
            byte[] lineBefore = resource(parent, LINE.replace('.', '/') + ".class");
            byte[] textBefore = resource(parent, TEXT.replace('.', '/') + ".class");
            byte[] inner = resource(parent, "net/neoforged/neoforge/client/gui/ConfigurationScreen$ConfigurationSectionScreen.class");
            require(sha(lineBefore).equals(LINE_HASH) && sha(textBefore).equals(TEXT_HASH), "Measurements enum JAR hash mismatch");
            require(sha(inner).equals(INNER_HASH), "NeoForge ConfigurationSectionScreen hash mismatch");
            Map<String, Object> hashes = new LinkedHashMap<>();
            hashes.put("lineColor_jar", sha(lineBefore)); hashes.put("textColor_jar", sha(textBefore));
            hashes.put("configuration_section_screen", sha(inner)); hashes.put("measurements_jar_sha256", JAR_SHA);
            Path lineTransformed = transformed.resolve(LINE.replace('.', '/') + ".class");
            Path textTransformed = transformed.resolve(TEXT.replace('.', '/') + ".class");
            hashes.put("lineColor_transformed", Files.isRegularFile(lineTransformed) ? sha(Files.readAllBytes(lineTransformed)) : null);
            hashes.put("textColor_transformed", Files.isRegularFile(textTransformed) ? sha(Files.readAllBytes(textTransformed)) : null);
            report.put("hashes_before_and_after", hashes);
            MeasurementsLoader loader = new MeasurementsLoader(transformed);
            Class<?> lineClass = Class.forName(LINE, true, loader);
            Class<?> textClass = Class.forName(TEXT, true, loader);
            Class<?> translatableEnum = Class.forName("net.neoforged.neoforge.common.TranslatableEnum");
            boolean helperActive = translatableEnum.isAssignableFrom(lineClass) && translatableEnum.isAssignableFrom(textClass);
            report.put("helper_translatable_enum_active", helperActive);
            require(helperActive, "Transformed enum classes do not implement TranslatableEnum");
            ContextAndSpec context = context(loader);
            acceptInMemoryConfig(context);
            Object screen = unsafeScreen(context);
            Map<String, String> enAsset = loadAsset(parent, "en_us");
            Map<String, String> jaAsset = loadAsset(parent, "ja_jp");
            for (String key : enExpected.keySet()) require(enExpected.get(key).equals(enAsset.get(key)), "English asset mismatch: " + key);
            for (String key : jaExpected.keySet()) require(jaExpected.get(key).equals(jaAsset.get(key)), "Japanese asset mismatch: " + key);
            install(enAsset);
            List<FieldRun> runs = new ArrayList<>();
            runs.add(runField(screen, "lineColor", lineClass, context.fieldSpecs.get("lineColor"), context.fieldValues.get("lineColor")));
            runs.add(runField(screen, "textColor", textClass, context.fieldSpecs.get("textColor"), context.fieldValues.get("textColor")));
            require(runs.get(0).enumNames().size() == 17 && runs.get(1).enumNames().size() == 18, "Enum count mismatch");
            report.put("consumer_runs_english", runs);
            require(runs.get(0).captions().equals(runs.get(0).enumNames()), "English fallback captions changed LineColor identifiers");
            require(runs.get(1).captions().equals(runs.get(1).enumNames()), "English fallback captions changed TextColor identifiers");
            install(jaAsset);
            // Recreate real elements under Japanese and collect the formatter captions.
            List<Map<String, Object>> japanese = new ArrayList<>();
            Map<String, Component> retainedComponents = new LinkedHashMap<>();
            for (String[] row : new String[][]{{"lineColor", LINE}, {"textColor", TEXT}}) {
                Class<?> type = Class.forName(row[1], true, loader);
                OptionInstance<?> option = enumOption(screen, row[0], context.fieldSpecs.get(row[0]),
                        context.fieldValues.get(row[0]), v -> {});
                List<Map<String, String>> rows = captions(option, type);
                for (Map<String, String> caption : rows) {
                    String expected = jaExpected.get(HELPER_PREFIX + type.getSimpleName() + "." + caption.get("enum"));
                    require(expected != null && expected.equals(caption.get("caption")),
                            "Japanese caption mismatch: " + type.getSimpleName() + "." + caption.get("enum"));
                }
                japanese.add(Map.of("field", row[0], "captions", rows));
                for (Object value : type.getEnumConstants()) {
                    String key = HELPER_PREFIX + type.getSimpleName() + "." + ((Enum<?>) value).name();
                    Component component = formatter(option).apply(value);
                    require(jaExpected.get(key).equals(component.getString()), "Initial retained caption differs: " + key);
                    retainedComponents.put(key, component);
                }
            }
            report.put("consumer_runs_japanese", japanese);
            report.put("accepted_japanese", jaExpected);
            report.put("accepted_english", enExpected);
            Map<String, String> missing = new LinkedHashMap<>(jaAsset);
            String missingKey = "atm11_japanese_helper.measurements.enum.LineColor.WHITE";
            missing.remove(missingKey);
            install(missing);
            OptionInstance<?> missingOption = enumOption(screen, "lineColor", context.fieldSpecs.get("lineColor"),
                    context.fieldValues.get("lineColor"), v -> {});
            Object white = lineClass.getField("WHITE").get(null);
            require("WHITE".equals(formatter(missingOption).apply(white).getString()),
                    "Missing helper key did not fall back to Enum.name()");
            Map<String, String> empty = new LinkedHashMap<>();
            install(empty);
            OptionInstance<?> missingLocaleOption = enumOption(screen, "lineColor", context.fieldSpecs.get("lineColor"),
                    context.fieldValues.get("lineColor"), v -> {});
            require("WHITE".equals(formatter(missingLocaleOption).apply(white).getString()),
                    "Missing locale did not fall back to Enum.name()");
            report.put("missing_key_fallback", Map.of("key", missingKey, "output", "WHITE", "pass", true));
            int fallbackCount = 0;
            for (String[] row : new String[][]{{"lineColor", LINE}, {"textColor", TEXT}}) {
                Class<?> type = Class.forName(row[1], true, loader);
                OptionInstance<?> option = enumOption(screen, row[0], context.fieldSpecs.get(row[0]),
                        context.fieldValues.get(row[0]), v -> {});
                for (Map<String, String> caption : captions(option, type)) {
                    require(caption.get("enum").equals(caption.get("caption")),
                            "Missing locale did not fall back for " + type.getSimpleName() + "." + caption.get("enum"));
                    fallbackCount++;
                }
            }
            report.put("missing_locale_fallback", Map.of("locale", "missing", "values", fallbackCount, "pass", fallbackCount == 35));
            install(enAsset);
            for (var entry : retainedComponents.entrySet())
                require(enExpected.get(entry.getKey()).equals(entry.getValue().getString()),
                        "Retained Component did not re-resolve in English: " + entry.getKey());
            install(jaAsset);
            for (var entry : retainedComponents.entrySet())
                require(jaExpected.get(entry.getKey()).equals(entry.getValue().getString()),
                        "Retained Component did not re-resolve in Japanese: " + entry.getKey());
            report.put("locale_switch_reresolution", Map.of("ja_to_en_to_ja", true,
                    "same_components_reused", true, "values", retainedComponents.size()));
            Map<String, Object> transformedSemantics = Map.of("lineColor", semantic(loader, LINE), "textColor", semantic(loader, TEXT));
            Map<String, Object> originalSemantics = Map.of("lineColor", semantic(parent, LINE), "textColor", semantic(parent, TEXT));
            require(transformedSemantics.equals(originalSemantics), "Transformed enum color semantics differ from original enums");
            report.put("semantics", Map.of("transformed", transformedSemantics, "original", originalSemantics,
                    "seeded_random_comparison", true));
            report.put("measurement_box_constructor_executed", false);
            OptionInstance<?> unrelatedOption = enumOption(screen, "lineColor", context.fieldSpecs.get("lineColor"),
                    context.fieldValues.get("lineColor"), v -> {});
            require("ONE".equals(formatter(unrelatedOption).apply(Unrelated.ONE).getString()),
                    "Unrelated enum literal behavior changed");
            report.put("unrelated_enum_literal", Map.of("enum", "ONE", "caption", "ONE", "pass", true));
            report.put("nightconfig_toml_enum_round_trip", enumNameRoundTrip(lineClass, textClass));
        } catch (Throwable failure) {
            report.put("pass", false);
            report.put("error", failure.toString());
            write(reportPath, report);
            throw failure;
        }
        report.put("pass", true);
        write(reportPath, report);
        System.out.println("PASS real Measurements enum consumer harness");
    }
}
