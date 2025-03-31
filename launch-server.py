#!/usr/bin/env python3
from signal import signal, SIG_IGN, SIGTERM, SIGINT
import subprocess
import sys

USAGE = """Usage: minecraftd [server jar path] [java options]*"""
JAVA_BIN = "/usr/bin/java"
JAVA_OPTS = [
    "-Xmx14G",
    "-XX:+UnlockExperimentalVMOptions",
    "-XX:G1MixedGCCountTarget=2",
    "-XX:+UseNUMA",
    "-XX:-DontCompileHugeMethods",
    "-XX:MaxNodeLimit=240000",
    "-XX:NodeLimitFudgeFactor=8000",
    "-XX:ReservedCodeCacheSize=400M",
    "-XX:NonNMethodCodeHeapSize=12M",
    "-XX:ProfiledCodeHeapSize=194M",
    "-XX:NonProfiledCodeHeapSize=194M",
    "-XX:NmethodSweepActivity=1",
    "-XX:+UseFastUnorderedTimeStamps",
    "-XX:+UseCriticalJavaThreadPriority",
    "-XX:ThreadPriorityPolicy=1",
    "-XX:G1SATBBufferEnqueueingThresholdPercent=30",
    "-XX:G1ConcMarkStepDurationMillis=5",
    "-XX:G1ConcRSHotCardLimit=16",
    "-XX:G1ConcRefinementServiceIntervalMillis=150",
    "-XX:G1RSetUpdatingPauseTimePercent=0",
    "-XX:G1HeapWastePercent=18",
    "-XX:GCTimeRatio=99",
    "-XX:AllocatePrefetchStyle=3",
    "-Dgraal.WriteableCodeCache=true",
]


def printf(fmt, *args):
    sys.stdout.write(fmt % tuple(args))
    sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
        exit(1)
    jar_path = sys.argv[1]
    opts = JAVA_OPTS + sys.argv[2:]
    args = [JAVA_BIN, "-server"] + opts + ["-jar", jar_path, "nogui"]

    printf("minecraftd: %s\n", " ".join(args))

    def preexec():
        signal(SIGTERM, SIG_IGN)
        signal(SIGINT, SIG_IGN)

    p = subprocess.Popen(args=args, stdin=subprocess.PIPE, preexec_fn=preexec)

    def handler(sig, _):
        printf("minecraftd: stopping server\n")
        p.stdin.write(b"stop\n")
        p.stdin.flush()

    signal(SIGTERM, handler)
    signal(SIGINT, handler)
    p.wait()
    printf("minecraftd: exit code is %d", p.returncode)
    sys.exit(p.returncode)
