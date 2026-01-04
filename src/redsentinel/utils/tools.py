import shutil
import os


def which(cmd):
    return shutil.which(cmd)


def is_termux():
    return "TERMUX_VERSION" in os.environ or os.path.exists("/data/data/com.termux")


def tool_status():
    return {
        "nmap": which("nmap"),
        "nikto": which("nikto") or which("nikto.pl"),
        "whatweb": which("whatweb"),
        "perl": which("perl"),
        "ruby": which("ruby"),
    }

