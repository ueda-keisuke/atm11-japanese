package helpertest;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Collection;
import java.util.List;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.tree.ClassNode;
import org.spongepowered.asm.launch.platform.container.ContainerHandleVirtual;
import org.spongepowered.asm.launch.platform.container.IContainerHandle;
import org.spongepowered.asm.mixin.transformer.IMixinTransformer;
import org.spongepowered.asm.mixin.transformer.IMixinTransformerFactory;
import org.spongepowered.asm.mixin.MixinEnvironment;
import org.spongepowered.asm.logging.ILogger;
import org.spongepowered.asm.logging.LoggerAdapterConsole;
import org.spongepowered.asm.service.*;

/** Offline class/resource provider only. It never loads Minecraft or opens a window. */
public final class OfflineMixinService extends MixinServiceAbstract
        implements IClassProvider, IClassBytecodeProvider, ITransformerProvider, IClassTracker {
    private static final ClassLoader LOADER = OfflineMixinService.class.getClassLoader();
    @Override public String getName() { return "ATM11OfflineVerification"; }
    @Override protected ILogger createLogger(String name) { return new LoggerAdapterConsole(name); }
    @Override public boolean isValid() { return Boolean.getBoolean("atm11.helper.offline"); }
    @Override public MixinEnvironment.Phase getInitialPhase() { return MixinEnvironment.Phase.DEFAULT; }
    @Override public IClassProvider getClassProvider() { return this; }
    @Override public IClassBytecodeProvider getBytecodeProvider() { return this; }
    @Override public ITransformerProvider getTransformerProvider() { return this; }
    @Override public IClassTracker getClassTracker() { return this; }
    @Override public IMixinAuditTrail getAuditTrail() { return null; }
    @Override public IFeatureValidator getFeatureValidator() { return null; }
    @Override public IAdviceProvider getAdviceProvider() { return null; }
    @Override public Collection<String> getPlatformAgents() { return List.of(); }
    @Override public IContainerHandle getPrimaryContainer() { return new ContainerHandleVirtual("offline-test"); }
    @Override public InputStream getResourceAsStream(String name) { String hidden = System.getProperty("atm11.helper.hideResourcePrefix", "");
        if (!hidden.isEmpty() && name.startsWith(hidden)) return null;
        return LOADER.getResourceAsStream(name); }
    @Override public URL[] getClassPath() { return new URL[0]; }
    @Override public Class<?> findClass(String name) throws ClassNotFoundException { return findClass(name, false); }
    @Override public Class<?> findClass(String name, boolean initialize) throws ClassNotFoundException {
        if (name.equals("net.neoforged.neoforge.server.command.generation.GenerationBar") || name.startsWith("com.yogpc.qp.machine.") || name.startsWith("com.direwolf20.mininggadgets.client.screens.MiningSettingScreen")
                || name.equals("com.mrbysco.measurements.config.LineColor") || name.equals("com.mrbysco.measurements.config.TextColor")) throw new ClassNotFoundException("Target loading forbidden in offline test: " + name);
        return Class.forName(name, initialize, LOADER);
    }
    @Override public Class<?> findAgentClass(String name, boolean initialize) throws ClassNotFoundException { return findClass(name, initialize); }
    @Override public ClassNode getClassNode(String name) throws ClassNotFoundException, IOException { return getClassNode(name, false); }
    @Override public ClassNode getClassNode(String name, boolean transform) throws ClassNotFoundException, IOException {
        return getClassNode(name, transform, ClassReader.EXPAND_FRAMES);
    }
    @Override public ClassNode getClassNode(String name, boolean transform, int flags) throws ClassNotFoundException, IOException {
        try (InputStream input = getResourceAsStream(name.replace('.', '/') + ".class")) {
            if (input == null) throw new ClassNotFoundException(name);
            ClassNode node = new ClassNode();
            new ClassReader(input).accept(node, flags);
            return node;
        }
    }
    @Override public Collection<ITransformer> getTransformers() { return List.of(); }
    @Override public Collection<ITransformer> getDelegatedTransformers() { return List.of(); }
    @Override public void addTransformerExclusion(String name) {}
    @Override public void registerInvalidClass(String name) {}
    @Override public boolean isClassLoaded(String name) { return false; }
    @Override public String getClassRestrictions(String name) { return ""; }
    public IMixinTransformer transformer() { return getInternal(IMixinTransformerFactory.class).createTransformer(); }
}
