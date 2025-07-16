import os
import time
import win32print


class ZebraZD220:
    def __init__(self):
        self.max_retries = 3
        self.retry_delay = 2

    def print_zpl_file(self, file_path, is_separator=False):
        """Imprime um arquivo ZPL ou etiqueta em branco"""
        try:
            if is_separator:
                zpl_content = self._create_blank_label()
                print("\nImprimindo etiqueta em branco como separador...")
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    zpl_content = f.read().strip()
                print(f"\nProcessando: {os.path.basename(file_path)}")

            for attempt in range(1, self.max_retries + 1):
                method_name = "Spooler do Windows"
                print(f"Tentativa {attempt}: {method_name}...")

                try:
                    if self._print_via_spooler(zpl_content):
                        print("✓ Impresso com sucesso!")
                        return True
                except Exception as e:
                    print(f"⚠️ Falha: {str(e)}")
                    time.sleep(self.retry_delay)

            print("✖ Todas as tentativas falharam")
            return False

        except Exception as e:
            print(f"Erro ao processar arquivo: {str(e)}")
            return False

    def _print_via_spooler(self, zpl_data):
        """Impressão via spooler do Windows"""
        try:
            printer_name = win32print.GetDefaultPrinter()
            if not printer_name:
                raise ValueError("Nenhuma impressora padrão configurada")

            hprinter = win32print.OpenPrinter(printer_name)
            if not hprinter:
                raise ValueError("Não foi possível acessar a impressora")

            try:
                job_info = ("ZPL Print", None, "RAW")
                job_id = win32print.StartDocPrinter(hprinter, 1, job_info)
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, zpl_data.encode('utf-8'))
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
                return True
            finally:
                win32print.ClosePrinter(hprinter)

        except Exception as e:
            raise RuntimeError(f"Spooler: {str(e)}")

    def _create_blank_label(self):
        """Cria ZPL para uma etiqueta em branco"""
        return """
        ^XA
        ^FO20,20^GB300,600,2^FS
        ^FO25,25^A0N, 30, 30^FB300,2,2,C^FDETIQUETA SEPARADORA^FS
        ^XZ
        """


def main():
    print("=== Sistema de Impressão Zebra ZD220 ===")
    print("Configuração recomendada:")
    print("1. Configurar a impressora Zebra como padrão no Windows")
    print("2. Executar como Administrador\n")

    printer = ZebraZD220()
    zpl_folder = "Coloque seus arquivos AQUI!"

    if not os.path.exists(zpl_folder):
        os.makedirs(zpl_folder)
        print(f"Diretório '{zpl_folder}' criado. Adicione arquivos .txt com ZPL.")
        return

    success_count = 0
    file_count = 0
    file_list = [f for f in os.listdir(zpl_folder) if f.lower().endswith('.txt')]

    for filename in sorted(file_list):
        file_count += 1
        file_path = os.path.join(zpl_folder, filename)

        if printer.print_zpl_file(file_path):
            success_count += 1
            # Imprime etiqueta separadora após cada impressão bem-sucedida
            printer.print_zpl_file(None, is_separator=True)

    print(f"\n✔ Concluído! {success_count}/{file_count} arquivos impressos com sucesso.")


if __name__ == "__main__":
    main()