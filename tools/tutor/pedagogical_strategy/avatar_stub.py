"""Avatar stub interface — placeholder for future avatar implementation.

This module defines the interface contract for visible tutor avatars.
No avatar logic is implemented. No AI generation. No real-person likenesses.
Avatars are presentation-layer only — they carry zero cognitive authority.

The stub is safe to import and call at all times. All functions are no-ops
that return documented sentinel values. is_avatar_implemented() always
returns False until explicit activation.

Governance invariants
---------------------
  Avatars may only map to visible roles in ALLOWED_VISIBLE_ROLES.
  No avatar may carry a real person name, likeness, or examiner authority.
  This stub must never raise — callers must be able to depend on it safely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from tools.tutor.pedagogical_strategy.profiles import ALLOWED_VISIBLE_ROLES


_NOT_IMPLEMENTED_STATUS = "not_implemented"

# Avatar interface table — maps avatar_id → visible_role.
# Intentionally empty at stub phase. Keys and values must only reference
# roles in ALLOWED_VISIBLE_ROLES when populated.
AVATAR_INTERFACE: dict[str, str] = {}


@dataclass
class AvatarStub:
    """Stub representation of a tutor avatar.

    Fields
    ------
    character_id : str
        The avatar/character identifier.
    visual_direction : str
        Brief description for future avatar generation (style/mood/setting).
        Must not reference real persons.
    status : str
        Always "not_implemented" until explicit activation.
    """

    character_id: str
    visual_direction: str = ""
    status: str = field(default=_NOT_IMPLEMENTED_STATUS)


def get_avatar_stub(character_id: str) -> AvatarStub:
    """Return an AvatarStub for the given character_id.

    Never raises. Returns a stub with status="not_implemented" regardless
    of whether character_id is known or unknown.
    """
    try:
        # Import here to avoid circular dependency risk during stub phase
        from tools.tutor.pedagogical_strategy.character_resolver import get_character
        char = get_character(character_id)
        visual_direction = char.get("visual_direction", "")
    except Exception:  # noqa: BLE001
        visual_direction = ""

    return AvatarStub(
        character_id=str(character_id) if character_id is not None else "",
        visual_direction=visual_direction,
        status=_NOT_IMPLEMENTED_STATUS,
    )


def is_avatar_implemented(character_id: str) -> bool:
    """Return True if the avatar for the given character_id is implemented.

    Always returns False — no avatar implementation exists yet.
    This function is a readiness gate: callers must check it before
    attempting to render any avatar.
    """
    return False


def resolve_avatar_to_role(avatar_id: str) -> Optional[str]:
    """Return the visible_role for a given avatar_id, or None if unknown.

    Return value is always in ALLOWED_VISIBLE_ROLES or None — never free text,
    never a real person name.
    """
    role = AVATAR_INTERFACE.get(avatar_id)
    if role is None:
        return None
    # Guard: only return the role if it is in the allowed set
    if role in ALLOWED_VISIBLE_ROLES:
        return role
    return None
