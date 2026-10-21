"""Deterministic four-transformation helper for the Social QuickRead pilot.

This module is an EXTRA sidecar.  It does not implement the full Zhongzhou
temporal inference engine and does not mutate Knowledge/Product canonical state.

Its job is deliberately narrow:

1. map a decade/year heavenly stem to the four transformed stars;
2. locate those stars in the natal chart when a star->palace mapping is supplied;
3. expose simple cross-layer structural interactions for manual/source-grounded
   interpretation.

It MUST NOT turn 化禄/化权/化科/化忌 into generic good/bad scores or invent
events.  Semantic interpretation remains source-backed and context dependent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable, Mapping


class TemporalLayer(str, Enum):
    NATAL = "NATAL"
    DECADE = "DECADE"
    YEAR = "YEAR"


class Mutagen(str, Enum):
    LU = "禄"
    QUAN = "权"
    KE = "科"
    JI = "忌"


class TemporalInputSource(str, Enum):
    """Where the structural temporal facts came from."""

    MANUAL_SCREENSHOT = "MANUAL_SCREENSHOT"
    VALIDATED_P1_RUNTIME = "VALIDATED_P1_RUNTIME"


HEAVENLY_STEMS = tuple("甲乙丙丁戊己庚辛壬癸")


# Zhongzhou ten-stem transformation table.
# Order is always 禄 / 权 / 科 / 忌.
TEN_STEM_TRANSFORMATIONS: dict[str, tuple[str, str, str, str]] = {
    "甲": ("廉贞", "破军", "武曲", "太阳"),
    "乙": ("天机", "天梁", "紫微", "太阴"),
    "丙": ("天同", "天机", "文昌", "廉贞"),
    "丁": ("太阴", "天同", "天机", "巨门"),
    "戊": ("贪狼", "太阴", "右弼", "天机"),
    "己": ("武曲", "贪狼", "天梁", "文曲"),
    "庚": ("太阳", "武曲", "太阴", "天同"),
    "辛": ("巨门", "太阳", "文曲", "文昌"),
    "壬": ("天梁", "紫微", "左辅", "武曲"),
    "癸": ("破军", "巨门", "太阴", "贪狼"),
}


@dataclass(frozen=True)
class TransformationMark:
    layer: TemporalLayer
    stem: str
    star: str
    mutagen: Mutagen
    palace: str = ""

    def validate(self) -> None:
        if self.stem not in TEN_STEM_TRANSFORMATIONS and self.layer is not TemporalLayer.NATAL:
            raise ValueError(f"unsupported heavenly stem: {self.stem}")
        if not self.star.strip():
            raise ValueError("TransformationMark.star is required")


class InteractionType(str, Enum):
    SAME_STAR_SAME_MUTAGEN = "SAME_STAR_SAME_MUTAGEN"
    SAME_STAR_CROSS_MUTAGEN = "SAME_STAR_CROSS_MUTAGEN"
    NATAL_STAR_REACTIVATED = "NATAL_STAR_REACTIVATED"
    SAME_PALACE_MULTI_LAYER = "SAME_PALACE_MULTI_LAYER"


@dataclass(frozen=True)
class TemporalInteraction:
    interaction_type: InteractionType
    star: str = ""
    palace: str = ""
    layers: tuple[str, ...] = ()
    mutagens: tuple[str, ...] = ()

    def validate(self) -> None:
        if len(set(self.layers)) != len(self.layers):
            raise ValueError("TemporalInteraction.layers must be unique")


@dataclass(frozen=True)
class Temporal4HSnapshot:
    """Structural snapshot only; contains no event-level interpretation."""

    decade_stem: str
    year_stem: str
    decade_marks: tuple[TransformationMark, ...]
    year_marks: tuple[TransformationMark, ...]
    natal_marks: tuple[TransformationMark, ...] = ()
    interactions: tuple[TemporalInteraction, ...] = ()
    input_source: TemporalInputSource = TemporalInputSource.MANUAL_SCREENSHOT
    runtime_run_id: str = ""
    schema_version: str = "0.1"

    def validate(self) -> None:
        if self.decade_stem not in TEN_STEM_TRANSFORMATIONS:
            raise ValueError(f"unsupported decade stem: {self.decade_stem}")
        if self.year_stem not in TEN_STEM_TRANSFORMATIONS:
            raise ValueError(f"unsupported year stem: {self.year_stem}")
        if self.input_source is TemporalInputSource.VALIDATED_P1_RUNTIME and not self.runtime_run_id.strip():
            raise ValueError("VALIDATED_P1_RUNTIME requires runtime_run_id")
        for row in (*self.natal_marks, *self.decade_marks, *self.year_marks):
            row.validate()
        for row in self.interactions:
            row.validate()

    def to_dict(self) -> dict:
        self.validate()
        data = asdict(self)
        data["input_source"] = self.input_source.value
        for key in ("natal_marks", "decade_marks", "year_marks"):
            data[key] = [
                {
                    **row,
                    "layer": row["layer"].value if isinstance(row["layer"], TemporalLayer) else row["layer"],
                    "mutagen": row["mutagen"].value if isinstance(row["mutagen"], Mutagen) else row["mutagen"],
                }
                for row in data[key]
            ]
        data["interactions"] = [
            {
                **row,
                "interaction_type": (
                    row["interaction_type"].value
                    if isinstance(row["interaction_type"], InteractionType)
                    else row["interaction_type"]
                ),
            }
            for row in data["interactions"]
        ]
        return data


def stem_for_gregorian_year(year: int) -> str:
    """Return the heavenly stem for a Gregorian calendar year.

    This is calendar arithmetic only; it does not decide the Zi Wei year-boundary
    convention for a birth/event timestamp.  The caller must already have chosen
    the target civil year under the project's temporal convention.
    """

    value = int(year)
    if value < 1:
        raise ValueError("Gregorian year must be >= 1")
    return HEAVENLY_STEMS[(value - 4) % 10]


def transformations_for_stem(
    stem: str,
    *,
    layer: TemporalLayer,
    star_to_palace: Mapping[str, str] | None = None,
) -> tuple[TransformationMark, ...]:
    """Return deterministic 禄权科忌 marks for one heavenly stem."""

    value = str(stem or "").strip()
    if value not in TEN_STEM_TRANSFORMATIONS:
        raise ValueError(f"unsupported heavenly stem: {value}")
    stars = TEN_STEM_TRANSFORMATIONS[value]
    mutagens = (Mutagen.LU, Mutagen.QUAN, Mutagen.KE, Mutagen.JI)
    palaces = star_to_palace or {}
    rows = tuple(
        TransformationMark(
            layer=layer,
            stem=value,
            star=star,
            mutagen=mutagen,
            palace=str(palaces.get(star, "") or "").strip(),
        )
        for star, mutagen in zip(stars, mutagens)
    )
    for row in rows:
        row.validate()
    return rows


def normalize_natal_marks(
    natal_transformations: Mapping[str, str] | Iterable[tuple[str, str]] | None,
    *,
    star_to_palace: Mapping[str, str] | None = None,
) -> tuple[TransformationMark, ...]:
    """Normalize already-known natal transformations.

    The caller supplies the natal facts.  This helper intentionally does not infer
    the natal stem from birth data.
    """

    if not natal_transformations:
        return ()
    items = (
        natal_transformations.items()
        if isinstance(natal_transformations, Mapping)
        else natal_transformations
    )
    reverse = {
        "禄": Mutagen.LU,
        "化禄": Mutagen.LU,
        "权": Mutagen.QUAN,
        "化权": Mutagen.QUAN,
        "科": Mutagen.KE,
        "化科": Mutagen.KE,
        "忌": Mutagen.JI,
        "化忌": Mutagen.JI,
    }
    palaces = star_to_palace or {}
    rows: list[TransformationMark] = []
    seen: set[tuple[str, str]] = set()
    for star, raw_mutagen in items:
        star_name = str(star or "").strip()
        label = str(raw_mutagen or "").strip()
        if label not in reverse:
            raise ValueError(f"unsupported natal mutagen: {label}")
        key = (star_name, reverse[label].value)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            TransformationMark(
                layer=TemporalLayer.NATAL,
                stem="",
                star=star_name,
                mutagen=reverse[label],
                palace=str(palaces.get(star_name, "") or "").strip(),
            )
        )
    return tuple(rows)


def detect_interactions(
    *,
    natal_marks: Iterable[TransformationMark] = (),
    decade_marks: Iterable[TransformationMark],
    year_marks: Iterable[TransformationMark],
) -> tuple[TemporalInteraction, ...]:
    """Detect only literal cross-layer structural overlaps.

    No 三方四正/opposition geometry is inferred here.  That belongs to a later
    relation-aware temporal resolver.
    """

    natal = tuple(natal_marks)
    decade = tuple(decade_marks)
    year = tuple(year_marks)
    rows = (*natal, *decade, *year)
    out: list[TemporalInteraction] = []

    by_star: dict[str, list[TransformationMark]] = {}
    for row in rows:
        by_star.setdefault(row.star, []).append(row)

    for star, marks in sorted(by_star.items()):
        layers = tuple(dict.fromkeys(item.layer.value for item in marks))
        if len(layers) < 2:
            continue
        mutagens = tuple(dict.fromkeys(item.mutagen.value for item in marks))
        interaction_type = (
            InteractionType.SAME_STAR_SAME_MUTAGEN
            if len(mutagens) == 1
            else InteractionType.SAME_STAR_CROSS_MUTAGEN
        )
        out.append(
            TemporalInteraction(
                interaction_type=interaction_type,
                star=star,
                palace=next((item.palace for item in marks if item.palace), ""),
                layers=layers,
                mutagens=mutagens,
            )
        )
        if any(item.layer is TemporalLayer.NATAL for item in marks):
            out.append(
                TemporalInteraction(
                    interaction_type=InteractionType.NATAL_STAR_REACTIVATED,
                    star=star,
                    palace=next((item.palace for item in marks if item.palace), ""),
                    layers=layers,
                    mutagens=mutagens,
                )
            )

    by_palace: dict[str, list[TransformationMark]] = {}
    for row in rows:
        if row.palace:
            by_palace.setdefault(row.palace, []).append(row)
    for palace, marks in sorted(by_palace.items()):
        layers = tuple(dict.fromkeys(item.layer.value for item in marks))
        if len(layers) < 2:
            continue
        out.append(
            TemporalInteraction(
                interaction_type=InteractionType.SAME_PALACE_MULTI_LAYER,
                palace=palace,
                layers=layers,
                mutagens=tuple(dict.fromkeys(item.mutagen.value for item in marks)),
            )
        )

    # Stable de-duplication.
    unique: list[TemporalInteraction] = []
    seen: set[tuple] = set()
    for row in out:
        key = (
            row.interaction_type.value,
            row.star,
            row.palace,
            row.layers,
            row.mutagens,
        )
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return tuple(unique)


def build_temporal_4h_snapshot(
    *,
    decade_stem: str,
    year_stem: str,
    star_to_palace: Mapping[str, str],
    natal_transformations: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
    input_source: TemporalInputSource = TemporalInputSource.MANUAL_SCREENSHOT,
    runtime_run_id: str = "",
) -> Temporal4HSnapshot:
    """Build a deterministic structural snapshot for manual QuickRead use."""

    decade_marks = transformations_for_stem(
        decade_stem,
        layer=TemporalLayer.DECADE,
        star_to_palace=star_to_palace,
    )
    year_marks = transformations_for_stem(
        year_stem,
        layer=TemporalLayer.YEAR,
        star_to_palace=star_to_palace,
    )
    natal_marks = normalize_natal_marks(
        natal_transformations,
        star_to_palace=star_to_palace,
    )
    interactions = detect_interactions(
        natal_marks=natal_marks,
        decade_marks=decade_marks,
        year_marks=year_marks,
    )
    snapshot = Temporal4HSnapshot(
        decade_stem=str(decade_stem).strip(),
        year_stem=str(year_stem).strip(),
        decade_marks=decade_marks,
        year_marks=year_marks,
        natal_marks=natal_marks,
        interactions=interactions,
        input_source=input_source,
        runtime_run_id=runtime_run_id,
    )
    snapshot.validate()
    return snapshot


def quickread_temporal_payload(snapshot: Temporal4HSnapshot) -> dict:
    """Return the narrow structural payload allowed into manual interpretation."""

    snapshot.validate()
    return {
        "mode": "social_quickread_temporal_4h_v0.1",
        "schema_version": snapshot.schema_version,
        "input_source": snapshot.input_source.value,
        "runtime_run_id": snapshot.runtime_run_id or None,
        "decade_stem": snapshot.decade_stem,
        "year_stem": snapshot.year_stem,
        "natal_marks": [
            {
                "star": row.star,
                "mutagen": row.mutagen.value,
                "palace": row.palace or None,
            }
            for row in snapshot.natal_marks
        ],
        "decade_marks": [
            {
                "star": row.star,
                "mutagen": row.mutagen.value,
                "palace": row.palace or None,
            }
            for row in snapshot.decade_marks
        ],
        "year_marks": [
            {
                "star": row.star,
                "mutagen": row.mutagen.value,
                "palace": row.palace or None,
            }
            for row in snapshot.year_marks
        ],
        "interactions": [
            {
                "type": row.interaction_type.value,
                "star": row.star or None,
                "palace": row.palace or None,
                "layers": list(row.layers),
                "mutagens": list(row.mutagens),
            }
            for row in snapshot.interactions
        ],
        "interpretation_contract": {
            "structural_facts_only": True,
            "generic_good_bad_scoring_forbidden": True,
            "event_inference_forbidden_without_source_backed_rule": True,
            "three_harmony_four_directions_not_inferred_here": True,
            "natal_reactivation_is_same_star_only_in_v0_1": True,
        },
    }



def build_temporal_4h_series(
    *,
    decade_stem: str,
    years: Iterable[int],
    star_to_palace: Mapping[str, str],
    natal_transformations: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
    input_source: TemporalInputSource = TemporalInputSource.MANUAL_SCREENSHOT,
    runtime_run_ids: Mapping[int, str] | None = None,
) -> tuple[tuple[int, Temporal4HSnapshot], ...]:
    """Build several year snapshots under one already-resolved decade stem.

    If the requested years cross a decade boundary, the caller must split the
    request and supply the correct decade stem for each segment.
    """

    ids = runtime_run_ids or {}
    rows: list[tuple[int, Temporal4HSnapshot]] = []
    seen: set[int] = set()
    for raw_year in years:
        year = int(raw_year)
        if year in seen:
            continue
        seen.add(year)
        rows.append(
            (
                year,
                build_temporal_4h_snapshot(
                    decade_stem=decade_stem,
                    year_stem=stem_for_gregorian_year(year),
                    star_to_palace=star_to_palace,
                    natal_transformations=natal_transformations,
                    input_source=input_source,
                    runtime_run_id=str(ids.get(year, "") or ""),
                ),
            )
        )
    if not rows:
        raise ValueError("build_temporal_4h_series requires at least one year")
    return tuple(rows)
