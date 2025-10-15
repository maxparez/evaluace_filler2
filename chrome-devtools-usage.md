# Chrome DevTools MCP - Použití a Workflow

## Konfigurace pro WSL2

V WSL2 je potřeba vytvořit wrapper script pro Chrome s `--no-sandbox` flagem:

```bash
cat > /tmp/chrome-wrapper.sh << 'EOF'
#!/bin/bash
/usr/bin/google-chrome --no-sandbox --disable-setuid-sandbox "$@"
EOF
chmod +x /tmp/chrome-wrapper.sh
```

Konfigurace v `~/.claude.json`:
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

## Workflow pro vyplňování formuláře

### 1. Otevření nové stránky
```javascript
mcp__chrome-devtools__new_page({
  url: "https://evaluace.opjak.cz/"
})
```

### 2. Vyplnění přístupového kódu
```javascript
// Najít pole v snapshot
mcp__chrome-devtools__take_snapshot()

// Vyplnit textové pole
mcp__chrome-devtools__fill({
  uid: "2_6",
  value: "00XcmS"
})

// Kliknout na tlačítko Pokračovat
mcp__chrome-devtools__click({
  uid: "3_7"
})
```

### 3. Zaškrtávání checkboxů
**DŮLEŽITÉ**: Po každém kliku se snapshot stává neplatný (stale), musíš vzít nový snapshot!

```javascript
// Vzít snapshot
mcp__chrome-devtools__take_snapshot()

// Kliknout na checkbox (toggle)
mcp__chrome-devtools__click({
  uid: "8_8"
})

// MUSÍŠ vzít nový snapshot před dalším klikem!
mcp__chrome-devtools__take_snapshot()
```

Checkboxy s `checked="true"` jsou zaškrtnuté, ostatní s `checked` bez true nejsou.

### 4. Hromadné vyplnění formuláře
Pro vyplnění více polí najednou:

```javascript
mcp__chrome-devtools__fill_form({
  elements: [
    {"uid": "11_12", "value": "38"},
    {"uid": "11_19", "value": "45"},
    {"uid": "11_21", "value": "33"},
    {"uid": "11_28", "value": "47"}
  ]
})
```

### 5. Navigace mezi stránkami
```javascript
// Kliknout na tlačítko Další
mcp__chrome-devtools__click({
  uid: "12_47"
})

// VŽDY po kliku vzít nový snapshot
mcp__chrome-devtools__take_snapshot()
```

### 6. JavaScript injection pro hromadné operace (DOPORUČENO!)
**Nejefektivnější metoda** - místo klikání na jednotlivé checkboxy použít JavaScript:

```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const topics = [
      "cizí jazyky/komunikace v cizím jazyce",
      "inkluze",
      "formativní hodnocení",
      "řízení organizace, leadership a řízení pedagogického procesu"
    ];

    // Nejdřív všechny odškrtnout
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    allCheckboxes.forEach(cb => {
      cb.checked = false;
      cb.dispatchEvent(new Event('change', { bubbles: true }));
    });

    // Pak zaškrtnout jen ty správné podle textu
    let checkedCount = 0;
    topics.forEach(topic => {
      allCheckboxes.forEach(checkbox => {
        const nextElement = checkbox.nextElementSibling || checkbox.parentElement?.nextElementSibling;
        if (nextElement && nextElement.textContent.trim().includes(topic.trim())) {
          checkbox.checked = true;
          checkbox.dispatchEvent(new Event('change', { bubbles: true }));
          checkedCount++;
        }
      });
    });

    return {
      totalCheckboxes: allCheckboxes.length,
      checkedCount: checkedCount
    };
  }`
})
```

**Výhody JavaScript přístupu:**
- ⚡ **Rychlost**: 1 volání místo desítek click operací
- 🎯 **Žádné stale snapshots**: Nemusíš řešit neplatné UID
- 💪 **Komplexní operace**: Můžeš dělat pokročilé DOM manipulace
- 🔍 **Lepší debugging**: Vrací JSON s výsledky

**Příklad - vyplnění formuláře čísly:**
```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const data = {
      "cizí jazyky/komunikace v cizím jazyce": { "2022/2023": 42, "2023/2024": 38 },
      "inkluze": { "2022/2023": 45, "2023/2024": 33 },
      "formativní hodnocení": { "2022/2023": 47, "2023/2024": 35 },
      "řízení organizace, leadership a řízení pedagogického procesu": { "2022/2023": 41, "2023/2024": 49 }
    };

    const inputs = document.querySelectorAll('input[type="text"], input[type="number"]');
    // ... logika pro vyplnění podle labelů a dat

    return { filled: inputs.length };
  }`
})
```

