import datetime
from pathlib import Path
from typing import Optional

import pytest
from psycopg import sql
from pydantic import SecretStr

from pglift import roles
from pglift.ctx import Context
from pglift.models import interface
from pglift.models.system import Instance


@pytest.mark.parametrize("with_password", [True, False])
def test_options(with_password: bool) -> None:
    role = interface.Role(
        name="r",
        password="skret",
        inherit=False,
        login=True,
        connection_limit=2,
        validity=datetime.datetime(2024, 1, 1),
        in_roles=["pg_monitor"],
    )
    options = roles.options(role, with_password=with_password)

    SQL = sql.SQL
    Composed = sql.Composed
    Identifier = sql.Identifier
    Literal = sql.Literal

    expected_seq = (
        [
            SQL("NOINHERIT"),
            SQL(" "),
            SQL("LOGIN"),
            SQL(" "),
            SQL("NOSUPERUSER"),
            SQL(" "),
            SQL("NOREPLICATION"),
            SQL(" "),
        ]
        + (
            [Composed([SQL("PASSWORD"), SQL(" "), Literal("skret")]), SQL(" ")]  # type: ignore[list-item]
            if with_password
            else []
        )
        + [
            Composed([SQL("VALID UNTIL"), SQL(" "), Literal("2024-01-01T00:00:00")]),  # type: ignore[list-item]
            SQL(" "),
            Composed(  # type: ignore[list-item]
                [SQL("CONNECTION LIMIT"), SQL(" "), Literal(2)]
            ),
            SQL(" "),
            Composed([SQL("IN ROLE"), SQL(" "), Composed([Identifier("pg_monitor")])]),  # type: ignore[list-item]
        ]
    )

    assert list(options) == expected_seq  # type: ignore[call-overload]


class Role(interface.Role):
    def __init__(
        self, name: str, password: Optional[str] = None, pgpass: bool = False
    ) -> None:
        super().__init__(
            name=name,
            password=SecretStr(password) if password is not None else None,
            pgpass=pgpass,
        )


@pytest.fixture
def passfile(ctx: Context) -> Path:
    fpath = ctx.settings.postgresql.auth.passfile
    fpath.write_text("*:999:*:edgar:fbi\n")
    return fpath


def test_in_pgpass(ctx: Context, instance: Instance, passfile: Path) -> None:
    assert roles.in_pgpass(ctx, instance, "edgar")
    assert not roles.in_pgpass(ctx, instance, "alice")


@pytest.mark.parametrize(
    "role, pgpass",
    [
        (Role("alice"), "*:999:*:edgar:fbi\n"),
        (Role("bob", "secret"), "*:999:*:edgar:fbi\n"),
        (Role("charles", pgpass=True), "*:999:*:edgar:fbi\n"),
        (Role("danny", "sss", True), "*:999:*:danny:sss\n*:999:*:edgar:fbi\n"),
        (Role("edgar", "fbi", True), "*:999:*:edgar:fbi\n"),
        (Role("edgar", None, False), ""),
    ],
)
def test_set_pgpass_entry_for(
    ctx: Context, instance: Instance, passfile: Path, role: Role, pgpass: str
) -> None:
    roles.set_pgpass_entry_for(ctx, instance, role)
    assert passfile.read_text() == pgpass
