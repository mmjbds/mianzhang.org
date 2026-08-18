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

    if reflexbench.width < WIDTH or reflexbench.height < PANEL_HEIGHT + 70:
        raise ValueError(
            f"ReflexBench source is too small: {reflexbench.width}x{reflexbench.height}"
        )

    # Keep the full source width and shift the crop upward so the head remains intact.
    reflexbench_panel = reflexbench.crop((0, 70, WIDTH, PANEL_HEIGHT + 70))
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