**Příklad - získání aktuálního stavu formuláře:**
```javascript
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return {
      checkedCheckboxes: Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.nextElementSibling?.textContent?.trim() || 'unknown'),
      filledInputs: Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'))
        .filter(input => input.value)
        .map(input => ({ label: input.placeholder || input.name, value: input.value }))
    };
  }`
})
```

## Mapování dat z HTML reportu na formulář

### HTML Report struktura (report_Otice_ZS_MS_733.html)
```html
<table>
  <thead>
    <tr>
      <th>vzdělávání_MŠ_1_I_4</th>
      <th>vzdělávání_ZŠ_1_II_7</th>
      <th>vzdělávání_ŠD_ŠK_1_V_1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>cizí jazyky/komunikace v cizím jazyce</td>
      <td>formativní hodnocení</td>
      <td>inkluze</td>
    </tr>
    <tr>
      <td>inkluze</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>formativní hodnocení</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>řízení organizace, leadership a řízení pedagogického procesu</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
```

### Formulář - Stránka 1: Výběr témat
Otázka: "V jaké oblasti jste realizovali vzdělávání pracovníků ve vzdělávání MŠ?"

Pro `vzdělávání_MŠ_1_I_4` zaškrtnout:
- cizí jazyky/komunikace v cizím jazyce ✓
- inkluze ✓
- formativní hodnocení ✓
- řízení organizace, leadership a řízení pedagogického procesu ✓

### Formulář - Stránka 2: Počet dětí podle školních roků
Pro každé vybrané téma vyplnit počty dětí:
- Školní rok 2022/2023
- Školní rok 2023/2024
- Školní rok 2024/2025
- Školní rok 2025/2026

## Dostupné DevTools funkce

### Console messages
```javascript
mcp__chrome-devtools__list_console_messages()
```

### Network requesty
```javascript
// Seznam všech requestů
mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["xhr", "fetch", "document"],
  pageSize: 50
})

// Detail konkrétního requestu
mcp__chrome-devtools__get_network_request({
  url: "https://example.com/api/endpoint"
})
```

### Performance monitoring
```javascript
// Spustit trace
mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})

// Zastavit trace a získat výsledky
mcp__chrome-devtools__performance_stop_trace()
```

## Klíčové body pro automatizaci

1. **JavaScript injection je král**: Používej `evaluate_script` pro hromadné operace místo jednotlivých kliků
2. **Snapshot management**: Pokud používáš click/fill API, vždy po změně stránky vzít nový snapshot
3. **UID mapování**: UID se mění po každém snapshot, nelze je cachovat
4. **Text matching**: Hledat checkboxy podle textu pomocí DOM manipulace v JS
5. **Sekce dotazníku**: Dotazník má více sekcí, každá s vlastním souborem otázek
6. **Validace**: Některá pole jsou povinná, musí být vyplněna nenulové číslo
7. **Event dispatching**: Po změně hodnot v JS vždy zavolat `dispatchEvent(new Event('change'))` pro triggering validace

## Plánovaná struktura projektu

```
/
├── data/
│   ├── report_Otice_ZS_MS_733.json    # Převedený z HTML
│   └── ...
├── src/
│   ├── parser.py                       # Parse HTML/JSON data
│   ├── navigator.py                    # Chrome DevTools navigation
│   ├── form_filler.py                  # Logic for filling forms
│   └── main.py                         # Main orchestration
└── chrome-devtools-usage.md            # Tato dokumentace
```
