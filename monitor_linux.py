import os
import time
import signal

class ProcessMonitor:
    def __init__(self, process_name):
        self.process_name = process_name
        self.active_pids = set()
        self.opens = 0
        self.initial_delay = 0.5  # Atraso inicial em segundos

    def get_process_pids(self):
        """Obtém PIDs dos processos com o nome especificado."""
        try:
            output = os.popen(f"pgrep -f {self.process_name}").read().strip()
            if output:
                return set(map(int, output.split()))
            return set()
        except Exception as e:
            print(f"Erro ao obter processos: {e}")
            return set()

    def is_process_running(self, pid):
        """Verifica se um processo com o PID fornecido está em execução."""
        try:
            output = os.popen(f"ps -p {pid} | grep {pid}").read().strip()
            return output != ""
        except Exception as e:
            print(f"Erro ao verificar processo: {e}")
            return False

    def handle_signal(self, signum, frame):
        """Trata sinais de interrupção."""
        print("Monitoramento interrompido pelo usuário.")
        exit(0)

    def monitor(self, interval=5):
        """Monitora a abertura dos processos."""
        try:
            # Atraso inicial para evitar captura durante a inicialização
            time.sleep(self.initial_delay)
            while True:
                current_pids = self.get_process_pids()
                print(f"Active PIDs: {self.active_pids}")
                print(f"Current PIDs: {current_pids}")

                # Identifica os PIDs abertos recentemente
                new_pids = current_pids - self.active_pids
                print(f"New PIDs: {new_pids}")

                # Verifica se os novos PIDs estão realmente em execução
                for pid in new_pids:
                    if self.is_process_running(pid):
                        self.opens += 1
                        self.active_pids.add(pid)

                # Atualiza o conjunto de PIDs ativos
                self.active_pids = current_pids

                print(f"Aberturas: {self.opens}")
                print("-----------------------------------")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Monitoramento interrompido pelo usuário.")

# Uso do monitor:
if __name__ == "__main__":
    process_name = "oosplash"  # Altere para o nome do processo que deseja monitorar
    monitor = ProcessMonitor(process_name)

    # Registra tratadores de sinal para interrupção e término
    signal.signal(signal.SIGINT, monitor.handle_signal)
    signal.signal(signal.SIGTERM, monitor.handle_signal)

    monitor.monitor(interval=5)
