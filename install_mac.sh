#!/usr/bin/env bash
# ============================================================
# Lumtext — Quraşdırma skripti (macOS)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     LUMTEXT — macOS Install         ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Python check
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 tapılmadı."
    echo "   https://python.org/downloads/ saytından yükləyin"
    exit 1
fi

echo "✓ Python3: $(python3 --version)"

# Xcode Command Line Tools (needed for some builds)
if ! xcode-select -p &>/dev/null 2>&1; then
    echo ""
    echo "Xcode Command Line Tools quraşdırılır..."
    xcode-select --install 2>/dev/null || true
    echo "⚠ Zəhmət olmasa yuxarıdakı pəncərədə 'Install' düyməsini basın,"
    echo "  bitdikdən sonra bu skripti yenidən çalışdırın."
    exit 0
fi

# Homebrew check (optional, for xclip alternative)
if ! command -v brew &>/dev/null; then
    echo ""
    echo "⚠ Homebrew tapılmadı (ixtiyari)."
    echo "  Quraşdırmaq üçün: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

# Virtual environment
echo ""
echo "Virtual mühit yaradılır..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install Python packages
echo ""
echo "Python paketləri quraşdırılır..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "  ✓ Paketlər quraşdırıldı"

touch core/__init__.py ui/__init__.py 2>/dev/null || true

# Create launch script
LAUNCHER="$SCRIPT_DIR/run_mac.command"
cat > "$LAUNCHER" << EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR"
source venv/bin/activate
exec python3 main.py
EOF
chmod +x "$LAUNCHER"
echo "  ✓ Launcher: $LAUNCHER"

# Create macOS .app bundle (optional)
APP_DIR="$SCRIPT_DIR/Lumtext.app"
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "$APP_DIR/Contents/MacOS"
    mkdir -p "$APP_DIR/Contents/Resources"

    cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Lumtext</string>
    <key>CFBundleIdentifier</key>
    <string>com.lumtext.app</string>
    <key>CFBundleName</key>
    <string>Lumtext</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
</dict>
</plist>
EOF

    cat > "$APP_DIR/Contents/MacOS/Lumtext" << EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR"
source venv/bin/activate
exec python3 main.py
EOF
    chmod +x "$APP_DIR/Contents/MacOS/Lumtext"
    echo "  ✓ .app bundle: $APP_DIR"
fi

# macOS Accessibility permission reminder
echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Quraşdırma tamamlandı! ✓           ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "  İşə salmaq:"
echo "    open run_mac.command"
echo "    (və ya Lumtext.app ikonuna 2 klik)"
echo ""
echo "  ⚠  Vacib: Sistem Tərcihləri →"
echo "     Təhlükəsizlik & Məxfilik →"
echo "     Girişəl → Klaviatura →"
echo "     terminal/run_mac.command əlavə edin"
echo "     (qısayol işləməsi üçün)"
echo ""
echo "  İlk açılışda Ayarlar → API açarınızı daxil edin"
echo ""
