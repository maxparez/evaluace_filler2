# Lokální instalace Chrome DevTools MCP pro projekt

## Proč lokální instalace?

Lokální instalace MCP serveru znamená, že bude dostupný **pouze v tomto projektu**, ne ve všech projektech globálně. To je užitečné když:
- Pracuješ na více projektech a ne všechny potřebují Chrome automation
- Chceš mít pro každý projekt specifickou konfiguraci
- Chceš sdílet konfiguraci s týmem přes git

## Instalace

### 1. Přidání MCP serveru lokálně do projektu

```bash
# Přejdi do adresáře projektu
cd /root/chrome_test

# Přidej MCP server lokálně (do .claude.json v projektu)
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

Tento příkaz vytvoří/upraví `.claude.json` **v aktuálním adresáři projektu**.

### 2. Konfigurace pro WSL2

Po přidání MCP serveru musíš upravit konfiguraci pro WSL2:

```bash
# Vytvoř Chrome wrapper script
cat > /tmp/chrome-wrapper.sh << 'EOF'
#!/bin/bash
/usr/bin/google-chrome --no-sandbox --disable-setuid-sandbox "$@"
EOF
chmod +x /tmp/chrome-wrapper.sh
```

### 3. Ruční úprava `.claude.json` v projektu

Otevři `.claude.json` v kořenovém adresáři projektu a najdi sekci `mcpServers`. Uprav ji takto:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated",
        "--headless",
        "--executablePath=/tmp/chrome-wrapper.sh"
      ],
      "env": {
        "DEBUG": "*"
      }
    }
  }
}
```

### 4. Restart Claude CLI

Pro načtení nové konfigurace musíš restartovat Claude CLI session:
- Ukonči aktuální session (exit nebo Ctrl+D)
- Spusť Claude CLI znovu v adresáři projektu

```bash
cd /root/chrome_test
claude
```

## Ověření instalace

Zkontroluj, že MCP server běží:

```bash
# V Claude CLI zkus:
# (použij nějaký MCP příkaz, např. otevření stránky)
```

Pokud funguje, uvidíš že Chrome DevTools MCP je dostupný jen v tomto projektu.

## Struktura projektu

```
/root/chrome_test/
├── .claude.json              # Lokální konfigurace MCP (NECOMMITOVAT do git!)
├── chrome-devtools-install.md # Tento návod
├── chrome-devtools-usage.md   # Návod na použití
├── report_Otice_ZS_MS_733.html
└── ...
```

## Gitignore

**DŮLEŽITÉ**: Přidej `.claude.json` do `.gitignore` pokud obsahuje tokeny nebo citlivá data:

```bash
echo ".claude.json" >> .gitignore
```

Nebo commituj `.claude.json` ale bez citlivých dat (tokens, passwords apod.).

## Rozdíl mezi lokální a globální instalací

### Lokální instalace (pro tento projekt)
```bash
cd /root/chrome_test
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
# Vytvoří/upraví: /root/chrome_test/.claude.json
```

MCP server bude dostupný **pouze když spustíš Claude CLI v tomto adresáři**.

### Globální instalace (pro všechny projekty)
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest --global
# Upraví: ~/.claude.json
```

MCP server bude dostupný **ve všech projektech**.

## Odebrání MCP serveru

Pokud už MCP server nepotřebuješ:

```bash
# Lokální odebrání (pouze z tohoto projektu)
cd /root/chrome_test
claude mcp remove chrome-devtools

# Globální odebrání (ze všech projektů)
claude mcp remove chrome-devtools --global
```

## Troubleshooting

### MCP server není dostupný
- Ujisti se, že jsi v správném adresáři projektu
- Zkontroluj že existuje `.claude.json` v aktuálním adresáři
- Restartuj Claude CLI session

### Chrome nefunguje ve WSL2
- Zkontroluj že existuje `/tmp/chrome-wrapper.sh` a má execute práva
- Ověř že Chrome je nainstalovaný: `google-chrome --version`
- Zkontroluj konfiguraci `--executablePath` v `.claude.json`

### Chci použít jiný Chrome channel (canary, beta)
Přidej do args v `.claude.json`:
```json
"args": [
  "chrome-devtools-mcp@latest",
  "--isolated",
  "--headless",
  "--channel=canary",
  "--executablePath=/tmp/chrome-wrapper.sh"
]
```
