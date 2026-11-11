// Decompile every function into one C file, and list defined strings with their referencing functions.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.StringDataInstance;
import java.io.*;

public class DumpAll extends GhidraScript {
  public void run() throws Exception {
    String out = getScriptArgs()[0];
    DecompInterface d = new DecompInterface(); d.openProgram(currentProgram);
    try (PrintWriter w = new PrintWriter(new FileWriter(out + "/decomp.c"))) {
      for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
        if (monitor.isCancelled()) break;
        DecompileResults r = d.decompileFunction(f, 60, monitor);
        w.println("// ==== " + f.getName() + " @ " + f.getEntryPoint());
        w.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// FAILED: " + r.getErrorMessage());
      }
    }
    try (PrintWriter w = new PrintWriter(new FileWriter(out + "/strings.tsv"))) {
      for (Data s : currentProgram.getListing().getDefinedData(true)) {
        if (!s.hasStringValue()) continue;
        StringBuilder refs = new StringBuilder();
        for (Reference ref : getReferencesTo(s.getAddress())) {
          Function f = getFunctionContaining(ref.getFromAddress());
          refs.append(f == null ? ref.getFromAddress().toString() : f.getName()).append(' ');
        }
        String v = String.valueOf(s.getValue()).replace("\t","\\t").replace("\n","\\n").replace("\r","\\r");
        w.println(s.getAddress() + "\t" + v + "\t" + refs.toString().trim());
      }
    }
  }
}
