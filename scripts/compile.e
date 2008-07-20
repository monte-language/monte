#!/usr/bin/env rune
def compile := <import:com.twistedmatrix.ecru.compiler>;
def dump := <import:com.twistedmatrix.ecru.bytecodeDumper>;
def text := stdin.getText();
def debugDump := <import:com.twistedmatrix.ecru.debugDump>;
def out := <unsafe:java.lang.makeSystem>.getOut();

def twist(b) {
  return if (b > 127) {
    b - 256
  } else {
    b
  }
}

def twistList(bs) {
  def sbs := [].diverge()
  for x in bs {
    sbs.push(twist(x))
  }
  return sbs.snapshot()
}

def modd := compile(e__quasiParser(text),
                    if (interp.getArgs().contains("-p")) {
                      privilegedScope
                    } else {
                      safeScope});

if (interp.getArgs().contains("-d")) {
  debugDump(modd, stdout)
} else {
  out.write(twistList(dump(modd)))
}
