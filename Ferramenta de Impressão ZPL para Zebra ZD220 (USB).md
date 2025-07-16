# Ferramenta de Impressão ZPL para Zebra ZD220 (USB)

Esta ferramenta Python permite ler múltiplos arquivos TXT contendo código ZPL e enviá-los sequencialmente para uma impressora Zebra ZD220 conectada via USB, com um intervalo configurável entre as impressões.

## Requisitos

- Python 3.x instalado.
- Biblioteca `python-escpos` instalada. Você pode instalá-la com pip:
  ```bash
  pip install python-escpos[usb]
  ;pip install win32printing
  ;pip install pywin32
  ```
- Sua impressora Zebra ZD220 conectada via USB.
- **IMPORTANTE**: Defina sua impressora termica como padrão

4.  **Prepare seus arquivos ZPL**: Crie uma pasta chamada `zpl_files` (ou o nome que você definir na variável `zpl_folder` no script) no mesmo diretório do script `zpl_printer.py`. Coloque todos os seus arquivos `.txt` contendo o código ZPL dentro desta pasta.

    **Exemplo de conteúdo de arquivo ZPL para etiqueta de 80x25mm (duas colunas):**
    ```zpl
    ^XA
    ^PW800
    ^LL250
    ^FO50,50^A0N,30,30^FDColuna 1 - Linha 1^FS
    ^FO50,80^A0N,30,30^FDColuna 1 - Linha 2^FS
    ^FO450,50^A0N,30,30^FDColuna 2 - Linha 1^FS
    ^FO450,80^A0N,30,30^FDColuna 2 - Linha 2^FS
    ^XZ
    ```
    *   `^PW800`: Define a largura da etiqueta em pontos (dots). Para 80mm, considerando 8 dots/mm, seria 640 dots. Ajuste conforme a resolução da sua impressora. O valor 800 foi usado como exemplo, mas pode precisar de ajuste fino.
    *   `^LL250`: Define o comprimento da etiqueta em pontos. Para 25mm, seria 200 dots. O valor 250 foi usado como exemplo.
    *   `^FOx,y`: Define a origem do campo (Field Origin) em coordenadas x,y.
    *   `^A0N,h,w`: Define a fonte (Font A, Normal, altura h, largura w).
    *   `^FDtext^FS`: Define os dados do campo (Field Data) e o final do campo (Field Separator).
    *   `^XZ`: Finaliza o formato ZPL.

5.  **Execute o script**: Abra um terminal ou prompt de comando, navegue até o diretório onde você salvou o `zpl_printer.py` e execute:
    ```bash
    python zpl_printer.py
    ```

    O script irá ler todos os arquivos `.txt` na pasta `zpl_files` (ou a pasta configurada), enviá-los para a impressora um por um e aguardar 4 segundos entre cada impressão.


### No Windows (Gerenciador de Dispositivos)

1.  Conecte sua impressora Zebra ZD220 ao computador via USB.
2.  Abra o **Gerenciador de Dispositivos** (você pode pesquisar por ele no menu Iniciar).
3.  Expanda as categorias até encontrar sua impressora. Ela pode estar em `Controladores USB (Universal Serial Bus)`, `Outros dispositivos` ou `Dispositivos de imagem`.
4.  Clique com o botão direito no nome da sua impressora (ex: `Zebra ZD220`) e selecione **Propriedades**.
5.  Vá para a aba **Detalhes**.
6.  No menu suspenso `Propriedade`, selecione **IDs de Hardware**.
7.  Você verá uma ou mais entradas no formato `USB\VID_XXXX&PID_YYYY...`.
    *   `XXXX` é o **VENDOR_ID** (ex: `0A5F`)
    *   `YYYY` é o **PRODUCT_ID** (ex: `0164`)
    Anote esses valores e use-os no script `zpl_printer.py`.

caso eu altere o script pra ter o vendor_id ou product_id

### No Linux (`lsusb`)

1.  Conecte sua impressora Zebra ZD220 ao computador via USB.
2.  Abra um terminal.
3.  Execute o comando:
    ```bash
    lsusb
    ```
4.  Procure por uma linha que se refira à sua impressora Zebra ZD220. Ela deve ser parecida com esta:
    ```
    Bus 001 Device 002: ID 0a5f:0001 Zebra Technologies Corp. ZD220
    ```
    *   `0a5f` é o **VENDOR_ID**.
    *   `0001` é o **PRODUCT_ID**.
    Anote esses valores e use-os no script `zpl_printer.py`.

## Solução de Problemas

-   **"Device not found"**: Verifique se o VENDOR_ID e PRODUCT_ID estão corretos no script e se a impressora está ligada e conectada via USB.
-   **Impressão em branco ou incorreta**: Verifique o código ZPL nos seus arquivos. Use um visualizador ZPL online (como Labelary.com) para validar seu código ZPL antes de imprimir.
