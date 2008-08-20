#!/usr/bin/env rune
def compile := <import:com.twistedmatrix.ecru.compiler>;
def dump := <import:com.twistedmatrix.ecru.bytecodeDumper>;
def text := stdin.getText();
def debugDump := <import:com.twistedmatrix.ecru.debugDump>;
def out := <unsafe:java.lang.makeSystem>.getOut();

def modd := compile(e__quasiParser(text),
                    if (interp.getArgs().contains("-p")) {
                      privilegedScope
                    } else {
                      safeScope});

if (interp.getArgs().contains("-d")) {
  debugDump(modd, stdout)
} else {
  dump.write(modd, out)
}
