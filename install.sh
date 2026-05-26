#!/usr/bin/env bash
# ============================================================
# Lumtext — Quraşdırma skripti (Linux)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     LUMTEXT — Quraşdırma            ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Python check
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 tapılmadı. Qurun: sudo apt install python3"
    exit 1
fi

echo "✓ Python3: $(python3 --version)"

# pip
if ! command -v pip3 &>/dev/null; then
    echo "pip3 quraşdırılır..."
    sudo apt-get install -y python3-pip
fi

# System deps (xclip — only needed on Linux for PRIMARY selection)
echo ""
echo "Sistem paketləri yoxlanılır..."
for pkg in xclip; do
    if ! command -v $pkg &>/dev/null; then
        echo "  → $pkg quraşdırılır..."
        sudo apt-get install -y $pkg 2>/dev/null || echo "  ⚠ $pkg quraşdırıla bilmədi"
    else
        echo "  ✓ $pkg mövcuddur"
    fi
done

# Qt deps for PyQt6
echo ""
echo "PyQt6 sistem asılılıqları..."
sudo apt-get install -y \
    libxcb-cursor0 libxcb-xinerama0 \
    libxkbcommon-x11-0 libgl1 \
    python3-dev 2>/dev/null || true

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
echo "  ✓ Paketlər quraşdırıldı ($(pip list 2>/dev/null | grep -c '^[a-zA-Z]') ədəd)"

# Create __init__.py files
touch core/__init__.py ui/__init__.py 2>/dev/null || true

# Create desktop launcher
echo ""
echo "Desktop qısayolu yaradılır..."
DESKTOP_FILE="$HOME/.local/share/applications/lumtext.desktop"
mkdir -p "$HOME/.local/share/applications"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Lumtext
Comment=AI-powered text processing tool
Exec=$SCRIPT_DIR/run.sh
Icon=$SCRIPT_DIR/ui/app_icon.png
Terminal=false
Categories=Utility;TextTool;
StartupNotify=false
X-GNOME-Autostart-enabled=false
EOF
chmod +x "$DESKTOP_FILE"
echo "  ✓ Desktop qısayolu: $DESKTOP_FILE"

# Create run script
cat > "$SCRIPT_DIR/run.sh" << EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR"
source venv/bin/activate
exec python3 main.py "\$@"
EOF
chmod +x "$SCRIPT_DIR/run.sh"

# Autostart
echo ""
read -p "Sistemlə birlikdə avtomatik başlasın? (y/n): " autostart
if [[ "$autostart" == "y" || "$autostart" == "Y" ]]; then
    AUTOSTART_DIR="$HOME/.config/autostart"
    mkdir -p "$AUTOSTART_DIR"
    cp "$DESKTOP_FILE" "$AUTOSTART_DIR/lumtext.desktop"
    sed -i 's/X-GNOME-Autostart-enabled=false/X-GNOME-Autostart-enabled=true/' "$AUTOSTART_DIR/lumtext.desktop"
    echo "  ✓ Autostart aktiv edildi"
fi

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Quraşdırma tamamlandı! ✓           ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "  Linux:     ./run.sh"
echo "  macOS:     python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 main.py"
echo "  Windows:   python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt && python main.py"
echo ""
echo "  İlk açılışda Ayarlar → API açarınızı daxil edin"
echo ""
