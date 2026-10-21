// Export per-function features for cross-build matching, one JSON object per line:
// entry, name, size, ninsn, shape (address-free instruction stream), callees, data refs, immediates.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.scalar.Scalar;
import ghidra.program.model.symbol.*;
import java.io.*;
import java.util.*;

public class ExportFeatures extends GhidraScript {
    static String esc(String s) { return s.replace("\\", "\\\\").replace("\"", "\\\""); }

    @Override
    public void run() throws Exception {
        PrintWriter w = new PrintWriter(new FileWriter(getScriptArgs()[0]));
        Listing listing = currentProgram.getListing();
        long lo = currentProgram.getMinAddress().getOffset(), hi = currentProgram.getMaxAddress().getOffset();
        for (Function f : listing.getFunctions(true)) {
            StringBuilder shape = new StringBuilder();
            List<String> callees = new ArrayList<>(), drefs = new ArrayList<>(), imms = new ArrayList<>();
            int n = 0;
            for (Instruction ins : listing.getInstructions(f.getBody(), true)) {
                n++;
                shape.append(ins.getMnemonicString());
                for (int i = 0; i < ins.getNumOperands(); i++) {
                    shape.append(i == 0 ? ' ' : ',');
                    for (Object o : ins.getOpObjects(i)) {
                        if (o instanceof Scalar) {
                            long v = ((Scalar) o).getUnsignedValue();
                            if (v >= lo && v <= hi) shape.append("A");
                            else { shape.append("#").append(Long.toHexString(v)); if (v > 0xff) imms.add(Long.toHexString(v)); }
                        } else if (o instanceof Address) shape.append("A");
                        else shape.append(o.toString());
                    }
                }
                shape.append(';');
                for (Reference r : ins.getReferencesFrom()) {
                    Address to = r.getToAddress();
                    if (!to.isMemoryAddress()) continue;
                    if (r.getReferenceType().isCall()) callees.add(to.toString());
                    else if (r.getReferenceType().isData()) drefs.add(to.toString());
                }
            }
            w.print("{\"entry\":\"" + f.getEntryPoint() + "\",\"name\":\"" + esc(f.getName(true)) + "\",\"size\":" + f.getBody().getNumAddresses()
                    + ",\"ninsn\":" + n + ",\"shape\":\"" + esc(shape.toString()) + "\",\"callees\":[");
            for (int i = 0; i < callees.size(); i++) w.print((i > 0 ? "," : "") + "\"" + callees.get(i) + "\"");
            w.print("],\"drefs\":[");
            for (int i = 0; i < drefs.size(); i++) w.print((i > 0 ? "," : "") + "\"" + drefs.get(i) + "\"");
            w.print("],\"imms\":[");
            for (int i = 0; i < imms.size(); i++) w.print((i > 0 ? "," : "") + "\"" + imms.get(i) + "\"");
            w.println("]}");
        }
        w.close();
        println("exported functions to " + getScriptArgs()[0]);
    }
}
