# Code Block Language Fix Script
# Usage: Run in PowerShell: .\fix-code-blocks.ps1

$files = Get-ChildItem -Recurse -Include *.md | Where-Object { $_.FullName -notmatch 'node_modules' }

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Pattern 1: bash/shell commands
    $content = $content -replace '```\r?\n(npm |pip |python |node |git |docker |kubectl |yarn |pnpm )', '```bash`n$1'
    
    # Pattern 2: PowerShell commands
    $content = $content -replace '```\r?\n(\$|Get-|Set-|Write-|Remove-|New-|Invoke-|Select-Object )', '```powershell`n$1'
    
    # Pattern 3: JSON
    $content = $content -replace '```\r?\n(\{)', '```json`n$1'
    
    # Pattern 4: JavaScript/TypeScript
    $content = $content -replace '```\r?\n(const |let |var |function |import |export |class |interface )', '```javascript`n$1'
    
    # Pattern 5: Python
    $content = $content -replace '```\r?\n(def |class |import |from |print\(|if __name__ )', '```python`n$1'
    
    # Pattern 6: TypeScript specific
    $content = $content -replace '```\r?\n(interface |type |enum )', '```typescript`n$1'
    
    # Pattern 7: YAML
    $content = $content -replace '```\r?\n([a-zA-Z_]+:\s)', '```yaml`n$1'
    
    # Pattern 8: Tables/plain text
    $content = $content -replace '```\r?\n(\|.*\|)', '```text`n$1'
    
    # Pattern 9: Directory trees
    $content = $content -replace '```\r?\n([a-zA-Z0-9/_-]+\r?\n[│├└─])', '```text`n$1'
    
    if ($content -ne $original) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "Fixed: $($file.Name)"
    }
}

Write-Host "Done!"
