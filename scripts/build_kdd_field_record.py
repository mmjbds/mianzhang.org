from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT = ASSETS / "kdd2026-two-paper-field-record.webp"

WIDTH = 1200
PANEL_HEIGHT = 801
DIVIDER_HEIGHT = 10
DIVIDER_COLOR = (198, 163, 72)


def build_field_record() -> None:
    reflexbench = Image.open(ASSETS / "kdd2026-reflexbench.webp").convert("RGB")
    cognitive_immunity = Image.open(
        ASSETS / "kdd2026-cognitive-immunity.webp"
    ).convert("RGB")

    # Preserve the close poster view while leaving the cap and head fully visible.
    reflexbench_crop = reflexbench.crop((0, 70, 1500, 1071))
    reflexbench_panel = reflexbench_crop.resize(
        (WIDTH, PANEL_HEIGHT), Image.Resampling.LANCZOS
    )
    cognitive_panel = ImageOps.fit(
        cognitive_immunity,
        (WIDTH, PANEL_HEIGHT),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    canvas = Image.new(
        "RGB",
        (WIDTH, PANEL_HEIGHT * 2 + DIVIDER_HEIGHT),
        DIVIDER_COLOR,
    )
    canvas.paste(reflexbench_panel, (0, 0))
    canvas.paste(cognitive_panel, (0, PANEL_HEIGHT + DIVIDER_HEIGHT))
    canvas.save(OUTPUT, "WEBP", quality=88, method=6)


if __name__ == "__main__":
    build_field_record()
