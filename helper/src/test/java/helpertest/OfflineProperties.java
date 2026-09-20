package helpertest;

import java.util.HashMap;
import java.util.Map;
import org.spongepowered.asm.service.IGlobalPropertyService;
import org.spongepowered.asm.service.IPropertyKey;

public final class OfflineProperties implements IGlobalPropertyService {
    private record Key(String name) implements IPropertyKey {}
    private final Map<IPropertyKey, Object> values = new HashMap<>();
    @Override public IPropertyKey resolveKey(String name) { return new Key(name); }
    @Override @SuppressWarnings("unchecked") public <T> T getProperty(IPropertyKey key) { return (T) values.get(key); }
    @Override public void setProperty(IPropertyKey key, Object value) { values.put(key, value); }
    @Override @SuppressWarnings("unchecked") public <T> T getProperty(IPropertyKey key, T fallback) { return (T) values.getOrDefault(key, fallback); }
    @Override public String getPropertyString(IPropertyKey key, String fallback) { return String.valueOf(values.getOrDefault(key, fallback)); }
}
