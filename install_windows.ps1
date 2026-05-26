<#
.SYNOPSIS
    Lumtext — Windows Quraşdırma skripti
.DESCRIPTION
    Virtual mühit yaradır, asılılıqları quraşdırır, işə salma qısayolu yaradır.
#>

Write-Host ""
Write-Host "╔══════════════════════════════════════╗"
Write-Host "║   LUMTEXT — Windows Install         ║"
Write-Host "╚══════════════════════════════════════╝"
Write-Host ""

# Python check
try {
    $py = Get-Command python -ErrorAction Stop
    Write-Host "✓ Python: $($py.Path)"
} catch {
    Write-Host "❌ Python tapılmadı."
    Write-Host "   https://python.org/downloads/ saytından yükləyin"
    Write-Host "   Quraşdırarkən 'Add Python to PATH' seçin!"
    exit 1
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

# Virtual environment
Write-Host ""
Write-Host "Virtual mühit yaradılır..."
if (-not (Test-Path "venv")) {
    python -m venv venv
}
$venvActivate = Join-Path $SCRIPT_DIR "venv\Scripts\Activate.ps1"

# Install packages
Write-Host ""
Write-Host "Python paketləri quraşdırılır..."
& python -m pip install --upgrade pip -q
& pip install -r requirements.txt -q
Write-Host "  ✓ Paketlər quraşdırıldı"

# Create __init__.py files
New-Item -ItemType File -Path "core\__init__.py" -Force | Out-Null
New-Item -ItemType File -Path "ui\__init__.py" -Force | Out-Null

# Create launcher batch file
$batContent = @"
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py
pause
"@
Set-Content -Path "run_lumtext.bat" -Value $batContent
Write-Host "  ✓ Launcher: run_lumtext.bat"

# Create PowerShell launcher
$psContent = @"
Set-Location "$SCRIPT_DIR"
& "$venvActivate"
python main.py
"@
Set-Content -Path "run_lumtext.ps1" -Value $psContent
Write-Host "  ✓ Launcher: run_lumtext.ps1"

# Desktop shortcut (optional)
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Lumtext.lnk"
if (-not (Test-Path $shortcutPath)) {
    try {
        $wshell = New-Object -ComObject WScript.Shell
        $shortcut = $wshell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = Join-Path $SCRIPT_DIR "run_lumtext.bat"
        $shortcut.WorkingDirectory = $SCRIPT_DIR
        $shortcut.Description = "Lumtext — AI text processing"
        $shortcut.Save()
        Write-Host "  ✓ Desktop qısayolu yaradıldı"
    } catch {
        Write-Host "  ⚠ Desktop qısayolu yaradıla bilmədi"
    }
}

Write-Host ""
Write-Host "╔══════════════════════════════════════╗"
Write-Host "║   Quraşdırma tamamlandı! ✓           ║"
Write-Host "╚══════════════════════════════════════╝"
Write-Host ""
Write-Host "  İşə salmaq:"
Write-Host "    run_lumtext.bat (və ya run_lumtext.ps1)"
Write-Host "    (və ya Desktop Lumtext qısayolu)"
Write-Host ""
Write-Host "  ⚠ Qısayol üçün:"
Write-Host "    AutoHotkey və ya PowerToys ilə"
Write-Host "    Ctrl+Shift+Space → run_lumtext.bat"
Write-Host ""
Write-Host "  İlk açılışda Ayarlar → API açarınızı daxil edin"
Write-Host ""
